from fastapi import FastAPI
from app.api.chat import chat_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Recommendation System API")

app.include_router(chat_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
