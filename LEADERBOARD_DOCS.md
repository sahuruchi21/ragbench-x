# RAGBench-X Leaderboard Dashboard

## Overview

The Leaderboard Dashboard is the central hub for comparing RAG pipeline configurations across 4 domains (Medical, Legal, Financial, General) using 5 key metrics.

## Features

### 1. **Domain Overview Cards** (4x Grid)
- Quick statistics for each domain
- Display best accuracy achieved
- Show number of benchmarks run
- Star indicator for best overall accuracy

```
🏥 Medical: 91% | 5 runs
⚖️ Legal: 84% | 3 runs
💰 Financial: 79% | 4 runs
🌐 General: 88% | 6 runs
```

### 2. **Main Leaderboard Table**
Sortable by domain with the following columns:
- **Rank**: Medal (🥇🥈🥉) or number
- **Domain**: Icon + label
- **Best Config**: Chunking strategy used
- **Scores**: Overall, Faithfulness, Hallucination, Recall, Relevancy
- **Runs**: Number of benchmarks

**Sorting Options:**
- Click domain tabs to reprioritize the leaderboard
- Configs sorted by overall score within each domain

### 3. **Per-Domain Leaderboard Sections**
Each domain has a detailed section showing:

#### 3a. Best Configuration Highlight
- Trophy emoji with golden highlight
- Best config details
- Score breakdown (4 key metrics)
- Question count

#### 3b. Configuration Ranking Table
Ranked configs per domain:
- Position, strategy, LLM provider, retrieval K
- All 5 metrics side-by-side
- Color-coded badges:
  - 🟢 Green: >= 70% (or <= 20% for hallucination)
  - 🟡 Amber: >= 50% (or <= 40% for hallucination)
  - 🔴 Red: < 50%

### 4. **Accuracy vs Latency Tradeoff Chart**
Visual scatter plot showing:
- X-axis: Latency (seconds)
- Y-axis: Accuracy (percentage)
- Color-coded by domain
- "Ideal zone" highlighted (top-right)
- Interactive data point list below

**Key Insights:**
- Config 1 (BGE+Rerank): 91% accuracy, 2.1s latency
- Config 2 (Dense+NoRerank): 81% accuracy, 0.9s latency
- Config 3 (Hybrid): 82% accuracy, 1.4s latency

### 5. **Key Findings Section**
6-card grid with domain-specific insights:

```
🏥 Medical
Reranking gives +23% faithfulness — most impactful domain

⚖️ Legal
Semantic chunking beats fixed-size by 18%

💰 Financial
Hybrid retrieval (dense + BM25) performs best

🌐 General
Simple dense retrieval is sufficient

⏱️ Latency
Adding reranker roughly doubles latency (0.9s → 2.1s)

🎯 Conclusion
No single config wins across all domains
```

### 6. **Call-to-Action**
Gradient banner asking "Which config is best for your use case?" with explanation.

---

## Data Model

### Leaderboard Response Format
```json
{
  "leaderboard": [
    {
      "domain": "medical",
      "total_runs": 15,
      "best_config": {
        "config": {
          "chunking_strategy": "semantic",
          "retrieval_k": 5,
          "rerank_k": 3,
          "llm_provider": "template"
        },
        "num_questions": 15,
        "avg_scores": {
          "overall_score": 0.91,
          "faithfulness": 0.88,
          "hallucination_rate": 0.12,
          "recall_at_k": 0.85,
          "answer_relevancy": 0.89
        }
      },
      "all_configs": [
        { ... },
        { ... }
      ]
    }
  ]
}
```

---

## Color Scheme

**Domains:**
- Medical: Rose 🏥
- Legal: Blue ⚖️
- Financial: Amber 💰
- General: Green 🌐

**Score Badges:**
- Green: Excellent (>= 70%)
- Amber: Good (>= 50%)
- Rose: Poor (< 50%)

---

## Components Used

### LeaderboardPage
Main page component that orchestrates:
- Stats cards
- Main leaderboard table
- Per-domain details
- Accuracy vs Latency chart
- Key findings
- CTA section

### ScoreBadge
Helper component for score display:
```jsx
<ScoreBadge value={0.85} invert={false} />
// Renders: 85% in green badge
```

### TradeoffChart
Interactive chart component showing accuracy-latency relationship:
- SVG-based visualization
- Grid lines and axis labels
- Color-coded data points by domain
- Legend and data table

---

## Styling

All styles defined in `frontend/src/index.css`:
- `.data-table`: Horizontal scrollable table with hover effects
- `.stat-card`: Quick stats with gradient backgrounds
- `.card`: Main content cards with glass morphism
- `.card-header`: Section headers with titles
- Color variables: `--accent-rose`, `--accent-blue`, `--accent-amber`, `--accent-green`

---

## Future Enhancements

1. **Export Functionality**
   - Download leaderboard as CSV
   - Generate PDF report

2. **Advanced Filtering**
   - Filter by metric (accuracy, latency, faithfulness)
   - Filter by chunking strategy or LLM provider

3. **Comparison Mode**
   - Side-by-side config comparison
   - Detailed diff metrics

4. **Time Series**
   - Track score improvements over time
   - Show config evolution

5. **Interactive Charts**
   - Click points to drill into config details
   - Tooltip with full config info

---

## Testing

Mock data provided in `TradeoffChart.jsx`:
```jsx
const tradeoffs = [
  { name: 'BGE + Hybrid + Rerank', accuracy: 0.91, latency: 2.1, domain: 'medical' },
  { name: 'Dense + No rerank', accuracy: 0.81, latency: 0.9, domain: 'general' },
  // ...
]
```

Replace with actual API data once benchmarks are run.

---

## API Integration

### Endpoint: `GET /api/leaderboard`
Returns aggregated leaderboard data across all domains.

### Endpoint: `GET /api/results`
Returns individual benchmark results (used for chart data).

Both endpoints already implemented in backend.
