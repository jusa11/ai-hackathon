from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import crud
from services.db_service import get_db

router = APIRouter()

@router.get("/")
def read_employees(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(get_db)):
    return crud.get_employees(db, skip=skip, limit=limit)

