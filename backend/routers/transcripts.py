from fastapi import APIRouter, HTTPException
from models import TranscriptInput, TranscriptResponse, QueueResponse
from services.supabase_service import supabase_service
from services.queue_service import queue_service
from typing import List

router = APIRouter()

@router.post("/", response_model=QueueResponse)
async def create_transcript(transcript: TranscriptInput):
    """Create transcript and queue for processing"""
    try:
        # Create transcript record with pending status
        data = {
            "company_name": transcript.company_name,
            "attendees": transcript.attendees,
            "date": transcript.date.isoformat(),
            "transcript_text": transcript.transcript_text,
            "status": "pending"
        }
        
        result = await supabase_service.create_transcript(data)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create transcript")
        
        # Queue the processing task
        task_id = queue_service.enqueue_transcript(
            result["id"], 
            transcript.transcript_text, 
            transcript.company_name
        )
        
        return QueueResponse(
            id=result["id"],
            task_id=task_id,
            status="queued",
            message=f"Transcript analysis queued for processing. Company: {transcript.company_name}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[TranscriptResponse])
async def get_transcripts():
    """Get all transcripts"""
    try:
        results = await supabase_service.get_transcripts()
        return [TranscriptResponse(**item) for item in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{transcript_id}", response_model=TranscriptResponse)
async def get_transcript(transcript_id: str):
    """Get specific transcript by ID"""
    try:
        # This would need to be implemented in supabase_service
        result = await supabase_service.get_transcript_by_id(transcript_id)
        if not result:
            raise HTTPException(status_code=404, detail="Transcript not found")
        return TranscriptResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))