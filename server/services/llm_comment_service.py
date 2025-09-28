import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML

load_dotenv()
YANDEXGPT_TOKEN = os.getenv("YANDEXGPT_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")


sdk = YCloudML(folder_id=FOLDER_ID, auth=YANDEXGPT_TOKEN)


def generate_comment(user_query: str, metric: str, result: dict) -> str:
    """
    Генерирует короткий комментарий от Yandex GPT по результатам метрики.
    """

    if isinstance(result, dict):
        result_str = "\n".join([f"{k}: {v}" for k, v in result.items()])
    else:
        result_str = str(result)

    prompt = f"""
Ты аналитик HR-данных.
Пользователь задал вопрос: "{user_query}"
Была рассчитана метрика: "{metric}"

Результаты (не делай догадок, описывай только эти данные):
{result_str}

Сформируй короткий комментарий (1–3 предложения) простыми словами,
выделяя основные выводы из этих данных, не придумывай числа.
"""

    model = sdk.models.completions("yandexgpt").configure(temperature=0.5)
    response = model.run(prompt)

    comment = response.alternatives[0].text.strip()
    return comment
