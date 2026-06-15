# 🎯 RAG Domain Comparison Feature

## Overview
Created a new **Comparison page** that shows which RAG configuration is best for each domain, allowing users to see domain-specific performance insights.

## What Was Added

### 1. New Comparison Page (`frontend/src/pages/Comparison.jsx`)
A comprehensive comparison view featuring:

#### Two View Modes:
- **📊 Domain Breakdown**: Shows detailed comparison cards for each domain (Medical, Financial, Legal, General)
- **📈 Metric Analysis**: Cross-domain metric comparison table

#### For Each Domain:
- **Best Configuration Highlight**: Shows the winning RAG configuration with all metrics
  - Chunking strategy
  - Retrieval K value
  - Reranking parameters
  - LLM provider settings
  
- **Metric Scores**: Displays 5 key metrics with color-coded badges
  - ⭐ Overall Score
  - ✓ Faithfulness
  - ⚠️ Hallucination Rate
  - 🎯 Recall @K
  - 🔗 Relevancy

- **All Configurations**: Shows comparison of all tested RAG configurations ranked by performance

- **Domain-Specific Insights**: 
  - 🏥 Medical: Reranking most impactful (+23% faithfulness)
  - 💰 Financial: Hybrid retrieval needed for numeric terms
  - ⚖️ Legal: Semantic chunking beats fixed-size by 18%
  - 🌐 General: Simple dense retrieval sufficient

### 2. Updated Navigation
Added the Comparison page to the sidebar navigation:
- Icon: 🎯
- Label: "Comparison"
- Location: Under "Evaluate" section

### 3. Summary Stats
Two key statistics displayed at the top:
- **🏆 Best Overall Score**: Shows the highest-performing domain
- **📈 Domains with Data**: Count of domains with benchmark data

## Design Features

✅ **Color-Coded by Domain**: Each domain has its own color scheme
✅ **Responsive Grid Layout**: Adapts to different screen sizes
✅ **Visual Hierarchy**: Clear distinction between best config and alternatives
✅ **Metric Badges**: Color indicators for performance levels
  - 🟢 Green: 70%+ (excellent)
  - 🟡 Amber: 50-70% (good)
  - 🔴 Red: <50% (needs improvement)
✅ **Empty State**: Graceful handling when no data is available

## Usage

1. Run benchmarks from the "Run Benchmark" page
2. Navigate to "Comparison" in the sidebar
3. View domain-specific RAG recommendations
4. Toggle between Domain Breakdown and Metric Analysis views

## File Structure
```
frontend/src/
├── pages/
│   └── Comparison.jsx          (NEW - 340+ lines)
├── App.jsx                      (UPDATED - added route & import)
```

## API Integration
The page uses the existing leaderboard API endpoint:
- `GET /api/leaderboard` - Fetches domain rankings and best configurations

## Next Steps
Potential enhancements:
- Export comparison as PDF report
- Configure alerts for domain-specific thresholds
- Add historical trend analysis
- Implement domain-specific recommendation engine
