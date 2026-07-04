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
            },
            "patterns": {
                "type": ["array", "string"],
                "items": {
                    "type": "string"
                },
                "description": "Alias compatible de pattern."
            },
            "max_results": {
                "type": "integer",
                "description": "Cantidad máxima de rutas a devolver.",
                "default": 200
            }
        },
        "required": ["pattern"],
    }

    def run(self, pattern: str | None = None, patterns=None, max_results: int = 200):
        if patterns is not None:
            if isinstance(patterns, list) and patterns:
                pattern = patterns[0]
            elif isinstance(patterns, str) and patterns:
                pattern = patterns

        if not pattern:
            return []

        try:
            max_results = max(1, int(max_results))
        except Exception:
            max_results = 200

        root = Path(".")

        matches = []

        for file in root.rglob(pattern):

            if any(part in IGNORE_DIRS for part in file.parts):
                continue

            if file.is_file():
                matches.append(str(file))

                if len(matches) >= max_results:
                    break

        return matches