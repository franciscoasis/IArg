from iarg.model import OllamaModel
from iarg.prompts import RESPONDER_PROMPT


class Responder:
    MAX_TOOL_RESULT_CHARS = 2500
    MAX_TOOLS_CONTEXT_CHARS = 8000

    def __init__(self):
        self.model = OllamaModel(
            model="qwen3:8b"
        )

    def _format_context(self, context: list) -> str:
        chunks = []
        total = 0

        for item in context:
            raw = str(item["result"])

            if len(raw) > self.MAX_TOOL_RESULT_CHARS:
                raw = (
                    raw[:self.MAX_TOOL_RESULT_CHARS]
                    + "\n... [resultado truncado]"
                )

            chunk = (
                f"=== {item['tool']} ===\n"
                f"{raw}\n\n"
            )

            chunk_len = len(chunk)

            if total + chunk_len > self.MAX_TOOLS_CONTEXT_CHARS:
                break

            chunks.append(chunk)
            total += chunk_len

        return "".join(chunks)

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


        text = self._format_context(context)


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