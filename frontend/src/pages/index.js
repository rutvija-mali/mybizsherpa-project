'use client'

import { useState } from 'react'
import TranscriptForm from '@/components/TranscriptForm'
import LinkedInForm from '@/components/LinkedInForm'
import Feed from '@/components/Feed'

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0)

  const handleSuccess = () => {
    setRefreshKey(prev => prev + 1)
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold text-center mb-8">AI Workflow Assistant</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <TranscriptForm onSuccess={handleSuccess} />
        <LinkedInForm onSuccess={handleSuccess} />
      </div>
      
      <Feed key={refreshKey} />
    </div>
  )
}