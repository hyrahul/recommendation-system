# app/api/chat.py

from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.chat.router import route_message
from app.llm.intent_classifier import IntentClassifier

router = APIRouter()

@router.post("/chat")
def chat_endpoint(
    user_message: str,
    user_id: int,
    db = Depends(get_db)
):
    intent = IntentClassifier(...).classify(user_message)

    response = route_message(
        db=db,
        user_id=user_id,
        user_message=user_message,
        intent=intent,
    )

    return response
