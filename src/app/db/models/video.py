from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)

    lecture_id = Column(
        BigInteger,
        ForeignKey("lectures.id", ondelete="CASCADE"),
        nullable=True
    )

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<Video id={self.id} title={self.title[:40]}...>"
