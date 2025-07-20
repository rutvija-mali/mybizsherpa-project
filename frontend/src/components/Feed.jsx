'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { api } from '@/lib/api'

export default function Feed() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const [transcripts, linkedinInsights] = await Promise.all([
        api.getTranscripts(),
        api.getLinkedInInsights()
      ])

      const feedItems = [
        ...transcripts.map((t) => ({
          id: t.id,
          type: 'transcript',
          title: `${t.company_name} - Transcript Analysis`,
          subtitle: `${t.attendees?.join(', ')} • ${t.date}`,
          content: t.transcript_text.substring(0, 150) + '...',
          result: t.insight_result,
          created_at: t.created_at,
          status: t.insight_result ? 'completed' : 'processing'
        })),
        ...linkedinInsights.map((l) => ({
          id: l.id,
          type: 'linkedin',
          title: 'LinkedIn Icebreaker Analysis',
          subtitle: 'Cold outreach strategy',
          content: l.linkedin_bio.substring(0, 150) + '...',
          result: l.icebreaker_result,
          created_at: l.created_at,
          status: l.icebreaker_result ? 'completed' : 'processing'
        }))
      ]

      feedItems.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      setItems(feedItems)
    } catch (error) {
      console.error('Error fetching data:', error)
      setError('Failed to load insights. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  // Auto-refresh every 30 seconds to check for processing completion
  useEffect(() => {
    const hasProcessingItems = items.some(item => item.status === 'processing')
    if (hasProcessingItems) {
      const interval = setInterval(fetchData, 30000) // 30 seconds
      return () => clearInterval(interval)
    }
  }, [items])

  if (loading && items.length === 0) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2">Loading insights...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center p-8">
        <p className="text-red-600 mb-4">{error}</p>
        <Button onClick={fetchData}>Try Again</Button>
      </div>
    )
  }

  if (items.length === 0) {
    return (
      <div className="text-center p-8">
        <h3 className="text-lg font-medium mb-2">No insights yet</h3>
        <p className="text-gray-600">Submit a transcript or LinkedIn analysis to get started!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Recent Insights</h2>
        <Badge variant="outline">{items.length} total</Badge>
      </div>
      
      {items.map((item) => (
        <Card key={item.id} className="transition-shadow hover:shadow-md">
          <CardHeader>
            <CardTitle className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant={item.type === 'transcript' ? 'default' : 'secondary'}>
                    {item.type === 'transcript' ? '📞' : '💼'} {item.type}
                  </Badge>
                  <Badge variant={item.status === 'completed' ? 'outline' : 'destructive'}>
                    {item.status}
                  </Badge>
                </div>
                <h3 className="font-semibold">{item.title}</h3>
                {item.subtitle && (
                  <p className="text-sm text-gray-600 font-normal">{item.subtitle}</p>
                )}
              </div>
              <span className="text-sm text-gray-500">
                {new Date(item.created_at).toLocaleDateString()}
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-sm text-gray-700 mb-2">Original Content:</h4>
                <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded border-l-4 border-gray-300">
                  {item.content}
                </p>
              </div>
              
              {item.result ? (
                <div>
                  <h4 className="font-medium text-sm text-gray-700 mb-2">AI Analysis:</h4>
                  <div className="text-sm whitespace-pre-wrap bg-blue-50 p-4 rounded border-l-4 border-blue-400">
                    {item.result}
                  </div>
                </div>
              ) : (
                <div className="flex items-center space-x-2 text-sm text-amber-600 bg-amber-50 p-3 rounded">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-amber-600"></div>
                  <span>Processing analysis... This may take a few moments.</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}