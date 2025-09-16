from sqlalchemy.orm import Session
from sqlalchemy import extract
import models


def get_employees(db: Session, skip: int = 0, limit: int | None = 100):
    query = db.query(models.Employee).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_total_employees_count(db: Session, month: int | None = None):
    query = db.query(models.Employee)

    if month:
        query = query.filter(
            extract('month', models.Employee.report_date) == month)

    return query.count()
