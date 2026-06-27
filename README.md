# IArg

IArg es un agente de IA local desarrollado en Python que utiliza modelos de lenguaje ejecutados mediante Ollama. El proyecto está diseñado con una arquitectura modular basada en herramientas, lo que facilita agregar nuevas capacidades y experimentar con agentes autónomos.

## Características

- Agente conversacional local.
- Arquitectura modular basada en herramientas.
- Lectura y exploración de proyectos.
- Manipulación de archivos.
- Planner para descomponer tareas complejas.
- Fácil extensión mediante nuevas herramientas.

## Estructura del proyecto

```
src/
└── iarg/
    ├── agent/
    ├── model/
    ├── planner/
    ├── tools/
    └── main.py
```

## Requisitos

- Python 3.12 o superior
- uv
- Ollama

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/IArg.git
cd IArg
```

Instalar las dependencias:

```bash
uv sync
```

## Uso

Iniciar el agente:

```bash
PYTHONPATH=src uv run python -m iarg.main chat
```

## Arquitectura

El agente sigue el siguiente flujo:

1. Recibe una consulta del usuario.
2. El modelo decide si necesita utilizar una herramienta.
3. Se ejecuta la herramienta correspondiente.
4. El resultado se incorpora nuevamente al contexto.
5. El modelo genera la respuesta final.

Las herramientas se encuentran en `src/iarg/tools` y pueden añadirse fácilmente implementando una nueva clase e integrándola en el agente.

## Roadmap

- [x] Agente conversacional
- [x] Integración con Ollama
- [x] Herramientas para archivos
- [x] Exploración de proyectos
- [ ] Planner
- [ ] Edición de archivos
- [ ] Memoria de conversación
- [ ] Soporte para múltiples modelos
- [ ] Tests

## Tecnologías

- Python
- Ollama
- uv

## Licencia

Este proyecto se distribuye bajo la licencia MIT.