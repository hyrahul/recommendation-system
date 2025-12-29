# app/chat/router.py

from sqlalchemy.orm import Session
from app.chat.intents import ChatIntent
from app.chat.handlers.recommendation import handle_recommendation
from app.chat.handlers.knowledge import handle_knowledge
from app.chat.handlers.clarification import handle_clarification


def route_message(
    db: Session,
    user_id: int,
    user_message: str,
    intent: ChatIntent
) -> dict:
    """
    Routes message to correct handler based on intent.
    """

if intent == "RECOMMENDATION":
        structured = handle_recommendation(
            db=db,
            user_id=user_id,
            user_message=user_message,
        )

        return formatter.format_recommendation(
            structured_response=structured,
            user_message=user_message,
            language_code=language_code,
        )

if intent == "MIXED":
    recommendation_structured = handle_recommendation(
        db=db,
        user_id=user_id,
        user_message=user_message,
    )

    knowledge_structured = handle_knowledge(
        db=db,
        user_message=user_message,
        user_id=user_id,
        language_code=language_code,
    )

    recommendation_text = formatter.format_recommendation(
        structured_response=recommendation_structured,
        user_message=user_message,
        language_code=language_code,
    )

    knowledge_text = formatter.format_knowledge(
        structured_response=knowledge_structured,
        user_message=user_message,
        language_code=language_code,
    )

    return f"{recommendation_text}\n\n{knowledge_text}"

    if intent == "KNOWLEDGE":
        structured = handle_knowledge(
            db=db,
            user_message=user_message,
            user_id=user_id,
            language_code=language_code,
        )

        return formatter.format_knowledge(
            structured_response=structured,
            user_message=user_message,
            language_code=language_code,
        )

    return handle_clarification(user_message)


    def handle_knowledge(
    db: Session,
    user_message: str,
    user_id: int,
    language_code: str,
) -> dict:
    """
    Handles KNOWLEDGE intent.
    Routes the query to the correct knowledge source.
    """

    # Order matters: most specific → most general
    faq_result = _search_faq(db, user_message, language_code)
    if faq_result:
        return faq_result

    qna_result = _search_qna(db, user_message, language_code)
    if qna_result:
        return qna_result

    video_result = _search_video(db, user_message, user_id)
    if video_result:
        return video_result

    access_result = _explain_access(db, user_id)
    if access_result:
        return access_result

    return {
        "type": "knowledge",
        "source": "none",
        "message": "Sorry, I couldn't find relevant information for your question.",
    }


def _search_faq(db: Session, message: str, language_code: str) -> dict | None:
    faq = (
        db.query(FAQ)
        .filter(
            FAQ.language_code == language_code,
            FAQ.question.ilike(f"%{message}%"),
            FAQ.is_active.is_(True),
        )
        .first()
    )

    if not faq:
        return None

    return {
        "type": "knowledge",
        "source": "faq",
        "question": faq.question,
        "answer": faq.answer,
    }


def _search_qna(
    db,
    message: str,
    language_code: str,
    user_category_ids: list[int],
):
    qnas = (
        db.query(QNA)
        .filter(
            QNA.language_code == language_code,
            QNA.question.ilike(f"%{message}%"),
        )
        .all()
    )

    if not qnas:
        return None

    # Simple heuristic: prefer QNA mentioning category name
    for qna in qnas:
        if any(cat_name.lower() in qna.question.lower() for cat_name in user_category_ids):
            return {
                "type": "knowledge",
                "source": "qna",
                "question": qna.question,
                "answer": qna.answer,
            }

    # Fallback: first match
    qna = qnas[0]
    return {
        "type": "knowledge",
        "source": "qna",
        "question": qna.question,
        "answer": qna.answer,
    }



def _search_video(db: Session, message: str, user_id: int) -> dict | None:
    video = (
        db.query(Video)
        .filter(
            Video.title.ilike(f"%{message}%"),
            Video.is_active.is_(True),
        )
        .first()
    )

    if not video:
        return None

    progress = (
        db.query(VideoStudent)
        .filter(
            VideoStudent.video_id == video.id,
            VideoStudent.user_id == user_id,
        )
        .one_or_none()
    )

    return {
        "type": "knowledge",
        "source": "video",
        "video_title": video.title,
        "video_url": video.url,
        "watch_status": progress.watch_status if progress else "NotStarted",
    }


def _explain_access(db: Session, user_id: int) -> dict | None:
    groups = (
        db.query(PermissionGroup.name)
        .join(
            PermissionGroupUser,
            PermissionGroup.permission_grp_id == PermissionGroupUser.permission_grp_id,
        )
        .filter(PermissionGroupUser.user_id == user_id)
        .all()
    )

    if not groups:
        return None

    return {
        "type": "knowledge",
        "source": "access",
        "message": "Your access is restricted based on your permission group.",
        "permission_groups": [g.name for g in groups],
    }

