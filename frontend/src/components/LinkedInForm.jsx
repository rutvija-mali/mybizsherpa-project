'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { api } from '@/lib/api'

export default function LinkedInForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    linkedin_bio: '',
    pitch_deck_content: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Basic validation
    if (formData.linkedin_bio.length < 50) {
      setError('LinkedIn bio seems too short. Please provide more detail.')
      setLoading(false)
      return
    }

    if (formData.pitch_deck_content.length < 100) {
      setError('Pitch deck content seems too short. Please provide more detail.')
      setLoading(false)
      return
    }

    try {
      await api.createLinkedInInsight(formData)
      setFormData({ linkedin_bio: '', pitch_deck_content: '' })
      onSuccess()
    } catch (error) {
      console.error('Error:', error)
      setError('Failed to create LinkedIn insight. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          💼 LinkedIn Icebreaker Generator
        </CardTitle>
        <p className="text-sm text-gray-600">
          Generate personalized cold outreach strategies based on LinkedIn profiles and your pitch deck.
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
              LinkedIn Bio/About Section
            </label>
            <Textarea
              placeholder="Paste the person's LinkedIn 'About' section here...
              
Example:
VP of Operations at TechStart Inc. Passionate about scaling operations and building efficient systems. Previously led ops at 2 unicorn startups..."
              value={formData.linkedin_bio}
              onChange={(e) => setFormData({ ...formData, linkedin_bio: e.target.value })}
              required
              rows={6}
              className="min-h-[120px]"
            />
            <p className="text-xs text-gray-500 mt-1">
              {formData.linkedin_bio.length} characters (minimum 50)
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">
              Your Pitch Deck Content
            </label>
            <Textarea
              placeholder="Summarize your pitch deck key points here...

Example:
Slide 1: AI-Powered Project Management Tool
Slide 2: 40% faster project delivery for teams
Slide 3: Used by 500+ scaling startups
Slide 4: Integrates with Slack, Asana, Jira
Slide 5: Case study: 65% reduction in meeting overhead
Slide 6: Pricing starts at $10/user/month"
              value={formData.pitch_deck_content}
              onChange={(e) => setFormData({ ...formData, pitch_deck_content: e.target.value })}
              required
              rows={8}
              className="min-h-[160px]"
            />
            <p className="text-xs text-gray-500 mt-1">
              {formData.pitch_deck_content.length} characters (minimum 100)
            </p>
          </div>
          
          <Button 
            type="submit" 
            disabled={loading || formData.linkedin_bio.length < 50 || formData.pitch_deck_content.length < 100} 
            className="w-full"
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Analyzing & Generating...
              </div>
            ) : (
              'Generate Icebreaker Strategy'
            )}
          </Button>
        </form>
        
        <div className="mt-4 text-xs text-gray-500">
          <p className="font-medium">This will analyze:</p>
          <ul className="list-disc list-inside mt-1 space-y-1">
            <li>Key buying signals from their background</li>
            <li>Smart discovery questions to ask</li>
            <li>Most relevant parts of your pitch</li>
            <li>Personalized cold outreach message</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}
