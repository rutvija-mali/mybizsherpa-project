// const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// export const api = {
//   async createTranscript(data) {
//     const response = await fetch(`${API_BASE}/api/transcripts/`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(data)
//     })
//     if (!response.ok) throw new Error('Failed to create transcript')
//     return response.json()
//   },

//   async getTranscripts() {
//     const response = await fetch(`${API_BASE}/api/transcripts/`)
//     if (!response.ok) throw new Error('Failed to fetch transcripts')
//     return response.json()
//   },

//   async createLinkedInInsight(data) {
//     const response = await fetch(`${API_BASE}/api/linkedin/`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify(data)
//     })
//     if (!response.ok) throw new Error('Failed to create LinkedIn insight')
//     return response.json()
//   },

//   async getLinkedInInsights() {
//     const response = await fetch(`${API_BASE}/api/linkedin/`)
//     if (!response.ok) throw new Error('Failed to fetch LinkedIn insights')
//     return response.json()
//   }
// }

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  // TRANSCRIPT METHODS
  async createTranscript(data) {
    const response = await fetch(`${API_BASE}/api/transcripts/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create transcript')
    return response.json()
  },

  async getTranscripts() {
    const response = await fetch(`${API_BASE}/api/transcripts/`)
    if (!response.ok) throw new Error('Failed to fetch transcripts')
    return response.json()
  },

  async getTranscript(id) {
    const response = await fetch(`${API_BASE}/api/transcripts/${id}`)
    if (!response.ok) throw new Error('Failed to fetch transcript')
    return response.json()
  },

  // LINKEDIN METHODS
  async createLinkedInInsight(data) {
    const response = await fetch(`${API_BASE}/api/linkedin/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error('Failed to create LinkedIn insight')
    return response.json()
  },

  async getLinkedInInsights() {
    const response = await fetch(`${API_BASE}/api/linkedin/`)
    if (!response.ok) throw new Error('Failed to fetch LinkedIn insights')
    return response.json()
  },

  async getLinkedInInsight(id) {
    const response = await fetch(`${API_BASE}/api/linkedin/${id}`)
    if (!response.ok) throw new Error('Failed to fetch LinkedIn insight')
    return response.json()
  },

  // QUEUE/TASK METHODS
  async getTaskStatus(taskId) {
    const response = await fetch(`${API_BASE}/api/tasks/status/${taskId}`)
    if (!response.ok) throw new Error('Failed to fetch task status')
    return response.json()
  },

  async getQueueStats() {
    const response = await fetch(`${API_BASE}/api/tasks/queue/stats`)
    if (!response.ok) throw new Error('Failed to fetch queue stats')
    return response.json()
  },

  // HEALTH CHECK
  async healthCheck() {
    const response = await fetch(`${API_BASE}/health`)
    if (!response.ok) throw new Error('Health check failed')
    return response.json()
  }
}