import pandas as pd
import random
import crud

# --- функции аналитики ---


def get_employees_df(db, limit: int | None = 100):
    employees = crud.get_employees(db, skip=0, limit=limit)
    if not employees:
        return pd.DataFrame()
    return pd.DataFrame([e.__dict__ for e in employees])


# Средний опыт
def get_average_experience(df: pd.DataFrame) -> float:
    if "experience" not in df.columns:
        return 0.0
    return df["experience"].mean()

# Средний возраст сотрудников


def get_average_fullyears(df: pd.DataFrame) -> float:
    if "fullyears" not in df.columns:
        return 0.0
    return df["fullyears"].mean()

# Количество сотрудников по полу


def get_count_by_sex(df: pd.DataFrame) -> dict:
    """
    Возвращает количество сотрудников по полу в формате {'M': ..., 'F': ...}.
    """
    if "sex" not in df.columns:
        return {"M": 0, "F": 0}

    counts = df["sex"].str.upper().value_counts()
    return {
        "M": int(counts.get("M", 0)),
        "F": int(counts.get("F", 0))
    }


def get_count_by_department_level(df: pd.DataFrame, level: str | None = None) -> dict:
    """
    Считает количество сотрудников по каждому уникальному значению выбранного уровня департамента.
    Если level не передан, выбирается случайный из доступных: department_3..6.
    """
    available_levels = ["department_3",
                        "department_4", "department_5", "department_6"]

    # Если level не передан или некорректный — выбираем случайный
    if not level or level not in available_levels:
        level = random.choice(
            [col for col in available_levels if col in df.columns])

    if level not in df.columns:
        return {}

    return df[level].value_counts().to_dict()


def get_employees_by_region(df: pd.DataFrame) -> dict:
    if "region" not in df.columns:
        return {"data": "This information is not available"}
    return df["region"].value_counts().to_dict()


def get_average_tenure_until_fire(df: pd.DataFrame, unit: str = "months") -> float:
    """
    Средний срок работы до увольнения.

    unit: "days" | "months" | "years"
    """
    if "hire_to_company" not in df.columns or "fire_from_company" not in df.columns:
        return 0.0

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


def get_average_experience_by_department(
    df: pd.DataFrame,
    level: str | None = None
) -> dict:
    """
    Считает средний опыт по выбранному уровню департамента.
    Если level не передан — считает по всем уровням сразу.
    """
    if "experience" not in df.columns:
        return {}

    if level is None:
        # Берём все department_3..6, если они есть
        results = {}
        for col in ["department_3", "department_4", "department_5", "department_6"]:
            if col in df.columns:
                results[col] = df.groupby(
                    col)["experience"].mean().round(2).to_dict()
        return results

    if level not in df.columns:
        return {}

    return df.groupby(level)["experience"].mean().round(2).to_dict()


def get_average_fte_by_department(df: pd.DataFrame, level: str = None) -> dict:
    """
    Считает средний FTE по выбранному уровню департамента.
    Если level не передан — выбирает случайный уровень.
    """
    possible_levels = ["department_3", "department_4",
                       "department_5", "department_6"]

    # Если level не передан или некорректный — берём случайный
    if level not in possible_levels:
        level = random.choice(possible_levels)

    if "fte" not in df.columns or level not in df.columns:
        return {}
    print("Используемый level:", level)
    print(df[level].unique())

    return df.groupby(level)["fte"].mean().round(2).to_dict()


def get_average_experience_by_region(df: pd.DataFrame) -> dict:
    """
    Считает средний experience по регионам.
    """
    if "experience" not in df.columns or "region" not in df.columns:
        return {}

    return df.groupby("region")["experience"].mean().round(2).to_dict()


def get_fired_count(df: pd.DataFrame, month: int | None = None) -> int:
    """
    Считает общее количество увольнений (firecount.sum()).
    Если month указан, берём только записи за этот месяц.
    """
    if "firecount" not in df.columns or "report_date" not in df.columns:
        return 0

    if month:
        df = df[df["report_date"].dt.month == month]

    return int(df["firecount"].sum())


def get_hire_count(df: pd.DataFrame, month: int | None = None) -> int:
    """
    Считает общее количество найма (hirecount.sum()).
    Если month указан, берём только записи за этот месяц.
    """
    if "hirecount" not in df.columns or "report_date" not in df.columns:
        return 0

    if month:
        df = df[df["report_date"].dt.month == month]

    return int(df["hirecount"].sum())


def get_count_by_work_form(df: pd.DataFrame) -> dict:
    """
    Количество сотрудников по work_form.
    0 = Onsite, 1 = Remote
    """
    if "work_form" not in df.columns:
        return {"error": "Column 'work_form' not found"}

    mapping = {0: "Очно", 1: "Удаленщик"}
    return df["work_form"].map(mapping).value_counts().to_dict()


def get_fte_sum(df: pd.DataFrame) -> float:
    """
    Сумма ставок FTE.
    """
    if "fte" not in df.columns:
        return 0.0
    return round(df["fte"].sum(), 2)


def get_fte_mean(df: pd.DataFrame) -> float:
    """
    Средний FTE.
    """
    if "fte" not in df.columns:
        return 0.0
    return round(df["fte"].mean(), 2)


def get_turnover_rate_by_month(df: pd.DataFrame, months: list[int] | None = None) -> float:
    """
    Текучесть кадров за выбранные месяцы (без учёта года).

    months: список чисел месяцев, например [7, 8, 9] для июля-сентября.
            Если None — берём все месяцы.
    """
    if "firecount" not in df.columns or "report_date" not in df.columns:
        return 0.0

    df_filtered = df.copy()

    if months:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin(
            months)]

    if df_filtered.empty:
        return 0.0

    total_fired = df_filtered["firecount"].sum()

    avg_employees = df_filtered.groupby(
        df_filtered["report_date"].dt.to_period("M")).size().mean()

    if avg_employees == 0:
        return 0.0

    return round((total_fired / avg_employees) * 100, 2)


def get_turnover_rate_by_department(
    df: pd.DataFrame,
    department: str,
    month: int | None = None
) -> dict:
    """
    Текучесть по всем департаментам указанного уровня (department_3..6).
    Если month не указан — считаем за июль-сентябрь.
    """
    required_cols = ["firecount", "report_date", "department_3",
                     "department_4", "department_5", "department_6"]
    if not all(col in df.columns for col in required_cols):
        return {}

    if department not in ["department_3", "department_4", "department_5", "department_6"]:
        return {}

    df_filtered = df.copy()

    # фильтр по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = {}
    for dep_name, group in df_filtered.groupby(department):
        total_fired = group["firecount"].sum()
        avg_employees = group.groupby(group["report_date"].dt.to_period("M")).size().mean()

        if avg_employees > 0:
            result[dep_name] = round((total_fired / avg_employees) * 100, 2)
        else:
            result[dep_name] = 0.0

    return result


def get_hires_and_fires_share_by_department(
    df: pd.DataFrame,
    department_3: str | None = None,
    department_4: str | None = None,
    department_5: str | None = None,
    department_6: str | None = None,
    month: int | None = None
) -> dict:
    """
    Доля новых наймов и увольнений по выбранной иерархии департаментов и месяцу.
    Если month не указан — по умолчанию берём июль, август, сентябрь.
    """
    required_cols = ["hirecount", "firecount", "report_date",
                     "department_3", "department_4", "department_5", "department_6"]
    if not all(col in df.columns for col in required_cols):
        return {"hire_rate": 0.0, "fire_rate": 0.0}

    df_filtered = df.copy()

    # Фильтруем по департаментам
    if department_3:
        df_filtered = df_filtered[df_filtered["department_3"] == department_3]
    if department_4:
        df_filtered = df_filtered[df_filtered["department_4"] == department_4]
    if department_5:
        df_filtered = df_filtered[df_filtered["department_5"] == department_5]
    if department_6:
        df_filtered = df_filtered[df_filtered["department_6"] == department_6]

    # Фильтруем по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {"hire_rate": 0.0, "fire_rate": 0.0}

    total_hired = df_filtered["hirecount"].sum()
    total_fired = df_filtered["firecount"].sum()

    avg_employees = df_filtered.groupby(
        df_filtered["report_date"].dt.to_period("M")).size().mean()
    if avg_employees == 0:
        return {"hire_rate": 0.0, "fire_rate": 0.0}

    hire_rate = round((total_hired / avg_employees) * 100, 2)
    fire_rate = round((total_fired / avg_employees) * 100, 2)

    return {"hire_rate": hire_rate, "fire_rate": fire_rate}


def get_turnover_rate_all_regions(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Текучесть по всем регионам.
    Возвращает словарь: {region: turnover_rate}.
    Если month указан — только за этот месяц.
    Иначе — по умолчанию за июль, август, сентябрь.
    """
    required_cols = ["firecount", "report_date", "region"]
    if not all(col in df.columns for col in required_cols):
        return {}

    df_filtered = df.copy()

    # Фильтруем по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = {}
    for region, group in df_filtered.groupby("region"):
        total_fired = group["firecount"].sum()
        avg_employees = group.groupby(
            group["report_date"].dt.to_period("M")).size().mean()
        turnover = round((total_fired / avg_employees) *
                         100, 2) if avg_employees else 0.0
        result[region] = turnover

    return result


def get_work_form_distribution(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Доля сотрудников по формам работы: удалённая vs офис.
    Если month указан — фильтруем только по этому месяцу.
    Иначе — по умолчанию за июль-сентябрь.
    """
    if "work_form" not in df.columns or "report_date" not in df.columns:
        return {}

    df_filtered = df.copy()

    # Фильтр по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {"remote": 0.0, "office": 0.0}

    total = len(df_filtered)
    remote_count = df_filtered[df_filtered["work_form"] == 1].shape[0]
    office_count = df_filtered[df_filtered["work_form"] == 0].shape[0]

    remote_pct = round((remote_count / total) * 100, 2)
    office_pct = round((office_count / total) * 100, 2)

    return {"remote": remote_pct, "office": office_pct}


def get_average_fte_by_work_form(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Средняя ставка FTE по формам работы: удалённая vs офис.
    Если month указан — фильтруем только по этому месяцу.
    Иначе — по умолчанию за июль-сентябрь.
    """
    if "work_form" not in df.columns or "fte" not in df.columns or "report_date" not in df.columns:
        return {"remote": 0.0, "office": 0.0}

    df_filtered = df.copy()

    # Фильтр по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {"remote": 0.0, "office": 0.0}

    # Средний FTE по удалённым
    remote_df = df_filtered[df_filtered["work_form"] == 1]
    office_df = df_filtered[df_filtered["work_form"] == 0]

    remote_avg = round(remote_df["fte"].mean(),
                       2) if not remote_df.empty else 0.0
    office_avg = round(office_df["fte"].mean(),
                       2) if not office_df.empty else 0.0

    return {"remote": remote_avg, "office": office_avg}


def get_turnover_rate_by_age_category(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Текучесть по возрастным категориям.
    month: если указан — только за этот месяц, иначе — июль-сентябрь.
    """
    required_cols = ["firecount", "report_date", "age_category"]
    if not all(col in df.columns for col in required_cols):
        return {}

    df_filtered = df.copy()

    # Фильтр по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = {}
    for age_cat, group in df_filtered.groupby("age_category"):
        total_fired = group["firecount"].sum()
        avg_employees = group.groupby(
            group["report_date"].dt.to_period("M")).size().mean()
        turnover = round((total_fired / avg_employees) *
                         100, 2) if avg_employees else 0.0
        result[age_cat] = turnover

    return result


def get_turnover_rate_by_experience_category(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Текучесть по категориям опыта.
    month: если указан — только за этот месяц, иначе — июль-сентябрь.
    """
    required_cols = ["firecount", "report_date", "experience_category"]
    if not all(col in df.columns for col in required_cols):
        return {}

    df_filtered = df.copy()

    # Фильтр по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = {}
    for exp_cat, group in df_filtered.groupby("experience_category"):
        total_fired = group["firecount"].sum()
        avg_employees = group.groupby(
            group["report_date"].dt.to_period("M")).size().mean()
        turnover = round((total_fired / avg_employees) *
                         100, 2) if avg_employees else 0.0
        result[exp_cat] = turnover

    return result


def get_average_experience_by_group(
    df: pd.DataFrame,
    service: str | None = None,
    department_3: str | None = None,
    department_4: str | None = None,
    department_5: str | None = None,
    department_6: str | None = None
) -> float:
    """
    Средний стаж (experience) по сервису или отделу.
    Если передан service — фильтруем по нему.
    Если переданы уровни департамента — фильтруем по ним.
    """
    if "experience" not in df.columns:
        return 0.0

    df_filtered = df.copy()

    if service:
        df_filtered = df_filtered[df_filtered["service"] == service]

    if department_3:
        df_filtered = df_filtered[df_filtered["department_3"] == department_3]
    if department_4:
        df_filtered = df_filtered[df_filtered["department_4"] == department_4]
    if department_5:
        df_filtered = df_filtered[df_filtered["department_5"] == department_5]
    if department_6:
        df_filtered = df_filtered[df_filtered["department_6"] == department_6]

    if df_filtered.empty:
        return 0.0

    return round(df_filtered["experience"].mean(), 2)


def get_turnover_rate_by_service(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Текучесть по сервисам.
    month: если указан — только за этот месяц, иначе — июль-сентябрь.
    """
    required_cols = ["firecount", "report_date", "service"]
    if not all(col in df.columns for col in required_cols):
        return {}

    df_filtered = df.copy()

    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = {}
    for service_name, group in df_filtered.groupby("service"):
        total_fired = group["firecount"].sum()
        avg_employees = group.groupby(
            group["report_date"].dt.to_period("M")).size().mean()
        turnover = round((total_fired / avg_employees) *
                         100, 2) if avg_employees else 0.0
        result[service_name] = turnover

    return result


def get_turnover_rate_by_work_form(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Текучесть по форме работы (0 = офис, 1 = удалёнка)
    month: если указан — только за этот месяц, иначе — июль-сентябрь.
    """
    required_cols = ["firecount", "report_date", "work_form"]
    if not all(col in df.columns for col in required_cols):
        return {}

    df_filtered = df.copy()

    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = {}
    for form, group in df_filtered.groupby("work_form"):
        total_fired = group["firecount"].sum()
        avg_employees = group.groupby(
            group["report_date"].dt.to_period("M")).size().mean()
        turnover = round((total_fired / avg_employees) *
                         100, 2) if avg_employees else 0.0
        label = "remote" if form == 1 else "office"
        result[label] = turnover

    return result


def get_fired_count_by_region(df: pd.DataFrame, month: int | None = None) -> dict:
    """
    Количество увольнений по регионам.
    month: если указан — только за этот месяц, иначе — июль-сентябрь.
    """
    required_cols = ["firecount", "report_date", "region"]
    if not all(col in df.columns for col in required_cols):
        return {}

    df_filtered = df.copy()

    # Фильтр по месяцу
    if month:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month == month]
    else:
        df_filtered = df_filtered[df_filtered["report_date"].dt.month.isin([
                                                                           7, 8, 9])]

    if df_filtered.empty:
        return {}

    result = df_filtered.groupby("region")["firecount"].sum().to_dict()
    return result


def get_employee_count_by_service(df: pd.DataFrame) -> dict:
    """
    Количество сотрудников по сервисам.
    """
    if "service" not in df.columns:
        return {}

    result = df["service"].value_counts().to_dict()
    return result


def get_average_fte_by_service(df: pd.DataFrame) -> dict:
    """
    Средний FTE по сервисам.
    """
    if "service" not in df.columns or "fte" not in df.columns:
        return {}

    result = df.groupby("service")["fte"].mean().round(2).to_dict()
    return result


def get_average_experience_by_region(df: pd.DataFrame) -> dict:
    """
    Средний стаж по регионам.
    """
    if "region" not in df.columns or "experience" not in df.columns:
        return {}

    result = df.groupby("region")["experience"].mean().round(2).to_dict()
    return result
