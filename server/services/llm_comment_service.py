import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML

load_dotenv()
YANDEXGPT_TOKEN = os.getenv("YANDEXGPT_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")


sdk = YCloudML(folder_id=FOLDER_ID, auth=YANDEXGPT_TOKEN)


def generate_comment_metrics(user_query: str, metric: str, result: dict) -> str:
    """
    Генерирует комментарий по результатам метрики.
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

Сформируй развернутый комментарий (3-10 предложений),
внеси свои предложений/решения как hr-аналитик, исходя из этих данных, но при
этом не придумывай числа и другие данные, исходи из того, что имеешь. При этом 
в тексте не указывай чисто техническую информацию (например названия использованных метрик).
"""

    model = sdk.models.completions("yandexgpt").configure(temperature=0.5)
    response = model.run(prompt)

    comment = response.alternatives[0].text.strip()
    return comment


def generate_comment_recommendations(recommendation: dict) -> str:
    """
    Добавляет системный комментарий от LLM к одной рекомендации.
    """
    prompt = f"""
Ты HR-аналитик. Даны данные по отделу:
{recommendation}

Сформулируй короткий, понятный комментарий (2-6 предложений) по этим данным. 
Дай рекомендации о том как улучишить или поддержывать этот результат.  
Не придумывай числа, говори только о том, что видно в этих данных.
"""
    model = sdk.models.completions("yandexgpt").configure(temperature=0.5)
    response = model.run(prompt)
    comment = response.alternatives[0].text.strip()

    return {**recommendation, "comment": comment}
