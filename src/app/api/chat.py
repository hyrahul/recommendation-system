# app/api/chat.py

from fastapi import APIRouter, Depends
from app.db.session import get_db
from app.chat.router import route_message
from app.llm.intent_classifier import IntentClassifier
from app.llm.ollama_client import OllamaClient
from app.dto.dto import *
import logging

logger = logging.getLogger(__name__)

chat_router = APIRouter()


@chat_router.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest, db=Depends(get_db)):

    llm_client = OllamaClient()

    intent = IntentClassifier(llm_client).classify(req.user_message)
    logger.info(
        "[CHAT] user_id=%s intent=%s message=%s", req.user_id, intent, req.user_message
    )

    if intent == "KNOWLEDGE":
        logger.info("[CHAT] Routing to KNOWLEDGE handler")
        ...
    elif intent == "RECOMMENDATION":
        logger.info("[CHAT] Routing to RECOMMENDATION handler")
        ...
    elif intent == "MIXED":
        logger.info("[CHAT] Routing to MIXED handler")
        ...
    else:
        logger.warning("[CHAT] Unknown intent=%s", intent)

    reply_text = route_message(
        db=db,
        user_id=req.user_id,
        user_message=req.user_message,
        intent=intent,
    )
    return ChatResponse(reply=reply_text)
