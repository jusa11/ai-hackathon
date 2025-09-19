import pandas as pd
from services.metrics import METRICS
from charts import metric_with_plot


def handle_user_query(parsed: dict, df: pd.DataFrame) -> dict:
    if "error" in parsed:
        return parsed

    metric = parsed.get("metric")
    filters = parsed.get("filters", {})

    func = METRICS.get(metric)
    if not func:
        return {"error": f"Метрика '{metric}' не найдена.", "raw": parsed}

    # используем универсальную функцию
    result_with_plot = metric_with_plot.get_metric_with_plot(
        func, df, **filters)

    return {**parsed, **result_with_plot}
