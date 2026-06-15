# 🏆 Domain-Specific Optimization and Performance Benchmarking of Retrieval-Augmented Generation (RAG) Architectures

### M.Tech Thesis Project | Ruchi Sahu | IIIT Naya Raipur
*RAGBench-X is a comprehensive evaluation framework and interactive diagnostic dashboard for systematically comparing RAG configurations across diverse industry domains.*

---

## 🎯 Table of Contents
1. [Overview & Thesis Abstract](#-overview--thesis-abstract)
2. [Key Features](#-key-features)
3. [Core Academic Contributions](#-core-academic-contributions)
4. [Repository Structure](#-repository-structure)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [Running the Application](#-running-the-application)
7. [Features in Detail](#-features-in-detail)
8. [Grounding & Hallucination Prevention](#-grounding--hallucination-prevention)
9. [Design System & UI Specs](#-design-system--ui-specs)
10. [Component Architecture](#-component-architecture)
11. [Usage & Customization](#-usage--customization)
12. [Quality Assurance & Accessibility](#-quality-assurance--accessibility)

---

## 🎯 Overview & Thesis Abstract

Retrieval-Augmented Generation (RAG) models have emerged as the state-of-the-art solution for grounding LLM outputs in proprietary data. However, RAG pipelines are highly sensitive to configuration choices—such as chunking size, embedding model, retrieval algorithm, and post-retrieval reranking. Moreover, a configuration that works well for one domain (e.g., General Knowledge) may perform poorly in specialized fields (e.g., Legal or Medical) due to variations in document structure and terminology.

**RAGBench-X** addresses this gap by offering:
1. **Systematic Multi-Domain Benchmarking:** Automated testing across **4 domains** (Medical, Financial, Legal, and General).
2. **Configuration Space Exploration:** Compares **18 distinct combinations** of chunking strategies (semantic vs. fixed-size), retrieval types (dense, sparse, hybrid), and reranking.
3. **Multi-Metric Diagnostics:** Separates retriever performance from generator performance using **5 key metrics** (Overall, Faithfulness, Hallucination, Recall, Relevancy).
4. **Accuracy-Latency Tradeoff Visualization:** An interactive Pareto frontier chart plotting the quality vs. speed trade-off.

---

## ✨ Key Features

* 🏥 **Domain-Specific Benchmarking:** Supports Medical (PubMedQA), Legal (ECTHR), Financial (FinQA), and General (NQ-Open) domains.
* 📊 **Interactive Leaderboard:** Real-time ranking of configurations, sortable by domain tabs, with color-coded performance badges and per-domain ranking tables.
* 📈 **Accuracy vs. Latency Chart:** Interactive SVG scatter plot illustrating the speed-quality tradeoff and highlighting the "Ideal Zone."
* 🔍 **Actionable Insights:** Displays domain-specific findings, performance drivers, and configuration optimization recommendations.
* 📱 **Fully Responsive:** Beautifully adapts to desktop (4-column grid), tablet (2-column grid), and mobile (1-column stack) with high accessibility (WCAG AAA).

---

## 🔬 Core Academic Contributions

### 1. Domain-Specific RAG Guidelines
Through systematic evaluation, this project demonstrates that a "one-size-fits-all" RAG setup is suboptimal. Key domain findings include:
* 🏥 **Medical (PubMedQA):** Adding a **Reranker** increases **Faithfulness by +23%**. Precise semantic sorting is crucial due to dense scientific terminology.
* ⚖️ **Legal (ECTHR):** **Semantic Chunking** outperforms fixed-size chunking by **18%** because legal clauses must remain logically intact to prevent citation errors.
* 💰 **Financial (FinQA):** **Hybrid Retrieval** is essential to index exact numeric values and tickers, which dense embeddings often fail to preserve.
* 🌐 **General (NQ-Open):** A simple **Dense Retrieval** model is sufficient, avoiding the computational overhead and latency of hybrid search and reranking.

### 2. Multi-Metric Evaluation Framework
Instead of using lexical metrics like BLEU/ROUGE on the final answer, RAGBench-X decouples RAG evaluation:
* **Retriever Metric:** `Recall@K` (measures how many target facts were successfully loaded into the prompt context).
* **Generator Metrics:** `Faithfulness` (groundedness in context), `Hallucination Rate` (rate of untruthful assumptions), and `Answer Relevancy` (alignment with query intent).

---

## 📁 Repository Structure

* [backend/](file:///Users/ruchi/ragbench-x/backend) — FastAPI Backend
  * [api/main.py](file:///Users/ruchi/ragbench-x/backend/api/main.py) — API endpoints for single/bulk benchmarking and leaderboard statistics
  * [data_loader/loader.py](file:///Users/ruchi/ragbench-x/backend/data_loader/loader.py) — Predefined datasets (PubMedQA, FinQA, ECTHR) and custom dataset ingestion
  * [rag/](file:///Users/ruchi/ragbench-x/backend/rag) — RAG pipeline components
    * [chunking.py](file:///Users/ruchi/ragbench-x/backend/rag/chunking.py) — Semantic and fixed-size chunk splitters
    * [retrieval.py](file:///Users/ruchi/ragbench-x/backend/rag/retrieval.py) — Dense (embeddings), sparse (TF-IDF), and hybrid retrieval
    * [reranker.py](file:///Users/ruchi/ragbench-x/backend/rag/reranker.py) — Post-retrieval ranking algorithms
    * [generation.py](file:///Users/ruchi/ragbench-x/backend/rag/generation.py) — Strict context-constrained prompt generation using Groq / LLMs
  * [evaluation/metrics.py](file:///Users/ruchi/ragbench-x/backend/evaluation/metrics.py) — Evaluation scoring metrics
* [frontend/](file:///Users/ruchi/ragbench-x/frontend) — React + Vite Dashboard Application
  * [src/pages/Leaderboard.jsx](file:///Users/ruchi/ragbench-x/frontend/src/pages/Leaderboard.jsx) — Main dashboard component displaying ranks and statistics
  * [src/components/TradeoffChart.jsx](file:///Users/ruchi/ragbench-x/frontend/src/components/TradeoffChart.jsx) — Interactive SVG scatter plot comparing Accuracy vs. Latency
  * [src/api.js](file:///Users/ruchi/ragbench-x/frontend/src/api.js) — Backend API request layer

---

## 🚀 Prerequisites & Installation

### Prerequisites
* Python 3.8+
* Node.js 16+
* npm or yarn
* Groq API Key (added to root `.env`)

### Installation

1. **Clone & Navigate**
   ```bash
   cd /Users/ruchi/ragbench-x
   ```

2. **Backend Setup**
   ```bash
   # Create Python environment
   python -m venv venv
   source venv/bin/activate  # or: venv\Scripts\activate on Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

---

## ⚙️ Running the Application

### 1. Start the Backend Server (FastAPI)
From the root directory, activate your Python virtual environment and run the backend using `uvicorn`:
```bash
# Activate virtual environment
source .venv/bin/activate

# Run FastAPI server
uvicorn backend.api.main:app --port 8000
```
*The backend API will run on:* `http://127.0.0.1:8000`

### 2. Start the Frontend Server (Vite)
Open a new terminal, navigate to the `frontend` folder, and run:
```bash
cd frontend
npm run dev
```
*The React Dashboard will be available at:* `http://localhost:5173/`

### 3. Generate Benchmark Data (Optional)
To pre-populate the leaderboard with initial evaluation data:
```bash
python scripts/run_eval.py
```

---

## 📊 Features in Detail

### 1. Domain Overview Cards (Top Row)
Displays top-level statistics for each domain:
```
┌──────────┬──────────┬──────────┬──────────┐
│ 🏥 MED   │ ⚖️ LEG   │ 💰 FIN   │ 🌐 GEN   │
│   91%    │   84%    │   79%    │   88%    │
│ 5 runs   │ 3 runs   │ 4 runs   │ 6 runs   │
└──────────┴──────────┴──────────┴──────────┘
```
* Shows best accuracy per domain and number of runs.
* Star indicator highlights the domain with the highest overall score.

### 2. Main Leaderboard Table
Interactive, sortable configuration rankings across all domains:
* Sort dynamically by domain button toggles.
* Medal icons (🥇, 🥈, 🥉) rank the top configurations.
* Badges color-code values to quickly highlight weak links.

### 3. Accuracy vs. Latency Tradeoff Chart
Visualizes the pareto frontier of speed and quality:
* **X-Axis:** Response latency (0 to 3 seconds).
* **Y-Axis:** Accuracy (0% to 100%).
* Shows an **"Ideal Zone"** (top-left: fast and accurate).
* Scatter points are color-coded by domain.

### 4. Per-Domain Rankings
Contains dedicated domain tables highlighting:
* **Trophy Highlight:** The best configuration setup for the selected domain.
* **Full Ranking List:** Complete breakdown of every configuration tested within that domain.

### 5. Actionable Findings Grid
Summarizes key takeaways from your evaluation runs:
* E.g., Reranker latency impacts, semantic chunking boundaries, and hybrid requirements.

---

## ⚠️ Grounding and Hallucination Prevention

To guarantee metric reliability, RAGBench-X enforces a strict **context constraint** on the generation model. When evaluating questions that are not supported by the loaded database:
* The LLM prompt restricts the model from using its own pre-trained weights to answer out-of-context queries.
* If no relevant facts are retrieved from the corpus, the model outputs: *"The information is not available in the provided context."*
* This refusal is scored as **100% Faithful** and **0% Hallucination** by the evaluation engine, illustrating a safe, production-grade RAG pipeline constraint.

---

## 🎨 Design System & UI Specs

### Color Palette
* **Background:** `#0a0a0f` (Deep purple-black)
* **Cards:** `rgba(20, 20, 35, 0.7)` (Glassmorphism frost overlay)
* **Text:** `#e8e8f0` (High contrast text)
* **Domain Branding:** 🏥 Rose | ⚖️ Blue | 💰 Amber | 🌐 Green

### Typography
* **Font Family:** `Inter` (Sans-Serif) for headings, `JetBrains Mono` for configs.
* **Size Scale:** Title `32px` | Section `20px` | Body `14px` | Caption `11px`.

### Badges & Thresholds
* 🟢 **Green (>= 70%):** Excellent performance.
* 🟡 **Amber (>= 50%):** Good / moderate performance.
* 🔴 **Rose (< 50%):** Poor performance / needs tuning.

---

## 🧩 Component Architecture

### [Leaderboard.jsx](file:///Users/ruchi/ragbench-x/frontend/src/pages/Leaderboard.jsx)
Main page component (355 lines) responsible for:
* Fetching statistics from the `/api/leaderboard` API.
* State management for sorting tabs, metric filters, and loading spinner.
* Rendering subcomponents, summary cards, and detail sections.

### [TradeoffChart.jsx](file:///Users/ruchi/ragbench-x/frontend/src/components/TradeoffChart.jsx)
Lightweight, responsive scatter plot (185 lines) using clean SVG elements:
* Renders axis grids, data coordinates, and interactive legend.
* Embeds custom width/height adjustments and tooltip support.

---

## 🎯 Usage & Customization

### Customizing Sort Order
In [Leaderboard.jsx](file:///Users/ruchi/ragbench-x/frontend/src/pages/Leaderboard.jsx), edit the default domain state:
```javascript
const [sortBy, setSortBy] = useState('medical'); // Options: 'medical', 'financial', 'legal', 'general'
```

### Modifying Key Findings
In [Leaderboard.jsx](file:///Users/ruchi/ragbench-x/frontend/src/pages/Leaderboard.jsx), modify the static `KEY_FINDINGS` array to edit recommendations:
```javascript
const KEY_FINDINGS = [
  { title: '🏥 Medical', text: 'Reranking gives +23% faithfulness...' },
  // Add or modify elements here
];
```

### Adjusting Chart Dimensions
In [TradeoffChart.jsx](file:///Users/ruchi/ragbench-x/frontend/src/components/TradeoffChart.jsx), adjust default dimensions:
```javascript
const width = 700;   // Default: 600
const height = 500;  // Default: 400
```

---

## ✅ Quality Assurance & Accessibility

* **Accessibility:** WCAG AAA compliance contrast ratios, keyboard-navigable tabs, ARIA labels for charts, and support for `prefers-reduced-motion`.
* **Mobile Responsiveness:** Targets touch areas (>=44px), scrolls wide tables horizontally on screens `<768px`, and drops side columns dynamically.
* **Performance:** Clean SVG chart payload, smooth CSS transitions (150-250ms), and cumulative layout shift (CLS) < 0.1.
