const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
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
  }
}