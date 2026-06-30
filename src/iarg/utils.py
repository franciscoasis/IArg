def clean_code(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        # sacar ```python
        lines = lines[1:]

        # sacar ```
        if lines[-1].startswith("```"):
            lines = lines[:-1]

        return "\n".join(lines)

    return text

def clean_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()