#!/usr/bin/env python3
"""
RAGBench-X Evaluation Runner
Run full benchmark evaluations from the command line.

Usage:
    python scripts/run_eval.py --domain medical --max-samples 5
    python scripts/run_eval.py --domain all --max-samples 3
    python scripts/run_eval.py --domain financial --strategy semantic --provider template
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.data_loader.loader import get_sample_data, get_all_domains
from backend.rag.pipeline import run_rag_pipeline
from backend.evaluation.metrics import evaluate_answer


def run_evaluation(domain, max_samples, strategy, provider, model_name):
    """Run evaluation on a single domain."""
    print(f"\n{'='*60}")
    print(f"  Domain: {domain.upper()}")
    print(f"  Strategy: {strategy} | Provider: {provider}")
    print(f"{'='*60}")
    
    samples = get_sample_data(domain, max_samples)
    results = []
    
    for i, sample in enumerate(samples):
        print(f"\n[{i+1}/{len(samples)}] {sample['question'][:80]}...")
        
        pipeline_result = run_rag_pipeline(
            documents=sample["context"],
            query=sample["question"],
            chunking_strategy=strategy,
            llm_provider=provider,
            llm_model=model_name,
        )
        
        retrieved_texts = [c["text"] for c in pipeline_result["retrieved_chunks"]]
        reranked_texts = [c["text"] for c in pipeline_result["reranked_chunks"]]
        
        scores = evaluate_answer(
            question=sample["question"],
            generated_answer=pipeline_result["answer"],
            gold_answer=sample["gold_answer"],
            context_chunks=reranked_texts,
            retrieved_chunks=retrieved_texts,
        )
        
        results.append({
            "question": sample["question"],
            "scores": scores,
            "answer_preview": pipeline_result["answer"][:100] + "...",
        })
        
        print(f"  Overall: {scores['overall_score']:.4f} | "
              f"Faithfulness: {scores['faithfulness']:.4f} | "
              f"Hallucination: {scores['hallucination_rate']:.4f} | "
              f"Recall: {scores['recall_at_k']:.4f}")
    
    # Average scores
    if results:
        avg = {}
        for key in results[0]["scores"]:
            avg[key] = round(sum(r["scores"][key] for r in results) / len(results), 4)
        
        print(f"\n{'─'*60}")
        print(f"  AVERAGES for {domain.upper()}:")
        for key, val in avg.items():
            print(f"    {key:25s}: {val:.4f}")
        
        return {"domain": domain, "num_samples": len(results), "averages": avg, "results": results}
    
    return None


def main():
    parser = argparse.ArgumentParser(description="RAGBench-X Evaluation Runner")
    parser.add_argument("--domain", default="all", help="Domain to evaluate (medical/financial/legal/general/all)")
    parser.add_argument("--max-samples", type=int, default=5, help="Max samples per domain")
    parser.add_argument("--strategy", default="semantic", help="Chunking strategy (fixed/sentence/paragraph/semantic)")
    parser.add_argument("--provider", default="template", help="LLM provider (template/gemini/ollama)")
    parser.add_argument("--model", default=None, help="LLM model name (for ollama)")
    parser.add_argument("--output", default=None, help="Output JSON file path")
    args = parser.parse_args()
    
    print("╔══════════════════════════════════════════╗")
    print("║         RAGBench-X Evaluation            ║")
    print("╚══════════════════════════════════════════╝")
    
    domains = get_all_domains() if args.domain == "all" else [args.domain]
    all_results = []
    
    for domain in domains:
        result = run_evaluation(domain, args.max_samples, args.strategy, args.provider, args.model)
        if result:
            all_results.append(result)
    
    # Summary
    print(f"\n\n{'='*60}")
    print("  FINAL SUMMARY")
    print(f"{'='*60}")
    for r in all_results:
        print(f"  {r['domain']:12s} → Overall: {r['averages']['overall_score']:.4f}")
    
    # Save results
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent / "backend" / "data" / "results" / "eval_results.json"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n  Results saved to: {output_path}")


if __name__ == "__main__":
    main()
