from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Channel(Base, TimestampMixin):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(255))
    niche: Mapped[str] = mapped_column(String(255))
    uploads_per_day: Mapped[int] = mapped_column(Integer, default=1)
    client_secret_path: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    owner = relationship("User", back_populates="channels")
    videos = relationship(
        "Video", back_populates="channel", cascade="all, delete-orphan"
    )
