from groq import Groq
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Updated to use a supported model
        self.model = "llama-3.3-70b-versatile"  # Production-ready model with 128K context

    async def generate_transcript_insight(self, transcript: str) -> str:
        prompt = f"""
        Review this transcript and provide insights in the following format:

        **What You Did Well:**
        - [Specific points about what went well and why]

        **Areas for Improvement:**
        - [Specific recommendations for improvement]

        **Things to Test Next Time:**
        - [Actionable suggestions for future conversations]

        Transcript:
        {transcript}
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    async def generate_linkedin_icebreaker(self, linkedin_bio: str, pitch_deck: str) -> str:
        prompt = f"""
        Based on this LinkedIn bio and pitch deck, provide a comprehensive analysis:

        LinkedIn Bio: {linkedin_bio}
        Pitch Deck Content: {pitch_deck}

        Please provide:
        1. **Company LinkedIn & Website** (if identifiable from bio)
        2. **Buying Signals** with explanations
        3. **Discovery Triggers** and smart questions
        4. **Preferred Buying Style** (inferred)
        5. **Top 5 Deck Highlights** for this person
        6. **Potential Issues** with deck relevance
        7. **Short Summary**
        8. **3 Reflection Questions** for meeting prep
        9. **Cold Outreach Icebreaker** (2-3 sentences)

        Format as a well-structured response with clear sections.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                max_tokens=2000,  # Increased for comprehensive response
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

groq_service = GroqService()