'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'

export default function Feed() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [queueStats, setQueueStats] = useState(null)
  const [showQueueStats, setShowQueueStats] = useState(false)

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
          status: t.status || (t.insight_result ? 'completed' : 'processing')
        })),
        ...linkedinInsights.map((l) => ({
          id: l.id,
          type: 'linkedin',
          title: 'LinkedIn Icebreaker Analysis',
          subtitle: 'Cold outreach strategy',
          content: l.linkedin_bio.substring(0, 150) + '...',
          result: l.icebreaker_result,
          created_at: l.created_at,
          status: l.status || (l.icebreaker_result ? 'completed' : 'processing')
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

  const fetchQueueStats = async () => {
    try {
      const stats = await api.getQueueStats()
      setQueueStats(stats)
    } catch (error) {
      console.error('Error fetching queue stats:', error)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  // Auto-refresh every 30 seconds to check for processing completion
  useEffect(() => {
    const hasProcessingItems = items.some(item => 
      item.status === 'processing' || item.status === 'pending'
    )
    
    if (hasProcessingItems) {
      const interval = setInterval(() => {
        fetchData()
        if (showQueueStats) {
          fetchQueueStats()
        }
      }, 15000) // Reduced to 15 seconds for better UX
      return () => clearInterval(interval)
    }
  }, [items, showQueueStats])

  const getStatusBadge = (status) => {
    const statusConfig = {
      'completed': { variant: 'default', color: 'bg-green-100 text-green-800', label: '✅ Completed' },
      'processing': { variant: 'destructive', color: 'bg-yellow-100 text-yellow-800', label: '⏳ Processing' },
      'pending': { variant: 'destructive', color: 'bg-blue-100 text-blue-800', label: '📋 Queued' },
      'failed': { variant: 'destructive', color: 'bg-red-100 text-red-800', label: '❌ Failed' }
    }
    
    const config = statusConfig[status] || statusConfig['pending']
    return (
      <Badge className={config.color}>
        {config.label}
      </Badge>
    )
  }

  const getProcessingMessage = (status) => {
    const messages = {
      'pending': 'Your request is queued and will be processed shortly...',
      'processing': 'AI is analyzing your content. This may take a few moments...',
      'failed': 'Processing failed. Please try resubmitting or contact support.'
    }
    return messages[status] || 'Processing...'
  }

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

  const processingCount = items.filter(item => 
    item.status === 'processing' || item.status === 'pending'
  ).length

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Recent Insights</h2>
        <div className="flex items-center gap-2">
          <Badge variant="outline">{items.length} total</Badge>
          {processingCount > 0 && (
            <Badge className="bg-yellow-100 text-yellow-800">
              {processingCount} processing
            </Badge>
          )}
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setShowQueueStats(!showQueueStats)
              if (!showQueueStats) fetchQueueStats()
            }}
          >
            {showQueueStats ? 'Hide' : 'Show'} Queue Stats
          </Button>
        </div>
      </div>

      {showQueueStats && queueStats && (
        <Card className="bg-gray-50">
          <CardHeader>
            <CardTitle className="text-lg">Queue Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="text-center">
                <div className="font-bold text-xl text-blue-600">
                  {queueStats.active_tasks}
                </div>
                <div className="text-gray-600">Active Tasks</div>
              </div>
              <div className="text-center">
                <div className="font-bold text-xl text-yellow-600">
                  {queueStats.scheduled_tasks}
                </div>
                <div className="text-gray-600">Scheduled</div>
              </div>
              <div className="text-center">
                <div className="font-bold text-xl text-purple-600">
                  {queueStats.reserved_tasks}
                </div>
                <div className="text-gray-600">Reserved</div>
              </div>
              <div className="text-center">
                <div className="font-bold text-xl text-green-600">
                  {queueStats.workers_online}
                </div>
                <div className="text-gray-600">Workers Online</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      
      {items.map((item) => (
        <Card key={item.id} className="transition-shadow hover:shadow-md">
          <CardHeader>
            <CardTitle className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant={item.type === 'transcript' ? 'default' : 'secondary'}>
                    {item.type === 'transcript' ? '📞' : '💼'} {item.type}
                  </Badge>
                  {getStatusBadge(item.status)}
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
                <div className={`flex items-center space-x-2 text-sm p-3 rounded ${
                  item.status === 'failed' 
                    ? 'text-red-600 bg-red-50' 
                    : item.status === 'pending'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-amber-600 bg-amber-50'
                }`}>
                  {item.status !== 'failed' && (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></div>
                  )}
                  <span>{getProcessingMessage(item.status)}</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}