# app/db/models/lecture.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.sql import func
from app.db.base import Base

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    category_id = Column(
        BigInteger,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False
    )
    difficulty = Column(String(50), nullable=False)
    is_searchable = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "difficulty IN ('Basic', 'Intermediate', 'Advanced')",
            name="chk_lecture_difficulty"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<Lecture id={self.id} title={self.title} "
            f"difficulty={self.difficulty} category_id={self.category_id}>"
        )
