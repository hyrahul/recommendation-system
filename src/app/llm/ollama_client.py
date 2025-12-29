import ollama

class OllamaClient:
    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model="qwen2.5",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        return response["message"]["content"]
