from iarg.tools.proyect import ProjectTool
from iarg.tools.files import FileTool
from iarg.tools.diff import DiffTool
from iarg.utils import clean_code


class CommandHandler:
    def __init__(self, agent):
        self.agent = agent

    def execute(self, prompt: str):
        """
        Ejecuta un comando.
        Si el prompt no es un comando devuelve None.
        """

        if prompt == "/clear":
            self.agent.model.messages.clear()
            return "Historial borrado."

        if prompt == "/tree":
            return ProjectTool.tree()

        if prompt.startswith("/read "):
            path = prompt.removeprefix("/read ")
            return self.agent._read_file(path)

        if prompt.startswith("/edit "):
            return self._edit(prompt.removeprefix("/edit "))

        return None

    def _edit(self, path: str):

        instruction = input("¿Qué querés cambiar? ")

        old_code = FileTool.read(path)

        new_code = self.agent.edit_file(path, instruction)

        new_code = clean_code(new_code)

        print(DiffTool.diff(old_code, new_code))

        ans = input("\n¿Aplicar cambios? (y/N): ")

        if ans.lower() == "y":
            FileTool.write(path, new_code)
            return "✅ Archivo modificado."

        return "❌ Cambios descartados."