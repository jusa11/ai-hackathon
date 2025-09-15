import pandas as pd
from services import analytics_service


def handle_user_query(parsed: dict, df: pd.DataFrame) -> dict:
    if "error" in parsed:
        return parsed

    metric = parsed.get("metric")

    if metric == "average_experience":
        result = analytics_service.get_average_experiance(df)
    elif metric == "employee_count_by_region":
        result = analytics_service.get_employees_by_region(df)
    elif metric == "average_tenure":
        result = analytics_service.average_tenure_until_fire(df)
    else:
        result = f"Метрика '{metric}' не найдена."

    return {**parsed, "result": result}
