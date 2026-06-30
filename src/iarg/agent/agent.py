from iarg.commands import CommandHandler
from iarg.model import OllamaModel
from iarg.tools import registry
from iarg.agent.planner import Planner
from iarg.agent.responder import Responder
from iarg.memory import Memory


class Agent:

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


    def run(self, prompt: str):

        # Guardamos el contexto anterior antes de agregar
        # la pregunta actual
        history = self.memory.get(limit=20)


        result = self.commands.execute(prompt)


        # Si es un comando interno
        if result is not None:

            self.memory.add(
                "user",
                prompt
            )

            self.memory.add(
                "assistant",
                result
            )

            return result


        # Planificar acción
        plan = self.planner.plan(prompt)


        context = []


        # Ejecutar herramientas
        for call in plan["steps"]:

            name = call["name"]
            args = call["arguments"]


            result = self.execute_tool(
                name,
                **args,
            )


            context.append({
                "tool": name,
                "arguments": args,
                "result": result,
            })


        # Generar respuesta final
        answer = self.responder.answer(
            question=prompt,
            context=context,
            history=history,
        )


        # Guardar conversación
        self.memory.add(
            "user",
            prompt
        )

        self.memory.add(
            "assistant",
            answer
        )


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


        content = response.get(
            "content",
            ""
        )


        self.memory.add(
            "user",
            instruction
        )


        self.memory.add(
            "assistant",
            content
        )


        return content