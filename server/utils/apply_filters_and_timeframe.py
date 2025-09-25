import pandas as pd
from typing import Dict


def apply_filters_and_timeframe(df: pd.DataFrame, filters: dict, timeframe: dict) -> pd.DataFrame:
    df_filtered = df.copy()

    filters = filters or {}
    timeframe = timeframe or {}

    # --- report_date в datetime ---
    if not pd.api.types.is_datetime64_any_dtype(df_filtered["report_date"]):
        df_filtered["report_date"] = pd.to_datetime(df_filtered["report_date"])

    # --- Фильтры по колонкам ---
    for key, value in filters.items():
        if key in df_filtered.columns and value is not None:
            df_filtered = df_filtered[df_filtered[key] == value]

    # --- Фильтр по времени ---
    if "month" in timeframe and timeframe["month"] is not None:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month ==
                                  timeframe["month"]]
    elif "months" in timeframe and timeframe["months"]:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin(
            timeframe["months"])]
    elif "start" in timeframe or "end" in timeframe:
        start = pd.to_datetime(timeframe.get(
            "start", df_filtered["report_date"].min()))
        end = pd.to_datetime(timeframe.get(
            "end", df_filtered["report_date"].max()))
        df_filtered = df_filtered[(df_filtered["report_date"] >= start) & (
            df_filtered["report_date"] <= end)]

    return df_filtered
