from iarg.tools.diff import DiffTool
from iarg.tools.files import FileTool
from iarg.utils import clean_code
from .base import Tool


class EditFileTool(Tool):
    name = "edit_file"

    description = (
        "Edita un archivo existente según una instrucción y devuelve el borrador para aprobación."
    )

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Ruta del archivo a editar."
            },
            "instruction": {
                "type": "string",
                "description": "Cambio que hay que aplicar al archivo."
            }
        },
        "required": ["path", "instruction"],
    }

    def run(self, path: str, instruction: str):
        original = FileTool.read(path)

        from iarg.model import OllamaModel

        model = OllamaModel(
            model="qwen2.5-coder:7b"
        )

        model.clear()

        model.add_message(
            "system",
            """
Sos un asistente experto en programación.
Tu tarea es editar archivos correctamente.
Devolvé solamente el archivo completo modificado.
No agregues explicaciones, markdown ni bloques de código.
Conservá la estructura general del archivo salvo que la instrucción pida otra cosa.
"""
        )

        model.add_message(
            "user",
            f"""
Archivo: {path}

Instrucción:
{instruction}

Archivo actual:
{original}
"""
        )

        response = model.complete()

        content = clean_code(
            response.get("content", "")
        )

        if not content:
            raise RuntimeError(
                f"No se pudo generar contenido nuevo para {path}."
            )

        if content == original:
            return {
                "path": path,
                "status": "sin_cambios",
            }

        return {
            "path": path,
            "status": "pendiente_aprobacion",
            "original": original,
            "content": content,
            "diff": DiffTool.diff(original, content),
        }