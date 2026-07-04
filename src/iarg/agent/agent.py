import json

from iarg.agent.planner import Planner
from iarg.agent.responder import Responder
from iarg.commands import CommandHandler
from iarg.memory import Memory
from iarg.model import OllamaModel
from iarg.tools import registry
from iarg.tools.diff import DiffTool
from iarg.tools.files import FileTool
from iarg.utils import clean_code


class Agent:
    MAX_PLANNER_CYCLES = 2

    def __init__(self):
        self.model = OllamaModel(
            model="qwen2.5-coder:7b"
        )

        self.memory = Memory()

        self.commands = CommandHandler(self)
        self.planner = Planner()
        self.responder = Responder()


    def execute_tool(self, name: str, **kwargs):
        tool = registry.get(name)

        if tool is None:
            raise ValueError(
                f"Herramienta '{name}' no encontrada."
            )

        return tool.run(**kwargs)


    def _read_file(self, path: str):
        return FileTool.read(path)


    def _apply_edit_result(self, result: dict):
        diff = result.get("diff")

        if diff:
            print(diff)

        ans = input("\n¿Aplicar cambios? (y/N): ")

        if ans.lower() != "y":
            return False

        FileTool.write(result["path"], result["content"])

        return True


    def run(self, prompt: str):

        # Guardamos el contexto anterior antes de agregar
        # la pregunta actual
        history = self.memory.get(limit=20)


        result = self.commands.execute(prompt)


        # Si es un comando interno
        if result is not None:

            self.memory.add_many([
                {
                    "role": "user",
                    "content": prompt,
                },
                {
                    "role": "assistant",
                    "content": result,
                },
            ])

            return result


        context = []
        executed = set()


        # Planificar y ejecutar acciones en ciclos cortos
        for _ in range(self.MAX_PLANNER_CYCLES):
            plan = self.planner.plan(
                prompt,
                history=history,
                context=context,
            )

            steps = plan.get("steps", [])

            if not steps:
                break

            new_tool_used = False

            for call in steps:
                name = call["name"]
                args = call["arguments"]

                signature = json.dumps(
                    {
                        "name": name,
                        "arguments": args,
                    },
                    sort_keys=True,
                    ensure_ascii=False,
                )

                if signature in executed:
                    continue

                executed.add(signature)

                result = self.execute_tool(
                    name,
                    **args,
                )

                if name == "edit_file" and isinstance(result, dict):
                    if result.get("status") == "pendiente_aprobacion":
                        approved = self._apply_edit_result(result)

                        result = {
                            **result,
                            "status": "actualizado" if approved else "descartado",
                        }

                context.append({
                    "tool": name,
                    "arguments": args,
                    "result": result,
                })

                new_tool_used = True

            if not new_tool_used:
                break


        # Generar respuesta final
        answer = self.responder.answer(
            question=prompt,
            context=context,
            history=history,
        )


        # Guardar conversación
        self.memory.add_many([
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "assistant",
                "content": answer,
            },
        ])


        return answer



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


Reglas:
- Devolvé SOLAMENTE el código completo.
- No agregues explicaciones.
- Conservá la estructura del archivo.


Archivo:

{text}
"""


        history = self.memory.get(limit=10)


        self.model.clear()


        self.model.add_message(
            "system",
            """
Sos un asistente experto en programación.
Tu tarea es modificar archivos correctamente.
"""
        )


        for message in history:
            self.model.add_message(
                message["role"],
                message["content"]
            )


        self.model.add_message(
            "user",
            prompt
        )


        response = self.model.complete()


        content = clean_code(
            response.get(
                "content",
                ""
            )
        )

        if not content:
            raise RuntimeError(
                f"No se pudo generar contenido nuevo para {path}."
            )

        if content == text:
            return {
                "path": path,
                "status": "sin_cambios",
            }

        return {
            "path": path,
            "status": "pendiente_aprobacion",
            "original": text,
            "content": content,
            "diff": DiffTool.diff(text, content),
        }