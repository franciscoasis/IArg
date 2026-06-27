from .base import Tool
from .files import FileTool


class ReadFileTool(Tool):
    name = "read_file"
    description = (
    "Lee el contenido de un archivo. "
    "Usá primero la herramienta tree si no conocés la estructura del proyecto."
)

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Ruta del archivo a leer."
            }
        },
        "required": ["path"]
    }

    def run(self, path: str):
        return FileTool.read(path)