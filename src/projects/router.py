from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from src.auth.auth import get_current_user
from src.auth.models import User
from src.projects.models import Project, ProjectData
from src.database import async_session
from src.projects import schemas, utils
from sqlalchemy import or_
from fastapi import UploadFile, File
from datetime import datetime

import json
import re
import os
from docx import Document
import shutil
import asyncio
import logging
from src.projects.projects import convert_docx_to_json

project_router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Асинхронная функция для обработки файла
async def process_file_and_update_db(file_path: str, project_id: int, db: AsyncSession):
    # Конвертация DOCX в JSON
    json_filepath = convert_docx_to_json(file_path)

    # Чтение JSON файла
    try:
        with open(json_filepath, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        logger.error(f"Ошибка чтения JSON файла: {e}")
        return

    # Начало транзакции базы данных
    try:
        async with db.begin():
            # Поиск проекта по ID
            project_result = await db.execute(
                select(Project).filter(Project.id_project == project_id)
            )
            project = project_result.scalar_one_or_none()

            if project is None:
                logger.warning(f"Проект с ID {project_id} не найден.")
                return

            # Получение или создание данных проекта
            project_data_result = await db.execute(
                select(ProjectData).filter(ProjectData.project_id == project_id)
            )
            project_data = project_data_result.scalar_one_or_none()

            if project_data is None:
                project_data = ProjectData(project_id=project_id, json_data=json_data)
                db.add(project_data)
                logger.info("Новые данные проекта добавлены.")
            else:
                project_data.json_data = json_data
                logger.info("Данные проекта обновлены.")

            await db.commit()
            logger.info("Изменения успешно сохранены.")

    except Exception as e:
        logger.error(f"Ошибка при обработке базы данных: {e}")



@project_router.get("/", response_model=List[schemas.Project], tags=["Проекты"])
async def get_list_available_project_info(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(utils.get_db)):
    if current_user.role in ['admin', 'reviewer']:
        query = select(Project)
    else:
        query = select(Project).where(Project.owner_id == current_user.id_user)
    result = await db.execute(query)
    projects = result.scalars().all()
    return projects


@project_router.post("/create/", response_model=schemas.Project, tags=["Проекты"])
async def create_project(
    background_tasks: BackgroundTasks,
    title: str = Form(...),  # Важное изменение: добавление Form(...)
    description: Optional[str] = Form(None),
    docs_file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(utils.get_db)
):
    if not title or not docs_file:
        raise HTTPException(status_code=422, detail="Необходимые поля: title и docs_file.")

    print(f"Title: {title}, Description: {description}, Filename: {docs_file.filename}")

    script_path = os.path.abspath(__file__)
    three_levels_up = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    file_location = f"{three_levels_up}/src/_resources/uploads/{docs_file.filename}"

    # Сохранение файла на сервере
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(docs_file.file, buffer)

    # Создание нового проекта
    new_project = Project(
        title=title,
        description=description,
        docs_file_path=file_location,
        owner_id=current_user.id_user,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        status='Ожидает проверки'  # Пример статуса, можно поменять
    )

    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    # Добавление фоновой задачи для обработки файла и обновления проекта
    background_tasks.add_task(process_file_and_update_db, file_location, new_project.id_project, db)

    return new_project

@project_router.get("/{project_id}/json-data", response_model=dict, tags=["Проекты"])
async def get_json_data(project_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(utils.get_db)):
    # Запрос для получения проекта по ID с проверкой прав доступа
    query = select(Project).where(
        Project.id_project == project_id,
        or_(
            Project.owner_id == current_user.id_user,
            current_user.role in ["admin", "reviewer"]
        )
    )
    result = await db.execute(query)

    # Извлечение проекта из результата
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Получение данных JSON из таблицы project_data
    json_data_query = select(ProjectData).where(ProjectData.project_id == project_id)
    json_data_result = await db.execute(json_data_query)
    project_data = json_data_result.scalar_one_or_none()

    if not project_data:
        raise HTTPException(status_code=404, detail="Project JSON data not found")

    # Возвращаем данные JSON
    return project_data.json_data


@project_router.delete("/delete/{project_id}/", tags=["Проекты"])
async def delete_project(
    project_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(utils.get_db)
):
    # Получаем проект из базы данных
    result = await db.execute(select(Project).filter(Project.id_project == project_id))
    project = result.scalars().first()

    # Проверка, существует ли проект
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден.")

    # Проверка прав пользователя
    if current_user.role not in ["admin", "reviewer"] and project.owner_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="У вас нет прав удалять этот проект.")

    # Удаление связанных данных проекта
    try:
        # Получаем связанные данные
        project_data_result = await db.execute(
            select(ProjectData).filter(ProjectData.project_id == project_id)
        )
        project_data = project_data_result.scalars().first()

        # Удаляем связанные проектные данные, если они существуют
        if project_data:
            await db.delete(project_data)
            logger.info(f"Данные проекта с ID {project_id} успешно удалены.")

        # Удаление проекта
        await db.delete(project)
        await db.commit()

        return {"detail": "Проект и связанные данные успешно удалены."}

    except Exception as e:
        logger.error(f"Ошибка при удалении проекта и связанных данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера при удалении проекта.")


@project_router.get("/{project_id}", response_model=schemas.Project, tags=["Проекты"])
async def get_project(project_id: int,
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(utils.get_db)):
    query = select(Project).where(Project.id_project == project_id)
    result = await db.execute(query)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id_user and current_user.role not in ['admin', 'reviewer']:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")
    return project
