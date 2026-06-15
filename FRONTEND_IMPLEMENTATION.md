# AGBench-X Leaderboard Frontend Implementation Guide

## 📋 Overview

This guide documents the implementation of the **RAGBench-X Leaderboard Dashboard** — a comprehensive interface for comparing RAG pipeline configurations across 4 domains (Medical, Legal, Financial, General) using 5 evaluation metrics.

---

## 🎯 Key Components

### 1. **Leaderboard Page** (`frontend/src/pages/Leaderboard.jsx`)

The main page component orchestrating all leaderboard sections.

#### State Management
```jsx
const [leaderboard, setLeaderboard] = useState([])
const [loading, setLoading] = useState(true)
const [sortBy, setSortBy] = useState('medical')
```

#### Key Functions

**Data Aggregation:**
```jsx
const allConfigs = leaderboard.flatMap(d => 
  (d.all_configs || []).map(c => ({
    ...c,
    domain: d.domain,
    totalLatency: 0, // from metadata
  }))
)
```

**Sorting Logic:**
```jsx
const sortedLeaderboard = [...leaderboard].sort((a, b) => {
  if (a.domain === sortBy) return -1
  if (b.domain === sortBy) return 1
  return scoreB - scoreA
})
```

#### Sections Rendered

1. **Header** - Title & description
2. **Stats Cards** - 4-column grid with domain scores
3. **Leaderboard Table** - Sortable by domain
4. **Tradeoff Chart** - Accuracy vs Latency visualization
5. **Per-Domain Details** - Individual rankings
6. **Key Findings** - 6 insight cards
7. **CTA** - "Which config is best?" section

---

### 2. **Score Badge Component** (`inline in Leaderboard.jsx`)

Renders color-coded performance metrics.

```jsx
function ScoreBadge({ value, invert = false }) {
  const v = typeof value === 'number' ? value : 0
  const pct = Math.round(v * 100)
  
  let color = 'var(--accent-rose)'
  if (!invert && v >= 0.7) color = 'var(--accent-green)'
  else if (!invert && v >= 0.5) color = 'var(--accent-amber)'
  else if (invert && v <= 0.2) color = 'var(--accent-green)'
  else if (invert && v <= 0.4) color = 'var(--accent-amber)'
  
  return <span style={{...}}>{ pct}%</span>
}
```

**Parameters:**
- `value` (number): Score between 0-1
- `invert` (boolean): For hallucination (lower is better)

**Output:**
- Green badge: >= 70% (excellent)
- Amber badge: >= 50% (good)
- Rose badge: < 50% (poor)

---

### 3. **Tradeoff Chart Component** (`frontend/src/components/TradeoffChart.jsx`)

SVG-based scatter plot showing accuracy-latency relationships.

#### Structure
```
SVG (600x400px)
├── Grid Lines (20% increments)
├── Axes (with labels & ticks)
├── Data Points (colored by domain)
├── Ideal Zone Highlight
└── Legend
└── Data Table
```

#### Key Variables
```jsx
const xScale = (val) => padding + (val / maxLatency) * (width - padding * 2)
const yScale = (val) => height - padding - (val / maxAccuracy) * (height - padding * 2)

// Domain to Color Mapping
const colors = {
  medical: 'var(--accent-rose)',
  financial: 'var(--accent-amber)',
  legal: 'var(--accent-blue)',
  general: 'var(--accent-green)',
}
```

#### Rendering Pipeline

1. **Grid**: Draw background grid lines for reference
2. **Axes**: Draw X/Y axes with accent color
3. **Labels**: Axis titles and numeric labels
4. **Data Points**: SVG circles sized by accuracy
5. **Ideal Zone**: Semi-transparent green overlay
6. **Legend**: 4-column legend with domain indicators
7. **Data Table**: Detailed configuration list

---

## 🎨 Styling

### Color Scheme

```css
/* Domain Colors */
--accent-rose: #fb7185     /* Medical */
--accent-blue: #60a5fa     /* Legal */
--accent-amber: #fbbf24    /* Financial */
--accent-green: #34d399    /* General */

/* UI Colors */
--bg-primary: #0a0a0f
--bg-secondary: #12121a
--bg-card: rgba(20, 20, 35, 0.7)
--text-primary: #e8e8f0
--text-secondary: #8b8ba3
```

### Responsive Design

```css
@media (max-width: 768px) {
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 480px) {
  .grid-4 { grid-template-columns: 1fr; }
}
```

---

## 📊 Data Flow

### API Integration

**Endpoint:** `GET /api/leaderboard`

**Response Structure:**
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
      "all_configs": [...]
    },
    // ... 3 more domains
  ]
}
```

### Data Transformation

1. **Fetch** leaderboard from `/api/leaderboard`
2. **Group** configs by domain
3. **Sort** domains (by `sortBy` selection)
4. **Render** tables, charts, and cards

---

## 🔄 Component Lifecycle

```jsx
useEffect(() => {
  api.getLeaderboard()
    .then(data => {
      setLeaderboard(data.leaderboard || [])
      setLoading(false)
    })
    .catch(() => setLoading(false))
}, [])
```

1. Component mounts → `loading = true`
2. API call initiated
3. Response received → Update state
4. Component re-renders with data

---

## 🧩 Section Breakdown

### Section 1: Domain Overview Cards
```jsx
<div className="grid-4" style={{ marginBottom: 32 }}>
  {leaderboard.map(d => (
    <div key={d.domain} className="stat-card">
      <div style={{ fontSize: 28 }}>{meta.icon}</div>
      <div className="stat-value">{(score * 100).toFixed(1)}%</div>
      <div className="stat-label">{meta.label}</div>
    </div>
  ))}
</div>
```

**Grid Layout:** 4 columns on desktop, 2 on tablet, 1 on mobile

---

### Section 2: Main Leaderboard
```jsx
<table className="data-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Domain</th>
      <th>Best Config</th>
      <th>Overall</th>
      <th>Faithfulness</th>
      <th>Hallucination</th>
      <th>Recall</th>
      <th>Relevancy</th>
      <th>Runs</th>
    </tr>
  </thead>
  <tbody>
    {sortedLeaderboard.map((domain, i) => (
      <tr key={domain.domain}>
        {/* cells */}
      </tr>
    ))}
  </tbody>
</table>
```

**Sorting:** Click domain tabs to change `sortBy` state

---

### Section 3: Per-Domain Details
```jsx
{sortedLeaderboard.filter(d => d.total_runs > 0).map(domain => (
  <div key={domain.domain} className="card">
    {/* Best config highlight */}
    {/* Config ranking table */}
  </div>
))}
```

Each domain gets its own card with:
- Best config highlight (trophy + metrics)
- Full config ranking table

---

### Section 4: Accuracy vs Latency Chart
```jsx
<TradeoffChart data={allConfigs} />
```

Pass aggregated config data from all domains.

---

### Section 5: Key Findings
```jsx
<div style={{ display: 'grid', gridTemplateColumns: '...' }}>
  {KEY_FINDINGS.map((finding, i) => (
    <div key={i} style={{ 
      borderLeft: '3px solid var(--accent-purple)',
      padding: 16,
      ...
    }}>
      <div>{finding.title}</div>
      <div>{finding.text}</div>
    </div>
  ))}
</div>
```

6 cards with domain insights hardcoded in `KEY_FINDINGS` constant.

---

### Section 6: Call-to-Action
```jsx
<div className="card" style={{
  background: 'var(--gradient-primary)',
  textAlign: 'center',
  padding: 40,
}}>
  <h3>Which config is best for your use case?</h3>
  <p>Domain-specific RAG configurations...</p>
</div>
```

Gradient background with question prompt.

---

## 🚀 Usage Example

```jsx
import Leaderboard from './pages/Leaderboard'

function App() {
  return <Leaderboard />
}
```

The component handles:
- Loading state
- Empty state (no benchmarks run)
- Full leaderboard display
- Error handling via API

---

## 🔧 Customization

### Change Sorting Default
```jsx
const [sortBy, setSortBy] = useState('legal') // was 'medical'
```

### Add More Metrics
```jsx
// In Key Findings
const KEY_FINDINGS = [
  // ... existing findings
  { title: '📊 New Insight', text: '...' },
]
```

### Adjust Chart Dimensions
```jsx
// In TradeoffChart
const width = 700  // was 600
const height = 500 // was 400
```

### Customize Colors
```css
/* In index.css */
--accent-rose: #ff0000 /* Change medical color */
```

---

## 📱 Responsive Breakpoints

| Breakpoint | Grid | Layout |
|-----------|------|--------|
| > 768px | 4 cols | Full width |
| 481-768px | 2 cols | Cards stack |
| < 480px | 1 col | Mobile optimized |

---

## ✅ Quality Checklist

- [x] Dark theme with accent colors
- [x] Loading state with spinner
- [x] Empty state message
- [x] Responsive grid layouts
- [x] Color-coded score badges
- [x] Sortable leaderboard
- [x] Per-domain breakdown
- [x] Accuracy vs Latency chart
- [x] Key findings section
- [x] Call-to-action section
- [x] API integration ready
- [x] Hover effects on elements
- [x] Modal/medal rankings (🥇🥈🥉)

---

## 🐛 Debugging Tips

1. **No data displaying?**
   - Check `/api/leaderboard` response
   - Verify `leaderboard` state in React DevTools

2. **Chart not showing?**
   - Ensure `TradeoffChart` component imported
   - Check `allConfigs` array not empty

3. **Sorting not working?**
   - Verify `setSortBy` function called on tab click
   - Check `sortBy` state updates

4. **Styles not applying?**
   - Verify CSS variables in `:root`
   - Check CSS file import in App.jsx

---

## 📚 References

- [API Endpoints](/ragbench-x/backend/api/main.py#L428)
- [CSS Variables](/ragbench-x/frontend/src/index.css#L1)
- [React Hooks](https://react.dev/reference/react)
- [SVG in React](https://react.dev/reference/react-dom/components/svg)

---

## 🎉 Next Steps

1. Run benchmarks to populate leaderboard
2. Monitor `/api/leaderboard` endpoint
3. Fine-tune key findings for domain
4. Add export/download functionality
5. Implement comparison mode
6. Add time-series tracking

---

**Last Updated:** May 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅
