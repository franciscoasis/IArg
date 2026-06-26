from pathlib import Path


class FileTool:
    @staticmethod
    def read(path: str) -> str:
        return Path(path).read_text(encoding="utf-8")