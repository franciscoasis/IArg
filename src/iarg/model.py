import ollama

from iarg.tools import registry


class OllamaModel:
    def __init__(self, model="qwen2.5-coder:7b"):
        self.model = model
        self.messages = []

    def add_message(self, role: str, content):
        self.messages.append({
            "role": role,
            "content": content,
        })

    def complete(self):
        response = ollama.chat(
            model=self.model,
            messages=self.messages,
            tools=registry.to_ollama(),
        )
    
        print(response)
    
        self.messages.append(response["message"])
    
        return response["message"]

    def clear(self):
        self.messages.clear()