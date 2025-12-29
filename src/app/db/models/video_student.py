from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class VideoStudent(Base):
    __tablename__ = "video_student"

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    video_id = Column(
        BigInteger,
        ForeignKey("video.id", ondelete="CASCADE"),
        primary_key=True
    )

    watch_status = Column(
        String(50),
        nullable=False
    )  # e.g. NotStarted, InProgress, Completed

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<VideoStudent user={self.user_id} video={self.video_id}>"
