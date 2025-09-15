import pandas as pd
import crud

# --- функции аналитики ---


def get_employees_df(db):
    employees = crud.get_employees(db)
    if not employees:
        return pd.DataFrame()
    return pd.DataFrame([e.__dict__ for e in employees])


def get_average_experiance(df: pd.DataFrame) -> float:
    if "experience" not in df.columns:
        return 0.0
    return df["experience"].mean()


def get_employees_by_region(df: pd.DataFrame) -> dict:
    if "region" not in df.columns:
        return {"data": "This information is not available"}
    return df["region"].value_counts().to_dict()


def average_tenure_until_fire(df: pd.DataFrame) -> float:
    if "hire_to_company" not in df.columns or "fire_from_company" not in df.columns:
        return 0.0
    fired_df = df.dropna(subset=["fire_from_company", "hire_to_company"])
    if fired_df.empty:
        return 0.0
    tenure_days = (fired_df["fire_from_company"] -
                   fired_df["hire_to_company"]).dt.days
    return round(tenure_days.mean(), 2)


