from sqlalchemy.orm import Session
import models

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    skip = int(skip)
    limit = int(limit)
    return db.query(models.Employee).offset(skip).limit(limit).all()
