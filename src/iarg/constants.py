SYSTEM_PROMPT = """
Sos un agente que dispone de herramientas.

Si necesitás más información, seguí llamando herramientas.

No respondas hasta tener toda la información necesaria.

Cuando quieras usar una herramienta respondé SOLAMENTE con JSON:

{
  "name": "...",
  "arguments": {...}
}

Cuando ya no necesites herramientas respondé normalmente.
"""

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".sql",
}

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}