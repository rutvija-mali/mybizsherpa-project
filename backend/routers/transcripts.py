from fastapi import APIRouter, HTTPException, BackgroundTasks
from models import TranscriptInput, TranscriptResponse
from services.groq_service import groq_service
from services.supabase_service import supabase_service
from typing import List

router = APIRouter()

async def process_transcript_insight(transcript_id: str, transcript_text: str):
    """Background task to process transcript insight"""
    try:
        insight = await groq_service.generate_transcript_insight(transcript_text)
        await supabase_service.update_transcript_insight(transcript_id, insight)
    except Exception as e:
        print(f"Error processing transcript insight: {e}")

@router.post("/", response_model=TranscriptResponse)
async def create_transcript(transcript: TranscriptInput, background_tasks: BackgroundTasks):
    try:
        # Create transcript record
        data = {
            "company_name": transcript.company_name,
            "attendees": transcript.attendees,
            "date": transcript.date.isoformat(),
            "transcript_text": transcript.transcript_text
        }
        
        result = await supabase_service.create_transcript(data)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create transcript")
        
        # Process insight in background
        background_tasks.add_task(process_transcript_insight, result["id"], transcript.transcript_text)
        
        return TranscriptResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TranscriptResponse])
async def get_transcripts():
    try:
        results = await supabase_service.get_transcripts()
        return [TranscriptResponse(**item) for item in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))