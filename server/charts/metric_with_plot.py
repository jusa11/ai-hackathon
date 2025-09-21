from charts import create_plot
from services import metrics  


def get_metric_with_plot(func, df, metric_name=None, **filters):
    """
    Вызывает метрику, строит график (если можно) и возвращает result, plot и title.
    """
    try:
        result = func(df, **filters)
    except TypeError:
        result = func(df)

    title = None
    type_chart = None
    if metric_name:
        title = metrics.METRICS.get(metric_name, {}).get("title", metric_name)
        type_chart = metrics.METRICS.get(
            metric_name, {}).get("type_chart", metric_name)

    return {
        "result": result,
        "title": title,
        "type_chart": type_chart,
    }
