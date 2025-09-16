import pandas as pd
from services.metrics import METRICS


def handle_user_query(parsed: dict, df: pd.DataFrame) -> dict:
    if "error" in parsed:
        return parsed

    metric = parsed.get("metric")
    filters = parsed.get("filters", {})

    func = METRICS.get(metric)
    if not func:
        return {"error": f"Метрика '{metric}' не найдена.", "raw": parsed}

    try:
        result = func(df, **filters)
    except TypeError:
        result = func(df)

    return {**parsed, "result": result}
