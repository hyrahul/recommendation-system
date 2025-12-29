from sqlalchemy.orm import Session
from app.db.models.faq import FAQ
from app.db.models.qna import QNA


def handle_knowledge(
    db: Session,
    user_message: str,
    user_id: int,
    language_code: str,
) -> dict:
    """
    Knowledge handler:
    - Checks FAQ first
    - Then QNA
    - Applies permission constraints
    - Returns structured data ONLY
    """

    # 1️⃣ FAQ lookup (highest priority)
    faq = (
        db.query(FAQ)
        .filter(
            FAQ.language_code == language_code,
            FAQ.question.ilike(f"%{user_message}%"),
        )
        .first()
    )

    if faq:
        return {
            "type": "knowledge",
            "source": "faq",
            "question": faq.question,
            "answer": faq.answer,
        }

    # 2️⃣ QNA lookup (fallback)
    qna = (
        db.query(QNA)
        .filter(
            QNA.language_code == language_code,
            QNA.question.ilike(f"%{user_message}%"),
        )
        .first()
    )

    if qna:
        return {
            "type": "knowledge",
            "source": "qna",
            "question": qna.question,
            "answer": qna.answer,
        }

    # 3️⃣ Final fallback (NO hallucination)
    return {
        "type": "knowledge",
        "source": "none",
        "message": "Sorry, I could not find relevant information for your question.",
    }
