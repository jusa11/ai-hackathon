import pandas as pd
import random
import crud
from utils.apply_filters_and_timeframe import apply_filters_and_timeframe


# --- функции аналитики ---


def get_employees_df(db, limit: int | None = 100):
    employees = crud.get_employees(db, skip=0, limit=limit)
    if not employees:
        return pd.DataFrame()
    return pd.DataFrame([e.__dict__ for e in employees])


# Средний опыт
def get_average_experience(df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}) -> dict:
    """
    Средний опыт сотрудников с учётом фильтров и периода.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}

    Возвращает словарь {group_key: avg_experience} для группировки через run_metric
    или {"all": avg_experience} для общего среднего.
    """
    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)

    if "experience" not in df_filtered.columns or df_filtered.empty:
        return {}

    # Если run_metric будет передавать group_by, то словарь создастся там.
    avg_exp = df_filtered["experience"].mean()

    # Возвращаем словарь для унификации (ключ "all" для несгруппированных случаев)
    return {"all": round(avg_exp, 2)}


# Средний возраст сотрудников


def get_average_fullyears(df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}) -> dict:
    """
    Средний полный стаж (в годах) сотрудников с учётом фильтров и периода.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}

    Возвращает словарь {group_key: avg_fullyears} для группировки через run_metric
    или {"all": avg_fullyears} для общего среднего.
    """
    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)

    if "fullyears" not in df_filtered.columns or df_filtered.empty:
        return {}

    avg_fullyears = df_filtered["fullyears"].mean()

    # Всегда возвращаем словарь для унификации
    return {"all": round(avg_fullyears, 2)}


# Количество сотрудников по полу


def get_count_by_sex(df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}) -> dict:
    """
    Количество сотрудников по полу с учётом фильтров и периода.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}

    Возвращает словарь {"M": count_male, "F": count_female}
    или сгруппированные данные через run_metric.
    """
    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)

    if "sex" not in df_filtered.columns or df_filtered.empty:
        return {"M": 0, "F": 0}

    counts = df_filtered["sex"].str.upper().value_counts()

    return {
        "M": int(counts.get("M", 0)),
        "F": int(counts.get("F", 0))
    }


def get_employees_by_region(df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}) -> dict:
    """
    Возвращает количество сотрудников по регионам.
    """
    if "region" not in df.columns:
        return {"data": "This information is not available"}

    df = apply_filters_and_timeframe(df, filters, timeframe)
    return df["region"].value_counts().to_dict()


def get_average_tenure_until_fire(
    df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}, unit: str = "months"
) -> float:
    """
    Средний срок работы до увольнения.

    unit: "days" | "months" | "years"
    """
    if "hire_to_company" not in df.columns or "fire_from_company" not in df.columns:
        return 0.0

    df = apply_filters_and_timeframe(df, filters, timeframe)

    fired_df = df.dropna(subset=["fire_from_company", "hire_to_company"])
    if fired_df.empty:
        return 0.0

    tenure_days = (fired_df["fire_from_company"] -
                   fired_df["hire_to_company"]).dt.days
    tenure_days = tenure_days[tenure_days >= 0]

    if tenure_days.empty:
        return 0.0

    if unit == "months":
        return round((tenure_days.mean() / 30), 0)
    elif unit == "years":
        return round((tenure_days.mean() / 365), 0)
    return round(tenure_days.mean(), 0)


def get_average_fte(
    df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}, group_by: list[str] | None = None
) -> dict:
    """
    Считает средний FTE сотрудников.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "service"])

    Возвращает:
      {"all": avg_fte} если group_by не указан
      {"group_key": avg_fte, ...} если group_by передан
    """
    df = apply_filters_and_timeframe(df, filters, timeframe)

    if "fte" not in df.columns or df.empty:
        return {}

    if group_by:
        return df.groupby(group_by)["fte"].mean().round(2).to_dict()

    return {"all": round(df["fte"].mean(), 2)}


def get_fired_count(
    df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}, group_by: list[str] | None = None
) -> dict | int:
    """
    Считает количество увольнений (firecount.sum()).

    filters: {"department_3": "Department-98", "sex": "M"}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["sex","department_3"])

    Возвращает:
      int — общее количество увольнений, если group_by не указан
      dict — {group_key: count, ...}, если group_by передан
    """
    if "firecount" not in df.columns or "report_date" not in df.columns:
        return 0

    df = apply_filters_and_timeframe(df, filters, timeframe)

    if df.empty:
        return 0 if not group_by else {}

    if group_by:
        return df.groupby(group_by)["firecount"].sum().astype(int).to_dict()

    return int(df["firecount"].sum())


def get_hire_count(
    df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}, group_by: list[str] | None = None
) -> dict | int:
    """
    Считает количество найма (hirecount.sum()).

    filters: {"department_3": "Department-98", "sex": "M"}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["sex","department_3"])

    Возвращает:
      int — общее количество найма, если group_by не указан
      dict — {group_key: count, ...}, если group_by передан
    """
    if "hirecount" not in df.columns or "report_date" not in df.columns:
        return 0

    df = apply_filters_and_timeframe(df, filters, timeframe)

    if df.empty:
        return 0 if not group_by else {}

    if group_by:
        return df.groupby(group_by)["hirecount"].sum().astype(int).to_dict()

    return int(df["hirecount"].sum())


def get_count_by_work_form(
    df: pd.DataFrame, filters: dict = {}, timeframe: dict = {}, group_by: list[str] | None = None
) -> dict:
    """
    Считает количество сотрудников по форме работы (0=Очно, 1=Удаленщик) с учётом фильтров, времени и группировки.

    filters: {"department_3": "Department-98", "sex": "M", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD","end":"YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["sex","department_3"])

    Возвращает словарь {group_key: count, ...} или {form: count} для несгруппированных случаев.
    """
    if "work_form" not in df.columns:
        return {}

    df = apply_filters_and_timeframe(df, filters, timeframe)
    if df.empty:
        return {}

    mapping = {0: "Очно", 1: "Удаленщик"}
    df["work_form_mapped"] = df["work_form"].map(mapping)

    if group_by:
        return df.groupby(group_by + ["work_form_mapped"]).size().to_dict()

    return df["work_form_mapped"].value_counts().to_dict()


def get_fte_sum(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {},
    group_by: list[str] | None = None
) -> dict:
    """
    Сумма ставок FTE сотрудников с учётом фильтров, временного периода и группировки.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD","end":"YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "service"])

    Возвращает:
      {"all": sum_fte} если group_by не указан
      {"group_key": sum_fte, ...} если group_by передан
    """
    df = apply_filters_and_timeframe(df, filters, timeframe)

    if "fte" not in df.columns or df.empty:
        return {}

    if group_by:
        return df.groupby(group_by)["fte"].sum().round(2).to_dict()

    return {"all": round(df["fte"].sum(), 2)}


def get_fte_mean(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {},
    group_by: list[str] | None = None
) -> dict:
    """
    Среднее значение ставок FTE с учётом фильтров, временного периода и группировки.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD","end":"YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "service"])

    Возвращает:
      {"all": mean_fte} если group_by не указан
      {"group_key": mean_fte, ...} если group_by передан
    """
    df = apply_filters_and_timeframe(df, filters, timeframe)

    if "fte" not in df.columns or df.empty:
        return {}

    if group_by:
        return df.groupby(group_by)["fte"].mean().round(2).to_dict()

    return {"all": round(df["fte"].mean(), 2)}


def get_turnover(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {},
    group_by: list[str] | None = None
) -> dict:
    """
    Текучесть кадров (%), с учётом фильтров, временного периода и группировки.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8} или {"months": [7,8,9]} или {"start": "YYYY-MM-DD","end":"YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "service"])

    Возвращает:
      {"all": turnover_rate} если group_by не указан
      {"group_key": turnover_rate, ...} если group_by передан
    """
    if "firecount" not in df.columns or "report_date" not in df.columns:
        return {}

    df = apply_filters_and_timeframe(df, filters, timeframe)

    if df.empty:
        return {}

    def _calc_turnover(sub_df: pd.DataFrame) -> float:
        total_fired = sub_df["firecount"].sum()
        avg_employees = sub_df.groupby(
            sub_df["report_date"].dt.to_period("M")
        ).size().mean()

        if avg_employees == 0:
            return 0.0

        return round((total_fired / avg_employees) * 100, 2)

    if group_by:
        return {key: _calc_turnover(g) for key, g in df.groupby(group_by)}

    return {"all": _calc_turnover(df)}


def get_hires_and_fires_share(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {},
    group_by: list[str] | None = None
) -> dict:
    """
    Доля новых наймов и увольнений (% от средней численности сотрудников) 
    с учётом фильтров, периода и группировки.

    filters: {"department_3": "Department-98", "service": "Крауд", ...}
    timeframe: {"month": 8}, {"months": [7,8,9]}, {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "service"])

    Возвращает:
      {"hire_rate": x, "fire_rate": y} если group_by не указан
      {"group_key": {"hire_rate": x, "fire_rate": y}, ...} если group_by указан
    """
    required_cols = {"hirecount", "firecount", "report_date"}
    if not required_cols.issubset(df.columns):
        return {}

    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)

    if df_filtered.empty:
        return {}

    def _calc_rates(sub_df: pd.DataFrame) -> dict:
        total_hired = sub_df["hirecount"].sum()
        total_fired = sub_df["firecount"].sum()
        avg_employees = sub_df.groupby(
            sub_df["report_date"].dt.to_period("M")
        ).size().mean()

        if avg_employees == 0:
            return {"hire_rate": 0.0, "fire_rate": 0.0}

        hire_rate = round((total_hired / avg_employees) * 100, 2)
        fire_rate = round((total_fired / avg_employees) * 100, 2)
        return {"hire_rate": hire_rate, "fire_rate": fire_rate}

    if group_by:
        result = {}
        for keys, group in df_filtered.groupby(group_by):
            result[keys if isinstance(keys, str) else tuple(
                keys)] = _calc_rates(group)
        return result

    return _calc_rates(df_filtered)


def get_work_form_distribution(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {},
    group_by: list[str] | None = None
) -> dict:
    """
    Доля сотрудников по формам работы: удалёнка (1) vs офис (0).
    Можно фильтровать и группировать по любым колонкам.

    filters: {"department_3": "Department-98", "sex": "F", ...}
    timeframe: {"month": 8}, {"months": [7,8,9]}, {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "service"])

    Возвращает:
      {"remote": x, "office": y} если group_by не указан
      {"group_key": {"remote": x, "office": y}, ...} если group_by указан
    """
    if "work_form" not in df.columns or "report_date" not in df.columns:
        return {}

    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)
    if df_filtered.empty:
        return {"remote": 0.0, "office": 0.0}

    def _calc_distribution(sub_df: pd.DataFrame) -> dict:
        total = len(sub_df)
        if total == 0:
            return {"remote": 0.0, "office": 0.0}
        remote_count = (sub_df["work_form"] == 1).sum()
        office_count = (sub_df["work_form"] == 0).sum()
        return {
            "remote": round((remote_count / total) * 100, 2),
            "office": round((office_count / total) * 100, 2),
        }

    if group_by:
        result = {}
        for keys, group in df_filtered.groupby(group_by):
            result[keys if isinstance(keys, str) else tuple(
                keys)] = _calc_distribution(group)
        return result

    return _calc_distribution(df_filtered)


def get_employee_count(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {},
    group_by: list[str] | None = None,
    target_col: str = "service"
) -> dict:
    """
    Количество сотрудников по target_col (по умолчанию — service).

    filters: {"department_3": "Department-98", "sex": "F", ...}
    timeframe: {"month": 8}, {"months": [7,8,9]}, {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    group_by: список колонок для группировки (например ["department_3", "sex"])
    target_col: колонка, по которой считаем количество (по умолчанию "service")

    Возвращает:
      {"value": count, ...} если group_by не указан
      {"group_key": {"value": count, ...}, ...} если group_by указан
    """
    if target_col not in df.columns or "report_date" not in df.columns:
        return {}

    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)
    if df_filtered.empty:
        return {}

    def _count(sub_df: pd.DataFrame) -> dict:
        return sub_df[target_col].value_counts().to_dict()

    if group_by:
        result = {}
        for keys, group in df_filtered.groupby(group_by):
            result[keys if isinstance(
                keys, str) else tuple(keys)] = _count(group)
        return result

    return _count(df_filtered)

def get_total_employees(
    df: pd.DataFrame,
    filters: dict = {},
    timeframe: dict = {}
) -> int:
    """
    Общее количество сотрудников в компании с учётом фильтров и временного периода.

    filters: {"department_3": "Department-98", "sex": "F", ...}
    timeframe: {"month": 8}, {"months": [7,8,9]}, {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}

    Возвращает:
      int — количество сотрудников
    """
    if "report_date" not in df.columns:
        return 0

    df_filtered = apply_filters_and_timeframe(df, filters, timeframe)
    if df_filtered.empty:
        return 0

    return len(df_filtered)
