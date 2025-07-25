from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Create Celery instance
celery_app = Celery(
    "ai_workflow",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    include=["celery_worker"],
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=3,
    broker_heartbeat=10,
    broker_pool_limit=1,
    redis_socket_keepalive=True,
)

# Windows-friendly Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    
    # Remove custom routing - let tasks go to default queue
    # task_routes={
    #     "celery_worker.process_transcript_task": "transcript_queue",
    #     "celery_worker.process_linkedin_task": "linkedin_queue",
    # },
    
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=1000,
    task_time_limit=300,  # 5 minutes max per task
    task_soft_time_limit=240,  # 4 minutes soft limit
    
    # Windows-specific configurations
    worker_pool='solo',  # Use solo pool to avoid multiprocessing issues
    worker_concurrency=1,  # Single worker process
    worker_disable_rate_limits=True,
    broker_connection_retry_on_startup=True,
    
    # Important: Use immediate acknowledgment for testing
    task_always_eager=False,  # Set to True for immediate execution during testing
    task_eager_propagates=True,
)

# Auto-discover tasks
celery_app.autodiscover_tasks()