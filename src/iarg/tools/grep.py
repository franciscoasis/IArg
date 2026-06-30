from ast import pattern
from pathlib import Path
import re
from iarg.constants import TEXT_EXTENSIONS
from .base import Tool


class GrepTool(Tool):
    name = "grep"

    description = (
        "Busca un texto o expresión regular dentro de todos los archivos del proyecto."
    )

    parameters = {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Texto o regex a buscar."
            },
            "path": {
                "type": "string",
                "description": "Directorio donde buscar.",
                "default": "."
            }
        },
        "required": ["pattern"]
    }

    def run(self, pattern: str, path="."):
        root = Path(path)

        try:
            regex = re.compile(pattern)
        except re.error:
            regex = re.compile(re.escape(pattern))

        results = []

        for file in root.rglob("*"):

            if not file.is_file():
                continue
        
            if ".git" in file.parts:
                continue
        
            if "__pycache__" in file.parts:
                continue
        
            if file.suffix not in TEXT_EXTENSIONS:
                continue
        
            try:
                text = file.read_text(encoding="utf-8")
            except Exception:
                continue

            for lineno, line in enumerate(text.splitlines(), 1):

                if regex.search(line):

                    results.append(
                        f"{file}:{lineno}: {line.strip()}"
                    )

        if not results:
            return "No se encontraron coincidencias."

        return "\n".join(results)