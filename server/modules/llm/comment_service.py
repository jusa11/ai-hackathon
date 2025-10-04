import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML

load_dotenv()
YANDEXGPT_TOKEN = os.getenv("YANDEXGPT_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")

sdk = YCloudML(folder_id=FOLDER_ID, auth=YANDEXGPT_TOKEN)

HISTORY = {
    "messages": [] 
}


def generate_comment_metrics(user_query: str, metric: str, result: dict) -> str:
    """
    Генерирует комментарий по результатам метрики.
    Использует историю последних 4 сообщений.
    """

    HISTORY["messages"].append(f"Пользователь: {user_query}")
    if len(HISTORY["messages"]) > 4:
        HISTORY["messages"] = HISTORY["messages"][-4:]

    if metric == "irrelevant" or result == "irrelevant":
        prompt = f"""
Ты HR-аналитик и помощник для HR-менеджера. Если пользователь назвал свое имя, то впоследствии 
обращайся к нему по имени.  
История последних сообщений:
{chr(10).join(HISTORY['messages'])}

Пользователь задал вопрос: "{user_query}".
Этот запрос не относится к доступным HR-метрикам и данным.
Ответь вежливо и понятно (не более 4-6 предложений), обратись на "ты". 
Предложи несколько релевантных метрик, которые можно запросить
(например: текучесть кадров, динамика найма, средний FTE, средний опыт по регионам). 
Не придумывай чисел и не указывай внутренние технические детали.
"""
    else:
        if isinstance(result, dict):
            N = 30
            items = list(result.items())
            shown = items[:N]
            result_str = "\n".join([f"{k}: {v}" for k, v in shown])
            if len(items) > N:
                result_str += f"\n...и ещё {len(items) - N} элементов."
        else:
            result_str = str(result)

        prompt = f"""
Ты аналитик HR-данных и коллега (обращайся на 'ты').
История последних сообщений:
{chr(10).join(HISTORY['messages'])}

Пользователь задал вопрос: "{user_query}"
Была рассчитана метрика: "{metric}"

Результаты (описывай ТОЛЬКО эти данные, не придумывай дополнительных чисел):
{result_str}

Сформулируй развернутый комментарий (3-10 предложений),
включи интерпретацию данных и практические рекомендации/следующие шаги для HR,
не придумывай новые числа и не упоминай внутренние названия функций/метрик.
"""

    model = sdk.models.completions("yandexgpt").configure(temperature=0.5)
    response = model.run(prompt)
    comment = response.alternatives[0].text.strip()

    HISTORY["messages"].append(f"LLM: {comment}")
    if len(HISTORY["messages"]) > 4:
        HISTORY["messages"] = HISTORY["messages"][-4:]

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
