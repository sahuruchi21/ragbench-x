import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api.js'

const DOMAIN_INFO = {
  medical:   { icon: '🏥', color: 'var(--accent-rose)',  label: 'Medical' },
  financial: { icon: '💰', color: 'var(--accent-amber)', label: 'Financial' },
  legal:     { icon: '⚖️', color: 'var(--accent-blue)',  label: 'Legal' },
  general:   { icon: '🌐', color: 'var(--accent-green)', label: 'General' },
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [datasets, setDatasets] = useState([])
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.getDatasets().catch(() => ({ datasets: [] })),
      api.getResults(null, 20).catch(() => ({ results: [], total: 0 })),
    ]).then(([ds, res]) => {
      setDatasets(ds.datasets || [])
      setResults(res.results || [])
      setLoading(false)
    })
  }, [])

  const totalRuns = results.length
  const avgScore = results.length
    ? (results.reduce((s, r) => s + (r.scores?.overall_score || 0), 0) / results.length).toFixed(3)
    : '—'
  const domainsCovered = [...new Set(results.map(r => r.domain))].length

  return (
    <div className="fade-in">
      <div className="page-header">
        <h1>RAGBench-X Dashboard</h1>
        <p>Benchmark RAG pipelines across Medical, Financial, Legal, and General domains with real-time scoring.</p>
      </div>

      {/* Stats Row */}
      <div className="grid-4" style={{ marginBottom: 32 }}>
        <div className="stat-card">
          <div className="stat-value">{totalRuns}</div>
          <div className="stat-label">Total Runs</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{avgScore}</div>
          <div className="stat-label">Avg Score</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{domainsCovered}/4</div>
          <div className="stat-label">Domains Tested</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">5</div>
          <div className="stat-label">Metrics</div>
        </div>
      </div>

      {/* Domain Cards */}
      <div className="card-header" style={{ marginBottom: 16 }}>
        <h2 className="card-title">Available Domains</h2>
        <button className="btn btn-primary btn-sm" onClick={() => navigate('/benchmark')}>
          🚀 Run Benchmark
        </button>
      </div>

      <div className="grid-2" style={{ marginBottom: 32 }}>
        {Object.entries(DOMAIN_INFO).map(([key, info]) => {
          const ds = datasets.find(d => d.id === key)
          const domainResults = results.filter(r => r.domain === key)
          const domainAvg = domainResults.length
            ? (domainResults.reduce((s, r) => s + (r.scores?.overall_score || 0), 0) / domainResults.length).toFixed(3)
            : null

          return (
            <div key={key} className="card" style={{ cursor: 'pointer' }} onClick={() => navigate(`/benchmark?domain=${key}`)}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16 }}>
                <div style={{
                  width: 48, height: 48, borderRadius: 'var(--radius-md)',
                  background: `${info.color}15`, display: 'flex', alignItems: 'center',
                  justifyContent: 'center', fontSize: 24
                }}>
                  {info.icon}
                </div>
                <div>
                  <div style={{ fontWeight: 700, fontSize: 16 }}>{info.label}</div>
                  <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                    {ds ? ds.description : 'Question Answering'}
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                  {ds ? `${ds.sample_count} samples` : '5 samples'}
                </span>
                {domainAvg && (
                  <span className={`score-badge ${domainAvg >= 0.7 ? 'excellent' : domainAvg >= 0.5 ? 'good' : domainAvg >= 0.3 ? 'average' : 'poor'}`}>
                    {domainAvg}
                  </span>
                )}
                {!domainAvg && (
                  <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>Not tested</span>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent Results */}
      {results.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div>
              <div className="card-title">Recent Results</div>
              <div className="card-subtitle">Latest benchmark runs across all domains</div>
            </div>
            <button className="btn btn-ghost btn-sm" onClick={() => navigate('/results')}>
              View All →
            </button>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>Domain</th>
                <th>Question</th>
                <th>Strategy</th>
                <th>Faithfulness</th>
                <th>Hallucination</th>
                <th>Overall</th>
              </tr>
            </thead>
            <tbody>
              {results.slice(0, 5).map((r, i) => (
                <tr key={i} className="fade-in" style={{ animationDelay: `${i * 80}ms` }}>
                  <td>
                    <span className={`domain-chip ${r.domain}`}>
                      {DOMAIN_INFO[r.domain]?.icon} {DOMAIN_INFO[r.domain]?.label || r.domain}
                    </span>
                  </td>
                  <td style={{ maxWidth: 250, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {r.question}
                  </td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: 13 }}>
                      {r.config?.chunking_strategy}
                    </span>
                  </td>
                  <td><ScoreCell value={r.scores?.faithfulness} /></td>
                  <td><ScoreCell value={r.scores?.hallucination_rate} invert /></td>
                  <td><ScoreCell value={r.scores?.overall_score} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Getting Started */}
      {results.length === 0 && !loading && (
        <div className="card" style={{ textAlign: 'center', padding: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>🚀</div>
          <h3 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>Ready to Benchmark</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: 24, maxWidth: 400, margin: '0 auto 24px' }}>
            Start by running your first benchmark to see RAG pipeline scores across different domains and configurations.
          </p>
          <button className="btn btn-primary btn-lg" onClick={() => navigate('/benchmark')}>
            Run Your First Benchmark
          </button>
        </div>
      )}
    </div>
  )
}

function ScoreCell({ value, invert }) {
  if (value === undefined || value === null) return <span style={{ color: 'var(--text-muted)' }}>—</span>
  const display = (value * 100).toFixed(1)
  const effective = invert ? 1 - value : value
  const cls = effective >= 0.7 ? 'excellent' : effective >= 0.5 ? 'good' : effective >= 0.3 ? 'average' : 'poor'
  return <span className={`score-badge ${cls}`}>{display}%</span>
}
