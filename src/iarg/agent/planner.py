import json

from iarg.model import OllamaModel
from iarg.prompts import PLANNER_PROMPT
from iarg.tools import registry
from iarg.utils import clean_json
from iarg.parser import parse_tool_call


class Planner:
    def __init__(self):
        self.model = OllamaModel(
            model="qwen3:8b"
        )

    def _format_context(self, context: list | None) -> str:
        if not context:
            return "Sin herramientas ejecutadas todavía."

        lines = []

        for item in context:
            lines.append(
                f"- {item['tool']}({json.dumps(item['arguments'], ensure_ascii=False, sort_keys=True)}): {item['result']}"
            )

        return "\n".join(lines)

    def plan(self, prompt: str, history: list | None = None, context: list | None = None):
        self.model.clear()

        self.model.add_message(
            "system",
            PLANNER_PROMPT + "\n\n" + registry.prompt(),
        )

        if history:
            recent_history = history[-6:]
            history_text = []

            for message in recent_history:
                history_text.append(
                    f"{message['role']}: {message['content']}"
                )

            history_block = "\n".join(history_text)
        else:
            history_block = "Sin historial relevante."

        self.model.add_message(
            "user",
            f"""
Consulta del usuario:
{prompt}

Historial relevante:
{history_block}

Herramientas ya ejecutadas:
{self._format_context(context)}

Devolvé solo el próximo plan mínimo en JSON.
""",
        )

        for _ in range(3):
            response = self.model.complete()

            parsed_calls = parse_tool_call(response)

            if parsed_calls:
                return {
                    "steps": parsed_calls,
                }

            content = clean_json(response["content"])

            try:
                plan = json.loads(content)

                steps = plan.get("steps", [])

                if isinstance(steps, list):
                    normalized_steps = []

                    for step in steps:
                        if not isinstance(step, dict):
                            continue

                        name = step.get("name")
                        if not name:
                            continue

                        arguments = step.get("arguments", {})

                        if isinstance(arguments, str):
                            try:
                                arguments = json.loads(arguments)
                            except Exception:
                                arguments = {}

                        if not isinstance(arguments, dict):
                            arguments = {}

                        normalized_steps.append(
                            {
                                "name": name,
                                "arguments": arguments,
                            }
                        )

                    return {
                        "steps": normalized_steps,
                    }

                return {"steps": []}
            except json.JSONDecodeError:
                self.model.add_message(
                    "user",
                    "La respuesta anterior no era un JSON válido. Respondé únicamente un JSON válido siguiendo exactamente el formato indicado. No uses markdown ni texto adicional.",
                )

        raise RuntimeError("El planner no pudo generar un JSON válido.")