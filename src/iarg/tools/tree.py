from pathlib import Path
from iarg.constants import TEXT_EXTENSIONS
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

        for p in sorted(root.rglob("*")):
            if p.is_file() and p.suffix not in TEXT_EXTENSIONS:
                continue
            if "__pycache__" in p.parts:
                continue

            if ".git" in p.parts:
                continue

            lines.append(str(p.relative_to(root)))

        return "\n".join(lines)