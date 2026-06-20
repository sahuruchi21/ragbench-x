"""
RAGBench-X Pipeline Orchestrator

Runs the full RAG pipeline:
Chunk → Embed → Retrieve → Rerank → Generate → Evaluate
"""

from typing import List, Dict, Optional
import time

# RAG components
from backend.rag.chunking import chunk_documents
from backend.rag.embedding import get_embedding_model
from backend.rag.retrieval import Retriever
from backend.rag.reranker import Reranker
from backend.rag.generation import generate_answer

# Evaluation metrics
from backend.evaluation.metrics import (
    compute_recall_at_k,
    compute_faithfulness,
    compute_hallucination_rate,
    compute_answer_relevancy
)


def run_rag_pipeline(
    documents: List[str],
    query: str,
    ground_truth: Optional[str] = None,
    chunking_strategy: str = "semantic",
    embedding_model: str = "e5",
    retrieval_type: str = "hybrid",
    retrieval_k: int = 30,
    rerank_k: int = 15,
    llm_provider: str = "groq",
    llm_model: Optional[str] = None,
    is_custom: bool = False,
) -> Dict:

    start_time = time.time()

    # -----------------------------
    # Step 1: Chunking
    # -----------------------------

    chunk_start = time.time()

    chunks = chunk_documents(
        documents,
        strategy=chunking_strategy
    )

    chunk_time = (
        time.time() - chunk_start
    )

    if not chunks:

        return {
            "answer":"No chunks generated",
            "score":0,
            "metrics":{
                "recall":0,
                "faithfulness":0,
                "hallucination":1,
                "answer_relevancy":0,
                "latency":0
            },
            "error":"No chunks created from input"
        }

    # -----------------------------
    # Step 2:
    # Embedding + Retrieval
    # -----------------------------

    retrieve_start = time.time()

    embedder = get_embedding_model(
        embedding_model
    )

    retriever = Retriever(
        chunks,
        embedder,
        retrieval_type=retrieval_type
    )

    retrieved = retriever.search(
        query,
        k=min(
            retrieval_k,
            len(chunks)
        )
    )

    # Debugging
    print(
        "\n=========== RETRIEVED ==========="
    )

    for i,(chunk,score) in enumerate(
        retrieved[:5]
    ):

        print(
            f"\nChunk {i+1}"
        )

        print(
            f"Score:{round(score,4)}"
        )

        print(
            chunk[:300]
        )

    print(
        "\n================================="
    )

    retrieve_time = (
        time.time()-retrieve_start
    )

    # -----------------------------
    # Step 3:
    # Reranking
    # -----------------------------

    rerank_start=time.time()

    reranker=Reranker()

    reranked=reranker.rerank(
        query,
        retrieved,
        top_k=min(
            rerank_k,
            len(retrieved)
        )
    )

    rerank_time=(
        time.time()-rerank_start
    )

    # -----------------------------
    # Step 4:
    # Generation
    # -----------------------------

    gen_start=time.time()

    context_chunks=[
        chunk
        for chunk,_ in reranked
    ]

    answer=generate_answer(
        query,
        context_chunks,
        provider=llm_provider,
        model_name=llm_model,
        is_custom=is_custom,
    )

    gen_time=(
        time.time()-gen_start
    )

    total_time=(
        time.time()-start_time
    )

    # -----------------------------
    # Step 5:
    # Evaluation
    # -----------------------------

    context_texts=[
        chunk
        for chunk,_ in reranked
    ]

    retrieved_texts=[
        chunk
        for chunk,_ in retrieved
    ]

    if ground_truth:

        recall=compute_recall_at_k(
            ground_truth,
            retrieved_texts
        )

    else:

        recall=None


    faith=compute_faithfulness(
        answer,
        context_texts
    )

    halluc=compute_hallucination_rate(
        answer,
        context_texts
    )

    relevancy=compute_answer_relevancy(
        query,
        answer
    )

    # -----------------------------
    # Final score (no double-counting: halluc = 1-faith)
    # -----------------------------

    if recall is not None:

        score=round(
            0.40*faith+
            0.35*recall+
            0.25*relevancy,
            2
        )

    else:

        score=round(
            0.55*faith+
            0.45*relevancy,
            2
        )

    return {

        "answer":answer,

        "score":score,

        "metrics":{

            "recall":
            round(
                recall,
                2
            ) if recall is not None
            else None,

            "faithfulness":
            round(
                faith,
                2
            ),

            "hallucination":
            round(
                halluc,
                2
            ),

            "answer_relevancy":
            round(
                relevancy,
                2
            ),

            "latency":
            round(
                total_time,
                2
            )
        },

        "retrieved_chunks":[

            {
                "text":chunk,
                "score":round(
                    score,
                    4
                )
            }

            for chunk,score
            in retrieved
        ],

        "reranked_chunks":[

            {
                "text":chunk,
                "score":round(
                    score,
                    4
                )
            }

            for chunk,score
            in reranked
        ],

        "metadata":{

            "chunking_strategy":
            chunking_strategy,

            "embedding_model":
            embedding_model,

            "retrieval_type":
            retrieval_type,

            "total_chunks":
            len(chunks),

            "retrieval_k":
            retrieval_k,

            "rerank_k":
            rerank_k,

            "llm_provider":
            llm_provider,

            "timings_ms":{

                "chunking":
                round(
                    chunk_time*1000,
                    2
                ),

                "retrieval":
                round(
                    retrieve_time*1000,
                    2
                ),

                "reranking":
                round(
                    rerank_time*1000,
                    2
                ),

                "generation":
                round(
                    gen_time*1000,
                    2
                ),

                "total":
                round(
                    total_time*1000,
                    2
                )
            }
        }
    }