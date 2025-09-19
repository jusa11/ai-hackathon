from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import models
from database import engine
from routers import analytics, employees, llm, plots

# --- БД ---
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- Routes ---
app.include_router(analytics.router, prefix='/analytics', tags=['analytics'])
app.include_router(employees.router, prefix='/employees', tags=['employees'])
app.include_router(plots.router, prefix='/metric', tags=['metric'])
app.include_router(llm.router, prefix='/llm', tags=['llm'])

# --- CORS ---
origins = [
    "http://localhost:3000",  # твой React dev-сервер
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
    # "https://твойдомен.ру"   # продакшн-домен
]


app = FastAPI()

# список доменов, с которых разрешены запросы
origins = [
    "http://localhost:3000",  # твой React dev-сервер
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
    # "https://твойдомен.ру"   # продакшн-домен
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],             # GET, POST, PUT, DELETE и т.п.
    allow_headers=["*"],             # заголовки
)
