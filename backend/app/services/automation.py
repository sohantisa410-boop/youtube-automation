from app.core.config import settings
from app.models.video import Video, VideoStatus


def generate_script(topic: str, niche: str) -> str:
    return (
        f"Today we are covering {topic} in the {niche} niche with practical insights."
    )


def generate_voice(script_text: str) -> str:
    _ = script_text
    if settings.storage_provider == "s3" and settings.storage_base_url:
        return f"{settings.storage_base_url}/videos/voice_sample.mp3"

    if settings.storage_provider == "cloudinary" and settings.cloudinary_cloud_name:
        return (
            f"https://res.cloudinary.com/{settings.cloudinary_cloud_name}"
            "/video/upload/voice_sample.mp3"
        )

    return "storage/videos/voice_sample.mp3"


def generate_video_asset() -> str:
    if settings.storage_provider == "s3" and settings.storage_base_url:
        return f"{settings.storage_base_url}/videos/video_sample.mp4"

    if settings.storage_provider == "cloudinary" and settings.cloudinary_cloud_name:
        return (
            f"https://res.cloudinary.com/{settings.cloudinary_cloud_name}"
            "/video/upload/video_sample.mp4"
        )

    return "storage/videos/video_sample.mp4"


def generate_thumbnail() -> str:
    if settings.storage_provider == "s3" and settings.storage_base_url:
        return f"{settings.storage_base_url}/thumbnails/thumb_sample.png"

    if settings.storage_provider == "cloudinary" and settings.cloudinary_cloud_name:
        return (
            f"https://res.cloudinary.com/{settings.cloudinary_cloud_name}"
            "/image/upload/thumb_sample.png"
        )

    return "storage/thumbnails/thumb_sample.png"


def generate_seo(topic: str) -> tuple[str, str]:
    title = f"{topic}: Complete Automation Guide"
    description = (
        f"Learn {topic} with an end-to-end automation workflow for YouTube growth."
    )
    return title, description


def mark_uploaded(video: Video):
    video.status = VideoStatus.UPLOADED
