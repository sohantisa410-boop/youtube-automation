from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.analytics import Analytics
from app.models.channel import Channel
from app.models.upload_queue import QueueStatus, UploadQueue
from app.models.user import User
from app.models.video import Video
from app.schemas.common import AnalyticsSummary

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    channel_count = (
        db.query(func.count(Channel.id))
        .filter(Channel.user_id == current_user.id)
        .scalar()
        or 0
    )
    video_count = (
        db.query(func.count(Video.id))
        .join(Channel, Channel.id == Video.channel_id)
        .filter(Channel.user_id == current_user.id)
        .scalar()
        or 0
    )
    scheduled_count = (
        db.query(func.count(UploadQueue.id))
        .join(Video, Video.id == UploadQueue.video_id)
        .join(Channel, Channel.id == Video.channel_id)
        .filter(
            Channel.user_id == current_user.id,
            UploadQueue.status == QueueStatus.PENDING,
        )
        .scalar()
        or 0
    )
    totals = (
        db.query(
            func.coalesce(func.sum(Analytics.views), 0),
            func.coalesce(func.sum(Analytics.likes), 0),
            func.coalesce(func.sum(Analytics.comments), 0),
        )
        .join(Video, Video.id == Analytics.video_id)
        .join(Channel, Channel.id == Video.channel_id)
        .filter(Channel.user_id == current_user.id)
        .one()
    )

    return AnalyticsSummary(
        channels=channel_count,
        videos=video_count,
        scheduled=scheduled_count,
        views=totals[0],
        likes=totals[1],
        comments=totals[2],
    )
