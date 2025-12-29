from fastapi import FastAPI
from app.api.chat import chat_router

app = FastAPI(title="Recommendation System API")

app.include_router(chat_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
