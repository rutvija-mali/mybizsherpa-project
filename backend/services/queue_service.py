from celery_app import celery_app
from celery_worker import process_transcript_task, process_linkedin_task
from celery.result import AsyncResult
from typing import Dict, Any
import socket

class QueueService:
    def __init__(self):
        self.celery_app = celery_app
        # Get the actual worker name dynamically
        self.worker_name = f"celery@{socket.gethostname()}"
    
    def enqueue_transcript(self, transcript_id: str, transcript_text: str, company_name: str) -> str:
        """
        Add transcript processing task to queue
        Returns: task_id
        """
        print(f"Enqueueing transcript task for ID: {transcript_id}")
        task = process_transcript_task.delay(transcript_id, transcript_text, company_name)
        print(f"Task enqueued with ID: {task.id}")
        return task.id
    
    def enqueue_linkedin(self, insight_id: str, linkedin_bio: str, pitch_deck: str) -> str:
        """
        Add LinkedIn processing task to queue
        Returns: task_id
        """
        print(f"Enqueueing LinkedIn task for ID: {insight_id}")
        task = process_linkedin_task.delay(insight_id, linkedin_bio, pitch_deck)
        print(f"Task enqueued with ID: {task.id}")
        return task.id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get status of a specific task
        """
        try:
            result = AsyncResult(task_id, app=self.celery_app)
            
            return {
                "task_id": task_id,
                "status": result.status,
                "result": result.result if result.ready() else None,
                "info": str(result.info) if result.info else None,
                "traceback": result.traceback if result.failed() else None
            }
        except Exception as e:
            return {
                "task_id": task_id,
                "status": "ERROR",
                "info": str(e)
            }
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """
        Get overall queue statistics
        """
        try:
            inspect = self.celery_app.control.inspect()
            
            active_tasks = inspect.active()
            scheduled_tasks = inspect.scheduled()
            reserved_tasks = inspect.reserved()
            
            # Debug: Print what workers are available
            print(f"Available workers: {list(active_tasks.keys()) if active_tasks else 'None'}")
            print(f"Looking for worker: {self.worker_name}")
            
            # Calculate stats using actual worker names
            total_active = 0
            total_scheduled = 0
            total_reserved = 0
            workers_online = 0
            
            if active_tasks:
                workers_online = len(active_tasks)
                for worker_tasks in active_tasks.values():
                    total_active += len(worker_tasks)
            
            if scheduled_tasks:
                for worker_tasks in scheduled_tasks.values():
                    total_scheduled += len(worker_tasks)
            
            if reserved_tasks:
                for worker_tasks in reserved_tasks.values():
                    total_reserved += len(worker_tasks)
            
            stats = {
                "active_tasks": total_active,
                "scheduled_tasks": total_scheduled,
                "reserved_tasks": total_reserved,
                "workers_online": workers_online,
                "worker_names": list(active_tasks.keys()) if active_tasks else []
            }
            
            return stats
            
        except Exception as e:
            print(f"Error getting queue stats: {str(e)}")
            return {
                "error": str(e),
                "active_tasks": 0,
                "scheduled_tasks": 0,
                "reserved_tasks": 0,
                "workers_online": 0,
                "worker_names": []
            }

queue_service = QueueService()