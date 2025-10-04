from collections import defaultdict

from modules.analytics.analytics_service import (
    get_turnover,
    get_fte_mean,
    get_average_experience,
    get_hires_to_cover_turnover,
    get_at_risk_departments,
    get_most_stable_departments
)


def recommend_turnover(df):
    """
    Рекомендации по текучести.
    """
    recs = []
    turnover = get_turnover(df)
    for dept, value in turnover.items():
        if value > 20:
            recs.append({
                "level": "warning",
                "message": f"В департаменте {dept} высокая текучесть: {value}%"
            })
    return recs


def recommend_fte(df):
    """
    Рекомендации по нагрузке.
    """
    recs = []
    fte = get_fte_mean(df)
    for dept, value in fte.items():
        if value > 1.2:
            recs.append({
                "level": "critical",
                "message": f"Перегрузка сотрудников в {dept}: средний FTE = {value}"
            })
        elif value < 0.7:
            recs.append({
                "level": "info",
                "message": f"В {dept} низкая загрузка (FTE={value}), можно перераспределить ресурсы"
            })
    return recs


def recommend_experience(df):
    """
    Рекомендации по стажу.
    """
    recs = []
    avg_exp = get_average_experience(df)
    for dept, value in avg_exp.items():
        if value < 1.5:
            recs.append({
                "level": "warning",
                "message": f"В {dept} низкий средний стаж ({value} лет). "
                "Высокий риск ухода новичков → стоит усилить адаптацию."
            })
    return recs


def recommend_hiring_plan(df):
    """
    Сколько нужно нанимать, чтобы покрыть отток.
    """
    recs = []
    hires_needed = get_hires_to_cover_turnover(df)
    if "all" in hires_needed:
        recs.append({
            "level": "info",
            "message": f"Чтобы компенсировать текучесть, нужно нанимать "
            f"{hires_needed['all']} сотрудников ежемесячно."
        })
    return recs


def recommend_risk_and_stability(df):
    """
    Автоматическое выявление зон риска и стабильных отделов.
    """
    recs = []
    at_risk = get_at_risk_departments(df)
    stable = get_most_stable_departments(df)

    for dept in at_risk.keys():
        recs.append({
            "level": "critical",
            "message": f"{dept} в зоне риска: высокая текучесть  + низкий FTE + низкий стаж."
        })

    for dept in stable.keys():
        recs.append({
            "level": "success",
            "message": f"{dept} стабилен: низкая текучесть и высокий стаж сотрудников."
        })
    return recs


def run_recommendations(df, per_level: int = 5):
    """
    Собирает все рекомендации и ограничивает количество в каждой категории уровня.
    """
    recs = []
    recs.extend(recommend_turnover(df))
    recs.extend(recommend_fte(df))
    recs.extend(recommend_experience(df))
    recs.extend(recommend_hiring_plan(df))
    recs.extend(recommend_risk_and_stability(df))

    grouped = defaultdict(list)
    for rec in recs:
        grouped[rec["level"]].append(rec)

    limited = []
    for level in ["critical", "warning", "info", "success"]:
        limited.extend(grouped[level][:per_level])

    return limited
