import os
from pathlib import Path
import re
from iarg.constants import TEXT_EXTENSIONS
from iarg.constants import IGNORE_DIRS
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
            },
            "paths": {
                "type": ["array", "string"],
                "items": {
                    "type": "string"
                },
                "description": "Alias compatible de path. Usa solo la primera ruta si es lista."
            },
            "max_results": {
                "type": "integer",
                "description": "Cantidad máxima de coincidencias a devolver.",
                "default": 200
            },
            "max_files": {
                "type": "integer",
                "description": "Cantidad máxima de archivos de texto a revisar.",
                "default": 400
            }
        },
        "required": ["pattern"]
    }

    def run(self, pattern: str, path=".", paths=None, max_results: int = 200, max_files: int = 400):
        # Compatibilidad con planners que envian `paths` en lugar de `path`.
        if paths is not None:
            if isinstance(paths, list) and paths:
                path = paths[0]
            elif isinstance(paths, str) and paths:
                path = paths

        try:
            max_results = max(1, int(max_results))
        except Exception:
            max_results = 200

        try:
            max_files = max(1, int(max_files))
        except Exception:
            max_files = 400

        root = Path(path)

        try:
            regex = re.compile(pattern)
        except re.error:
            regex = re.compile(re.escape(pattern))

        results = []
        scanned_files = 0
        hit_limit = False

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [
                dirname
                for dirname in dirnames
                if dirname not in IGNORE_DIRS
            ]

            current = Path(dirpath)

            for filename in filenames:
                file = current / filename

                if file.suffix not in TEXT_EXTENSIONS:
                    continue

                scanned_files += 1

                if scanned_files > max_files:
                    hit_limit = True
                    break

                try:
                    text = file.read_text(encoding="utf-8")
                except Exception:
                    continue

                for lineno, line in enumerate(text.splitlines(), 1):

                    if regex.search(line):

                        results.append(
                            f"{file}:{lineno}: {line.strip()}"
                        )

                        if len(results) >= max_results:
                            hit_limit = True
                            break

                if hit_limit:
                    break

            if hit_limit:
                break

        if not results:
            return "No se encontraron coincidencias."

        output = "\n".join(results)

        if hit_limit:
            output += (
                f"\n\n[grep truncado: max_results={max_results}, max_files={max_files}]"
            )

        return output