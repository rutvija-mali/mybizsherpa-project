from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class TranscriptInput(BaseModel):
    company_name: str
    attendees: List[str]
    date: date
    transcript_text: str

class TranscriptResponse(BaseModel):
    id: str
    company_name: str
    attendees: List[str]
    date: date
    transcript_text: str
    insight_result: Optional[str] = None
    created_at: str

class LinkedInInput(BaseModel):
    linkedin_bio: str
    pitch_deck_content: str

class LinkedInResponse(BaseModel):
    id: str
    linkedin_bio: str
    company_linkedin: Optional[str] = None
    company_website: Optional[str] = None
    pitch_deck_content: str
    icebreaker_result: Optional[str] = None
    created_at: str