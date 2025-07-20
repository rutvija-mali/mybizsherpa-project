'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { api } from '@/lib/api'

export default function TranscriptForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    company_name: '',
    attendees: '',
    date: '',
    transcript_text: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Basic validation
    if (formData.transcript_text.length < 200) {
      setError('Transcript seems too short. Please provide a more complete conversation.')
      setLoading(false)
      return
    }

    if (!formData.attendees.includes(',') && formData.attendees.split(' ').length < 2) {
      setError('Please include at least 2 attendees (you and the prospect).')
      setLoading(false)
      return
    }

    try {
      await api.createTranscript({
        ...formData,
        attendees: formData.attendees.split(',').map(a => a.trim())
      })
      
      setFormData({ company_name: '', attendees: '', date: '', transcript_text: '' })
      onSuccess()
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to create transcript analysis. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          📞 Transcript Insight Generator
        </CardTitle>
        <p className="text-sm text-gray-600">
          Upload your sales call transcript to get AI-powered feedback on your performance, 
          including what you did well and areas for improvement.
        </p>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert className="mb-4" variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Company Name *
            </label>
            <Input
              placeholder="e.g., Acme Corp, TechStart Inc"
              value={formData.company_name}
              onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">
              Meeting Attendees *
            </label>
            <Input
              placeholder="John Smith (you), Sarah Johnson (prospect), Mike Chen (decision maker)"
              value={formData.attendees}
              onChange={(e) => setFormData({ ...formData, attendees: e.target.value })}
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Separate names with commas. Include roles if helpful.
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">
              Meeting Date *
            </label>
            <Input
              type="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">
              Call Transcript *
            </label>
            <Textarea
              placeholder="Paste your full call transcript here...

Example format:
John: Thanks for taking the time to meet with us today. I wanted to discuss our new project management solution.
Sarah: We're currently using spreadsheets and it's getting chaotic with our team growth.
John: I understand that pain point. Our solution offers automated task tracking...

Tip: Copy transcript from Zoom, Teams, or Otter.ai"
              value={formData.transcript_text}
              onChange={(e) => setFormData({ ...formData, transcript_text: e.target.value })}
              required
              rows={12}
              className="min-h-[200px]"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>{formData.transcript_text.length} characters (minimum 200)</span>
              <span>💡 Longer transcripts = better insights</span>
            </div>
          </div>
          
          <Button 
            type="submit" 
            disabled={loading || formData.transcript_text.length < 200} 
            className="w-full"
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Analyzing Conversation...
              </div>
            ) : (
              'Generate Sales Insight'
            )}
          </Button>
        </form>
        
        <div className="mt-6 bg-blue-50 p-4 rounded-lg">
          <h4 className="font-medium text-sm text-blue-800 mb-2">💡 What You'll Get:</h4>
          <ul className="text-xs text-blue-700 space-y-1">
            <li>• <strong>What You Did Well:</strong> Specific strengths in your approach</li>
            <li>• <strong>Areas for Improvement:</strong> Actionable feedback for better results</li>
            <li>• <strong>Next Time Recommendations:</strong> Tactics to test in future calls</li>
          </ul>
        </div>
        
        <div className="mt-4 bg-gray-50 p-3 rounded text-xs text-gray-600">
          <strong>Common transcript sources:</strong> Zoom auto-transcript, Microsoft Teams, 
          Otter.ai, Rev.com, or manual notes. The more complete the conversation, the better the analysis.
        </div>
      </CardContent>
    </Card>
  )
}