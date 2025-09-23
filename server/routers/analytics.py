from typing import Optional
from fastapi import Query
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import analytics_service
from services.db_service import get_db
import crud


router = APIRouter()


@router.get("/average-experience/")
def average_experience(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_average_experience(df)}

# Общее количество сотрудников


@router.get('/total-employees')
def total_employees(month: int | None = Query(None, ge=1, le=12), db: Session = Depends(get_db)):
    """
    month: необязательный параметр (1-12). Если указан, считаем только сотрудников за этот месяц.
    """
    total = crud.get_total_employees_count(db, month=month)
    return {"result": total}

# Средний возраст


@router.get("/average-age/")
def average_fullyears(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_average_fullyears(df)}


@router.get("/count-by-sex")
def count_by_sex(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_count_by_sex(df)}


@router.get("/employee-count-by-department-level/")
def employee_count_by_department_level(
    level: Optional[str] = Query(
        None, description="Уровень департамента: department_3/4/5/6"
    ),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_count_by_department_level(df, level=level)
    return {"result": result}


@router.get("/employees-by-region/")
def employees_by_region(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_employees_by_region(df)}


@router.get("/average-tenure-until-fire")
def average_tenure_until_fire(unit: str = "months", db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_average_tenure_until_fire(df, unit)}


@router.get("/average-experience-by-department/")
def average_experience_by_department(
    level: str | None = None,
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_average_experience_by_department(
        df, level=level)
    return {"result": result}


@router.get("/average-fte-by-department")
def average_fte_by_department(
    level: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_average_fte_by_department(df, level)}


@router.get("/average-experience-by-region")
def average_experience_by_region(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_average_experience_by_region(df)}


@router.get("/fired-count")
def fired_count(month: int | None = Query(None, ge=1, le=12), db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_fired_count(df, month=month)}


@router.get("/hired-count")
def hired_count(month: int | None = Query(None, ge=1, le=12), db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_hire_count(df, month=month)}


@router.get("/count-by-work-form")
def count_by_work_form(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_count_by_work_form(df)}


@router.get("/fte-sum")
def fte_sum_endpoint(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_fte_sum(df)}


@router.get("/fte-mean")
def fte_mean_endpoint(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    return {"result": analytics_service.get_fte_mean(df)}


@router.get("/turnover-rate")
def turnover_rate_endpoint(months: str | None = None, db: Session = Depends(get_db)):
    """
    months: через запятую, например "7,8,9" для июля-сентября.
    """
    df = analytics_service.get_employees_df(db, limit=None)
    month_list = [int(m) for m in months.split(",")] if months else None
    return {"result": analytics_service.get_turnover_rate_by_month(df, month_list)}


@router.get("/turnover-by-department")
def turnover_by_department(
    department: str = Query(
        ..., description="Уровень: department_3, department_4, department_5 или department_6"),
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_turnover_rate_by_department(
        df,
        department=department,
        month=month
    )
    return {"department": department, "result": result}


@router.get("/hires-and-fires-share")
def hires_and_fires_share(
    department_3: str | None = None,
    department_4: str | None = None,
    department_5: str | None = None,
    department_6: str | None = None,
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_hires_and_fires_share_by_department(
        df,
        department_3=department_3,
        department_4=department_4,
        department_5=department_5,
        department_6=department_6,
        month=month
    )
    return {"result": result}


@router.get("/turnover-all-regions")
def turnover_all_regions(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_turnover_rate_all_regions(df, month=month)
    return {"result": result}


@router.get("/work-form-distribution")
def work_form_distribution_endpoint(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_work_form_distribution(df, month=month)
    return {"result": result}


@router.get("/average-fte-by-work-form")
def average_fte_by_work_form_endpoint(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_average_fte_by_work_form(df, month=month)
    return {"result": result}


@router.get("/turnover-by-age-category")
def turnover_by_age_category(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_turnover_rate_by_age_category(
        df, month=month)
    return {"result": result}


@router.get("/turnover-by-experience-category")
def turnover_by_experience_category(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_turnover_rate_by_experience_category(
        df, month=month)
    return {"result": result}


@router.get("/average-experience-by-group")
def average_experience_by_group_endpoint(
    service: str | None = None,
    department_3: str | None = None,
    department_4: str | None = None,
    department_5: str | None = None,
    department_6: str | None = None,
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_average_experience_by_group(
        df,
        service=service,
        department_3=department_3,
        department_4=department_4,
        department_5=department_5,
        department_6=department_6
    )
    return {"result": result}


@router.get("/turnover-by-service")
def turnover_by_service(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_turnover_rate_by_service(df, month=month)
    return {"result": result}


@router.get("/turnover-by-work-form")
def turnover_by_work_form(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_turnover_rate_by_work_form(df, month=month)
    return {"result": result}


@router.get("/fired-by-region")
def fired_by_region(
    month: int | None = Query(None, ge=1, le=12),
    db: Session = Depends(get_db)
):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_fired_count_by_region(df, month=month)
    return {"result": result}


@router.get("/employee-count-by-service")
def employee_count_by_service_endpoint(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_employee_count_by_service(df)
    return {"result": result}


@router.get("/average-fte-by-service")
def average_fte_by_service_endpoint(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_average_fte_by_service(df)
    return {"result": result}


@router.get("/average-experience-by-region")
def average_experience_by_region_endpoint(db: Session = Depends(get_db)):
    df = analytics_service.get_employees_df(db, limit=None)
    result = analytics_service.get_average_experience_by_region(df)
    return {"result": result}
