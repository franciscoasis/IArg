import typer

from iarg.agent import Agent
from iarg.ui.app import launch_gui


app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    help="IArg: asistente local por CLI y GUI.",
)


def run_cli_chat():
    agent = Agent()

    while True:
        prompt = input("> ")

        if prompt == "exit":
            break

        print(agent.run(prompt))


@app.command()
def chat():
    """Inicia IArg en modo chat por terminal."""
    run_cli_chat()


@app.command()
def gui():
    """Inicia IArg en interfaz gráfica."""
    launch_gui()


if __name__ == "__main__":
    app()