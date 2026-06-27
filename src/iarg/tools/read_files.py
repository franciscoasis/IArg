from .base import Tool
from .files import FileTool


class ReadFilesTool(Tool):
    name = "read_files"

    description = (
        "Lee el contenido de varios archivos en una sola llamada."
    )

    parameters = {
        "type": "object",
        "properties": {
            "paths": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Lista de rutas a leer."
            }
        },
        "required": ["paths"]
    }

    def run(self, paths: list[str]):
        result = []

        for path in paths:

            try:
                text = FileTool.read(path)

                result.append(
                    f"""Archivo: {path}

{text}
"""
                )

            except Exception as e:

                result.append(
                    f"""Archivo: {path}

ERROR: {e}
"""
                )

        return "\n\n" + "=" * 80 + "\n\n".join(result)