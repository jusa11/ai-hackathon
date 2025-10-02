from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from services import metrics
from services.db_service import get_db
from charts import metric_with_plot
from services.cached_df_service import get_full_df_cached
import random

router = APIRouter()


@router.get("/{metric_name}")
def get_plot(
    metric_name: str,
    request: Request,
    db: Session = Depends(get_db)
):
    filters = dict(request.query_params)

    df = get_full_df_cached(db)

    if metric_name == "random":
        dict_keys = [k for k, m in metrics.METRICS.items()
                     if m.get("has_plot")]
    elif metric_name == "big":
        dict_keys = [k for k, m in metrics.METRICS.items() if m.get(
            "has_plot") and m.get("big")]
    else:
        dict_keys = [metric_name]

    if not dict_keys:
        return {"error": f"Нет доступных метрик для '{metric_name}'"}

    selected_keys = random.sample(dict_keys, min(3, len(dict_keys)))

    results = []
    for key in selected_keys:
        meta = metrics.METRICS.get(key)
        if not meta:
            results.append({"metric": key, "error": "Метрика не найдена"})
            continue

        func = meta["func"]
        try:
            metric_result = metric_with_plot.get_metric_with_plot(
                func, df, metric_name=key, **filters
            )
            results.append({"metric": key, "data": metric_result})
        except Exception as e:
            results.append({"metric": key, "error": str(e)})

    return results
