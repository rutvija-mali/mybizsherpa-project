from supabase import create_client, Client
import os
from typing import List, Dict, Any, Optional

class SupabaseService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase credentials")
        self.client: Client = create_client(url, key)
    
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
    
    async def update_transcript_insight(self, transcript_id: str, insight: str) -> Dict[str, Any]:
        try:
            result = self.client.table("transcripts").update({"insight_result": insight}).eq("id", transcript_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            raise Exception(f"Supabase error: {str(e)}")
    
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
    
    async def update_linkedin_insight(self, insight_id: str, icebreaker_result: str) -> bool:
        """
        Fixed version - returns boolean success status and uses correct variable name
        """
        try:
            # Fixed: Don't shadow the parameter name with 'result'
            response = self.client.table("linkedin_insights").update({
                "icebreaker_result": icebreaker_result
            }).eq("id", insight_id).execute()
            
            # Return True if update was successful
            return bool(response.data)
            
        except Exception as e:
            print(f"❌ Supabase update error: {str(e)}")
            raise Exception(f"Supabase error: {str(e)}")

supabase_service = SupabaseService()