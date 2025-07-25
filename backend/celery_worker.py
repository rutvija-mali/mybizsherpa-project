from celery_app import celery_app
from services.groq_service import groq_service
from services.supabase_service import supabase_service
import asyncio
import traceback
from datetime import datetime

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_transcript_task(self, transcript_id: str, transcript_text: str, company_name: str):
    """
    Celery task to process transcript with AI
    """
    try:
        print(f"[{datetime.now()}] Starting transcript task for ID: {transcript_id}")
        
        # Update status to processing
        asyncio.run(supabase_service.update_transcript_status(transcript_id, "processing"))
        
        # Process with AI
        insight = asyncio.run(groq_service.generate_transcript_insight(transcript_text))
        
        # Update with result
        asyncio.run(supabase_service.update_transcript_insight(transcript_id, insight))
        asyncio.run(supabase_service.update_transcript_status(transcript_id, "completed"))
        
        print(f"[{datetime.now()}] Completed transcript task for ID: {transcript_id}")
        
        return {
            "task_id": self.request.id,
            "transcript_id": transcript_id,
            "status": "completed",
            "company_name": company_name
        }
        
    except Exception as exc:
        print(f"[{datetime.now()}] Error in transcript task: {str(exc)}")
        print(traceback.format_exc())
        
        # Update status to failed
        asyncio.run(supabase_service.update_transcript_status(transcript_id, "failed"))
        
        # Retry logic
        if self.request.retries < self.max_retries:
            print(f"Retrying transcript task... Attempt {self.request.retries + 1}")
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        
        raise exc

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_linkedin_task(self, insight_id: str, linkedin_bio: str, pitch_deck: str):
    """
    Celery task to process LinkedIn insight with AI
    """
    try:
        print(f"[{datetime.now()}] Starting LinkedIn task for ID: {insight_id}")
        
        # Update status to processing
        asyncio.run(supabase_service.update_linkedin_status(insight_id, "processing"))
        
        # Process with AI
        result = asyncio.run(groq_service.generate_linkedin_icebreaker(linkedin_bio, pitch_deck))
        
        # Update with result
        asyncio.run(supabase_service.update_linkedin_insight(insight_id, result))
        asyncio.run(supabase_service.update_linkedin_status(insight_id, "completed"))
        
        print(f"[{datetime.now()}] Completed LinkedIn task for ID: {insight_id}")
        
        return {
            "task_id": self.request.id,
            "insight_id": insight_id,
            "status": "completed"
        }
        
    except Exception as exc:
        print(f"[{datetime.now()}] Error in LinkedIn task: {str(exc)}")
        print(traceback.format_exc())
        
        # Update status to failed
        asyncio.run(supabase_service.update_linkedin_status(insight_id, "failed"))
        
        # Retry logic
        if self.request.retries < self.max_retries:
            print(f"Retrying LinkedIn task... Attempt {self.request.retries + 1}")
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
        
        raise exc