from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import analytics_service
from services.db_service import get_db


router = APIRouter()


@router.get("/average-experience/")
def average_experience(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db)
    return {"result": analytics_service.get_average_experiance(df)}


@router.get("/employees-by-region/")
def employees_by_region(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db)
    return {"result": analytics_service.get_employees_by_region(df)}


@router.get("/average-tenure-until-fire")
def average_tenure_until_fire(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db)
    return {"result": analytics_service.average_tenure_until_fire(df)}
