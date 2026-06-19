import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "memory://")
BACKEND_URL = "rpc://" if REDIS_URL == "memory://" else REDIS_URL

celery_app = Celery("youtube_automation_workers", broker=REDIS_URL, backend=BACKEND_URL)
celery_app.conf.imports = (
    "tasks.jobs",
    "tasks.script_task",
)
celery_app.conf.task_routes = {
    "tasks.jobs.script_generator_worker": {"queue": "script"},
    "tasks.jobs.voice_generator_worker": {"queue": "voice"},
    "tasks.jobs.video_generator_worker": {"queue": "video"},
    "tasks.jobs.thumbnail_generator_worker": {"queue": "thumbnail"},
    "tasks.jobs.upload_worker": {"queue": "upload"},
    "tasks.jobs.analytics_worker": {"queue": "analytics"},
}
