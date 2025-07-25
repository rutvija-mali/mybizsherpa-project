from fastapi import APIRouter, HTTPException
from models import LinkedInInput, LinkedInResponse, QueueResponse
from services.supabase_service import supabase_service
from services.queue_service import queue_service
from typing import List
import traceback

router = APIRouter()

@router.post("/", response_model=QueueResponse)
async def create_linkedin_insight(linkedin: LinkedInInput):
    """Create LinkedIn insight and queue for processing"""
    try:
        # Create LinkedIn insight record with pending status
        data = {
            "linkedin_bio": linkedin.linkedin_bio,
            "pitch_deck_content": linkedin.pitch_deck_content,
            "status": "pending"
        }
        
        result = await supabase_service.create_linkedin_insight(data)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create LinkedIn insight")
        
        # Queue the processing task
        task_id = queue_service.enqueue_linkedin(
            result["id"],
            linkedin.linkedin_bio,
            linkedin.pitch_deck_content
        )
        
        return QueueResponse(
            id=result["id"],
            task_id=task_id,
            status="queued",
            message="LinkedIn icebreaker analysis queued for processing"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[LinkedInResponse])
async def get_linkedin_insights():
    """Get all LinkedIn insights"""
    try:
        results = await supabase_service.get_linkedin_insights()
        return [LinkedInResponse(**item) for item in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{insight_id}", response_model=LinkedInResponse)
async def get_linkedin_insight(insight_id: str):
    """Get specific LinkedIn insight by ID"""
    try:
        # This would need to be implemented in supabase_service
        result = await supabase_service.get_linkedin_insight_by_id(insight_id)
        if not result:
            raise HTTPException(status_code=404, detail="LinkedIn insight not found")
        return LinkedInResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Keep test endpoints for debugging
@router.post("/test-groq")
async def test_groq_service():
    """Test endpoint to check if Groq service is working"""
    try:
        from services.groq_service import groq_service
        
        test_bio = "VP of Operations at TechStart Inc. Passionate about scaling operations."
        test_pitch = "AI-Powered Project Management Tool. 40% faster delivery."

        result = await groq_service.generate_linkedin_icebreaker(test_bio, test_pitch)

        return {
            "status": "success",
            "result_length": len(result) if result else 0,
            "result_preview": result[:200] if result else "No result"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.post("/test-supabase/{insight_id}")
async def test_supabase_update(insight_id: str):
    """Test endpoint to check if Supabase update is working"""
    try:
        test_result = "TEST UPDATE - This is a manual test update"
        success = await supabase_service.update_linkedin_insight(insight_id, test_result)

        return {
            "status": "success" if success else "failed",
            "insight_id": insight_id,
            "update_success": success
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }