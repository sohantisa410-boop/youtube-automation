from datetime import datetime

from tasks.celery_app import celery_app


@celery_app.task(name="tasks.jobs.script_generator_worker")
def script_generator_worker(topic: str, niche: str):
    return {
        "script": f"Automation script for {topic} in {niche}",
        "generated_at": datetime.utcnow().isoformat(),
    }


@celery_app.task(name="tasks.jobs.voice_generator_worker")
def voice_generator_worker(script_text: str):
    _ = script_text
    return {"voice_path": "storage/videos/voice_from_worker.mp3"}


@celery_app.task(name="tasks.jobs.video_generator_worker")
def video_generator_worker(voice_path: str):
    _ = voice_path
    return {"video_path": "storage/videos/video_from_worker.mp4"}


@celery_app.task(name="tasks.jobs.thumbnail_generator_worker")
def thumbnail_generator_worker(title: str):
    _ = title
    return {"thumbnail_path": "storage/thumbnails/thumb_from_worker.png"}


@celery_app.task(
    bind=True,
    name="tasks.jobs.upload_worker",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def upload_worker(self, video_id: int, channel_id: int):
    _ = (self, video_id, channel_id)
    return {"status": "uploaded", "video_id": video_id}


@celery_app.task(name="tasks.jobs.analytics_worker")
def analytics_worker(video_id: int):
    return {"video_id": video_id, "views": 0, "likes": 0, "comments": 0}
