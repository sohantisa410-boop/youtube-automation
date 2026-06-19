from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class VideoStatus(str, Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    SCHEDULED = "scheduled"
    UPLOADED = "uploaded"
    FAILED = "failed"


class Video(Base, TimestampMixin):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(
        ForeignKey("channels.id", ondelete="CASCADE"), index=True
    )
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text, default="")
    script_text: Mapped[str] = mapped_column(Text, default="")
    voice_path: Mapped[str] = mapped_column(String(500), nullable=True)
    video_path: Mapped[str] = mapped_column(String(500), nullable=True)
    thumbnail_path: Mapped[str] = mapped_column(String(500), nullable=True)
    seo_keywords: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[VideoStatus] = mapped_column(
        SqlEnum(VideoStatus), default=VideoStatus.DRAFT
    )

    channel = relationship("Channel", back_populates="videos")
