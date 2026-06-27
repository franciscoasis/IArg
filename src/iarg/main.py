# Este es un programa simple que utiliza un agente para procesar prompts y generar respuestas.

from iarg.agent import Agent

agent = Agent()

while True:
    prompt = input("> ")

    if prompt == "exit":
        break

    print(agent.run(prompt))