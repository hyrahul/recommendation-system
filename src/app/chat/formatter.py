class ResponseFormatter:
    def __init__(self, llm_client):
        self.llm = llm_client

    # -------------------------
    # KNOWLEDGE
    # -------------------------
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

    # -------------------------
    # RECOMMENDATION
    # -------------------------
    def format_recommendation(
        self,
        structured_response: dict,
        user_message: str,
        language_code: str,
    ) -> str:
        prompt = f"""
You are an assistant for a training system.

Rules:
- Recommend courses ONLY from the provided data.
- Explain briefly WHY the recommendation fits the user.
- Respond in language: {language_code}

User request:
{user_message}

Recommendation data:
{structured_response}

Provide a polite recommendation.
"""
        return self.llm.generate(prompt).strip()

    # -------------------------
    # MIXED
    # -------------------------
    def format_mixed(
        self,
        recommendation_structured: dict,
        knowledge_structured: dict,
        user_message: str,
        language_code: str,
    ) -> str:
        prompt = f"""
You are an assistant for a training system.

Rules:
- First answer the user's question.
- Then provide a relevant course recommendation.
- Use ONLY the information provided.
- Respond in language: {language_code}

User message:
{user_message}

Knowledge information:
{knowledge_structured}

Recommendation information:
{recommendation_structured}

Provide a clear, structured response.
"""
        return self.llm.generate(prompt).strip()
