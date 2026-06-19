from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.channel import Channel
from app.models.user import User
from app.models.video import Video, VideoStatus
from app.schemas.common import (
    MessageResponse,
    VideoGenerateRequest,
    VideoOut,
    VideoUploadRequest,
)
from app.services.automation import (
    generate_script,
    generate_seo,
    generate_thumbnail,
    generate_video_asset,
    generate_voice,
)

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("", response_model=list[VideoOut])
def list_videos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Video)
        .join(Channel, Channel.id == Video.channel_id)
        .filter(Channel.user_id == current_user.id)
        .order_by(Video.created_at.desc())
        .all()
    )


@router.post("/generate", response_model=VideoOut)
def generate_video(
    payload: VideoGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    channel = db.get(Channel, payload.channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Channel not found")

    script = generate_script(payload.topic, channel.niche)
    title, description = generate_seo(payload.topic)
    voice_path = generate_voice(script)
    video_path = generate_video_asset()
    thumbnail_path = generate_thumbnail()

    video = Video(
        channel_id=channel.id,
        title=title,
        description=description,
        script_text=script,
        voice_path=voice_path,
        video_path=video_path,
        thumbnail_path=thumbnail_path,
        seo_keywords=f"{payload.topic},{channel.niche},automation",
        status=VideoStatus.GENERATED,
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


@router.post("/upload", response_model=MessageResponse)
def upload_video(
    payload: VideoUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    video = db.get(Video, payload.video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    channel = db.get(Channel, video.channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    video.status = VideoStatus.UPLOADED
    db.commit()
    return MessageResponse(message="Video upload dispatched")
