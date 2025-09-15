import re
import json

def parse_llm_json(llm_response: str) -> dict:
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", llm_response, re.DOTALL)
    if matches:
        json_str = matches[0]
    else:
        brace_match = re.search(r"(\{.*\})", llm_response, re.DOTALL)
        if brace_match:
            json_str = brace_match.group(1)
        else:
            return {"error": "Не найден JSON", "raw": llm_response}

    try:
        return json.loads(json_str.strip())
    except Exception as e:
        return {"error": f"Не удалось распарсить JSON: {e}", "raw": json_str}