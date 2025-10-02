from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import auto_recommendations_service, llm_comment_service
from services.db_service import get_db
from services.cached_df_service import get_full_df_cached

router = APIRouter()


@router.get("/query/")
def get_recommendations(db: Session = Depends(get_db)):
    df = get_full_df_cached(db)

    recommendations = auto_recommendations_service.run_recommendations(df)

    recommendations_with_comments = [
        llm_comment_service.generate_comment_recommendations(rec)
        for rec in recommendations
    ]

    return {"recommendations": recommendations_with_comments}
