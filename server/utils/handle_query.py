from typing import Dict, Any, List
import pandas as pd
from .run_metric import run_metric
from services.llm_comment_service import generate_comment
from services.metrics import METRICS


def handle_user_query(parsed: dict, df: pd.DataFrame, user_query: str) -> Dict[str, Any]:
    if "error" in parsed:
        return {"result_text": parsed["error"], "result": None, "has_plot": False}

    metric_name = parsed.get("metric")
    filters = parsed.get("filters", {})
    group_by = parsed.get("group_by", [])
    timeframe = parsed.get("timeframe", {})
    print(f"Filter: {parsed}")

    meta = METRICS.get(metric_name)
    if not meta:
        return {"result_text": f"Метрика '{metric_name}' не найдена.", "result": None, "has_plot": False}

    func = meta["func"]
    type_chart = meta.get("type_chart", "bar")

    result_with_plot = run_metric(
        func, df, filters, timeframe, group_by, type_chart)
    result = result_with_plot.get("result")
    type_chart = result_with_plot.get("type_chart")
    has_plot = result_with_plot.get("has_plot")

    try:
        comment = generate_comment(user_query, metric_name, result)
    except Exception as e:
        comment = f"Не удалось сгенерировать комментарий: {str(e)}"

    return {"result_text": comment, "result": result, "type_chart": type_chart, "has_plot": has_plot}
