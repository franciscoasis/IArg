import os
from pathlib import Path
from iarg.constants import TEXT_EXTENSIONS
from iarg.constants import IGNORE_DIRS
from .base import Tool


class TreeTool(Tool):
    name = "tree"

    description = "Muestra la estructura de archivos de un directorio."

    parameters = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directorio a listar. Si se omite, usa el directorio actual."
            }
        }
    }

    def run(self, path="."):
        root = Path(path)

        lines = []

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [
                dirname
                for dirname in dirnames
                if dirname not in IGNORE_DIRS
            ]

            current = Path(dirpath)

            for filename in filenames:
                file_path = current / filename

                if file_path.suffix not in TEXT_EXTENSIONS:
                    continue

                lines.append(str(file_path.relative_to(root)))

        return "\n".join(sorted(lines))