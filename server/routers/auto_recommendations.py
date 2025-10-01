# routers/recommendations_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import analytics_service, auto_recommendations_service, llm_comment_service
from services.db_service import get_db

router = APIRouter()


@router.get("/query/")
def get_recommendations(db: Session = Depends(get_db)):
    # данные сотрудников
    df = analytics_service.get_employees_df(db, limit=None)

    # рекомендации
    recommendations = auto_recommendations_service.run_recommendations(df)

    # LLM-комментарии для каждой рекомендации
    recommendations_with_comments = [
        llm_comment_service.generate_comment_recommendations(rec)
        for rec in recommendations
    ]

    return {"recommendations": recommendations_with_comments}
