# from fastapi import APIRouter, HTTPException, BackgroundTasks
# from models import LinkedInInput, LinkedInResponse
# from services.groq_service import groq_service
# from services.supabase_service import supabase_service
# from typing import List

# router = APIRouter()

# async def process_linkedin_insight(insight_id: str, linkedin_bio: str, pitch_deck: str):
#     """Background task to process LinkedIn insight"""
#     try:
#         result = await groq_service.generate_linkedin_icebreaker(linkedin_bio, pitch_deck)
#         await supabase_service.update_linkedin_insight(insight_id, result)
#     except Exception as e:
#         print(f"Error processing LinkedIn insight: {e}")

# @router.post("/", response_model=LinkedInResponse)
# async def create_linkedin_insight(linkedin: LinkedInInput, background_tasks: BackgroundTasks):
#     try:
#         # Create LinkedIn insight record
#         data = {
#             "linkedin_bio": linkedin.linkedin_bio,
#             "pitch_deck_content": linkedin.pitch_deck_content
#         }
        
#         result = await supabase_service.create_linkedin_insight(data)
#         if not result:
#             raise HTTPException(status_code=500, detail="Failed to create LinkedIn insight")
        
#         # Process insight in background
#         background_tasks.add_task(
#             process_linkedin_insight, 
#             result["id"], 
#             linkedin.linkedin_bio, 
#             linkedin.pitch_deck_content
#         )
        
#         return LinkedInResponse(**result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/", response_model=List[LinkedInResponse])
# async def get_linkedin_insights():
#     try:
#         results = await supabase_service.get_linkedin_insights()
#         return [LinkedInResponse(**item) for item in results]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException, BackgroundTasks
from models import LinkedInInput, LinkedInResponse
from services.groq_service import groq_service
from services.supabase_service import supabase_service
from typing import List
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

async def process_linkedin_insight(insight_id: str, linkedin_bio: str, pitch_deck: str):
    """Background task to process LinkedIn insight"""
    logger.info(f"🚀 BACKGROUND TASK STARTED for insight_id: {insight_id}")
    
    try:
        # Test 1: Check if we can reach Groq service
        logger.info("📞 Calling Groq service...")
        result = await groq_service.generate_linkedin_icebreaker(linkedin_bio, pitch_deck)
        logger.info(f"✅ Groq returned result (length: {len(result) if result else 0})")
        logger.info(f"📝 First 100 chars of result: {result[:100] if result else 'NONE'}")
        
        # Test 2: Check if we can update Supabase
        logger.info("💾 Updating Supabase...")
        update_success = await supabase_service.update_linkedin_insight(insight_id, result)
        logger.info(f"✅ Supabase update result: {update_success}")
        
    except Exception as e:
        logger.error(f"❌ ERROR in background task: {str(e)}")
        logger.error(f"📚 Full traceback: {traceback.format_exc()}")
        
        # Try to update with error message for debugging
        try:
            error_msg = f"ERROR: {str(e)}"
            await supabase_service.update_linkedin_insight(insight_id, error_msg)
            logger.info("💾 Updated record with error message")
        except Exception as update_error:
            logger.error(f"❌ Failed to update with error: {update_error}")

@router.post("/", response_model=LinkedInResponse)
async def create_linkedin_insight(linkedin: LinkedInInput, background_tasks: BackgroundTasks):
    logger.info("🏁 CREATE LINKEDIN INSIGHT ENDPOINT CALLED")
    
    try:
        # Log inputs
        logger.info(f"📊 LinkedIn bio length: {len(linkedin.linkedin_bio)}")
        logger.info(f"📊 Pitch deck length: {len(linkedin.pitch_deck_content)}")
        logger.info(f"📝 Bio preview: {linkedin.linkedin_bio[:100]}...")
        
        # Create LinkedIn insight record
        data = {
            "linkedin_bio": linkedin.linkedin_bio,
            "pitch_deck_content": linkedin.pitch_deck_content
        }
        
        logger.info("💾 Creating Supabase record...")
        result = await supabase_service.create_linkedin_insight(data)
        
        if not result:
            logger.error("❌ Supabase returned no result")
            raise HTTPException(status_code=500, detail="Failed to create LinkedIn insight")
        
        logger.info(f"✅ Created insight with ID: {result.get('id')}")
        logger.info(f"📋 Initial icebreaker_result: {result.get('icebreaker_result')}")
        
        # Add background task
        logger.info("🔄 Adding background task...")
        background_tasks.add_task(
            process_linkedin_insight, 
            result["id"], 
            linkedin.linkedin_bio, 
            linkedin.pitch_deck_content
        )
        logger.info("✅ Background task added successfully")
        
        return LinkedInResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ ERROR in create endpoint: {str(e)}")
        logger.error(f"📚 Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[LinkedInResponse])
async def get_linkedin_insights():
    logger.info("📋 GET LINKEDIN INSIGHTS ENDPOINT CALLED")
    try:
        results = await supabase_service.get_linkedin_insights()
        logger.info(f"📊 Found {len(results)} insights")
        
        # Log each result's status
        for i, item in enumerate(results):
            has_result = bool(item.get('icebreaker_result'))
            logger.info(f"📄 Insight {i+1}: ID={item.get('id')}, Has Result={has_result}")
        
        return [LinkedInResponse(**item) for item in results]
    except Exception as e:
        logger.error(f"❌ ERROR in get endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add a test endpoint to manually trigger Groq
@router.post("/test-groq")
async def test_groq_service():
    """Test endpoint to check if Groq service is working"""
    logger.info("🧪 TESTING GROQ SERVICE")
    try:
        test_bio = "VP of Operations at TechStart Inc. Passionate about scaling operations."
        test_pitch = "AI-Powered Project Management Tool. 40% faster delivery."
        
        result = await groq_service.generate_linkedin_icebreaker(test_bio, test_pitch)
        
        return {
            "status": "success",
            "result_length": len(result) if result else 0,
            "result_preview": result[:200] if result else "No result"
        }
    except Exception as e:
        logger.error(f"❌ Groq test failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# Add a test endpoint to manually trigger Supabase update
@router.post("/test-supabase/{insight_id}")
async def test_supabase_update(insight_id: str):
    """Test endpoint to check if Supabase update is working"""
    logger.info(f"🧪 TESTING SUPABASE UPDATE for ID: {insight_id}")
    try:
        test_result = "TEST UPDATE - This is a manual test update"
        success = await supabase_service.update_linkedin_insight(insight_id, test_result)
        
        return {
            "status": "success" if success else "failed",
            "insight_id": insight_id,
            "update_success": success
        }
    except Exception as e:
        logger.error(f"❌ Supabase test failed: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }