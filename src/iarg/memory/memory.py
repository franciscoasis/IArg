import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from iarg.constants import MEMORY_MAX_MESSAGES
from iarg.constants import MEMORY_MAX_CONTENT_CHARS
from iarg.constants import MEMORY_RECENT_MESSAGES
from iarg.constants import MEMORY_SUMMARY_MAX_ITEMS


class Memory:
    MAX_MESSAGES = MEMORY_MAX_MESSAGES
    MAX_CONTENT_CHARS = MEMORY_MAX_CONTENT_CHARS
    RECENT_MESSAGES = MEMORY_RECENT_MESSAGES
    SUMMARY_MAX_ITEMS = MEMORY_SUMMARY_MAX_ITEMS

    def __init__(self, path="memory.json"):
        self.path = Path(path)

        if self.path.exists():
            self.messages = json.loads(
                self.path.read_text()
            )
        else:
            self.messages = []

        self._prune()


    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": self._normalize_content(content),
        })

        self._prune()

        self.save()

    def add_many(self, messages: list[dict], persist: bool = True):
        normalized = []

        for message in messages:
            role = message.get("role", "user")
            content = self._normalize_content(
                message.get("content", "")
            )

            normalized.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        self.messages.extend(normalized)
        self._prune()

        if persist:
            self.save()


    def get(self, limit=None):
        if limit is None:
            return self.messages
    
        return self.messages[-limit:]


    def clear(self):
        self.messages = []
        self.save()


    def set_limits(
        self,
        max_messages: int | None = None,
        max_content_chars: int | None = None,
        recent_messages: int | None = None,
        summary_max_items: int | None = None,
    ) -> dict:
        if max_messages is not None:
            self.MAX_MESSAGES = max(10, int(max_messages))

        if max_content_chars is not None:
            self.MAX_CONTENT_CHARS = max(100, int(max_content_chars))

        if recent_messages is not None:
            self.RECENT_MESSAGES = max(1, int(recent_messages))

        if summary_max_items is not None:
            self.SUMMARY_MAX_ITEMS = max(1, int(summary_max_items))

        self._prune()
        self.save()

        return self.stats()


    def compact(self) -> dict:
        before = len(self.messages)

        if before <= 1:
            return {
                "before": before,
                "after": before,
                "changed": False,
            }

        recent_target = min(self.RECENT_MESSAGES, before - 1)

        if recent_target < 1:
            self._prune()
            self.save()
            after = len(self.messages)
            return {
                "before": before,
                "after": after,
                "changed": after != before,
            }

        old_messages = self.messages[:-recent_target]
        recent_messages = self.messages[-recent_target:]

        summary = self._build_summary(old_messages)
        self.messages = [summary] + recent_messages

        if len(self.messages) > self.MAX_MESSAGES:
            self.messages = self.messages[-self.MAX_MESSAGES:]

        self.save()

        after = len(self.messages)
        return {
            "before": before,
            "after": after,
            "changed": after != before,
        }


    def stats(self) -> dict:
        total = len(self.messages)

        summary_count = 0
        user_count = 0
        assistant_count = 0
        other_count = 0
        total_chars = 0

        for message in self.messages:
            role = message.get("role")
            content = str(message.get("content", ""))
            total_chars += len(content)

            if "[RESUMEN_MEMORIA]" in content:
                summary_count += 1

            if role == "user":
                user_count += 1
            elif role == "assistant":
                assistant_count += 1
            else:
                other_count += 1

        avg_chars = int(total_chars / total) if total else 0

        file_bytes = self.path.stat().st_size if self.path.exists() else 0

        return {
            "path": str(self.path),
            "total_messages": total,
            "summary_messages": summary_count,
            "user_messages": user_count,
            "assistant_messages": assistant_count,
            "other_messages": other_count,
            "total_chars": total_chars,
            "avg_chars_per_message": avg_chars,
            "file_size_bytes": file_bytes,
            "limits": {
                "max_messages": self.MAX_MESSAGES,
                "max_content_chars": self.MAX_CONTENT_CHARS,
                "recent_messages": self.RECENT_MESSAGES,
                "summary_max_items": self.SUMMARY_MAX_ITEMS,
            },
        }


    def _normalize_content(self, content) -> str:
        text = str(content)

        if len(text) <= self.MAX_CONTENT_CHARS:
            return text

        return text[:self.MAX_CONTENT_CHARS] + "\n... [mensaje truncado]"


    def _build_summary(self, messages: list[dict]) -> dict:
        if not messages:
            return {
                "role": "system",
                "content": "[RESUMEN_MEMORIA]\nNo había mensajes para resumir.",
            }

        user_count = 0
        assistant_count = 0
        other_count = 0

        for message in messages:
            role = message.get("role")

            if role == "user":
                user_count += 1
            elif role == "assistant":
                assistant_count += 1
            else:
                other_count += 1

        sample = messages[-self.SUMMARY_MAX_ITEMS:]

        lines = [
            "[RESUMEN_MEMORIA]",
            (
                "Conversación compactada: "
                f"{len(messages)} mensajes ("
                f"user={user_count}, assistant={assistant_count}, other={other_count})."
            ),
            "Últimos puntos relevantes:",
        ]

        for message in sample:
            role = message.get("role", "unknown")
            content = " ".join(
                str(message.get("content", "")).split()
            )

            if len(content) > 160:
                content = content[:160] + "..."

            lines.append(
                f"- {role}: {content}"
            )

        summary_content = self._normalize_content(
            "\n".join(lines)
        )

        return {
            "role": "system",
            "content": summary_content,
        }


    def _prune(self):
        if len(self.messages) <= self.MAX_MESSAGES:
            return

        recent_target = min(self.RECENT_MESSAGES, self.MAX_MESSAGES - 1)

        if recent_target < 1:
            self.messages = self.messages[-self.MAX_MESSAGES:]
            return

        old_messages = self.messages[:-recent_target]
        recent_messages = self.messages[-recent_target:]

        summary = self._build_summary(old_messages)

        self.messages = [summary] + recent_messages

        if len(self.messages) > self.MAX_MESSAGES:
            self.messages = self.messages[-self.MAX_MESSAGES:]


    def save(self):
        payload = json.dumps(
            self.messages,
            indent=2,
            ensure_ascii=False,
        )

        self.path.parent.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=self.path.parent) as temp_file:
            temp_file.write(payload)
            temp_path = Path(temp_file.name)

        temp_path.replace(self.path)