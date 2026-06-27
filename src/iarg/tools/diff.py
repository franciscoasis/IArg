import difflib


class DiffTool:
    @staticmethod
    def diff(old: str, new: str) -> str:
        return "\n".join(
            difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile="original",
                tofile="nuevo",
                lineterm="",
            )
        )