import pandas as pd
from typing import Dict


def apply_filters_and_timeframe(df: pd.DataFrame, filters: dict, timeframe: dict) -> pd.DataFrame:
    df_filtered = df.copy()

    # --- фильтры по колонкам ---
    for col, value in filters.items():
        if col in df_filtered.columns:
            # Если колонка строковая, фильтруем без учёта регистра
            if df_filtered[col].dtype == object:
                df_filtered = df_filtered[df_filtered[col].str.lower() == str(
                    value).lower()]
            else:
                df_filtered = df_filtered[df_filtered[col] == value]

    # --- фильтры по периоду (timeframe) ---
    if "month" in timeframe:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month ==
                                  timeframe["month"]]
    elif "months" in timeframe:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin(
            timeframe["months"])]
    elif "start" in timeframe and "end" in timeframe:
        df_filtered = df_filtered[(df_filtered["report_date"] >= timeframe["start"]) &
                                  (df_filtered["report_date"] <= timeframe["end"])]

    return df_filtered
