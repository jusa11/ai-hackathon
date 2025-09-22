from charts import create_plot
from services import metrics


def get_metric_with_plot(func, df, metric_name=None, **filters):
    """
    Вызывает метрику, строит график (если можно) и возвращает result, title и флаги.
    """
    try:
        result = func(df, **filters)
    except TypeError:
        result = func(df)

    title = None
    type_chart = None
    has_plot = False

    if metric_name:
        meta = metrics.METRICS.get(metric_name, {})
        title = meta.get("title", metric_name)
        type_chart = meta.get("type_chart")  # либо None, либо 'bar'/'pie'
        has_plot = meta.get("has_plot", False)

    return {
        "result": result,
        "title": title,
        "type_chart": type_chart,  # можно использовать для выбора компонента графика
        "has_plot": has_plot,      # именно True/False
    }
