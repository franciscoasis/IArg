from iarg.model import OllamaModel
from iarg.prompts import RESPONDER_PROMPT


class Responder:
    def __init__(self):
        self.model = OllamaModel(
            model="qwen3:8b"
        )

    def answer(self, question: str, context: list, history: list):

        self.model.clear()

        self.model.add_message(
            "system",
            RESPONDER_PROMPT,
        )

        # Agregar memoria previa
        for message in history:
            self.model.add_message(
                message["role"],
                message["content"],
            )


        text = ""

        for item in context:
            text += (
                f"=== {item['tool']} ===\n"
                f"{item['result']}\n\n"
            )


        self.model.add_message(
            "user",
            f"""
Pregunta:
{question}

Información de herramientas:
{text}
"""
        )


        return self.model.complete()["content"]