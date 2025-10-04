from typing import Dict, Any
import pandas as pd

def general_hr_summary_stub(df: pd.DataFrame, user_query: str) -> Dict[str, Any]:
    """
    Функция-заглушка, вызывается, когда LLM не смог построить метрику
    или результат пустой. Возвращает общий HR-анализ с текстом и структурой.
    """
    summary = {}
    comments = []

    # --- Средний опыт ---
    if "experience" in df.columns and not df.empty:
        avg_exp = round(df["experience"].mean(), 2)
        summary["average_experience"] = avg_exp
        comments.append(f"Средний опыт сотрудников: {avg_exp} лет.")

    # --- Средний возраст ---
    if "age" in df.columns and not df.empty:
        avg_age = round(df["age"].mean(), 1)
        summary["average_age"] = avg_age
        comments.append(f"Средний возраст сотрудников: {avg_age} лет.")

    # --- Средний FTE ---
    if "fte" in df.columns and not df.empty:
        avg_fte = round(df["fte"].mean(), 2)
        summary["average_fte"] = avg_fte
        comments.append(f"Средняя ставка FTE: {avg_fte}.")

    # --- Текучесть ---
    if "firecount" in df.columns and "hirecount" in df.columns and not df.empty:
        turnover = round(df["firecount"].sum() / max(1, df["hirecount"].sum()), 2)
        summary["turnover_rate"] = turnover
        comments.append(f"Примерная текучесть кадров: {turnover*100}%.")

    # --- Формируем текст как LLM ---
    if comments:
        result_text = " ".join(comments)
    else:
        result_text = "Нет данных для анализа."

    # --- Возвращаем структуру, совместимую с handle_user_query ---
    return {
        "result_text": result_text,
        "result": summary,
        "type_chart": "bar",  # фронт ждёт поле type_chart
        "has_plot": False     # графика нет
    }
