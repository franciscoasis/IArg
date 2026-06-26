from iarg.model import OllamaModel
from iarg.tools.files import FileTool
import traceback

model = OllamaModel()

while True:
    prompt = input("> ")

    if prompt == "exit":
        break

    if prompt.startswith("/read "):
        path = prompt.removeprefix("/read ")

        try:
            text = FileTool.read(path)

            response = model.chat(
                f"Explicá el siguiente archivo de Python:\n\n{text}"
            )

            print(response)

        except Exception:
            traceback.print_exc()

        continue

    print(model.chat(prompt))