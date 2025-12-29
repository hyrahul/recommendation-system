# app/db/models/lecture_prerequisite.py

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    DateTime,
    PrimaryKeyConstraint
)
from sqlalchemy.sql import func
from app.db.base import Base

class LecturePrerequisite(Base):
    __tablename__ = "lecture_prerequisites"

    lecture_id = Column(
        BigInteger,
        ForeignKey("lectures.id", ondelete="RESTRICT"),
        nullable=False
    )

    prerequisite_lecture_id = Column(
        BigInteger,
        ForeignKey("lectures.id", ondelete="RESTRICT"),
        nullable=False
    )

    created_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint(
            "lecture_id",
            "prerequisite_lecture_id",
            name="pk_lecture_prerequisites"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<LecturePrerequisite lecture_id={self.lecture_id} "
            f"requires={self.prerequisite_lecture_id}>"
        )
