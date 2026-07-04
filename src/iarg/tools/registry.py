from .read_file import ReadFileTool
from .tree import TreeTool
from .grep import GrepTool
from .read_files import ReadFilesTool
from .find_files import FindFilesTool
from .glob import GlobTool
from .edit_file import EditFileTool

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def get(self, name):
        return self.tools.get(name)

    def list(self):
        return list(self.tools.values())

    def to_ollama(self):
        return [tool.to_ollama() for tool in self.tools.values()]
    
    def prompt(self):
        lines = ["Herramientas disponibles:\n"]

        for tool in self.list():
            lines.append(f"- {tool.name}: {tool.description}")

        return "\n".join(lines)


registry = ToolRegistry()


registry.register(ReadFileTool())
registry.register(TreeTool())
registry.register(GrepTool())
registry.register(ReadFilesTool())
registry.register(FindFilesTool())
registry.register(GlobTool())
registry.register(EditFileTool())