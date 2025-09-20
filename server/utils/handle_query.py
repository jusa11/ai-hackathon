import pandas as pd
from services.metrics import METRICS
from charts import metric_with_plot


def handle_user_query(parsed: dict, df: pd.DataFrame) -> dict:
    # Если LLM вернул ошибку
    if "error" in parsed:
        return parsed

    metric_name = parsed.get("metric")
    filters = parsed.get("filters", {})

    # Получаем метрику из METRICS
    meta = METRICS.get(metric_name)
    if not meta:
        return {"error": f"Метрика '{metric_name}' не найдена.", "raw": parsed}

    # Берём функцию
    func = meta["func"]

    # Вызываем универсальную функцию для получения результата и графика
    try:
        result_with_plot = metric_with_plot.get_metric_with_plot(
            func, df, **filters)
    except Exception as e:
        return {"error": f"Ошибка при вычислении метрики: {str(e)}"}

    # Объединяем результат с исходным парсингом LLM
    return {**parsed, **result_with_plot}
