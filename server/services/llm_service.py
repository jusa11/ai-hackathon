import os
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")

giga = GigaChat(credentials=GIGACHAT_CLIENT_SECRET, verify_ssl_certs=False)


def askGiga(user_query: str) -> str:
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
- "metric" должен быть одним из: ["average_experience", "employee_count_by_region", "average_tenure"].
- Если метрика не распознаётся — укажи "metric": null.
- "filters" оставляй пустым, если они не нужны.
- "result" не заполняй, это вычислит сервер.

Вопрос пользователя: "{user_query}"
"""
    response = giga.chat(prompt)
    return response.choices[0].message.content
