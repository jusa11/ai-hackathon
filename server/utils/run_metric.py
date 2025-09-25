from typing import Callable, List, Dict, Any
import pandas as pd
from utils.apply_filters_and_timeframe import apply_filters_and_timeframe


def safe_serialize_result(result):
    """Сериализация результата для JSON: ключи строки, числа float."""
    if isinstance(result, dict):
        new_result = {}
        for k, v in result.items():
            new_k = "-".join(map(str, k)) if isinstance(k,
                                                        (tuple, list)) else str(k)
            new_result[new_k] = safe_serialize_result(v)
        return new_result
    elif isinstance(result, list):
        return [safe_serialize_result(i) for i in result]
    elif isinstance(result, (float, int)):
        return float(result)
    elif hasattr(result, "item"):  # np.float64
        return float(result.item())
    else:
        return result


def run_metric(
    func: Callable,
    df: pd.DataFrame,
    filters: Dict = {},
    timeframe: Dict = {},
    group_by: List[str] = [],
    type_chart: str = "bar"
) -> Dict[str, Any]:
    """Запуск метрики с фильтрами, группировкой и периодом."""

    print(func, filters, group_by, timeframe)

    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)
    if df_filtered.empty:
        return {"result": {}, "type_chart": type_chart, "has_plot": False}

    if group_by:
        result = {}
        grouped = df_filtered.groupby(group_by)
        for group_keys, group_df in grouped:
            key = "-".join(map(str, group_keys)
                           ) if isinstance(group_keys, tuple) else str(group_keys)
            try:
                value = func(group_df)
            except Exception:
                value = None
            result[key] = value
    else:
        try:
            result = func(df_filtered)
        except Exception:
            result = None

    result = safe_serialize_result(result)
    has_plot = True if result else False

    print(f"run_metric: {result}")

    return {"result": result, "type_chart": type_chart, "has_plot": has_plot}
