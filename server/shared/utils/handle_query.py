from typing import Dict, Any, List
import pandas as pd
import json
from .run_metric import run_metric
from modules.llm.comment_service import generate_comment_metrics
from modules.analytics.metrics import METRICS
from shared.general_hr_summary_stub import general_hr_summary_stub


def _coerce_relevant(val) -> bool | None:
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    if s in ("false", "0", "no", "нет", "n"):
        return False
    if s in ("true", "1", "yes", "да", "y"):
        return True
    return None


def _metric_is_null(metric_val) -> bool:
    if metric_val is None:
        return True
    if isinstance(metric_val, str) and metric_val.strip().lower() in ("", "null", "none", "нет"):
        return True
    return False


def handle_user_query(parsed: dict, df: pd.DataFrame, user_query: str) -> dict:
    metric_name = parsed.get("metric")
    filters = parsed.get("filters", {})
    group_by = parsed.get("group_by", [])
    timeframe = parsed.get("timeframe", {})

    relevant = _coerce_relevant(parsed.get("relevant"))

    if not relevant or _metric_is_null(metric_name):
        try:
            comment = generate_comment_metrics(
                user_query, "irrelevant", "irrelevant")
        except Exception as e:
            comment = f"Не удалось сгенерировать комментарий: {str(e)}"
        return {
            "result_text": comment,
            "result": "irrelevant",
            "type_chart": None,
            "has_plot": False
        }

    meta = METRICS.get(metric_name)
    if not meta:
        return general_hr_summary_stub(df, user_query)

    func = meta["func"]
    type_chart = meta.get("type_chart", "bar")

    result_with_plot = run_metric(
        func, df, filters, timeframe, group_by, metric_name=metric_name
    )
    result = result_with_plot.get("result")
    has_plot = result_with_plot.get("has_plot", False)

    if not result:
        return general_hr_summary_stub(df, user_query)

    try:
        comment = generate_comment_metrics(user_query, metric_name, result)
    except Exception as e:
        comment = f"Не удалось сгенерировать комментарий: {str(e)}"

    return {
        "result_text": comment,
        "result": result,
        "type_chart": type_chart,
        "has_plot": has_plot
    }
