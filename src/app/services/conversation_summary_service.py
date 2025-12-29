class ConversationSummaryService:
    def __init__(self, llm_client):
        self.llm = llm_client

    def summarize(self, messages: list[str]) -> str:
        prompt = f"""
Summarize the following conversation in 2–3 sentences.
Focus on learning topics and user intent.

Conversation:
{chr(10).join(messages)}
"""
        return self.llm.generate(prompt).strip()
