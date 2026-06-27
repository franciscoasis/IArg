from abc import ABC, abstractmethod


class Tool(ABC):
    name = ""
    description = ""
    parameters = {}

    @abstractmethod
    def run(self, **kwargs):
        pass

    def to_ollama(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }