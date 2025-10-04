from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from shared.database import engine
import shared.models as models
from shared.employees import router as employees
from modules.analytics.router import router as analytics
from modules.charts.router import router as charts
from modules.llm.router import router as llm
from modules.recommendations.router import router as recommendations


# --- БД ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
app.include_router(employees, prefix='/employees', tags=['employees'])
app.include_router(analytics, prefix='/analytics', tags=['analytics'])
app.include_router(charts, prefix='/metric', tags=['metric'])
app.include_router(llm, prefix='/llm', tags=['llm'])
app.include_router(recommendations,
                   prefix='/recommendations', tags=['recommendations'])
