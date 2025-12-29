from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama

app = FastAPI(title="Recommendation System API")

# -------------------------------
# Request / Response Models
# -------------------------------
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# -------------------------------
# Chat Endpoint (Ollama)
# -------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        response = ollama.chat(
            model="qwen2.5",
            messages=[
                {"role": "system", "content": "You are a helpful recommendation assistant."},
                {"role": "user", "content": req.message},
            ],
        )

        # Defensive extraction (Ollama responses can vary)
        reply = (
            response.get("message", {})
            .get("content")
        )

        if not reply:
            raise ValueError("Empty response from model")

        return {"reply": reply}

    except Exception as e:
        # Always return JSON so UI never crashes
        raise HTTPException(
            status_code=500,
            detail=f"Ollama error: {str(e)}"
        )


# -------------------------------
# Health Check
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
