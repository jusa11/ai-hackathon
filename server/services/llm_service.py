import os
from gigachat import GigaChat
from dotenv import load_dotenv
from services.metrics import METRICS

load_dotenv()
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")

giga = GigaChat(credentials=GIGACHAT_CLIENT_SECRET, verify_ssl_certs=False)

# Создаём список метрик с описанием и alias для LLM
available_metrics = []
for k, v in METRICS.items():
    aliases = v.get("aliases", [])
    desc = v.get("description", "")
    if k == "average-experience":
        # Отдельно подчёркиваем, что метрика умеет группироваться
        desc += " Поддерживает группировки по age_category, sex, service, department_*."
    available_metrics.append(
        {"key": k, "description": desc, "aliases": aliases})


def askGiga(user_query: str) -> str:
    """
    Определяет, какую метрику использовать, и возвращает строго JSON с ключом 'metric' и 'filters'.
    LLM не делает вычислений — только выбирает метрику.
    """
    # Формируем понятный prompt
    prompt = f"""
Ты помощник аналитика HR. 
Твоя задача — только выбрать метрику и сформировать JSON по строго фиксированным правилам.
Важно:
- Некоторые метрики умеют группироваться. Например, "average-experience" может быть сгруппирована по:
  age_category, sex, service, department_3-6
- Никогда не придумывай новые ключи вроде "average-experience-by-age-category".
- Всегда используй существующие ключи из списка.

Доступные метрики (ключ + описание + alias):
{available_metrics}

Формат ответа ВСЕГДА:
{{
  "metric": "ключ_метрики", 
  "filters": {{ "service": "...", "sex": "M" }},
  "group_by": ["age_category", "sex"],
  "timeframe": {{"month": 7}} 
}}

Правила:
1. "metric" — один из ключей или alias из списка выше. Важно никогда не придумывай свой!!!!
2. В "filters" НИКОГДА не добавляй поля про время (month, months, start, end). Используй только:
   ["service","sex","region","work_form",
    "department_3","department_4","department_5","department_6",
    "age_category","experience_category"]. 
3. "group_by" — массив, где элементы ТОЛЬКО из тех же полей.
4. "timeframe":
   - Если указан конкретный месяц, возвращай {{"month": N}} где N ∈ [7,8,9].
   - Если указан диапазон месяцев, возвращай {{"months":[7,8,9]}}.
   - Если указан диапазон дат, возвращай {{"start":"2025-07-01","end":"2025-09-30"}}.
   - Если про время ничего не сказано — верни пустой объект: {{}}
5. Никогда не делай вычислений и не пиши числа в "result".
6. Ответ ВСЕГДА только JSON, без комментариев и текста.
7. Если метрика не распознаётся — укажи "metric": null.

Вопрос пользователя: "{user_query}"
"""

    response = giga.chat(prompt)
    return response.choices[0].message.content
