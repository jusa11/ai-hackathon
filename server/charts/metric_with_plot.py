from charts import create_plot


def get_metric_with_plot(func, df, **filters):
    """Вызывает метрику, строит график (если можно) и возвращает оба значения."""
    try:
        result = func(df, **filters)
    except TypeError:
        result = func(df)

    plot = None
    if isinstance(result, dict) and result:
        plot = create_plot.plot_metric(result, title=func.__name__, kind="bar")

    return {"result": result, "plot": plot}
