from typing import Dict, Any, List
import pandas as pd
from .run_metric import run_metric
from services.llm_comment_service import generate_comment
from services.metrics import METRICS
from services.general_hr_summary_stub import general_hr_summary_stub


def handle_user_query(parsed: dict, df: pd.DataFrame, user_query: str) -> Dict[str, Any]:
    metric_name = parsed.get("metric")
    filters = parsed.get("filters", {})
    group_by = parsed.get("group_by", [])
    timeframe = parsed.get("timeframe", {})

    meta = METRICS.get(metric_name)

    # Если метрика не найдена — возвращаем заглушку
    if not meta:
        return general_hr_summary_stub(df, user_query)

    func = meta["func"]
    type_chart = meta.get("type_chart", "bar")

    result_with_plot = run_metric(
        func, df, filters, timeframe, group_by, type_chart)
    result = result_with_plot.get("result")
    has_plot = result_with_plot.get("has_plot", False)

    # Если результат пустой — возвращаем заглушку
    if not result:
        return general_hr_summary_stub(df, user_query)

    # Генерация комментария через LLM
    try:
        from services.llm_comment_service import generate_comment
        comment = generate_comment(user_query, metric_name, result)
    except Exception as e:
        comment = f"Не удалось сгенерировать комментарий: {str(e)}"

    return {
        "result_text": comment,
        "result": result,
        "type_chart": type_chart,
        "has_plot": has_plot
    }
