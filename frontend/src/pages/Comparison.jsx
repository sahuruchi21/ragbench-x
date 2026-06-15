import { useState, useEffect } from 'react'
import { api } from '../api.js'

const DOMAIN_META = {
  medical:   { icon: '🏥', color: '#ef4444', label: 'Medical' },
  financial: { icon: '💰', color: '#f59e0b', label: 'Financial' },
  legal:     { icon: '⚖️', color: '#3b82f6', label: 'Legal' },
  general:   { icon: '🌐', color: '#10b981', label: 'General' },
}

function ScoreBar({ score, color }) {
  const pct = Math.round((score || 0) * 100)
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 4, minWidth: 100 }}>
      <div style={{ fontSize: 14, fontWeight: 600, color: color }}>{pct}%</div>
      <div style={{
        height: 8,
        background: 'var(--bg-secondary)',
        borderRadius: 4,
        overflow: 'hidden',
      }}>
        <div style={{
          width: `${pct}%`,
          height: '100%',
          background: color,
          transition: 'width 0.3s ease',
        }} />
      </div>
    </div>
  )
}

function getConfigName(config) {
  const provider = config?.llm_provider || 'unknown'
  const chunking = config?.chunking_strategy || 'default'
  return `${provider} + ${chunking}`
}

export default function Comparison() {
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

  // Transform data: configs as rows, domains as columns
  const configMap = new Map()
  
  leaderboard.forEach(domainData => {
    const domain = domainData.domain
    domainData.all_configs.forEach(configData => {
      const configKey = JSON.stringify(configData.config)
      
      if (!configMap.has(configKey)) {
        configMap.set(configKey, {
          config: configData.config,
          name: getConfigName(configData.config),
          scores: {}
        })
      }
      
      configMap.get(configKey).scores[domain] = configData.avg_scores.overall_score
    })
  })

  const configs = Array.from(configMap.values())
  const domains = ['medical', 'financial', 'legal', 'general']
  const hasData = configs.length > 0

  // Calculate average score per config across domains
  configs.forEach(config => {
    const scores = domains.map(d => config.scores[d] || 0).filter(s => s > 0)
    config.avgScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0
  })

  // Sort by average score
  configs.sort((a, b) => b.avgScore - a.avgScore)

  return (
    <div className="fade-in">
      <div className="page-header">
        <h1>🎯 RAG Configuration Comparison</h1>
        <p>Compare RAG pipeline performance across Medical, Financial, Legal, and General domains</p>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner spinner-lg" />
          <span>Loading comparison data...</span>
        </div>
      )}

      {!loading && !hasData && (
        <div className="card" style={{ textAlign: 'center', padding: 60 }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>📊</div>
          <h3 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>No Results Yet</h3>
          <p style={{ color: 'var(--text-secondary)', maxWidth: 400, margin: '0 auto' }}>
            Run benchmarks to see RAG configuration comparisons across domains.
          </p>
        </div>
      )}

      {!loading && hasData && (
        <div className="card">
          <div style={{ overflowX: 'auto' }}>
            <table style={{
              width: '100%',
              borderCollapse: 'separate',
              borderSpacing: 0,
            }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border-light)' }}>
                  <th style={{
                    padding: '16px',
                    textAlign: 'left',
                    fontSize: 12,
                    fontWeight: 700,
                    color: 'var(--text-muted)',
                    textTransform: 'uppercase',
                    position: 'sticky',
                    left: 0,
                    background: 'var(--bg-primary)',
                    zIndex: 10,
                    minWidth: 200,
                  }}>
                    Configuration
                  </th>
                  {domains.map(domain => {
                    const meta = DOMAIN_META[domain]
                    return (
                      <th key={domain} style={{
                        padding: '16px',
                        textAlign: 'center',
                        fontSize: 12,
                        fontWeight: 700,
                        color: 'var(--text-muted)',
                        textTransform: 'uppercase',
                        minWidth: 140,
                      }}>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
                          <span style={{ fontSize: 20 }}>{meta.icon}</span>
                          <span>{meta.label}</span>
                        </div>
                      </th>
                    )
                  })}
                  <th style={{
                    padding: '16px',
                    textAlign: 'center',
                    fontSize: 12,
                    fontWeight: 700,
                    color: 'var(--text-muted)',
                    textTransform: 'uppercase',
                    minWidth: 120,
                  }}>
                    Avg Score
                  </th>
                </tr>
              </thead>
              <tbody>
                {configs.map((config, idx) => {
                  const isTop = idx === 0
                  
                  return (
                    <tr key={idx} style={{
                      borderBottom: '1px solid var(--border-light)',
                      background: isTop ? 'rgba(16, 185, 129, 0.05)' : 'transparent',
                    }}>
                      <td style={{
                        padding: '16px',
                        position: 'sticky',
                        left: 0,
                        background: isTop ? 'rgba(16, 185, 129, 0.05)' : 'var(--bg-primary)',
                        zIndex: 5,
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                          {isTop && <span style={{ fontSize: 16 }}>🏆</span>}
                          <div>
                            <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>
                              {config.name}
                            </div>
                            <div style={{
                              fontSize: 11,
                              color: 'var(--text-muted)',
                              fontFamily: 'var(--font-mono)',
                            }}>
                              K={config.config?.retrieval_k || 5}
                              {config.config?.rerank_k > 0 && ` → ${config.config.rerank_k}`}
                            </div>
                          </div>
                        </div>
                      </td>
                      {domains.map(domain => {
                        const score = config.scores[domain]
                        const meta = DOMAIN_META[domain]
                        
                        return (
                          <td key={domain} style={{
                            padding: '16px',
                            textAlign: 'center',
                          }}>
                            {score > 0 ? (
                              <ScoreBar score={score} color={meta.color} />
                            ) : (
                              <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>—</span>
                            )}
                          </td>
                        )
                      })}
                      <td style={{
                        padding: '16px',
                        textAlign: 'center',
                      }}>
                        <div style={{
                          fontSize: 18,
                          fontWeight: 700,
                          color: isTop ? '#10b981' : 'var(--text-primary)',
                        }}>
                          {Math.round(config.avgScore * 100)}%
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Key Findings */}
          <div style={{
            marginTop: 32,
            paddingTop: 32,
            borderTop: '1px solid var(--border-light)',
          }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 16 }}>💡 Key Findings</h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: 16,
            }}>
              {domains.map(domain => {
                const meta = DOMAIN_META[domain]
                const domainData = leaderboard.find(d => d.domain === domain)
                const bestConfig = domainData?.best_config
                
                if (!bestConfig) return null
                
                return (
                  <div key={domain} style={{
                    padding: 16,
                    background: `${meta.color}10`,
                    borderRadius: 8,
                    border: `1px solid ${meta.color}30`,
                  }}>
                    <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8 }}>
                      {meta.icon} {meta.label}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 8 }}>
                      Best: {getConfigName(bestConfig.config)}
                    </div>
                    <div style={{ fontSize: 20, fontWeight: 700, color: meta.color }}>
                      {Math.round(bestConfig.avg_scores.overall_score * 100)}%
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}