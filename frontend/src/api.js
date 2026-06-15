const API_BASE = '/api'

async function request(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'API request failed')
  }
  return res.json()
}

export const api = {
  getDatasets: () => request('/datasets'),
  getDomains: () => request('/domains'),
  getSamples: (domain, max = 5) => request(`/samples/${domain}?max_samples=${max}`),
  
  runBenchmark: (data) => request('/benchmark', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  runBenchmarkAll: (data) => request('/benchmark/all', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  runCustomBenchmark: (data) => request('/benchmark/custom', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  compareConfigs: (data) => request('/benchmark/compare', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  getResults: (domain, limit = 100) => {
    const params = new URLSearchParams({ limit })
    if (domain) params.append('domain', domain)
    return request(`/results?${params}`)
  },

  getLeaderboard: () => request('/leaderboard'),

  clearResults: () => request('/results', { method: 'DELETE' }),
}
