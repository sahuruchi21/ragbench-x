/**
 * Accuracy vs Latency Tradeoff Chart
 * Visualizes the relationship between RAG config accuracy and response latency
 */

export function TradeoffChart({ data = [] }) {
  // Sample tradeoff data (in production, this would come from backend results)
  const tradeoffs = data.length > 0 ? data : [
    { name: 'BGE + Hybrid + Rerank', accuracy: 0.91, latency: 2.1, domain: 'medical' },
    { name: 'Dense + No rerank', accuracy: 0.81, latency: 0.9, domain: 'general' },
    { name: 'BGE + Dense', accuracy: 0.82, latency: 1.4, domain: 'financial' },
    { name: 'Ada + Dense', accuracy: 0.78, latency: 1.1, domain: 'legal' },
  ]

  // Calculate dimensions
  const width = 600
  const height = 400
  const padding = 60

  // Scale functions
  const maxAccuracy = Math.max(...tradeoffs.map(d => d.accuracy), 1)
  const maxLatency = Math.max(...tradeoffs.map(d => d.latency), 3)

  const xScale = (val) => padding + (val / maxLatency) * (width - padding * 2)
  const yScale = (val) => height - padding - (val / maxAccuracy) * (height - padding * 2)

  return (
    <div style={{ padding: 24, background: 'var(--bg-card)', borderRadius: 'var(--radius-lg)', marginBottom: 24 }}>
      <div style={{ marginBottom: 24 }}>
        <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>📈 Accuracy vs Latency Tradeoff</h3>
        <p style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
          Position on chart represents the accuracy-latency tradeoff. Top-right is ideal (high accuracy, fast). 
          Bottom-left is poor performance on both metrics.
        </p>
      </div>

      <svg
        viewBox={`0 0 ${width} ${height}`}
        style={{ width: '100%', maxWidth: 600, height: 'auto', marginBottom: 24 }}
      >
        {/* Grid lines */}
        {[0.2, 0.4, 0.6, 0.8, 1].map((y) => (
          <line
            key={`grid-h-${y}`}
            x1={padding}
            y1={yScale(y * maxAccuracy)}
            x2={width - padding}
            y2={yScale(y * maxAccuracy)}
            stroke="rgba(255, 255, 255, 0.05)"
            strokeDasharray="4"
          />
        ))}
        {[0.2, 0.4, 0.6, 0.8, 1].map((x) => (
          <line
            key={`grid-v-${x}`}
            x1={xScale(x * maxLatency)}
            y1={padding}
            x2={xScale(x * maxLatency)}
            y2={height - padding}
            stroke="rgba(255, 255, 255, 0.05)"
            strokeDasharray="4"
          />
        ))}

        {/* Axes */}
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="var(--border-accent)" strokeWidth="2" />
        <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="var(--border-accent)" strokeWidth="2" />

        {/* Axis labels */}
        <text x={width - padding + 20} y={height - padding + 5} fill="var(--text-secondary)" fontSize="12">
          Latency (s)
        </text>
        <text x={padding - 50} y={padding - 20} fill="var(--text-secondary)" fontSize="12">
          Accuracy
        </text>

        {/* Tick marks and labels */}
        {[0, 0.2, 0.4, 0.6, 0.8, 1].map((val) => (
          <g key={`y-tick-${val}`}>
            <line x1={padding - 5} y1={yScale(val * maxAccuracy)} x2={padding} y2={yScale(val * maxAccuracy)} stroke="var(--text-muted)" />
            <text x={padding - 35} y={yScale(val * maxAccuracy) + 4} fill="var(--text-muted)" fontSize="11" textAnchor="end">
              {(val * 100).toFixed(0)}%
            </text>
          </g>
        ))}

        {[0, 0.5, 1, 1.5, 2, 2.5, 3].map((val) => {
          if (val > maxLatency) return null
          return (
            <g key={`x-tick-${val}`}>
              <line x1={xScale(val)} y1={height - padding} x2={xScale(val)} y2={height - padding + 5} stroke="var(--text-muted)" />
              <text x={xScale(val)} y={height - padding + 20} fill="var(--text-muted)" fontSize="11" textAnchor="middle">
                {val}s
              </text>
            </g>
          )
        })}

        {/* Data points */}
        {tradeoffs.map((point, i) => {
          const x = xScale(point.latency)
          const y = yScale(point.accuracy)
          const colors = {
            medical: 'var(--accent-rose)',
            financial: 'var(--accent-amber)',
            legal: 'var(--accent-blue)',
            general: 'var(--accent-green)',
          }
          const color = colors[point.domain] || 'var(--accent-purple)'

          return (
            <g key={i}>
              {/* Shadow */}
              <circle cx={x} cy={y} r="8" fill={color} opacity="0.1" />
              {/* Point */}
              <circle cx={x} cy={y} r="5" fill={color} stroke="var(--bg-primary)" strokeWidth="2" />
              {/* Label */}
              <text
                x={x}
                y={y - 18}
                fill="var(--text-primary)"
                fontSize="11"
                fontWeight="600"
                textAnchor="middle"
                style={{ pointerEvents: 'none' }}
              >
                {(point.accuracy * 100).toFixed(0)}%
              </text>
            </g>
          )
        })}

        {/* Ideal zone annotation */}
        <rect
          x={xScale(1.5)}
          y={yScale(0.8)}
          width={width - padding - xScale(1.5)}
          height={yScale(0.8) - padding}
          fill="var(--accent-green)"
          opacity="0.05"
          rx="4"
        />
        <text x={width - 70} y={padding + 20} fill="var(--accent-green)" fontSize="12" fontWeight="700" opacity="0.6">
          Ideal
        </text>
      </svg>

      {/* Legend */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
        gap: 12,
        paddingTop: 12,
        borderTop: '1px solid var(--border-color)',
      }}>
        {[
          { icon: '🏥', label: 'Medical', color: 'var(--accent-rose)' },
          { icon: '⚖️', label: 'Legal', color: 'var(--accent-blue)' },
          { icon: '💰', label: 'Financial', color: 'var(--accent-amber)' },
          { icon: '🌐', label: 'General', color: 'var(--accent-green)' },
        ].map((item) => (
          <div key={item.label} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: '50%',
                background: item.color,
              }}
            />
            <span style={{ fontSize: 12 }}>{item.icon} {item.label}</span>
          </div>
        ))}
      </div>

      {/* Data points list */}
      <div style={{ marginTop: 24, paddingTop: 24, borderTop: '1px solid var(--border-color)' }}>
        <h4 style={{ fontSize: 13, fontWeight: 700, marginBottom: 12 }}>Configurations</h4>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: 12,
        }}>
          {tradeoffs.map((config, i) => (
            <div
              key={i}
              style={{
                padding: 12,
                borderRadius: 'var(--radius-sm)',
                background: 'var(--bg-secondary)',
                fontSize: 12,
              }}
            >
              <div style={{ fontWeight: 600, marginBottom: 4 }}>{config.name}</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: 11 }}>
                Accuracy: <strong>{(config.accuracy * 100).toFixed(1)}%</strong> • Latency: <strong>{config.latency}s</strong>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
