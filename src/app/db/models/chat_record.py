from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class ChatRecord(Base):
    __tablename__ = "chat_record"

    record_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    chat_title = Column(String(20), nullable=True)
    chat_summary = Column(String(200), nullable=True)

    started_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    ended_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<ChatRecord id={self.record_id} user_id={self.user_id}>"
