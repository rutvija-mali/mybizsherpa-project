from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from routers import transcripts, linkedin, tasks  # Add tasks import
import sys 

load_dotenv()

app = FastAPI(title="AI Workflow API", version="1.0.0")

print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
print("Python version:", sys.version)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://mybizsherpa-project.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcripts.router, prefix="/api/transcripts", tags=["transcripts"])
app.include_router(linkedin.router, prefix="/api/linkedin", tags=["linkedin"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])  # New router

@app.get("/")
async def root():
    return {"message": "AI Workflow API with Queue is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "queue_enabled": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
