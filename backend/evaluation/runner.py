"""
RAGBench-X Evaluation Runner

Orchestrates evaluation across multiple samples:
- Runs the full RAG pipeline for each sample
- Aggregates per-metric scores (skipping None values)
- Returns a structured summary report
"""

from typing import List, Dict, Optional

from backend.rag.pipeline import run_rag_pipeline
from backend.evaluation.metrics import evaluate_answer


def run_evaluation(
    samples: List[Dict],
    chunking_strategy: str = "semantic",
    embedding_model: str = "bge",
    retrieval_type: str = "hybrid",
    retrieval_k: int = 10,
    rerank_k: int = 5,
    llm_provider: str = "groq",
    llm_model: Optional[str] = None,
) -> Dict:
    """
    Runs the RAG pipeline + evaluation for a list of samples.

    Each sample must have:
        - question    : str
        - context     : List[str]
        - gold_answer : str  (may be empty/None for custom questions)

    Returns:
        {
            "results":        List[Dict],   # per-sample scores
            "aggregate":      Dict,         # averaged metrics
            "total_samples":  int,
        }
    """

    per_sample_results: List[Dict] = []

    for sample in samples:

        question    = sample.get("question", "")
        context     = sample.get("context", [])
        gold_answer = sample.get("gold_answer") or None  # treat "" as None

        # Normalise context to a flat list of strings
        if isinstance(context, str):
            context = [context]

        # ── Run RAG pipeline ──────────────────────────────────────────
        pipeline_result = run_rag_pipeline(
            documents=context,
            query=question,
            ground_truth=gold_answer,
            chunking_strategy=chunking_strategy,
            embedding_model=embedding_model,
            retrieval_type=retrieval_type,
            retrieval_k=retrieval_k,
            rerank_k=rerank_k,
            llm_provider=llm_provider,
            llm_model=llm_model,
        )

        generated_answer = pipeline_result["answer"]

        retrieved_texts = [
            c["text"] for c in pipeline_result["retrieved_chunks"]
        ]
        reranked_texts = [
            c["text"] for c in pipeline_result["reranked_chunks"]
        ]

        # ── Evaluate ──────────────────────────────────────────────────
        scores = evaluate_answer(
            question=question,
            generated_answer=generated_answer,
            gold_answer=gold_answer,
            context_chunks=reranked_texts,
            retrieved_chunks=retrieved_texts,
        )

        per_sample_results.append({
            "question":         question,
            "generated_answer": generated_answer,
            "gold_answer":      gold_answer,
            "scores":           scores,
            "pipeline_metrics": pipeline_result["metrics"],
            "latency_ms":       pipeline_result["metrics"]["latency"] * 1000,
        })

    # ── Aggregate (ignore None values — metric not applicable) ────────
    aggregate = _aggregate_scores(per_sample_results)

    return {
        "results":       per_sample_results,
        "aggregate":     aggregate,
        "total_samples": len(per_sample_results),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _aggregate_scores(results: List[Dict]) -> Dict:
    """
    Averages each metric across all samples, skipping None values.
    If a metric is None for every sample, returns None for that metric.
    """

    metric_keys = [
        "faithfulness",
        "hallucination_rate",
        "recall_at_k",
        "answer_relevancy",
        "bleu_score",
        "overall_score",
    ]

    aggregated: Dict = {}

    for key in metric_keys:
        values = [
            r["scores"][key]
            for r in results
            if r["scores"].get(key) is not None
        ]

        if values:
            aggregated[key] = round(sum(values) / len(values), 4)
        else:
            aggregated[key] = None  # N/A — no gold answers in this batch

    return aggregated
