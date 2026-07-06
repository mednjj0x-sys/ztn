"""Celery worker entry point."""

from celery import Celery

from apps.config.settings import settings

# Create Celery app
celery_app = Celery(
    "ztn_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["apps.worker.tasks"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)


@celery_app.task(name="health_check")
def health_check_task():
    """Health check task for monitoring."""
    return {"status": "healthy"}


if __name__ == "__main__":
    celery_app.start()
