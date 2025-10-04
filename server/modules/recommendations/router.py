from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modules.recommendations import recommendations_service
from modules.llm import comment_service
from shared.db_service import get_db
from shared.cached_df_service import get_full_df_cached

router = APIRouter()


@router.get("/query/")
def get_recommendations(db: Session = Depends(get_db)):
    df = get_full_df_cached(db)

    recommendations = recommendations_service.run_recommendations(df)

    recommendations_with_comments = [
        comment_service.generate_comment_recommendations(rec)
        for rec in recommendations
    ]

    return {"recommendations": recommendations_with_comments}
