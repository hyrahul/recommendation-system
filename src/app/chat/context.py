from sqlalchemy.orm import Session
from app.db.models import Category, Lecture, LectureStudent


def resolve_user_category_ids(db: Session, user_id: int) -> list[int]:
    """
    Resolve all category IDs the user is associated with.
    Returns empty list if none.
    """

    rows = (
        db.query(Category.id)
        .join(Lecture, Lecture.category_id == Category.id)
        .join(LectureStudent, LectureStudent.lecture_id == Lecture.id)
        .filter(LectureStudent.user_id == user_id)
        .distinct()
        .all()
    )

    return [row[0] for row in rows]
