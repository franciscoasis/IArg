from pathlib import Path


class ProjectTool:
    @staticmethod
    def tree(root: str = ".") -> str:
        paths = []

        for path in sorted(Path(root).rglob("*")):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue

            paths.append(str(path))

        return "\n".join(paths)