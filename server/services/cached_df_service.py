# services/cached_df_service.py
import time
from services import analytics_service

_cache = {"df": None, "timestamp": 0}


def get_full_df_cached(db, ttl: int = 60):
    """
    Возвращает DataFrame с данными сотрудников из кэша.
    Обновляет его раз в ttl секунд.
    """
    now = time.time()
    if _cache["df"] is None or (now - _cache["timestamp"]) > ttl:
        print("Refreshing employees DataFrame...")
        _cache["df"] = analytics_service.get_employees_df(db, limit=None)
        _cache["timestamp"] = now
    return _cache["df"]
