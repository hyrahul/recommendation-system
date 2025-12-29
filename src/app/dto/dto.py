from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_message: str
    user_id: int
    language_code: str = "en"


class ChatResponse(BaseModel):
    reply: str
