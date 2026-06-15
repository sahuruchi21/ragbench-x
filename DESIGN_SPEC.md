# 🎨 AGBench-X Leaderboard Visual Design

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        PAGE HEADER                              │
│  🏆 Leaderboard                                                 │
│  Best performing RAG configurations ranked by domain.           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────┬──────────────┬──────────────┐
│   STAT CARD  │  STAT CARD   │  STAT CARD   │  STAT CARD   │
│  🏥 Medical  │  ⚖️ Legal    │  💰 Financial│  🌐 General  │
│    91%       │     84%      │     79%      │     88%      │
│  5 runs      │   3 runs     │   4 runs     │   6 runs     │
└──────────────┴──────────────┴──────────────┴──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ LEADERBOARD TABLE                          [🏥 ⚖️ 💰 🌐]        │
├──┬─────────┬──────────┬─────────┬──────────┬───────────────────┤
│# │ Domain  │ Config   │ Overall │ Faith.  │ Halluc. │ Recall  │
├──┼─────────┼──────────┼─────────┼──────────┼─────────┼─────────┤
│🥇│ 🏥 Med  │ Semantic │ 91%🟢   │ 88%🟢   │ 12%🟢   │ 85%🟢  │
│🥈│ ⚖️ Leg  │ Semantic │ 84%🟢   │ 81%🟢   │ 15%🟢   │ 79%🟡  │
│🥉│ 💰 Fin  │ Hybrid   │ 79%🟢   │ 76%🟡   │ 18%🟡   │ 82%🟢  │
│4 │ 🌐 Gen  │ Dense    │ 88%🟢   │ 85%🟢   │ 14%🟢   │ 87%🟢  │
└──┴─────────┴──────────┴─────────┴──────────┴─────────┴─────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 📈 ACCURACY VS LATENCY TRADEOFF                                 │
│                                                                 │
│  100% ┌───────────────────────────────────────────────          │
│       │                            ●                            │
│  90%  │                  ●         Ideal Zone                   │
│       │               ●  ● ●       (light green)                │
│  80%  │            ●     ●                                       │
│       │         ●                                                │
│  70%  ├─────●───────────────────────────────────                │
│       │  0.5s    1.0s    1.5s    2.0s    2.5s    3.0s Latency  │
│       │                                                          │
│  Legend: 🏥 Medical  ⚖️ Legal  💰 Financial  🌐 General        │
│                                                                 │
│  Configs:                                                        │
│  • BGE + Rerank: 91% accuracy, 2.1s latency                    │
│  • Dense Only: 81% accuracy, 0.9s latency                      │
│  • Hybrid: 82% accuracy, 1.4s latency                          │
│  • Ada + Dense: 78% accuracy, 1.1s latency                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🏥 MEDICAL DOMAIN LEADERBOARD                                   │
│ 15 total runs • 4 configurations                                │
├─────────────────────────────────────────────────────────────────┤
│                         🏆 BEST CONFIG                          │
│  Strategy: SEMANTIC CHUNKING                                    │
│  Overall: 91% | Faithfulness: 88% | Hallucination: 12%          │
│  Recall: 85% | Tested on 15 questions                           │
├──┬──────────┬──────────┬──────────────────────────────────────┤
│# │ Strategy │ Provider │ Overall │ Faithful │ Halluc. │ Recall │
├──┼──────────┼──────────┼──────────┼──────────┼─────────┼────────┤
│🥇│Semantic  │ template │ 91%🟢   │ 88%🟢    │ 12%🟢   │ 85%🟢 │
│🥈│Fixed-size│ template │ 85%🟢   │ 82%🟢    │ 18%🟡   │ 79%🟡 │
│🥉│Hybrid    │ template │ 78%🟢   │ 75%🟡    │ 22%🟡   │ 76%🟡 │
│4 │Dense     │ template │ 72%🟡   │ 68%🟡    │ 28%🟡   │ 71%🟡 │
└──┴──────────┴──────────┴──────────┴──────────┴─────────┴────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ⚖️ LEGAL DOMAIN LEADERBOARD                                     │
│ 3 total runs • 2 configurations                                 │
├─────────────────────────────────────────────────────────────────┤
│                         🏆 BEST CONFIG                          │
│  Strategy: SEMANTIC CHUNKING                                    │
│  Overall: 84% | Faithfulness: 81% | Hallucination: 15%          │
│  Recall: 79% | Tested on 3 questions                            │
├──┬──────────┬──────────┬──────────────────────────────────────┤
│# │ Strategy │ Provider │ Overall │ Faithful │ Halluc. │ Recall │
├──┼──────────┼──────────┼──────────┼──────────┼─────────┼────────┤
│🥇│Semantic  │ template │ 84%🟢   │ 81%🟢    │ 15%🟢   │ 79%🟡 │
│🥈│Fixed-size│ template │ 76%🟡   │ 72%🟡    │ 25%🟡   │ 71%🟡 │
└──┴──────────┴──────────┴──────────┴──────────┴─────────┴────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🔍 KEY FINDINGS                                                 │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│             │             │             │                     │
│ 🏥 MEDICAL  │ ⚖️ LEGAL    │ 💰 FINANCE  │ 🌐 GENERAL          │
│             │             │             │                     │
│ Reranking   │ Semantic    │ Hybrid      │ Simple dense        │
│ gives +23%  │ chunking    │ retrieval   │ retrieval is        │
│ faithfulness│ beats       │ performs    │ sufficient —        │
│ — most      │ fixed-size  │ best —      │ no need for         │
│ impactful   │ by 18% —    │ numerical   │ reranker            │
│ domain for  │ legal docs  │ terms need  │ overhead            │
│ retrieval   │ have natural│ exact       │                     │
│ quality     │ boundaries  │ keyword     │                     │
│             │             │ matching    │                     │
└─────────────┴─────────────┴─────────────┴─────────────────────┘

┌─────────────┬─────────────┐
│             │             │
│ ⏱️ LATENCY   │ 🎯 CONCLUSION
│             │             │
│ Adding a    │ No single   │
│ reranker    │ config wins │
│ roughly     │ across all  │
│ doubles     │ domains —   │
│ latency     │ domain-     │
│ (0.9s →     │ specific    │
│ 2.1s) —     │ tuning is   │
│ not always  │ essential   │
│ worth it    │             │
└─────────────┴─────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ❓ Which config is best for your use case?                    │
│                                                                 │
│  Domain-specific RAG configurations can significantly impact    │
│  performance. Choose the strategy that best matches your        │
│  requirements for accuracy, speed, and faithfulness.            │
│                                                                 │
│                    [Gradient Background]                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Hierarchy

```
<Leaderboard>
  ├─ Page Header
  │  ├─ Title: "🏆 Leaderboard"
  │  └─ Description
  │
  ├─ Stats Grid (4-column)
  │  ├─ Domain Card (Medical)
  │  ├─ Domain Card (Legal)
  │  ├─ Domain Card (Financial)
  │  └─ Domain Card (General)
  │
  ├─ Leaderboard Table
  │  ├─ Domain Sort Buttons
  │  └─ Data Table
  │     ├─ Rank
  │     ├─ Domain (with emoji)
  │     ├─ Best Config
  │     └─ 5 Metric Columns (Score Badges)
  │
  ├─ Tradeoff Chart
  │  ├─ SVG Scatter Plot
  │  ├─ Grid Lines
  │  ├─ Axes & Labels
  │  ├─ Data Points (colored by domain)
  │  ├─ Ideal Zone Highlight
  │  ├─ Legend
  │  └─ Data Table
  │
  ├─ Per-Domain Sections (repeat for each domain)
  │  ├─ Domain Header
  │  ├─ Best Config Highlight
  │  │  ├─ Trophy Emoji
  │  │  ├─ Config Name
  │  │  └─ 4 Key Metrics
  │  └─ Config Ranking Table
  │
  ├─ Key Findings Grid (6-column)
  │  ├─ Finding Card (Medical)
  │  ├─ Finding Card (Legal)
  │  ├─ Finding Card (Financial)
  │  ├─ Finding Card (General)
  │  ├─ Finding Card (Latency)
  │  └─ Finding Card (Conclusion)
  │
  └─ CTA Banner
     ├─ Question
     └─ Description
```

---

## Color & Typography

### Type Scale
```
Page Title:    32px bold     (e8e8f0)
Section Title: 20px bold     (e8e8f0)
Card Title:    16px bold     (e8e8f0)
Body:          14px normal   (8b8ba3)
Label:         12px normal   (5a5a73)
Caption:       11px normal   (5a5a73)
```

### Background Layers
```
Level 0: #0a0a0f (Main background)
Level 1: #12121a (Secondary background)
Level 2: rgba(20, 20, 35, 0.7) (Cards with glass effect)
Level 3: rgba(255, 255, 255, 0.03) (Subtle overlay)
```

### Accent Accents
```
Primary gradient:   Purple → Blue → Cyan
Warm gradient:      Rose → Amber
Cool gradient:      Cyan → Purple
Card gradient:      Purple (0.08 opacity) → Blue (0.04)
```

---

## Interactive States

### Buttons
```
Normal:
  Background: var(--bg-input)
  Color: var(--text-secondary)

Hover:
  Background: var(--bg-input) (slightly brighter)
  Transform: scale(1.02)

Active (sortBy === key):
  Background: var(--domain-color)20
  Color: var(--domain-color)
```

### Table Rows
```
Normal: bg-transparent
Hover: rgba(167, 139, 250, 0.04)
Best: rgba(52, 211, 153, 0.06) (green for #1)
```

### Cards
```
Normal:
  Background: var(--bg-card)
  Shadow: var(--shadow-sm)

Hover:
  Background: var(--bg-card-hover)
  Shadow: var(--shadow-md)
  Border: var(--border-accent)
```

---

## Responsive Breakpoints

### Large Screen (> 1024px)
- 4-column grid: 25% width each
- Full data table with all columns visible
- Chart at 600x400px
- Key findings: 6 columns

### Medium Screen (768px - 1024px)
- 2-column grid: 50% width each
- Table: Horizontal scroll on mobile columns
- Chart: 70vw width
- Key findings: 3 columns

### Small Screen (< 768px)
- 1-column grid: 100% width
- Table: Simplified with essential columns only
- Chart: 100vw width (with padding)
- Key findings: 1-2 columns
- Font sizes reduced

---

## Animation Timings

```
Fade-in Page:      300ms ease
Hover Effects:     150ms ease
Loading Spinner:   800ms linear infinite
Table Row Hover:   150ms ease
Button Click:      100ms ease
```

---

## Accessibility Features

✅ **High Contrast**: Text passes WCAG AAA (7:1 ratio)  
✅ **Color Blind**: No red-only indicators, uses text + badges  
✅ **Keyboard Navigation**: Tab through sorting buttons  
✅ **ARIA Labels**: Chart has alt text via legend  
✅ **Semantic HTML**: Proper heading hierarchy (h1-h4)  
✅ **Focus Indicators**: Visible on interactive elements  
✅ **Reduced Motion**: Respects prefers-reduced-motion  

---

## Mobile Considerations

📱 **Touch Targets**: All buttons >= 44px  
📱 **No Hover State**: Buttons work on tap/click  
📱 **Readable Text**: >= 16px base size  
📱 **Scrollable Tables**: Horizontal scroll on small screens  
📱 **Optimized Images**: SVG chart scales perfectly  
📱 **Safe Area**: Padding on notched devices  

---

## Dark Mode (Default)

The design uses a carefully crafted dark theme:
- **Primary**: Deep purple-black (#0a0a0f)
- **Cards**: Frosted glass effect
- **Accents**: Vibrant neon colors for readability
- **No light mode**: Optimized for late-night analysis

---

## Visual Hierarchy

1. **Most Important**: Page title + key stats
2. **Important**: Main leaderboard table
3. **Supporting**: Per-domain details
4. **Insights**: Key findings
5. **Call-to-Action**: CTA banner at bottom

---

This design creates a professional, information-rich dashboard while maintaining excellent readability and mobile responsiveness. 🎨
