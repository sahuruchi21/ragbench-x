"""
RAGBench-X Reranker Module
Re-sorts retrieved chunks by relevance using keyword + bigram overlap scoring.
"""

import re
from typing import List, Tuple
from collections import Counter


class Reranker:
    """
    Cross-encoder-style reranker using keyword + bigram overlap + position scoring.
    No model downloads needed — pure Python.
    """

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        return re.findall(r'\b[a-z]+\b', text)

    def _get_bigrams(self, tokens: List[str]) -> List[Tuple[str, str]]:
        return [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]

    def _keyword_overlap_score(self, query: str, chunk: str) -> float:
        """Score based on keyword + bigram overlap between query and chunk."""
        query_tokens = self._tokenize(query)
        chunk_tokens = self._tokenize(chunk)
        query_token_set = set(query_tokens)
        chunk_token_set = set(chunk_tokens)

        if not query_token_set:
            return 0.0

        # --- Unigram coverage ---
        overlap = len(query_token_set & chunk_token_set)
        coverage = overlap / len(query_token_set)

        # --- Bigram coverage ---
        query_bigrams = set(self._get_bigrams(query_tokens))
        chunk_bigrams = set(self._get_bigrams(chunk_tokens))
        if query_bigrams:
            bigram_overlap = len(query_bigrams & chunk_bigrams)
            bigram_coverage = bigram_overlap / len(query_bigrams)
        else:
            bigram_coverage = coverage

        # --- Term frequency boost ---
        chunk_tf = Counter(chunk_tokens)
        tf_boost = sum(chunk_tf.get(qt, 0) for qt in query_token_set) / (len(chunk_tokens) + 1)

        # Weighted: 50% unigram coverage, 30% bigram coverage, 20% TF boost
        return 0.5 * coverage + 0.3 * bigram_coverage + 0.2 * min(tf_boost * 5, 1.0)

    def rerank(self, query: str, chunks_with_scores: List[Tuple[str, float]], top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Rerank retrieved chunks using keyword + bigram overlap scoring.
        Combines original retrieval score with reranking score.
        """
        reranked = []
        for chunk, retrieval_score in chunks_with_scores:
            rerank_score = self._keyword_overlap_score(query, chunk)
            # Weighted combination: 40% retrieval, 60% reranking
            combined = 0.4 * retrieval_score + 0.6 * rerank_score
            reranked.append((chunk, combined))

        reranked.sort(key=lambda x: x[1], reverse=True)
        return reranked[:top_k]
