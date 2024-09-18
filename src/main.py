from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import auth_router
from src.projects.router import project_router
from src.review.router import review_router

from src.database import database

app = FastAPI(
    title="Конкурсант API"
)

# Подключение к маршрутам
app.include_router(auth_router, prefix="/auth")
app.include_router(project_router, prefix="/projects", tags=["Проекты"])
app.include_router(review_router, prefix="/reviews", tags=["Проверка"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пример конечной точки для проверки
@app.get("/", tags=["Стартовая страница"])
async def read_root():
    return {"message": "Добро пожаловать в API Конкурсант"}
