from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.channel import Channel
from app.models.upload_queue import QueueStatus, UploadQueue
from app.models.user import User
from app.models.video import Video, VideoStatus
from app.schemas.common import MessageResponse, QueueOut, ScheduleRequest

router = APIRouter(tags=["scheduler"])


@router.post("/schedule", response_model=MessageResponse)
def schedule_video(
    payload: ScheduleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    video = db.get(Video, payload.video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    channel = db.get(Channel, video.channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    existing_queue_item = (
        db.query(UploadQueue)
        .filter(UploadQueue.video_id == video.id)
        .first()
    )
    if existing_queue_item:
        raise HTTPException(
            status_code=400,
            detail="Video is already scheduled",
        )

    if video.status != VideoStatus.GENERATED:
        raise HTTPException(
            status_code=400,
            detail="Only generated videos can be scheduled",
        )

    queue_item = UploadQueue(
        video_id=video.id,
        scheduled_at=payload.scheduled_at,
        status=QueueStatus.PENDING,
    )
    video.status = VideoStatus.SCHEDULED
    db.add(queue_item)
    db.commit()
    return MessageResponse(message="Video scheduled")


@router.get("/queue", response_model=list[QueueOut])
def list_queue(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(UploadQueue)
        .join(Video, Video.id == UploadQueue.video_id)
        .join(Channel, Channel.id == Video.channel_id)
        .filter(Channel.user_id == current_user.id)
        .order_by(UploadQueue.scheduled_at.asc())
        .all()
    )
