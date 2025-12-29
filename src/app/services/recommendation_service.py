from sqlalchemy.orm import Session
from typing import Optional

from app.db.models.user import User
from app.db.models.category import Category
from app.db.models.lecture import Lecture
from app.db.models.lecture_prerequisite import LecturePrerequisite
from app.db.models.lecture_student import LectureStudent
from app.services.dto import RecommendationResult

def _get_user_affiliation(db: Session, user_id: int) -> str:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")
    return user.affiliation


def _get_visible_category_ids(db: Session, affiliation: str) -> list[int]:
    categories = (
        db.query(Category.id)
        .filter(
            (Category.visibility == affiliation) |
            (Category.visibility == "OverseasCommon")
        )
        .all()
    )
    return [c.id for c in categories]


def _get_candidate_lectures(
    db: Session,
    category_ids: list[int]
) -> list[Lecture]:
    return (
        db.query(Lecture)
        .filter(
            Lecture.category_id.in_(category_ids),
            Lecture.is_searchable.is_(True)
        )
        .all()
    )


def _get_completed_lecture_ids(db: Session, user_id: int) -> set[int]:
    rows = (
        db.query(LectureStudent.lecture_id)
        .filter(
            LectureStudent.user_id == user_id,
            LectureStudent.study_status == "Completed"
        )
        .all()
    )
    return {row.lecture_id for row in rows}


def _get_prerequisite_map(db: Session) -> dict[int, set[int]]:
    prereqs = {}
    rows = db.query(
        LecturePrerequisite.lecture_id,
        LecturePrerequisite.prerequisite_lecture_id
    ).all()

    for lecture_id, prereq_id in rows:
        prereqs.setdefault(lecture_id, set()).add(prereq_id)

    return prereqs


def recommend(
    db: Session,
    user_id: int,
    desired_level: Optional[str] = None
) -> RecommendationResult:

    affiliation = _get_user_affiliation(db, user_id)

    category_ids = _get_visible_category_ids(db, affiliation)
    if not category_ids:
        return RecommendationResult(
            status="BLOCKED",
            lectures=[],
            reason="NO_VISIBLE_CATEGORIES"
        )

    candidates = _get_candidate_lectures(db, category_ids)
    if not candidates:
        return RecommendationResult(
            status="NO_MATCH",
            lectures=[],
            reason="NO_LECTURES_AVAILABLE"
        )

    completed = _get_completed_lecture_ids(db, user_id)
    prereq_map = _get_prerequisite_map(db)

    eligible = []
    missing_prereqs = set()

    for lecture in candidates:
        required = prereq_map.get(lecture.id, set())
        unmet = required - completed

        if not unmet:
            eligible.append(lecture)
        else:
            missing_prereqs.update(unmet)

    # Difficulty priority
    difficulty_order = ["Basic", "Intermediate", "Advanced"]

    for level in difficulty_order:
        for lecture in eligible:
            if lecture.difficulty == level:
                return RecommendationResult(
                    status="OK",
                    lectures=[lecture]
                )

    if missing_prereqs:
        prereq_lectures = (
            db.query(Lecture)
            .filter(Lecture.id.in_(missing_prereqs))
            .all()
        )
        return RecommendationResult(
            status="PREREQUISITE_REQUIRED",
            lectures=prereq_lectures
        )

    return RecommendationResult(
        status="NO_MATCH",
        lectures=[],
        reason="NO_ELIGIBLE_LECTURES"
    )
