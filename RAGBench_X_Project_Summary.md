# RAGBench-X — Project Summary in Simple Words
### M.Tech Thesis | Ruchi Sahu | IIIT Naya Raipur

---

## 🤔 The Problem You Started With

> *"When you build an AI system that answers questions using documents (called RAG), there are many settings you can choose — like how to split documents, how to search them, etc. Nobody knows which settings work best for which type of topic. Does a medical AI need different settings than a legal AI?"*

---

## 📦 Step 1 — You Took 4 Real Datasets

| Domain | Dataset | What it is |
|--------|---------|-----------|
| 🏥 Medical | PubMedQA | Real biomedical research questions |
| 💰 Financial | FinQA | Real financial report questions |
| ⚖️ Legal | ECtHR (LexGLUE) | European court case texts |
| 🌐 General | NQ Open | Everyday factual questions |

---

## ⚙️ Step 2 — You Built a RAG Pipeline

Think of RAG like a **smart open-book exam system**:

```
Question comes in
    ↓
Split documents into chunks (like cutting a book into paragraphs)
    ↓
Search for the most relevant chunks (like ctrl+F but smarter)
    ↓
Re-rank the results (pick the BEST ones from the top results)
    ↓
Give those chunks to an LLM (like GPT) and say "answer using only this"
    ↓
Get the answer
```

---

## 🔧 Step 3 — You Changed the Settings and Compared

You tested **different combinations** of:

- **Chunking** — how to split documents (by sentence / fixed size / semantic meaning)
- **Retrieval** — how to search (keyword search / meaning-based / both)
- **Reranking** — how many top results to re-sort

---

## 📊 Step 4 — You Measured 5 Things for Each Answer

| Metric | Simple meaning |
|--------|---------------|
| Faithfulness | Did the AI stick to what the document said? |
| Hallucination Rate | Did it make things up? |
| Recall@K | Did it find the right paragraphs? |
| Answer Relevancy | Did it actually answer the question? |
| BLEU | How similar is the answer to the correct answer? |

---

## 🏆 Step 5 — You Built a Live Dashboard to See Results

- A **leaderboard** showing which configuration won for each domain
- A **comparison page** showing side-by-side scores
- A **benchmark runner** where you can test any question live

---

## 📌 What You Concluded (from your actual data — 239 runs)

1. **One setting does NOT work for all domains** — this is the main finding
2. **Medical** — Using a reranker with higher k (rerank_k=15) gave **~22% better faithfulness** than low reranking
3. **Legal** — Fixed chunking worked better in practice because legal documents are already well-structured
4. **Financial** — Hybrid retrieval (keyword + meaning combined) scored higher because financial data has exact numbers and tickers
5. **General** — Simple dense retrieval works fine; no need for heavy reranking on everyday questions

---

## ✅ Fact Check — Claims vs. Actual Data

| Domain | Claim | Real Data | Verdict |
|--------|-------|-----------|---------|
| 🏥 Medical | Reranking adds +23% faithfulness | rerank_k=5 → 0.617, rerank_k=15 → 0.836 (+21.9%) | ✅ True |
| ⚖️ Legal | Semantic chunking is better | Fixed: 0.890, Semantic: 0.635–0.709 | ❌ Fixed actually won |
| 💰 Financial | Hybrid retrieval is best | Hybrid 0.840–0.885 vs Dense 0.819 | ✅ Reasonable |
| 🌐 General | Dense-only is sufficient | Dense: 0.858, Sentence+Hybrid: 0.934 | ⚠️ Mixed |

> **Key insight for viva:** Do NOT say "semantic chunking is better for legal" — your real data shows the opposite. Say instead: *"Fixed chunking outperformed semantic in our runs, likely because legal documents are already logically structured."*

---

## 🎤 One-Line Answer for Any Interviewer

> *"I built a system that automatically tests different RAG configurations across Medical, Financial, Legal, and General domains, measures them on 5 metrics, and shows on a live dashboard which configuration works best — and I found that the best setup is different for every domain, so you can't just pick one and use it everywhere."*

---

## 🔬 Technical Stack Used

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI (Python) |
| Frontend Dashboard | React + Vite |
| Embedding Model | BAAI/bge-base-en-v1.5 |
| LLM Provider | Groq |
| Retrieval | Dense (BGE) + Sparse (TF-IDF) + Hybrid |
| Reranker | Cross-encoder reranking |
| Datasets | PubMedQA, FinQA, LexGLUE, NQ Open |

---

*Generated: June 2026 | RAGBench-X Project*
