import pandas as pd
from services.metrics import METRICS
from charts import metric_with_plot
from services import llm_comment_service  # новый импорт


def handle_user_query(parsed: dict, df: pd.DataFrame, user_query: str) -> dict:
    if "error" in parsed:
        return {"result_text": parsed["error"], "result": None, "has_plot": False}

    metric_name = parsed.get("metric")
    filters = parsed.get("filters", {})

    meta = METRICS.get(metric_name)
    if not meta:
        return {
            "result_text": f"Метрика '{metric_name}' не найдена.",
            "result": None,
            "has_plot": False,
        }

    func = meta["func"]

    try:
        result_with_plot = metric_with_plot.get_metric_with_plot(
            func, df, metric_name=metric_name, **filters
        )
    except Exception as e:
        return {
            "result_text": f"Ошибка при вычислении метрики: {str(e)}",
            "result": None,
            "has_plot": False,
        }

    result = result_with_plot.get("result")
    type_chart = result_with_plot.get("type_chart")
    has_plot = result_with_plot.get("has_plot")

    # Человекопонятный текст через LLM
    try:
        comment = llm_comment_service.generate_comment(
            user_query=user_query,
            metric=metric_name,
            result=result
        )
    except Exception as e:
        comment = f"Не удалось сгенерировать комментарий: {str(e)}"

    return {
        "result_text": comment,   # только человекопонятный текст
        "result": result,         # данные для графика
        "type_chart": type_chart,  # можно использовать для выбора компонента графика
        "has_plot": has_plot
    }
