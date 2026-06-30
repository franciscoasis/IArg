import json
from pathlib import Path


class Memory:

    def __init__(self, path="memory.json"):
        self.path = Path(path)

        if self.path.exists():
            self.messages = json.loads(
                self.path.read_text()
            )
        else:
            self.messages = []


    def add(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        self.save()


    def get(self, limit=None):
        if limit is None:
            return self.messages
    
        return self.messages[-limit:]


    def clear(self):
        self.messages = []
        self.save()


    def save(self):
        self.path.write_text(
            json.dumps(
                self.messages,
                indent=2,
                ensure_ascii=False
            )
        )