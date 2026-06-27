from iarg.commands import CommandHandler
from iarg.model import OllamaModel
from iarg.tools import registry
import json
from iarg.parser import parse_tool_call
from iarg.prompts import BASE_SYSTEM_PROMPT

class Agent:
    def __init__(self):
        self.model = OllamaModel()
        self.commands = CommandHandler(self)

        self.model.add_message(
            "system",
            BASE_SYSTEM_PROMPT + "\n\n" + registry.prompt(),
        )

    def execute_tool(self, name: str, **kwargs):
        tool = registry.get(name)

        if tool is None:
            raise ValueError(f"Herramienta '{name}' no encontrada.")

        return tool.run(**kwargs)

    def run(self, prompt: str):
        result = self.commands.execute(prompt)

        if result is not None:
            return result

        self.model.add_message("user", prompt)

        for _ in range(10):  # evita bucles infinitos
            response = self.model.complete()

            calls = parse_tool_call(response)

            if calls is None:
                return response["content"]

            for call in calls:

                # Compatibilidad con tool calling nativo de Ollama
                if "function" in call:
                    name = call["function"]["name"]
                    args = call["function"]["arguments"]

                # Compatibilidad con Qwen (JSON en content)
                else:
                    name = call["name"]
                    args = call["arguments"]

                result = self.execute_tool(name, **args)

                self.model.add_message("tool", str(result))

        return "Se alcanzó el límite de llamadas a herramientas."

    def edit_file(self, path: str, instruction: str):
        text = self.execute_tool(
            "read_file",
            path=path,
        )

        prompt = f"""
Sos un programador experto.

Modificá el siguiente archivo siguiendo esta instrucción.

Instrucción:
{instruction}

Devolvé SOLAMENTE el código completo del archivo.

Archivo:

{text}
"""

        self.model.add_message("user", prompt)

        response = self.model.complete()

        return response.get("content", "")  