class IntentClassifier:
    def __init__(self, llm_client):
        self.llm = llm_client

    def classify(self, user_message: str) -> str:
        """
        Returns one of:
        RECOMMENDATION | KNOWLEDGE | MIXED | UNCLEAR
        """
        prompt = f"""
Classify the user message into ONE category only.

Categories:
- RECOMMENDATION
- KNOWLEDGE
- MIXED
- UNCLEAR

Return ONLY the category name.

User message:
"{user_message}"
"""
        return self.llm.generate(prompt).strip()
