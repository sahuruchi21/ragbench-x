import { useState } from 'react'
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard.jsx'
import Benchmark from './pages/Benchmark.jsx'
import Leaderboard from './pages/Leaderboard.jsx'
import Comparison from './pages/Comparison.jsx'
import Results from './pages/Results.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/benchmark" element={<Benchmark />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/comparison" element={<Comparison />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">R</div>
        <div>
          <div className="sidebar-logo-text">RAGBench-X</div>
          <div className="sidebar-logo-badge">v1.0</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-title">Overview</div>
        <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} end>
          <span className="nav-icon">📊</span> Dashboard
        </NavLink>

        <div className="nav-section-title">Evaluate</div>
        <NavLink to="/benchmark" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <span className="nav-icon">🚀</span> Run Benchmark
        </NavLink>
        <NavLink to="/leaderboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <span className="nav-icon">🏆</span> Leaderboard
        </NavLink>
        <NavLink to="/comparison" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <span className="nav-icon">🎯</span> Comparison
        </NavLink>
        <NavLink to="/results" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <span className="nav-icon">📋</span> Results History
        </NavLink>

        <div style={{ flex: 1 }} />
        <div className="nav-section-title">Info</div>
        <div className="nav-link" style={{ cursor: 'default', fontSize: 12, color: 'var(--text-muted)' }}>
          <span className="nav-icon">⚡</span> 4 Domains • 5 Metrics
        </div>
      </nav>
    </aside>
  )
}
