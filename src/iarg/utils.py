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