
# 📊 AGBench-X Leaderboard — Visual Overview

## Dashboard Layout

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     🏆 LEADERBOARD                        ┃
┃  Best performing RAG configurations ranked by domain.    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│                 │                 │                 │                 │
│  🏥 Medical     │  ⚖️ Legal       │  💰 Financial   │  🌐 General     │
│     91%         │     84%         │     79%         │     88%         │
│  5 runs         │  3 runs         │  4 runs         │  6 runs         │
│                 │                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│  Leaderboard              [🏥 Medical ▼]  [⚖️ Legal]  [💰 Finance]  [🌐 Gen]│
├─┬────────┬──────────┬────────┬────────┬────────┬────────┬────────┬─────┤
│#│ Domain │ Config   │ Overall│Faithful│Halluc. │ Recall │Relevan.│Runs │
├─┼────────┼──────────┼────────┼────────┼────────┼────────┼────────┼─────┤
│🥇│Medical │Semantic  │91% 🟢  │88% 🟢  │12% 🟢  │85% 🟢  │89% 🟢  │ 15  │
│🥈│Legal   │Semantic  │84% 🟢  │81% 🟢  │15% 🟢  │79% 🟡  │83% 🟢  │ 12  │
│🥉│Finance │Hybrid    │79% 🟢  │76% 🟡  │18% 🟡  │82% 🟢  │78% 🟡  │ 10  │
│ 4│General │Dense     │88% 🟢  │85% 🟢  │14% 🟢  │87% 🟢  │86% 🟢  │ 18  │
└─┴────────┴──────────┴────────┴────────┴────────┴────────┴────────┴─────┘

┌───────────────────────────────────────────────────────────────────────┐
│                 📈 ACCURACY VS LATENCY TRADEOFF                       │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│ 100%│                                                                 │
│  90%│                        ●           ← Best scores here          │
│  80%│                    ●   ●   ●                                   │
│  70%│                 ●                                              │
│  60%│             ●                                                  │
│     │ ┌──────────────────────────────────────────────────────        │
│     │ 0    0.5s  1.0s  1.5s  2.0s  2.5s  3.0s  (Latency)             │
│     │                                                                 │
│  Legend: 🏥 Medical │ ⚖️ Legal │ 💰 Financial │ 🌐 General          │
│                                                                       │
│  Ideal Zone: Fast + Accurate (top-right corner) ✨                  │
│                                                                       │
│  Configs:                                                             │
│  • BGE + Rerank:      91% accuracy, 2.1s latency (accurate but slow) │
│  • Dense Only:        81% accuracy, 0.9s latency (fast but less acc) │
│  • Hybrid:            82% accuracy, 1.4s latency (balanced)          │
│  • Ada + Dense:       78% accuracy, 1.1s latency (fast, less acc)    │
└───────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│ 🏥 MEDICAL DOMAIN LEADERBOARD                    15 total runs • 4   │
├───────────────────────────────────────────────────────────────────────┤
│                      🏆 BEST CONFIG                                   │
│  Strategy: SEMANTIC CHUNKING                                         │
│  Score Breakdown:    91% Overall | 88% Faithfulness                  │
│                      12% Hallucination | 85% Recall | 89% Relevancy  │
│  Tested on 15 questions                                              │
├─┬──────────┬──────────┬────────────────────────────────────────────┤
│#│ Strategy │ Provider │ Overall │ Faithful │ Halluc. │ Recall      │
├─┼──────────┼──────────┼────────────────────────────────────────────┤
│🥇│Semantic  │template  │ 91% 🟢  │ 88% 🟢   │ 12% 🟢  │ 85% 🟢     │
│🥈│Fixed-size│template  │ 85% 🟢  │ 82% 🟢   │ 18% 🟡  │ 79% 🟡     │
│🥉│Hybrid    │template  │ 78% 🟢  │ 75% 🟡   │ 22% 🟡  │ 76% 🟡     │
│ 4│Dense     │template  │ 72% 🟡  │ 68% 🟡   │ 28% 🟡  │ 71% 🟡     │
└─┴──────────┴──────────┴────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│ ⚖️ LEGAL DOMAIN LEADERBOARD                      12 total runs • 2   │
├───────────────────────────────────────────────────────────────────────┤
│                      🏆 BEST CONFIG                                   │
│  Strategy: SEMANTIC CHUNKING                                         │
│  Score Breakdown:    84% Overall | 81% Faithfulness                  │
│                      15% Hallucination | 79% Recall | 83% Relevancy  │
│  Tested on 12 questions                                              │
├─┬──────────┬──────────┬────────────────────────────────────────────┤
│#│ Strategy │ Provider │ Overall │ Faithful │ Halluc. │ Recall      │
├─┼──────────┼──────────┼────────────────────────────────────────────┤
│🥇│Semantic  │template  │ 84% 🟢  │ 81% 🟢   │ 15% 🟢  │ 79% 🟡     │
│🥈│Fixed-size│template  │ 76% 🟡  │ 72% 🟡   │ 25% 🟡  │ 71% 🟡     │
└─┴──────────┴──────────┴────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│              │              │              │              │
│  🏥 Medical  │  ⚖️ Legal    │ 💰 Financial │ 🌐 General   │
│              │              │              │              │
│ Reranking    │ Semantic     │ Hybrid       │ Simple dense │
│ gives +23%   │ chunking     │ retrieval    │ retrieval is │
│ faithfulness │ beats        │ performs     │ sufficient — │
│ — most       │ fixed-size   │ best —       │ no need for  │
│ impactful    │ by 18% —     │ numerical    │ reranker     │
│ domain for   │ legal docs   │ terms need   │ overhead     │
│ retrieval    │ have natural │ exact        │              │
│ quality      │ boundaries   │ keyword      │              │
│              │              │ matching     │              │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌──────────────┬──────────────┐
│              │              │
│ ⏱️ Latency    │ 🎯 Conclusion│
│              │              │
│ Adding a     │ No single    │
│ reranker     │ config wins  │
│ roughly      │ across all   │
│ doubles      │ domains —    │
│ latency      │ domain-      │
│ (0.9s →      │ specific     │
│ 2.1s) —      │ tuning is    │
│ not always   │ essential    │
│ worth it     │              │
└──────────────┴──────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  ❓ Which config is best for your use case?                          │
│                                                                       │
│  Domain-specific RAG configurations can significantly impact          │
│  performance. Choose the strategy that best matches your             │
│  requirements for accuracy, speed, and faithfulness.                 │
│                                                                       │
│                   [Gradient Background: Purple→Blue→Cyan]            │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Mobile View

```
┏━━━━━━━━━━━━━━━━━━┓
┃ 🏆 LEADERBOARD  ┃
┗━━━━━━━━━━━━━━━━━━┛

┌──────────────────┐
│ 🏥 Medical       │
│     91%          │
│   5 runs         │
└──────────────────┘

┌──────────────────┐
│ ⚖️ Legal         │
│     84%          │
│   3 runs         │
└──────────────────┘

┌──────────────────┐
│ 💰 Financial     │
│     79%          │
│   4 runs         │
└──────────────────┘

┌──────────────────┐
│ 🌐 General       │
│     88%          │
│   6 runs         │
└──────────────────┘

┌──────────────────────────────┐
│ Leaderboard [🏥 ▼]           │
├──────────────────────────────┤
│ 🥇 🏥 Medical │ 91% │ 15   │
│ 🥈 ⚖️ Legal   │ 84% │ 12   │
│ 🥉 💰 Finance │ 79% │ 10   │
│ 4  🌐 General │ 88% │ 18   │
└──────────────────────────────┘

[Chart responsive to mobile width]

[One finding card per line]
```

---

## Interactive Elements

### Sort Buttons
```
Click to change sort order:
┌──────┬──────┬──────┬──────┐
│ 🏥   │ ⚖️   │ 💰   │ 🌐   │
│Med   │Leg   │Fin   │Gen   │
└──────┴──────┴──────┴──────┘
  ↑
Highlights when selected
```

### Score Badges
```
🟢 Green: >= 70% (Excellent)
🟡 Amber: >= 50% (Good)  
🔴 Rose:  < 50% (Poor)

Examples:
91% 🟢  →  Excellent
76% 🟡  →  Good
48% 🔴  →  Poor
```

### Medals
```
🥇  First place (Rank 1)
🥈  Second place (Rank 2)
🥉  Third place (Rank 3)
1-10  Fourth+ places
```

---

## Color Usage

### Domain Colors (Applied Consistently)
```
🏥 Medical:
  - Rose accent: #fb7185
  - Light background: rgba(251, 113, 133, 0.1)
  - Strong accent: rgba(251, 113, 133, 0.3)

⚖️ Legal:
  - Blue accent: #60a5fa
  - Light background: rgba(96, 165, 250, 0.1)
  - Strong accent: rgba(96, 165, 250, 0.3)

💰 Financial:
  - Amber accent: #fbbf24
  - Light background: rgba(251, 191, 36, 0.1)
  - Strong accent: rgba(251, 191, 36, 0.3)

🌐 General:
  - Green accent: #34d399
  - Light background: rgba(52, 211, 153, 0.1)
  - Strong accent: rgba(52, 211, 153, 0.3)
```

### UI Colors (Dark Theme)
```
Background:     #0a0a0f  (Deep purple-black)
Card:           rgba(20, 20, 35, 0.7)  (Semi-transparent glass)
Text Primary:   #e8e8f0  (Off-white)
Text Secondary: #8b8ba3  (Gray)
Text Muted:     #5a5a73  (Dark gray)
Border:         rgba(255, 255, 255, 0.06)
Accent Border:  rgba(167, 139, 250, 0.3)
```

---

## Animations

### Smooth Transitions (in CSS)
```
Fast:    150ms ease        (button hover, badge change)
Normal:  250ms ease        (page fade-in, state change)
Chart:   800ms ease-in-out (data point appearance)
```

### Loading State
```
[Spinner] Loading leaderboard...

  Spinning circle animation
  Centered on page
  Gray text below
  Auto-hides when data loads
```

### Empty State
```
When no benchmarks run yet:

    📊
    
No Results Yet

Run benchmarks from the "Run Benchmark" page
to populate the leaderboard...

[Grey background card]
```

---

## Component Sizes

### Stat Cards
- Desktop: 25% width (4 columns)
- Tablet: 50% width (2 columns)
- Mobile: 100% width (1 column)
- Height: 140px
- Padding: 24px

### Main Table
- Columns: 9 (responsive with horizontal scroll on mobile)
- Row height: 48px
- Font: 14px body, 11px labels
- Hover background: rgba(167, 139, 250, 0.04)

### Best Config Highlight
- Background: Domain color + 10% opacity
- Border: Domain color + 30% opacity
- Padding: 16px
- Metrics displayed in 4-column grid

### Chart (SVG)
- Desktop: 600x400px
- Tablet: 70vw width
- Mobile: 100vw width (with padding)
- Responsive via viewBox

### Key Findings
- Desktop: 6 columns (3 rows)
- Tablet: 3 columns (2 rows)
- Mobile: 1 column (6 rows)
- Card padding: 16px
- Left border: 3px accent

---

## Responsive Behavior

### Large Screen (> 1024px)
```
Full desktop experience
- 4 stat cards in one row
- All table columns visible
- Chart at full size
- 6 findings in one row
```

### Medium Screen (768px - 1024px)
```
Optimized for tablet
- 2 stat cards per row
- Table with horizontal scroll
- Chart 70vw wide
- 3 findings per row
```

### Small Screen (< 768px)
```
Mobile-first design
- 1 stat card per row
- Essential table columns only
- Chart full width with padding
- 1-2 findings per row
- Larger touch targets (44px+)
```

---

## Accessibility Features

### Keyboard Navigation
- Tab through all buttons
- Sort buttons highlightable
- Visible focus indicators

### Color Contrast
- Text to background: 7:1 ratio (WCAG AAA)
- No color-only indicators
- Text + visual elements combined

### Text Sizes
- Headings: 32px (h1), 20px (h2), 16px (h3)
- Body: 14px (readable at all sizes)
- Labels: 12px (sufficient contrast)

### ARIA Labels
- Chart described with legend
- Table headers labeled
- Buttons have clear labels

---

## Example Configurations

```
Config 1: BGE + Semantic + Rerank
├─ Chunking: Semantic
├─ Retrieval: Dense (BGE) + Rerank
├─ K: 5
└─ Performance: 91% accuracy, 2.1s latency

Config 2: Dense + No Rerank
├─ Chunking: Fixed-size
├─ Retrieval: Dense only
├─ K: 5
└─ Performance: 81% accuracy, 0.9s latency

Config 3: Hybrid (Dense + BM25)
├─ Chunking: Semantic
├─ Retrieval: Dense + BM25
├─ K: 5
└─ Performance: 82% accuracy, 1.4s latency

Config 4: Ada + Dense
├─ Chunking: Fixed-size
├─ Retrieval: Dense (Ada)
├─ K: 5
└─ Performance: 78% accuracy, 1.1s latency
```

---

This visual overview shows the complete leaderboard layout, responsive design, color usage, and interactive elements. 🎨
