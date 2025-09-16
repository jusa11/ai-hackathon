import os
from gigachat import GigaChat
from dotenv import load_dotenv
from services.metrics import METRICS  

load_dotenv()
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")

giga = GigaChat(credentials=GIGACHAT_CLIENT_SECRET, verify_ssl_certs=False)


def askGiga(user_query: str) -> str:
    available_metrics = list(METRICS.keys())  

    prompt = f"""
Ты помощник аналитика HR.
Пользователь задаёт вопрос о метриках сотрудников.

Всегда отвечай строго в JSON формате:
{{
  "metric": "название_метрики",
  "filters": {{}}, 
  "result": null
}}

Правила:
- "metric" должен быть одним из: {available_metrics}.
- Если метрика не распознаётся — укажи "metric": null.
- "filters" оставляй пустым, если они не нужны.
- "result" не заполняй, это вычислит сервер.

Вопрос пользователя: "{user_query}"
"""
    response = giga.chat(prompt)
    return response.choices[0].message.content
