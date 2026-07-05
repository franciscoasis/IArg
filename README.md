# IArg

IArg es un agente de IA local desarrollado en Python que utiliza modelos de lenguaje ejecutados mediante Ollama. El proyecto está diseñado con una arquitectura modular basada en herramientas, lo que facilita agregar nuevas capacidades y experimentar con agentes autónomos.

## Características

- Agente conversacional local sin dependencias externas.
- Arquitectura modular basada en herramientas.
- Lectura, exploración y análisis de proyectos.
- Manipulación y edición de archivos.
- Planner para descomponer tareas complejas.
- Sistema de memoria conversacional con compactación automática.
- Herramientas avanzadas: grep con límites, tree, diff, find_files.
- Fácil extensión mediante nuevas herramientas.
- Optimización de latencia con truncado de contexto.

## Estructura del proyecto

```
src/iarg/
├── agent/              # Lógica del agente
│   ├── agent.py        # Orquestación principal
│   ├── planner.py      # Descomposición de tareas
│   └── responder.py    # Generación de respuestas
├── memory/             # Sistema de memoria conversacional
│   └── memory.py       # Gestión y compactación de memoria
├── tools/              # Herramientas disponibles
│   ├── base.py         # Clase base para herramientas
│   ├── diff.py         # Comparación de archivos
│   ├── edit_file.py    # Edición de archivos
│   ├── find_files.py   # Búsqueda de archivos
│   ├── grep.py         # Búsqueda en contenido (con límites)
│   ├── read_file.py    # Lectura de archivos
│   ├── tree.py         # Estructura de directorios
│   └── registry.py     # Registro de herramientas
├── ui/                 # Interfaz gráfica
│   └── app.py          # Aplicación UI
├── main.py             # Punto de entrada
├── model.py            # Integración con Ollama
├── parser.py           # Parseo de respuestas
├── commands.py         # Comandos disponibles
└── prompts.py          # Templates de prompts
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

Iniciar la interfaz gráfica:

```bash
PYTHONPATH=src uv run python -m iarg.main gui
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
- [x] Planner
- [x] Edición de archivos
- [x] Memoria de conversación
- [x] Compactación automática de memoria
- [x] Comandos de control (`/memory-stats`, `/memory-config`, `/memory-compact`)
- [ ] Soporte para múltiples modelos
- [ ] Tests unitarios
- [ ] Persistencia mejorada
- [ ] Integración con sistemas externos

## Tecnologías

- Python
- Ollama
- uv

## Licencia

Este proyecto se distribuye bajo la licencia MIT.