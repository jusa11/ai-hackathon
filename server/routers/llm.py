from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import UserQuery
from services import llm_service, analytics_service
from utils import parse_llm, handle_query
from services.db_service import get_db

router = APIRouter()


@router.post("/query/")
def analytics_query(body: UserQuery, db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)

    llm_response = llm_service.askYandexGPT(body.user_query)
    parsed = parse_llm.parse_llm_json(llm_response)
    print(f"LLM: {handle_query.handle_user_query(parsed, df, body.user_query)}")
    return handle_query.handle_user_query(parsed, df, body.user_query)
