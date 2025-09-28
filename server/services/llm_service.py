import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML
from services.metrics import METRICS

load_dotenv()

YANDEXGPT_TOKEN = os.getenv("YANDEXGPT_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")


sdk = YCloudML(
    folder_id=FOLDER_ID,
    auth=YANDEXGPT_TOKEN,
    enable_server_data_logging=False,
)

valid_values = {
    "age_category": ["18-25", "25-40", "40-60"],
    "service": [
        "Доставка", "Крауд", "Вертикали", "Еда", "Коммерческий департамент",
        "Лавка", "Маркет", "Поисковый портал", "Такси", "Финтех"
    ],
    "sex": ["M", "F"],
    "experience_category": [
        "1 мес", "2 мес", "3 мес",
        "до 1 года", "1-2 года", "2-3 года", "3-5 лет", "более 5 лет"
    ],
    "work_form": [0, 1],
}

available_metrics = []
for k, v in METRICS.items():
    aliases = v.get("aliases", [])
    desc = v.get("description", "")
    if k == "average-experience":
        desc += " Поддерживает группировки по age_category, sex, service, department_*."
    available_metrics.append(
        {"key": k, "description": desc, "aliases": aliases}
    )


def askYandexGPT(user_query: str) -> str:
    """
    Отправляет запрос к Yandex GPT и возвращает строго JSON строку с ключами:
    'metric', 'filters', 'group_by', 'timeframe'
    """
    model = sdk.models.completions("yandexgpt").configure(temperature=0.5)

    prompt = f"""
Ты помощник аналитика HR. 
Твоя задача — только выбрать метрику и сформировать JSON по строго фиксированным правилам.

Доступные метрики (ключ + описание + alias):
{available_metrics}

Доступные колонки и допустимые значения:
{valid_values}

Формат ответа ВСЕГДА:
{{
  "metric": "ключ_метрики", 
  "filters": {{ "service": "...", "sex": "M" }},
  "group_by": ["age_category", "sex"],
  "timeframe": {{"month": 7}} 
}}

Правила:
1. "metric" — один из ключей или alias из списка выше.
2. В "filters" и "group_by" используй ТОЛЬКО значения из допустимых списков выше.
3. Если в вопросе пользователя значение не совпадает с допустимым — возвращай null для этого фильтра.
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

    result = model.run(prompt)
    json_str = result.alternatives[0].text

    print(f"YandexGPT response: {json_str}")

    return json_str
