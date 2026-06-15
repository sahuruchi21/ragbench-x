import { useState, useEffect } from 'react'
import { api } from '../api.js'

const DOMAIN_META = {
  medical:   { icon: '🏥', label: 'Medical' },
  financial: { icon: '💰', label: 'Financial' },
  legal:     { icon: '⚖️', label: 'Legal' },
  general:   { icon: '🌐', label: 'General' },
  custom:    { icon: '🔧', label: 'Custom' },
}

export default function Results() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')
  const [expanded, setExpanded] = useState(null)

  useEffect(() => {
    loadResults()
  }, [filter])

  const loadResults = () => {
    setLoading(true)
    api.getResults(filter || undefined, 100)
      .then(data => {
        setResults(data.results || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }

  const handleClear = async () => {
    if (confirm('Are you sure you want to clear all results?')) {
      await api.clearResults()
      setResults([])
    }
  }

  return (
    <div className="fade-in">
      <div className="page-header">
        <h1>Results History</h1>
        <p>Browse all benchmark runs with detailed scores and answers.</p>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24, alignItems: 'center', flexWrap: 'wrap' }}>
        <div
          className={`domain-chip ${!filter ? 'active' : ''} general`}
          onClick={() => setFilter('')}
        >
          All
        </div>
        {Object.entries(DOMAIN_META).filter(([k]) => k !== 'custom').map(([key, meta]) => (
          <div
            key={key}
            className={`domain-chip ${key} ${filter === key ? 'active' : ''}`}
            onClick={() => setFilter(key)}
          >
            {meta.icon} {meta.label}
          </div>
        ))}
        <div style={{ flex: 1 }} />
        {results.length > 0 && (
          <button className="btn btn-ghost btn-sm" onClick={handleClear} style={{ color: 'var(--accent-rose)' }}>
            🗑 Clear All
          </button>
        )}
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner spinner-lg" />
          <span>Loading results...</span>
        </div>
      )}

      {!loading && results.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>📋</div>
          <h3 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>No Results Yet</h3>
          <p style={{ color: 'var(--text-secondary)' }}>
            Run benchmarks to see results appear here.
          </p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div className="card-title">{results.length} Result{results.length !== 1 ? 's' : ''}</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {results.map((r, i) => {
              const meta = DOMAIN_META[r.domain] || { icon: '📁', label: r.domain }
              const isExpanded = expanded === r.id
              return (
                <div
                  key={r.id || i}
                  className="fade-in"
                  style={{
                    borderBottom: '1px solid var(--border-color)',
                    animationDelay: `${i * 50}ms`,
                  }}
                >
                  <div
                    style={{
                      display: 'flex', alignItems: 'center', gap: 16, padding: '16px 0',
                      cursor: 'pointer',
                    }}
                    onClick={() => setExpanded(isExpanded ? null : r.id)}
                  >
                    <span style={{ fontSize: 20 }}>{meta.icon}</span>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: 600, fontSize: 14, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {r.question}
                      </div>
                      <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                        {meta.label} • {r.config?.chunking_strategy} • {new Date(r.timestamp).toLocaleString()}
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      <ScoreBadge value={r.scores?.overall_score} />
                      <span style={{ fontSize: 12, color: 'var(--text-muted)', transform: isExpanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }}>
                        ▼
                      </span>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="slide-up" style={{ padding: '0 0 20px 36px' }}>
                      {/* Score Grid */}
                      <div className="grid-3" style={{ marginBottom: 16, gap: 12 }}>
                        {[
                          { k: 'faithfulness', l: 'Faithfulness' },
                          { k: 'hallucination_rate', l: 'Hallucination', inv: true },
                          { k: 'recall_at_k', l: 'Recall@K' },
                          { k: 'answer_relevancy', l: 'Relevancy' },
                          { k: 'bleu_score', l: 'BLEU' },
                          { k: 'overall_score', l: 'Overall' },
                        ].map(m => (
                          <div key={m.k} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 12px', background: 'var(--bg-glass)', borderRadius: 'var(--radius-sm)' }}>
                            <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{m.l}</span>
                            <ScoreBadge value={r.scores?.[m.k]} invert={m.inv} />
                          </div>
                        ))}
                      </div>
                      <div className="answer-block" style={{ marginBottom: 12 }}>
                        <div className="answer-label">Generated Answer</div>
                        {r.generated_answer}
                      </div>
                      <div className="answer-block gold-answer">
                        <div className="answer-label">Gold Answer</div>
                        {r.gold_answer}
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

function ScoreBadge({ value, invert }) {
  if (value === undefined || value === null) return <span style={{ color: 'var(--text-muted)' }}>—</span>
  const display = (value * 100).toFixed(1)
  const effective = invert ? 1 - value : value
  const cls = effective >= 0.7 ? 'excellent' : effective >= 0.5 ? 'good' : effective >= 0.3 ? 'average' : 'poor'
  return <span className={`score-badge ${cls}`}>{display}%</span>
}
