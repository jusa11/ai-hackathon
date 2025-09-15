from fastapi import FastAPI
import models
from database import engine
from routers import analytics, employees, llm

# --- БД ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Routes ---
app.include_router(analytics.router, prefix='/analytics', tags=['analytics'])
app.include_router(employees.router, prefix='/employees', tags=['employees'])
app.include_router(llm.router, prefix='/llm', tags=['llm'])
