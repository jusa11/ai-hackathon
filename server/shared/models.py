from sqlalchemy import Column, Integer, String, Float, DateTime
from shared.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)  
    fullyears = Column(Integer)
    age_category = Column(String)
    service = Column(String)
    sex = Column(String)
    department_3 = Column(String)
    department_4 = Column(String)
    department_5 = Column(String)
    department_6 = Column(String)
    experience_category = Column(String)
    experience = Column(Float)
    fire_from_company = Column(DateTime)
    hire_to_company = Column(DateTime)
    hirecount = Column(Integer)
    firecount = Column(Integer)
    fte = Column(Float)
    real_day = Column(Integer)
    report_date = Column(DateTime)
    work_form = Column(Integer)
    region = Column(String)
