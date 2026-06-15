import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../api.js'

const DOMAINS = [
  { id: 'medical',   icon: '🏥', label: 'Medical' },
  { id: 'financial', icon: '💰', label: 'Financial' },
  { id: 'legal',     icon: '⚖️', label: 'Legal' },
  { id: 'general',   icon: '🌐', label: 'General' },
]

const STRATEGIES = ['semantic', 'sentence', 'fixed', 'paragraph']

export default function Benchmark() {
  const [searchParams] = useSearchParams()
  const [domain, setDomain] = useState(searchParams.get('domain') || 'medical')
  const [samples, setSamples] = useState([])
  const [questionMode, setQuestionMode] = useState('select') // ✅ NEW: 'select' or 'custom'
  const [selectedQuestion, setSelectedQuestion] = useState('')
  const [customQuestion, setCustomQuestion] = useState('') // ✅ NEW
  const [strategy, setStrategy] = useState('semantic')
  const [mode, setMode] = useState('single')
  const [loading, setLoading] = useState(false)
  const [loadingSamples, setLoadingSamples] = useState(false)
  const [result, setResult] = useState(null)
  const [compareResult, setCompareResult] = useState(null)
  const [allResult, setAllResult] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
  setLoadingSamples(true)
  setResult(null)
  setCompareResult(null)
  setAllResult(null)

  // Clear old custom question when switching domains
  setCustomQuestion('')
    api.getSamples(domain).then(data => {
      setSamples(data.samples || [])
      if (data.samples?.length) setSelectedQuestion(data.samples[0].question)
      setLoadingSamples(false)
    }).catch(() => setLoadingSamples(false))
  }, [domain])

  // ✅ Get the actual question to use
  const getQuestionText = () => {
  return questionMode === 'custom'
    ? customQuestion.trim()
    : selectedQuestion
}

  const runSingle = async () => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await api.runBenchmark({
        question: getQuestionText(),
        domain,
        chunking_strategy: strategy,
      })
      setResult(res)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  const runCompare = async () => {
    setLoading(true)
    setError(null)
    setCompareResult(null)
    try {
      const res = await api.compareConfigs({
        question: getQuestionText(),
        domain,
      })
      setCompareResult(res)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  const runAll = async () => {
    setLoading(true)
    setError(null)
    setAllResult(null)
    try {
      const res = await api.runBenchmarkAll({
        domain,
        max_samples: 5,
        chunking_strategy: strategy,
      })
      setAllResult(res)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  const handleRun = () => {
    if (mode === 'single') runSingle()
    else if (mode === 'compare') runCompare()
    else if (mode === 'all') runAll()
  }

  // ✅ Validate if we can run
  const canRun = () => {
  // Full-domain benchmark doesn't require question input
  if (mode === 'all') return true

  // Custom question mode
  if (questionMode === 'custom') {
    return customQuestion.trim().length > 0
  }

  // Default selected question mode
  return selectedQuestion.length > 0
}

  return (
    <div className="fade-in">
      <div className="page-header">
        <h1>Run Benchmark</h1>
        <p>Select a domain, pick a question, choose your RAG config, and see live scores.</p>
      </div>

      {/* Domain Selector */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-title" style={{ marginBottom: 16 }}>Select Domain</div>
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {DOMAINS.map(d => (
            <div
              key={d.id}
              className={`domain-chip ${d.id} ${domain === d.id ? 'active' : ''}`}
              onClick={() => setDomain(d.id)}
            >
              {d.icon} {d.label}
            </div>
          ))}
        </div>
      </div>

      {/* Config Panel */}
      <div className="grid-2" style={{ marginBottom: 24 }}>
        <div className="card">
          <div className="card-title" style={{ marginBottom: 16 }}>Question</div>
          
          {/* ✅ NEW: Question Mode Toggle */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            <button
              className={`btn ${questionMode === 'select' ? 'btn-primary' : 'btn-ghost'}`}
              style={{ flex: 1, fontSize: 13 }}
              onClick={() => setQuestionMode('select')}
            >
              📋 Select Question
            </button>
            <button
              className={`btn ${questionMode === 'custom' ? 'btn-primary' : 'btn-ghost'}`}
              style={{ flex: 1, fontSize: 13 }}
              onClick={() => setQuestionMode('custom')}
            >
              ✏️ Custom Question
            </button>
          </div>

          {loadingSamples ? (
            <div className="loading-overlay" style={{ padding: 20 }}>
              <div className="spinner" /> Loading samples...
            </div>
          ) : (
            <>
              {/* ✅ Select Mode */}
              {questionMode === 'select' && (
                <div className="input-group">
                  <label>Select a question</label>
                  <select
                    className="select"
                    value={selectedQuestion}
                    onChange={e => setSelectedQuestion(e.target.value)}
                  >
                    {samples.map((s, i) => (
                      <option key={i} value={s.question}>
                        {s.question.length > 80 ? s.question.slice(0, 80) + '...' : s.question}
                      </option>
                    ))}
                  </select>
                  <div style={{ marginTop: 12, padding: 12, background: 'var(--bg-glass)', borderRadius: 'var(--radius-sm)', fontSize: 13, color: 'var(--text-secondary)' }}>
                    {selectedQuestion}
                  </div>
                </div>
              )}

              {/* ✅ Custom Mode */}
              {questionMode === 'custom' && (
                <div className="input-group">
                  <label>Type your question</label>
                  <textarea
                    className="select"
                    style={{ 
                      minHeight: 100, 
                      fontFamily: 'inherit',
                      resize: 'vertical',
                      padding: 12
                    }}
                    placeholder="Enter your custom question here..."
                    value={customQuestion}
                    onChange={e => setCustomQuestion(e.target.value)}
                  />
                  <div style={{ marginTop: 8, fontSize: 12, color: 'var(--text-muted)' }}>
                    💡 Tip: Custom questions won't have gold answers for comparison
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        <div className="card">
          <div className="card-title" style={{ marginBottom: 16 }}>Configuration</div>
          <div className="input-group" style={{ marginBottom: 16 }}>
            <label>Benchmark Mode</label>
            <select className="select" value={mode} onChange={e => setMode(e.target.value)}>
              <option value="single">Single Question — one strategy</option>
              <option value="compare">Compare — all strategies on one question</option>
              <option value="all">Full Domain — all questions, one strategy</option>
            </select>
          </div>
          {mode !== 'compare' && (
            <div className="input-group" style={{ marginBottom: 16 }}>
              <label>Chunking Strategy</label>
              <select className="select" value={strategy} onChange={e => setStrategy(e.target.value)}>
                {STRATEGIES.map(s => (
                  <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
                ))}
              </select>
            </div>
          )}
          <button
            className="btn btn-primary btn-lg"
            style={{ width: '100%', marginTop: 8 }}
            onClick={handleRun}
            disabled={loading || !canRun()}
          >
            {loading ? <><span className="spinner" /> Running...</> : '🚀 Run Benchmark'}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card" style={{ borderColor: 'var(--accent-rose)', background: 'rgba(251,113,133,0.05)', marginBottom: 24 }}>
          <div style={{ color: 'var(--accent-rose)', fontWeight: 600 }}>⚠ Error</div>
          <div style={{ color: 'var(--text-secondary)', marginTop: 8 }}>{error}</div>
        </div>
      )}

      {/* Single Result */}
      {result && <SingleResult data={result} isCustom={questionMode === 'custom'} />}

      {/* Compare Result */}
      {compareResult && <CompareResult data={compareResult} isCustom={questionMode === 'custom'} />}

      {/* All Domain Result */}
      {allResult && <AllDomainResult data={allResult} />}
    </div>
  )
}

function SingleResult({ data, isCustom }) {
  const s = data.scores
  return (
    <div className="slide-up">
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-header">
          <div>
            <div className="card-title">Benchmark Result</div>
            <div className="card-subtitle">
              {data.domain} • {data.config?.chunking_strategy} strategy
              {isCustom && ' • Custom Question'}
            </div>
          </div>
          <span className={`score-badge ${s.overall_score >= 0.7 ? 'excellent' : s.overall_score >= 0.5 ? 'good' : s.overall_score >= 0.3 ? 'average' : 'poor'}`} style={{ fontSize: 18, padding: '8px 18px' }}>
            {(s.overall_score * 100).toFixed(1)}%
          </span>
        </div>

        <ScoreBreakdown scores={s} />

        <div style={{ marginTop: 24 }}>
          <div className="answer-block">
            <div className="answer-label">Generated Answer</div>
            {data.generated_answer}
          </div>
          {!isCustom && data.gold_answer && (
            <div className="answer-block gold-answer">
              <div className="answer-label">Gold (Expected) Answer</div>
              {data.gold_answer}
            </div>
          )}
        </div>

        {data.pipeline_metadata?.timings && (
          <div style={{ marginTop: 20, display: 'flex', gap: 16, flexWrap: 'wrap' }}>
            {Object.entries(data.pipeline_metadata.timings).map(([k, v]) => (
              <div key={k} style={{ fontSize: 12, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                {k.replace('_ms', '')}: <span style={{ color: 'var(--accent-cyan)' }}>{v}ms</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function CompareResult({ data, isCustom }) {
  const best = data.best_config
  return (
    <div className="slide-up">
      {/* Best Config Banner */}
      <div className="best-config-banner">
        <div className="trophy">🏆</div>
        <div className="info">
          <h3>Best RAG Configuration: {best.strategy.toUpperCase()} Chunking</h3>
          <p>
            Overall Score: <strong>{(best.overall_score * 100).toFixed(1)}%</strong> — This configuration produced the most faithful and relevant answer for this question.
          </p>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-header">
          <div>
            <div className="card-title">Strategy Comparison</div>
            <div className="card-subtitle">
              All chunking strategies tested on: "{data.question}"
              {isCustom && ' (Custom Question)'}
            </div>
          </div>
        </div>

        <table className="data-table">
          <thead>
            <tr>
              <th>Strategy</th>
              <th>Overall</th>
              <th>Faithfulness</th>
              <th>Hallucination</th>
              <th>Recall</th>
              <th>Relevancy</th>
              <th>BLEU</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {data.comparisons
              .sort((a, b) => b.scores.overall_score - a.scores.overall_score)
              .map((c, i) => (
                <tr key={i} style={c.strategy === best.strategy ? { background: 'rgba(52,211,153,0.06)' } : {}}>
                  <td>
                    <span style={{ fontWeight: 700 }}>
                      {c.strategy === best.strategy && '🥇 '}{c.strategy}
                    </span>
                  </td>
                  <td><ScoreBadge value={c.scores.overall_score} /></td>
                  <td><ScoreBadge value={c.scores.faithfulness} /></td>
                  <td><ScoreBadge value={c.scores.hallucination_rate} invert /></td>
                  <td><ScoreBadge value={c.scores.recall_at_k} /></td>
                  <td><ScoreBadge value={c.scores.answer_relevancy} /></td>
                  <td><ScoreBadge value={c.scores.bleu_score} /></td>
                  <td>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: 13, color: 'var(--text-secondary)' }}>
                      {c.timings?.total_ms}ms
                    </span>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {/* Best Answer */}
      <div className="card">
        <div className="card-title" style={{ marginBottom: 12 }}>Best Answer ({best.strategy})</div>
        <div className="answer-block">
          <div className="answer-label">Generated by {best.strategy} chunking</div>
          {best.answer}
        </div>
        {!isCustom && data.gold_answer && (
          <div className="answer-block gold-answer">
            <div className="answer-label">Gold (Expected) Answer</div>
            {data.gold_answer}
          </div>
        )}
      </div>
    </div>
  )
}

function AllDomainResult({ data }) {
  return (
    <div className="slide-up">
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="card-header">
          <div>
            <div className="card-title">Full Domain Benchmark — {data.domain}</div>
            <div className="card-subtitle">{data.total_questions} questions evaluated</div>
          </div>
        </div>

        {/* Average Scores */}
        <div style={{ marginBottom: 24 }}>
          <h4 style={{ fontSize: 14, fontWeight: 700, marginBottom: 12, color: 'var(--text-secondary)' }}>
            Average Scores
          </h4>
          <ScoreBreakdown scores={data.average_scores} />
        </div>

        {/* Per-Question Table */}
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Question</th>
              <th>Overall</th>
              <th>Faithfulness</th>
              <th>Hallucination</th>
              <th>Recall</th>
            </tr>
          </thead>
          <tbody>
            {data.results.map((r, i) => (
              <tr key={i}>
                <td style={{ color: 'var(--text-muted)' }}>{i + 1}</td>
                <td style={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {r.question}
                </td>
                <td><ScoreBadge value={r.scores.overall_score} /></td>
                <td><ScoreBadge value={r.scores.faithfulness} /></td>
                <td><ScoreBadge value={r.scores.hallucination_rate} invert /></td>
                <td><ScoreBadge value={r.scores.recall_at_k} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function ScoreBreakdown({ scores }) {
  if (!scores) return null
  const metrics = [
    { key: 'faithfulness',      label: 'Faithfulness',      desc: 'How grounded in context' },
    { key: 'hallucination_rate', label: 'Hallucination Rate', desc: 'Lower is better', invert: true },
    { key: 'recall_at_k',       label: 'Recall@K',           desc: 'Context coverage' },
    { key: 'answer_relevancy',   label: 'Answer Relevancy',   desc: 'Question relevance' },
    { key: 'bleu_score',         label: 'BLEU Score',          desc: 'vs gold answer' },
  ]
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {metrics.map(m => {
        const val = scores[m.key]
        if (val === undefined) return null
        const effective = m.invert ? 1 - val : val
        const pct = (val * 100).toFixed(1)
        const cls = effective >= 0.7 ? 'excellent' : effective >= 0.5 ? 'good' : effective >= 0.3 ? 'average' : 'poor'
        return (
          <div key={m.key}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
              <span style={{ fontSize: 13, fontWeight: 600 }}>{m.label}</span>
              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{m.desc}</span>
            </div>
            <div className="score-bar-container">
              <div className="score-bar">
                <div className={`score-bar-fill ${cls}`} style={{ width: `${val * 100}%` }} />
              </div>
              <span className="score-value" style={{ color: `var(--accent-${cls === 'excellent' ? 'green' : cls === 'good' ? 'blue' : cls === 'average' ? 'amber' : 'rose'})` }}>
                {pct}%
              </span>
            </div>
          </div>
        )
      })}
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