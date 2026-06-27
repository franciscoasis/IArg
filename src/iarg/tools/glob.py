from pathlib import Path

from .base import Tool
from iarg.constants import IGNORE_DIRS


class GlobTool(Tool):
    name = "glob"

    description = (
        "Busca archivos usando patrones glob. "
        "Ejemplos: '*.py', '**/*.md', 'src/**/*.py'."
    )

    parameters = {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Patrón glob."
            }
        },
        "required": ["pattern"],
    }

    def run(self, pattern: str):
        matches = []

        for file in Path(".").glob(pattern):

            if any(part in IGNORE_DIRS for part in file.parts):
                continue

            if file.is_file():
                matches.append(str(file))

        return {
            "count": len(matches),
            "files": matches,
        }