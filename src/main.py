from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import auth_router
from src.projects.router import project_router

from src.database import database

app = FastAPI()

# Подключение к маршрутам
app.include_router(auth_router, prefix="/auth")
app.include_router(project_router, prefix="/projects")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL вашего React приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пример конечной точки для проверки
@app.get("/", tags=["Стартовая страница"])
async def read_root():
    return {"message": "Добро пожаловать в API Конкурсант"}
