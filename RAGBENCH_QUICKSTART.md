# 🚀 AGBench-X Leaderboard Quick Start

## What You Get

A professional **Leaderboard Dashboard** for comparing RAG pipeline configurations with:

✅ **4 Domain Support** — Medical, Legal, Financial, General  
✅ **5 Key Metrics** — Overall, Faithfulness, Hallucination, Recall, Relevancy  
✅ **18 Pipeline Configs** — Automatic comparison & ranking  
✅ **Accuracy vs Latency Chart** — Visual tradeoff analysis  
✅ **Interactive Sorting** — Click domain tabs to reorder  
✅ **Per-Domain Insights** — 6 key findings + recommendations  

---

## 📁 Files Created

```
frontend/src/
├── pages/
│   └── Leaderboard.jsx              ← Main leaderboard page
└── components/
    └── TradeoffChart.jsx             ← Accuracy vs Latency visualization

Documentation/
├── LEADERBOARD_DOCS.md              ← Feature documentation
├── FRONTEND_IMPLEMENTATION.md       ← Developer guide
└── RAGBENCH_QUICKSTART.md          ← This file
```

---

## 🎯 Key Features Explained

### 1. **Domain Overview Cards** (Top Row)
Shows best score for each domain at a glance:
```
🏥 91%  |  ⚖️ 84%  |  💰 79%  |  🌐 88%
Medical | Legal  | Financial | General
5 runs  | 3 runs | 4 runs   | 6 runs
```

### 2. **Main Leaderboard Table**
All domains ranked with configurable sorting:
- Click domain buttons to reprioritize
- See best config strategy per domain
- Compare all 5 metrics side-by-side

### 3. **Per-Domain Rankings**
Each domain gets its own section:
- 🏆 Best config highlighted with trophy
- Full ranking of all tested configs
- Exact score values and question counts

### 4. **Accuracy vs Latency Chart**
Scatter plot showing the speed-quality tradeoff:
- X-axis: Response time (0-3 seconds)
- Y-axis: Accuracy (0-100%)
- Green zone: Ideal (fast + accurate)
- Color-coded by domain

### 5. **Key Findings**
6 insights from benchmark analysis:
```
🏥 Medical → Reranking +23% faithfulness
⚖️ Legal → Semantic chunking +18%
💰 Financial → Hybrid retrieval best
🌐 General → Simple dense works well
⏱️ Latency → Reranker costs 2x time
🎯 Conclusion → Domain-specific tuning essential
```

---

## 🔌 How It Works

### Data Flow
```
Backend: /api/leaderboard endpoint
         ↓
         Aggregate results by domain & config
         ↓
React: Fetch on component mount
       ↓
       Sort & group by domain
       ↓
       Render cards, tables, chart, findings
```

### Running Benchmarks
1. Go to **Run Benchmark** page
2. Select domain & configuration
3. Run tests
4. Results automatically appear on Leaderboard

### Sorting
Click domain tabs at top of main table:
```jsx
{/* Domain buttons */}
{Object.entries(DOMAIN_META).map(([key, info]) => (
  <button onClick={() => setSortBy(key)}>
    {info.icon} {info.label}
  </button>
))}
```

---

## 🎨 Visual Design

### Color Palette
```
🏥 Medical    → Rose    (#fb7185)
⚖️ Legal      → Blue    (#60a5fa)
💰 Financial  → Amber   (#fbbf24)
🌐 General    → Green   (#34d399)
```

### Score Badges
```
🟢 Green (≥70%)    → Excellent
🟡 Amber (≥50%)    → Good
🔴 Rose  (<50%)    → Poor
```

### Dark Theme
- Background: `#0a0a0f`
- Cards: `rgba(20, 20, 35, 0.7)` (glassmorphism)
- Text: `#e8e8f0` (high contrast)
- Accents: Vibrant gradient colors

---

## 📊 Sample Data

Here's what the leaderboard shows with real benchmarks:

```
╔════════════════════════════════════════════════════════════════╗
║ 🏆 LEADERBOARD                          Sorted by: Medical     ║
╠════════════════════════════════════════════════════════════════╣
║ # Domain  Config        Overall Faithful Halluc  Recall        ║
║ ─────────────────────────────────────────────────────────────  ║
║ 🥇 Medical Semantic      91%     88%     12%     85%           ║
║ 🥈 Legal   Semantic      84%     81%     15%     79%           ║
║ 🥉 Finance Hybrid        79%     76%     18%     82%           ║
║    General Dense         88%     85%     14%     87%           ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 🔧 Integration Checklist

- [x] Component created: `Leaderboard.jsx`
- [x] Chart component created: `TradeoffChart.jsx`
- [x] API calls: `api.getLeaderboard()`
- [x] Data transformation & sorting
- [x] Responsive grid layouts
- [x] Dark theme styling
- [x] Color-coded badges
- [x] Loading & empty states
- [x] Key findings section
- [x] CTA banner

---

## 📈 Metrics Explained

| Metric | Range | What It Means |
|--------|-------|---------------|
| **Overall** | 0-1 | Average of all metrics (primary score) |
| **Faithfulness** | 0-1 | How accurately RAG answers match retrieved context |
| **Hallucination** | 0-1 | Rate of made-up answers (lower is better) |
| **Recall** | 0-1 | Percentage of relevant chunks retrieved |
| **Relevancy** | 0-1 | Quality of retrieved documents |

---

## 🎛️ Customization

### Change Default Sort Domain
```jsx
const [sortBy, setSortBy] = useState('medical') // ← Change this
```

### Add New Domain Insight
```jsx
const KEY_FINDINGS = [
  // ... existing
  { title: '🔬 New Finding', text: 'Description here...' },
]
```

### Adjust Chart Size
```jsx
const width = 700   // was 600
const height = 500  // was 400
```

---

## 🚦 Testing

### View Leaderboard
1. Run backend: `python -m backend.api.main`
2. Run frontend: `npm run dev`
3. Navigate to `/leaderboard`

### Test with Sample Data
- If no benchmarks run, see "No Results Yet" message
- Run benchmarks from `/benchmark` page
- Leaderboard updates automatically

### Check API Response
```bash
curl http://localhost:8000/api/leaderboard | jq
```

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Table shows no data | Run benchmarks first |
| Chart not rendering | Check `TradeoffChart` import |
| Sorting not working | Verify `setSortBy` function |
| Styles missing | Clear browser cache |
| API errors | Check backend server running |

---

## 📱 Mobile Experience

✅ Responsive design for all screen sizes:
- Desktop (>768px): Full 4-column grid
- Tablet (481-768px): 2-column grid
- Mobile (<480px): 1-column stack

Chart scales responsively using SVG viewBox.

---

## 🚀 Next Steps

1. **Run Benchmarks**
   ```
   Go to Run Benchmark page → Select domain/config → Run tests
   ```

2. **Monitor Leaderboard**
   ```
   Results auto-populate on the Leaderboard page
   ```

3. **Analyze Findings**
   ```
   Read key insights → Check accuracy vs latency tradeoff
   ```

4. **Optimize Config**
   ```
   Pick best config for your use case
   ```

---

## 📚 More Info

- Full feature docs: [`LEADERBOARD_DOCS.md`](./LEADERBOARD_DOCS.md)
- Implementation guide: [`FRONTEND_IMPLEMENTATION.md`](./FRONTEND_IMPLEMENTATION.md)
- Component JSDoc: [`TradeoffChart.JSDoc.js`](./frontend/src/components/TradeoffChart.JSDoc.js)
- Backend API: [`backend/api/main.py`](./backend/api/main.py#L428)

---

## 🎉 You're All Set!

The Leaderboard Dashboard is ready to use. Start running benchmarks and watch the leaderboard populate with real performance data!

**Happy Benchmarking! 🚀**

---

*AGBench-X Leaderboard Dashboard — M.Tech Thesis · Ruchi Sahu · IIIT Naya Raipur*
