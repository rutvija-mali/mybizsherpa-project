from supabase import create_client, Client
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
        self.client: Client = create_client(url, key)
    
    # TRANSCRIPT METHODS
    async def create_transcript(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = self.client.table("transcripts").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def get_transcripts(self) -> List[Dict[str, Any]]:
        try:
            result = self.client.table("transcripts").select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def get_transcript_by_id(self, transcript_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific transcript by ID"""
        try:
            result = self.client.table("transcripts").select("*").eq("id", transcript_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def update_transcript_insight(self, transcript_id: str, insight: str) -> Dict[str, Any]:
        try:
            result = self.client.table("transcripts").update({"insight_result": insight}).eq("id", transcript_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def update_transcript_status(self, transcript_id: str, status: str) -> Dict[str, Any]:
        """Update transcript processing status"""
        try:
            result = self.client.table("transcripts").update({
                "status": status,
                "updated_at": "now()"
            }).eq("id", transcript_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error updating transcript status: {str(e)}")
    
    # LINKEDIN METHODS
    async def create_linkedin_insight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = self.client.table("linkedin_insights").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def get_linkedin_insights(self) -> List[Dict[str, Any]]:
        try:
            result = self.client.table("linkedin_insights").select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def get_linkedin_insight_by_id(self, insight_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific LinkedIn insight by ID"""
        try:
            result = self.client.table("linkedin_insights").select("*").eq("id", insight_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
    async def update_linkedin_insight(self, insight_id: str, icebreaker_result: str) -> bool:
        """Update LinkedIn insight with AI result"""
        try:
            response = self.client.table("linkedin_insights").update({
                "icebreaker_result": icebreaker_result
            }).eq("id", insight_id).execute()
            
            return bool(response.data)
        
        except Exception as e:
            print(f"Supabase update error: {str(e)}")
            raise Exception(f"Supabase error: {str(e)}")
    
    async def update_linkedin_status(self, insight_id: str, status: str) -> Dict[str, Any]:
        """Update LinkedIn insight processing status"""
        try:
            result = self.client.table("linkedin_insights").update({
                "status": status,
                "updated_at": "now()"
            }).eq("id", insight_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error updating LinkedIn status: {str(e)}")
    
    # TASK TRACKING METHODS (Optional - for advanced queue monitoring)
    async def create_task_log(self, task_id: str, task_type: str, record_id: str, status: str = "started") -> Dict[str, Any]:
        """Log task execution for monitoring"""
        try:
            data = {
                "task_id": task_id,
                "task_type": task_type,
                "record_id": record_id,
                "status": status,
                "started_at": "now()"
            }
            result = self.client.table("task_logs").insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Task log creation failed: {str(e)}")
            return None  # Non-critical, don't raise
    
    async def update_task_log(self, task_id: str, status: str, error_message: str = None) -> bool:
        """Update task log status"""
        try:
            update_data = {
                "status": status,
                "completed_at": "now()"
            }
            if error_message:
                update_data["error_message"] = error_message
            
            result = self.client.table("task_logs").update(update_data).eq("task_id", task_id).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Task log update failed: {str(e)}")
            return False  # Non-critical, don't raise

supabase_service = SupabaseService()