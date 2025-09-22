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
Пользователь задаёт вопрос о метриках сотрудников.

Всегда отвечай строго в JSON формате, без каких-либо чисел:
{{
  "metric": "ключ_метрики",
  "filters": {{}}
}}

Правила:
- "metric" должен быть одним из ключей доступных метрик.
- Если метрика не распознаётся — укажи "metric": null.
- В "filters" указывай параметры, если они явно есть в вопросе:
  * Для метрики count-by-department-level указывай "level": одно из department_3, department_4, department_5, department_6.
  * Если уровень департамента не указан — filters оставь пустым.
- Никогда не делай расчётов и не подставляй числа — сервер сам их вычислит.

Доступные метрики с описанием:
{available_metrics}

Вопрос пользователя: "{user_query}"
"""

    response = giga.chat(prompt)
    print(response.choices[0].message.content)
    return response.choices[0].message.content
