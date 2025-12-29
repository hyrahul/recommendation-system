from sqlalchemy.orm import Session
from typing import Optional, cast, Dict, Set

from app.db.models.user import User
from app.db.models.category import Category
from app.db.models.lecture import Lecture
from app.db.models.lecture_prerequisite import LecturePrerequisite
from app.db.models.lecture_student import LectureStudent
from app.services.dto import RecommendationResult
import logging

logger = logging.getLogger(__name__)


def _get_user_affiliation(db: Session, user_id: int) -> str:
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise ValueError(f"User {user_id} not found")
    return cast(str, user.affiliation)


def _get_visible_category_ids(db: Session, affiliation: str) -> list[int]:
    categories = (
        db.query(Category.id)
        .filter(
            (Category.visibility == affiliation)
            | (Category.visibility == "OverseasCommon")
        )
        .all()
    )
    return [c.id for c in categories]


def _get_candidate_lectures(db: Session, category_ids: list[int]) -> list[Lecture]:
    return (
        db.query(Lecture)
        .filter(Lecture.category_id.in_(category_ids), Lecture.is_searchable.is_(True))
        .all()
    )


def _get_completed_lecture_ids(db: Session, user_id: int) -> set[int]:
    rows = (
        db.query(LectureStudent.lecture_id)
        .filter(
            LectureStudent.user_id == user_id,
            LectureStudent.study_status == "Completed",
        )
        .all()
    )
    return {row.lecture_id for row in rows}


def _get_prerequisite_map(db: Session) -> Dict[int, Set[int]]:
    prerequisite_map: Dict[int, Set[int]] = {}

    rows = db.query(LecturePrerequisite).all()
    for row in rows:
        lecture_id = cast(int, row.lecture_id)
        prereq_id = cast(int, row.prerequisite_lecture_id)

        prerequisite_map.setdefault(lecture_id, set()).add(prereq_id)

    return prerequisite_map


def recommend(
    db: Session,
    user_id: int,
    desired_level: Optional[str] = None,
) -> RecommendationResult:

    affiliation = _get_user_affiliation(db, user_id)

    category_ids = _get_visible_category_ids(db, affiliation)
    if not category_ids:
        return RecommendationResult(
            status="BLOCKED",
            lectures=[],
            reason="NO_VISIBLE_CATEGORIES",
        )

    candidates = _get_candidate_lectures(db, category_ids)
    if not candidates:
        return RecommendationResult(
            status="NO_MATCH",
            lectures=[],
            reason="NO_LECTURES_AVAILABLE",
        )

    completed = _get_completed_lecture_ids(db, user_id)
    prereq_map = _get_prerequisite_map(db)

    eligible = []
    missing_prereqs = set()

    for lecture in candidates:
        lecture_id = cast(int, lecture.id)
        lecture_title = cast(str, lecture.title)
        lecture_difficulty = cast(str, lecture.difficulty)
        required = prereq_map.get(lecture_id, set())
        unmet = required - completed

        can_take = not unmet
        logger.info(
            "[RECOMMENDATION] user=%s lecture_id=%s title=%s difficulty=%s can_take=%s unmet_prereqs=%s",
            user_id,
            lecture_id,
            lecture_title,
            lecture_difficulty,
            can_take,
            list(unmet),
        )

        if can_take:
            eligible.append(lecture)
        else:
            # Track prerequisites ONLY if lecture matches desired level
            lecture_difficulty = cast(str, lecture.difficulty)
            if desired_level is None or lecture_difficulty == desired_level:
                missing_prereqs.update(unmet)

    # ---------------------------
    # Difficulty priority
    # ---------------------------
    if desired_level:
        difficulty_order = [desired_level]
    else:
        difficulty_order = ["Advanced", "Intermediate", "Basic"]

    # ---------------------------
    # Recommend prerequisite if needed
    # ---------------------------
    if missing_prereqs:
        prereq_lectures = (
            db.query(Lecture).filter(Lecture.id.in_(missing_prereqs)).all()
        )

        return RecommendationResult(
            status="PREREQUISITE_REQUIRED",
            lectures=prereq_lectures,
            reason="PREREQUISITE_NOT_COMPLETED",
        )

    # ---------------------------
    # Return eligible lecture
    # ---------------------------
    for level in difficulty_order:
        for lecture in eligible:
            if lecture.difficulty == level:
                return RecommendationResult(
                    status="OK",
                    lectures=[lecture],
                    reason="ELIGIBLE_LECTURE_FOUND",
                )

    return RecommendationResult(
        status="NO_MATCH",
        lectures=[],
        reason="NO_ELIGIBLE_LECTURES",
    )
