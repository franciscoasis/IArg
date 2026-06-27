from pathlib import Path

from .base import Tool
from iarg.constants import IGNORE_DIRS


class FindFilesTool(Tool):
    name = "find_files"

    description = (
        "Busca archivos por nombre o patrón (*.py, *.md, etc.) "
        "y devuelve las rutas encontradas."
    )

    parameters = {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Patrón de búsqueda (ej: *.py, agent.py)"
            }
        },
        "required": ["pattern"],
    }

    def run(self, pattern: str):
        root = Path(".")

        matches = []

        for file in root.rglob(pattern):

            if any(part in IGNORE_DIRS for part in file.parts):
                continue

            if file.is_file():
                matches.append(str(file))

        return matches