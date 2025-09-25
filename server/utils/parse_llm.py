import re
import json


def parse_llm_json(llm_response: str) -> dict:
  
    s = llm_response.replace("“", '"').replace("”", '"')


    matches = re.findall(r"```json\s*(\{.*?\})\s*```", s, re.DOTALL)
    if matches:
        json_str = matches[0]
    else:
        brace_match = re.search(r"(\{.*\})", s, re.DOTALL)
        if brace_match:
            json_str = brace_match.group(1)
        else:
            return {"error": "Не найден JSON", "raw": s}

    try:
        obj = json.loads(json_str)
    except Exception as e:
        return {"error": f"Не удалось распарсить JSON: {e}", "raw": json_str}


    gb = obj.get("group_by")
    if isinstance(gb, str):
        obj["group_by"] = [gb]
    elif gb is None:
        obj["group_by"] = []


    tf = obj.get("timeframe", {})
    if not isinstance(tf, dict):
        obj["timeframe"] = {}
    else:
      
        if "month" in tf:
            try:
                obj["timeframe"]["month"] = int(tf["month"])
            except:
                obj["timeframe"]["month"] = None
        if "months" in tf and isinstance(tf["months"], list):
            obj["timeframe"]["months"] = [
                int(m) for m in tf["months"] if isinstance(m, int) or m.isdigit()]
     


    obj.setdefault("filters", {})
    obj.setdefault("group_by", [])
    obj.setdefault("timeframe", {})

    return obj
