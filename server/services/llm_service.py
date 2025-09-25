import os
from gigachat import GigaChat
from dotenv import load_dotenv
from services.metrics import METRICS

load_dotenv()
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")

giga = GigaChat(credentials=GIGACHAT_CLIENT_SECRET, verify_ssl_certs=False)


def askGiga(user_query: str) -> str:
    """
    Определяет, какую метрику использовать, и возвращает строго JSON с ключом 'metric' и 'filters'.
    LLM не делает вычислений — только выбирает метрику.
    """
    available_metrics = [
        {"key": k, "description": v.get("description", "")}
        for k, v in METRICS.items()
    ]

    # Формируем понятный prompt
    prompt = f"""
Ты помощник аналитика HR. 
Твоя задача — только выбрать метрику и сформировать JSON по строго фиксированным правилам.

Формат ответа ВСЕГДА:
{{
  "metric": "ключ_метрики", 
  "filters": {{ "service": "...", "sex": "M" }},
  "group_by": ["age_category", "sex"],
  "timeframe": {{"month": 7}} 
}}

Правила:
1. "metric" — один из ключей из списка ниже. Никогда не придумывай свой.
   Доступные метрики:
   {list(METRICS.keys())}

2. ВАЖНО:
- В "filters" НИКОГДА не добавляй поля про время (month, months, start, end).
- В "filters" могут быть только поля: 
  ["service","sex","region","work_form",
   "department_3","department_4","department_5","department_6",
   "age_category","experience_category"].

- Для времени используй только объект "timeframe".

   Если в вопросе явно нет фильтров — оставляй пустым: {{}}.

3. "group_by" — массив, где элементы ТОЛЬКО из:
   ["sex","region","work_form",
    "department_3","department_4","department_5","department_6",
    "age_category","experience_category"]

   Если группировка не указана — верни [].

4. "timeframe":
   - Если указан конкретный месяц, возвращай {{"month": N}} где N ∈ [7,8,9].
   - Если указан диапазон месяцев, возвращай {{"months":[7,8,9]}}.
   - Если указан диапазон дат, возвращай {{"start":"2025-07-01","end":"2025-09-30"}}.
   - Если про время ничего не сказано — верни пустой объект: {{}}.

5. Никогда не делай вычислений и не пиши числа в "result".
6. Ответ ВСЕГДА только JSON, без комментариев и текста.
7. Если метрика не распознаётся — укажи "metric": null.

Вот пример правильного ответа
{{
  "metric": "turnover-rate-by-age-category",
  "filters": {{ "department_3": "Department-98" }},
  "group_by": ["age_category"],
  "timeframe": {{ "month": 8 }}
}}

Вот пример неправильного ответа:
(НЕ ДЕЛАЙ ТАК):
{{
  "metric": "turnover-rate-by-age-category",
  "filters": {{ "department_3": "Department-98", "month": "8" }},
  "group_by": ["age_category"],
  "timeframe": {{ "month": 8 }}
}}


Вопрос пользователя: "{user_query}"
"""

    response = giga.chat(prompt)
    return response.choices[0].message.content
