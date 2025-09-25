from services import metrics


def get_metric_with_plot(func, df, metric_name=None, **filters):

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
        type_chart = meta.get("type_chart")  
        has_plot = meta.get("has_plot", False)

    return {
        "result": result,
        "title": title,
        "type_chart": type_chart,  
        "has_plot": has_plot,     
    }
