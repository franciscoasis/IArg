from iarg.model import OllamaModel


class Planner:

    def __init__(self):
        self.model = OllamaModel()

    def plan(self, prompt: str) -> str:
        self.model.clear()

        self.model.add_message(
            "system",
            """
Sos un planner.

No respondas la pregunta.

Decidí únicamente qué herramientas habría que usar.

Respondé una lista.

Ejemplo:

tree
glob src/**/*.py
read_files src/a.py src/b.py
grep Agent src
"""
        )

        self.model.add_message("user", prompt)

        return self.model.complete()["content"]