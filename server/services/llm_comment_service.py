import os
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()
GIGACHAT_CLIENT_SECRET = os.getenv("GIGACHAT_CLIENT_SECRET")

giga = GigaChat(credentials=GIGACHAT_CLIENT_SECRET, verify_ssl_certs=False)


def generate_comment(user_query: str, metric: str, result: dict) -> str:
    """
    Генерирует короткий комментарий от LLM по результатам метрики
    """
    # Преобразуем результат в читаемый вид для LLM
    result_str = "\n".join([f"{k}: {v}" for k, v in result.items()]) if isinstance(
        result, dict) else str(result)

    prompt = f"""
Ты аналитик HR-данных.
Пользователь задал вопрос: "{user_query}"
Была рассчитана метрика: "{metric}"

Результаты (не делай догадок, описывай только эти данные):
{result_str}

Сформируй короткий комментарий (1–3 предложения) простыми словами,
выделяя основные выводы из этих данных, не придумывай числа.
"""
    response = giga.chat(prompt)
    return response.choices[0].message.content.strip()
