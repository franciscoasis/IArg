import json


def parse_tool_call(message):
    if message.get("tool_calls"):
        return message["tool_calls"]

    try:
        call = json.loads(message["content"])

        if "name" in call:
            return [call]

    except Exception:
        pass

    return None