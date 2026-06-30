import json

from iarg.model import OllamaModel
from iarg.prompts import PLANNER_PROMPT
from iarg.tools import registry
from iarg.utils import clean_json


class Planner:
    def __init__(self):
        self.model = OllamaModel(
            model="qwen3:8b"
        )

    def plan(self, prompt: str):
        self.model.clear()

        self.model.add_message(
            "system",
            PLANNER_PROMPT + "\n\n" + registry.prompt(),
        )

        self.model.add_message(
            "user",
            prompt,
        )

        for _ in range(3):
            response = self.model.complete()

            content = clean_json(response["content"])

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                self.model.add_message(
                    "user",
                    "La respuesta anterior no era un JSON válido. Respondé únicamente un JSON válido siguiendo exactamente el formato indicado. No uses markdown ni texto adicional.",
                )

        raise RuntimeError("El planner no pudo generar un JSON válido.")