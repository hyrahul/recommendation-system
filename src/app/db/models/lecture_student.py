# app/db/models/lecture_student.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    ForeignKey,
    DateTime,
    CheckConstraint,
    PrimaryKeyConstraint
)
from sqlalchemy.sql import func
from app.db.base import Base

class LectureStudent(Base):
    __tablename__ = "lecture_students"

    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    lecture_id = Column(
        BigInteger,
        ForeignKey("lectures.id", ondelete="RESTRICT"),
        nullable=False
    )

    study_status = Column(String(50), nullable=False)

    updated_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        PrimaryKeyConstraint(
            "user_id",
            "lecture_id",
            name="pk_lecture_students"
        ),
        CheckConstraint(
            "study_status IN ('NotStarted', 'InProgress', 'Completed')",
            name="chk_study_status"
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<LectureStudent user_id={self.user_id} "
            f"lecture_id={self.lecture_id} "
            f"status={self.study_status}>"
        )
