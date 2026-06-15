import { useState, useEffect } from 'react'
import { api } from '../api.js'

const DOMAIN_META = {
  medical:   { icon: '🏥', color: '#ef4444', label: 'Medical' },
  financial: { icon: '💰', color: '#f59e0b', label: 'Financial' },
  legal:     { icon: '⚖️', color: '#3b82f6', label: 'Legal' },
  general:   { icon: '🌐', color: '#10b981', label: 'General' },
}

function getScoreClass(score) {
  if (score >= 0.90) return 'excellent'
  if (score >= 0.75) return 'good'
  if (score >= 0.60) return 'average'
  return 'poor'
}

function getHallucinationClass(score) {
  if (score <= 0.10) return 'excellent'
  if (score <= 0.25) return 'good'
  if (score <= 0.40) return 'average'
  return 'poor'
}

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getLeaderboard()
      .then(data => {
        setLeaderboard(data.leaderboard || [])
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="loading-overlay">
        <div className="spinner spinner-lg" />
        <span>Loading leaderboard...</span>
      </div>
    )
  }

  const hasData = leaderboard.length > 0

  return (
    <div className="fade-in">
      <div className="page-header">
        <h1>🏆 RAGBench-X Leaderboard</h1>
        <p>Rank and analyze the best performing RAG configurations across multiple domains</p>
      </div>

      {!hasData ? (
        <div className="card" style={{ textAlign: 'center', padding: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>🏆</div>
          <h3 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>No Rankings Yet</h3>
          <p style={{ color: 'var(--text-secondary)', maxWidth: 400, margin: '0 auto' }}>
            Run benchmarks to generate leaderboard rankings and find your top configuration.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 40 }}>
          {leaderboard.map((domainData, i) => {
            const domain = domainData.domain
            const meta = DOMAIN_META[domain] || { icon: '📁', color: 'var(--accent-purple)', label: domain }
            const bestConfig = domainData.best_config

            return (
              <div key={i} className="card fade-in" style={{ animationDelay: `${i * 100}ms` }}>
                
                {/* Domain Title */}
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
                  <span style={{ fontSize: 28 }}>{meta.icon}</span>
                  <div>
                    <h2 style={{ fontSize: 22, fontWeight: 850, margin: 0 }}>
                      {meta.label} Domain
                    </h2>
                    <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                      Based on {domainData.total_runs || 0} evaluation runs
                    </span>
                  </div>
                </div>

                {/* Best Config Banner */}
                {bestConfig && (
                  <div className="best-config-banner">
                    <span className="trophy">🏆</span>
                    <div className="info" style={{ flex: 1 }}>
                      <h3>Top Performer</h3>
                      <p style={{ margin: 0, fontWeight: 500 }}>
                        {(bestConfig.config?.llm_provider || 'unknown').toUpperCase()} + {bestConfig.config?.chunking_strategy || 'default'} chunking (k={bestConfig.config?.retrieval_k || 5})
                      </p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div className="score-badge excellent">
                        ★ {Math.round((bestConfig.avg_scores?.overall_score || 0) * 100)}% Overall
                      </div>
                    </div>
                  </div>
                )}

                {/* Configurations Table */}
                <div style={{ overflowX: 'auto', marginTop: 16 }}>
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th style={{ width: 60 }}>Rank</th>
                        <th>RAG Configuration</th>
                        <th>Chunking</th>
                        <th>Faithfulness</th>
                        <th>Hallucination</th>
                        <th>Relevancy</th>
                        <th style={{ textAlign: 'right' }}>Overall Score</th>
                      </tr>
                    </thead>
                    <tbody>
                      {domainData.all_configs.map((cfg, idx) => {
                        const isTop = idx === 0
                        const scores = cfg.avg_scores || {}
                        
                        return (
                          <tr 
                            key={idx} 
                            style={{ 
                              background: isTop ? 'rgba(52, 211, 153, 0.04)' : 'transparent',
                              borderLeft: isTop ? '3px solid var(--accent-green)' : 'none'
                            }}
                          >
                            <td style={{ fontWeight: 700, paddingLeft: isTop ? 13 : 16 }}>
                              {isTop ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `#${idx + 1}`}
                            </td>
                            <td>
                              <div style={{ fontWeight: 600, textTransform: 'uppercase' }}>
                                {cfg.config?.llm_provider || 'unknown'}
                              </div>
                              <div style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                                {cfg.config?.retrieval_type || 'hybrid'} • {cfg.config?.embedding_model || 'bge'} (k={cfg.config?.retrieval_k || 5}{cfg.config?.rerank_k > 0 ? ` → ${cfg.config.rerank_k}` : ''})
                              </div>
                            </td>
                            <td style={{ textTransform: 'capitalize', color: 'var(--text-secondary)' }}>
                              {cfg.config?.chunking_strategy || 'default'}
                            </td>
                            <td>
                              <span className={`score-badge ${getScoreClass(scores.faithfulness || 0)}`}>
                                {Math.round((scores.faithfulness || 0) * 100)}%
                              </span>
                            </td>
                            <td>
                              <span className={`score-badge ${getHallucinationClass(scores.hallucination_rate || 0)}`}>
                                {Math.round((scores.hallucination_rate || 0) * 100)}%
                              </span>
                            </td>
                            <td>
                              <span className={`score-badge ${getScoreClass(scores.answer_relevancy || 0)}`}>
                                {Math.round((scores.answer_relevancy || 0) * 100)}%
                              </span>
                            </td>
                            <td style={{ textAlign: 'right', fontWeight: 700, fontSize: 15 }}>
                              <span className={`score-badge ${getScoreClass(scores.overall_score || 0)}`}>
                                {Math.round((scores.overall_score || 0) * 100)}%
                              </span>
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>

              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}