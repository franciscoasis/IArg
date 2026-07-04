import json


def parse_tool_call(message):
    tool_calls = message.get("tool_calls")

    if tool_calls:
        normalized = []

        for call in tool_calls:
            function = call.get("function", call)

            name = function.get("name")
            if not name:
                continue

            arguments = function.get("arguments", {})

            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except Exception:
                    arguments = {}

            normalized.append({
                "name": name,
                "arguments": arguments,
            })

        return normalized or None

    try:
        call = json.loads(message["content"])

        if "name" in call:
            arguments = call.get("arguments", {})

            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except Exception:
                    arguments = {}

            return [{
                "name": call["name"],
                "arguments": arguments,
            }]

    except Exception:
        pass

    return None