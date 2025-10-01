from routers import analytics, employees, llm, plots, auto_recommendations
from database import engine
import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


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
app.include_router(analytics.router, prefix='/analytics', tags=['analytics'])
app.include_router(employees.router, prefix='/employees', tags=['employees'])
app.include_router(plots.router, prefix='/metric', tags=['metric'])
app.include_router(llm.router, prefix='/llm', tags=['llm'])
app.include_router(auto_recommendations.router,
                   prefix='/recomendations', tags=['recomendations'])
