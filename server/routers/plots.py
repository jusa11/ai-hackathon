from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import analytics_service, metrics  # тут METRICS с has_plot
from services.db_service import get_db
from charts import metric_with_plot
import random

router = APIRouter()


@router.get("/{metric_name}")
def get_plot(metric_name: str, db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)

    if metric_name == "random":
        # Выбираем только метрики с has_plot=True
        dict_keys = [key for key, meta in metrics.METRICS.items()
                     if meta.get("has_plot")]
        if not dict_keys:
            return {"error": "Нет доступных метрик для построения графиков."}

        selected_keys = random.sample(dict_keys, min(3, len(dict_keys)))

        results = []
        for key in selected_keys:
            func = metrics.METRICS[key]["func"]
            try:
                metric_result = metric_with_plot.get_metric_with_plot(
                    func, df, metric_name=key)
                results.append({
                    "metric": key,
                    "data": metric_result
                })
            except Exception as e:
                results.append({
                    "metric": key,
                    "error": str(e)
                })
        return results

    # Обычный режим — одна метрика
    meta = metrics.METRICS.get(metric_name)
    if not meta:
        return {"error": f"Метрика '{metric_name}' не найдена."}

    func = meta["func"]
    try:
        metric_result = metric_with_plot.get_metric_with_plot(
            func, df, metric_name)
        return [{
            "metric": metric_name,
            "data": metric_result
        }]
    except Exception as e:
        return [{
            "metric": metric_name,
            "error": str(e)
        }]


