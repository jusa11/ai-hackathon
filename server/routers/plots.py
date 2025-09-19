from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import analytics_service, metrics
from services.db_service import get_db
from charts import metric_with_plot


router = APIRouter()


@router.get("/{metric_name}")
def get_plot(metric_name: str, db: Session = Depends(get_db)):
    func = metrics.METRICS.get(metric_name)
    df = analytics_service.get_employees_df(db, limit=None)
    if not func:
        return {"error": f"Метрика '{metric_name}' не найдена."}
    return metric_with_plot.get_metric_with_plot(func, df)
