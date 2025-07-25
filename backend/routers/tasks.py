from fastapi import APIRouter, HTTPException
from services.queue_service import queue_service
from models import TaskStatusResponse
from typing import Dict, Any

router = APIRouter()

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get status of a specific task"""
    try:
        status = queue_service.get_task_status(task_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queue/stats")
async def get_queue_stats() -> Dict[str, Any]:
    """Get queue statistics"""
    try:
        stats = queue_service.get_queue_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))