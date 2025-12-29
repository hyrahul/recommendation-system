class ResponseFormatter:
    def __init__(self, llm_client):
        self.llm = llm_client

    def format_knowledge(
        self,
        structured_response: dict,
        user_message: str,
        language_code: str,
    ) -> str:
        prompt = f"""
You are an assistant for a training system.

Rules:
- Use ONLY the information provided.
- Do NOT invent facts.
- Do NOT add extra content.
- Respond in language: {language_code}

User question:
{user_message}

System-provided information:
{structured_response}

Provide a clear and helpful answer.
"""
        return self.llm.generate(prompt).strip()
