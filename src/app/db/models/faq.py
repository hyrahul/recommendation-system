from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func
from app.db.base import Base


class FAQ(Base):
    __tablename__ = "faq"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    language_code = Column(String(10), nullable=False)  # e.g. 'ko', 'en'

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self) -> str:
        return f"<FAQ id={self.id} lang={self.language_code}>"
