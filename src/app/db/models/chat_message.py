from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.db.base import Base


class ChatMessage(Base):
    __tablename__ = "chat_message"

    message_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    record_id = Column(
        BigInteger,
        ForeignKey("chat_record.record_id", ondelete="CASCADE"),
        nullable=False
    )

    sender = Column(String(20), nullable=False)
    message_text = Column(Text, nullable=False)

    sent_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<ChatMessage id={self.message_id} record_id={self.record_id}>"
