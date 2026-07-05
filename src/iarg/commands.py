from iarg.tools.proyect import ProjectTool


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
            self.agent.memory.clear()
            return "Historial borrado."

        if prompt == "/tree":
            return ProjectTool.tree()

        if prompt == "/memory-stats":
            return self._memory_stats()

        if prompt.startswith("/memory-config"):
            return self._memory_config(prompt)

        if prompt == "/memory-compact":
            return self._memory_compact()

        if prompt.startswith("/read "):
            path = prompt.removeprefix("/read ")
            return self.agent._read_file(path)

        if prompt.startswith("/edit "):
            edit_payload = prompt.removeprefix("/edit ")

            if "::" in edit_payload:
                path, instruction = edit_payload.split("::", 1)
                return self._edit(path.strip(), instruction.strip())

            return self._edit(edit_payload)

        return None

    def _edit(self, path: str, instruction: str | None = None):

        if instruction is None:
            instruction = input("¿Qué querés cambiar? ")

        result = self.agent.edit_file(path, instruction)

        if not isinstance(result, dict):
            return "❌ No se pudo generar una edición válida."

        if result.get("status") == "sin_cambios":
            return "No hizo falta cambiar nada."

        approved = self.agent._apply_edit_result(result)

        if approved:
            return "✅ Archivo modificado."

        return "❌ Cambios descartados."

    def _memory_stats(self):
        stats = self.agent.memory.stats()
        limits = stats["limits"]

        lines = [
            "Estado de memoria:",
            f"- archivo: {stats['path']}",
            f"- tamaño archivo: {stats['file_size_bytes']} bytes",
            f"- mensajes totales: {stats['total_messages']}",
            f"- resumenes: {stats['summary_messages']}",
            f"- user/assistant/other: {stats['user_messages']}/{stats['assistant_messages']}/{stats['other_messages']}",
            f"- caracteres totales: {stats['total_chars']}",
            f"- promedio por mensaje: {stats['avg_chars_per_message']}",
            "Límites activos:",
            f"- max_messages: {limits['max_messages']}",
            f"- max_content_chars: {limits['max_content_chars']}",
            f"- recent_messages: {limits['recent_messages']}",
            f"- summary_max_items: {limits['summary_max_items']}",
        ]

        return "\n".join(lines)

    def _memory_config(self, prompt: str):
        parts = prompt.split()

        if len(parts) == 1 or (len(parts) == 2 and parts[1].lower() == "show"):
            return self._memory_stats()

        allowed = {
            "max_messages",
            "max_content_chars",
            "recent_messages",
            "summary_max_items",
        }

        updates = {}

        for token in parts[1:]:
            if "=" not in token:
                return (
                    "Uso inválido. Ejemplo: "
                    "/memory-config max_messages=220 recent_messages=90"
                )

            key, value = token.split("=", 1)
            key = key.strip()
            value = value.strip()

            if key not in allowed:
                return (
                    f"Parámetro desconocido: {key}. "
                    "Permitidos: max_messages, max_content_chars, recent_messages, summary_max_items"
                )

            try:
                updates[key] = int(value)
            except Exception:
                return f"Valor inválido para {key}: {value}. Debe ser entero."

        stats = self.agent.memory.set_limits(**updates)
        limits = stats["limits"]

        lines = [
            "Configuración de memoria actualizada.",
            f"- max_messages: {limits['max_messages']}",
            f"- max_content_chars: {limits['max_content_chars']}",
            f"- recent_messages: {limits['recent_messages']}",
            f"- summary_max_items: {limits['summary_max_items']}",
            f"- mensajes actuales: {stats['total_messages']}",
        ]

        return "\n".join(lines)

    def _memory_compact(self):
        result = self.agent.memory.compact()

        lines = [
            "Compactación de memoria ejecutada.",
            f"- antes: {result['before']}",
            f"- después: {result['after']}",
            f"- cambios aplicados: {'sí' if result['changed'] else 'no'}",
        ]

        return "\n".join(lines)