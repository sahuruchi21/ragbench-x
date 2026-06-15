from typing import List, Tuple, Dict
from collections import Counter
import re
import math

from backend.rag.embedding import cosine_similarity


class BM25:

    def __init__(self, k1=1.5, b=0.75):
        self.k1=k1
        self.b=b

    def _tokenize(self,text):
        return re.findall(
            r'\b[a-z]+\b',
            text.lower()
        )

    def fit(self,documents):

        self.documents=documents
        self.doc_tokens=[
            self._tokenize(d)
            for d in documents
        ]

        self.doc_len=[
            len(x)
            for x in self.doc_tokens
        ]

        self.avgdl=sum(
            self.doc_len
        )/len(
            self.doc_len
        )

        self.doc_freq={}
        self.doc_tf=[]

        for tokens in self.doc_tokens:

            tf=Counter(tokens)
            self.doc_tf.append(tf)

            for t in tf:

                self.doc_freq[t]=(
                    self.doc_freq.get(
                        t,
                        0
                    )+1
                )

        self.idf={}

        N=len(documents)

        for t,df in self.doc_freq.items():

            self.idf[t]=math.log(
                (
                    N-df+0.5
                )/
                (
                    df+0.5
                )+1
            )


    def score(self,query,idx):

        query_tokens=self._tokenize(
            query
        )

        score=0

        dl=self.doc_len[idx]
        tf=self.doc_tf[idx]

        for term in query_tokens:

            if term not in self.idf:
                continue

            freq=tf.get(
                term,
                0
            )

            numerator=(
                freq*
                (
                    self.k1+1
                )
            )

            denominator=(
                freq+
                self.k1*
                (
                    1-self.b+
                    self.b*
                    (
                        dl/
                        self.avgdl
                    )
                )
            )

            score+=(
                self.idf[term]*
                (
                    numerator/
                    denominator
                )
            )

        return score


class DenseRetriever:

    def __init__(
        self,
        chunks,
        embedder
    ):

        self.chunks=chunks
        self.embedder=embedder

        self.embedder.fit(
            chunks
        )

        self.chunk_vectors=(
            self.embedder
            .embed_batch(
                chunks
            )
        )


    def search(
        self,
        query,
        k=15
    ):

        # Query expansion
        expansions={

            "robbery":
            "crime theft punishment sentencing imprisonment legal",

            "negligence":
            "tort duty care liability breach",

            "contract":
            "agreement consideration legal obligation"
        }

        expanded_query=query.lower()

        for key,val in expansions.items():

            if key in query.lower():

                expanded_query+=(
                    " "+val
                )


        query_vector=(
            self.embedder.embed(
                expanded_query
            )
        )

        similarities=[]

        for i,vec in enumerate(
            self.chunk_vectors
        ):

            sim=cosine_similarity(
                query_vector,
                vec
            )

            similarities.append(
                (
                    i,
                    sim
                )
            )

        similarities.sort(
            key=lambda x:x[1],
            reverse=True
        )

        return [
            (
                self.chunks[idx],
                score
            )
            for idx,score in similarities[:k]
        ]


class SparseRetriever:

    def __init__(
        self,
        chunks
    ):

        self.chunks=chunks

        self.bm25=BM25()

        self.bm25.fit(
            chunks
        )


    def search(
        self,
        query,
        k=15
    ):

        scores=[]

        for i in range(
            len(self.chunks)
        ):

            scores.append(
                (
                    i,
                    self.bm25.score(
                        query,
                        i
                    )
                )
            )

        scores.sort(
            key=lambda x:x[1],
            reverse=True
        )

        return [
            (
                self.chunks[idx],
                score
            )
            for idx,score in scores[:k]
        ]


class HybridRetriever:

    def __init__(
        self,
        chunks,
        embedder,
        alpha=0.6
    ):

        self.dense=(
            DenseRetriever(
                chunks,
                embedder
            )
        )

        self.sparse=(
            SparseRetriever(
                chunks
            )
        )

        self.alpha=alpha


    def search(
        self,
        query,
        k=15
    ):

        dense=(
            self.dense.search(
                query,
                k*2
            )
        )

        sparse=(
            self.sparse.search(
                query,
                k*2
            )
        )

        scores={}

        for chunk,score in dense:

            scores[chunk]=(
                self.alpha*
                score
            )

        for chunk,score in sparse:

            scores[chunk]=(
                scores.get(
                    chunk,
                    0
                )
                +
                (
                    1-self.alpha
                )*score
            )

        results=sorted(
            scores.items(),
            key=lambda x:x[1],
            reverse=True
        )

        return results[:k]
# ============================
# FACTORY CLASS
# ============================

class Retriever:
    """
    Main Retriever class
    Keeps compatibility with existing pipeline code
    """

    def __init__(
        self,
        chunks: List[str],
        embedder,
        retrieval_type: str = "dense"
    ):

        self.chunks = chunks
        self.retrieval_type = retrieval_type

        if retrieval_type == "dense":

            self.retriever = DenseRetriever(
                chunks,
                embedder
            )

        elif retrieval_type == "sparse":

            self.retriever = SparseRetriever(
                chunks
            )

        elif retrieval_type == "hybrid":

            self.retriever = HybridRetriever(
                chunks,
                embedder
            )

        else:

            raise ValueError(
                f"Unknown retrieval type: {retrieval_type}"
            )


    def search(
        self,
        query: str,
        k: int = 15
    ):

        return self.retriever.search(
            query,
            k
        )