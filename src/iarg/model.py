import ollama

from iarg.tools import registry


class OllamaModel:
    def __init__(self, model="qwen2.5-coder:7b", tools=None):
        self.model = model
        self.tools = tools
        self.messages = []

    def add_message(self, role: str, content):
        self.messages.append({
            "role": role,
            "content": content,
        })

    def complete(self):
        kwargs = {
            "model": self.model,
            "messages": self.messages,
        }

        if self.tools is not None:
            kwargs["tools"] = self.tools

        response = ollama.chat(**kwargs)

        self.messages.append(response["message"])

        return response["message"]
    
    def clear(self):
        self.messages.clear()