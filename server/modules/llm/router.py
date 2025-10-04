from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime
import json
from modules.analytics import analytics_service
from shared.schemas import UserQuery
from modules.llm import define_metric_service
from shared.utils import parse_llm, handle_query
from shared.db_service import get_db


router = APIRouter()


@router.post("/query/")
def analytics_query(body: UserQuery, db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)

    llm_response = define_metric_service.askYandexGPT(body.user_query)
    parsed = parse_llm.parse_llm_json(llm_response)
    result = handle_query.handle_user_query(parsed, df, body.user_query)

    record = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": body.user_query,
        "response": str(result)
    }
    with open("user_queries.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"LLM: {handle_query.handle_user_query(parsed, df, body.user_query)}")
    return result
