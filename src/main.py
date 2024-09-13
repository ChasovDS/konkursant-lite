from fastapi import FastAPI
from src.auth.router import auth_router
from src.projects.router import project_router
from src.database import database
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL вашего React фронт-энд приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)