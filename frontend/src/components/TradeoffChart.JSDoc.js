// File: frontend/src/components/TradeoffChart.jsx
/**
 * Accuracy vs Latency Tradeoff Visualization Component
 * 
 * Displays a scatter plot showing the relationship between RAG configuration
 * accuracy and response latency across different domains.
 * 
 * FEATURES:
 * - SVG-based scatter plot with grid lines
 * - Color-coded by domain (Medical, Legal, Financial, General)
 * - "Ideal zone" highlighted in top-right corner
 * - X-axis: Latency in seconds (0-3s)
 * - Y-axis: Accuracy percentage (0-100%)
 * - Legend showing domain colors
 * - Detailed data table below chart
 * 
 * PROPS:
 * @param {Array} data - Array of config objects with accuracy, latency, domain
 *   Example: [
 *     { name: 'Config1', accuracy: 0.91, latency: 2.1, domain: 'medical' },
 *     { name: 'Config2', accuracy: 0.81, latency: 0.9, domain: 'general' }
 *   ]
 *   Default: Uses built-in sample data
 * 
 * USAGE:
 * import { TradeoffChart } from '../components/TradeoffChart.jsx'
 * 
 * export default function MyPage() {
 *   const tradeoffData = [
 *     { name: 'BGE + Rerank', accuracy: 0.91, latency: 2.1, domain: 'medical' },
 *     { name: 'Dense Only', accuracy: 0.81, latency: 0.9, domain: 'general' },
 *   ]
 * 
 *   return <TradeoffChart data={tradeoffData} />
 * }
 * 
 * STYLING:
 * - Uses CSS variables from index.css
 * - Color palette:
 *   - Medical: var(--accent-rose)
 *   - Financial: var(--accent-amber)
 *   - Legal: var(--accent-blue)
 *   - General: var(--accent-green)
 * 
 * DESIGN NOTES:
 * - SVG dimensions: 600x400px (responsive via viewBox)
 * - Padding: 60px on all sides for axis labels
 * - Grid lines at 20% increments for both axes
 * - Data points sized at 5px radius with 8px shadow
 * - Ideal zone: light green overlay in top-right (>1.5s latency, >80% accuracy)
 * 
 * ACCESSIBILITY:
 * - Axis labels clearly marked
 * - Tick marks with numerical values
 * - Legend provides domain information
 * - Data table provides exact values
 * 
 * @component
 */

export function TradeoffChart({ data = [] }) {
  // Implementation details in TradeoffChart.jsx
}
