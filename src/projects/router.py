from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from src.auth.auth import get_current_user
from src.auth.models import User
from src.projects.models import Project, GeneralInfo, AuthorInfo, ProjectDetails, ProjectGeography, TeamMember, Mentor, ProjectResult, TaskEvent, MediaResource, Expense, OwnFund, PartnerSupport, AdditionalFile
from src.database import async_session
from src.projects import schemas
from src.projects.schemas import CompleteProjectInfo, ProjectCreate
from src.projects.models import GeneralInfo, OtherAdditionalFile
from src.projects.schemas import OtherAdditionalFileCreate
import shutil

project_router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@project_router.post("/", response_model=schemas.Project, tags=["Проекты"])
async def create_project(project: schemas.ProjectCreate,
                         current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    new_project = Project(**project.dict(), owner_id=current_user.id_user)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

@project_router.get("/{project_id}", response_model=schemas.Project, tags=["Проекты"])
async def get_project(project_id: int,
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id_project == project_id)
    result = await db.execute(query)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id_user and current_user.role not in ['admin', 'reviewer']:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")
    return project


@project_router.get("/", response_model=List[schemas.Project], tags=["Проекты"])
async def list_projects(current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    if current_user.role in ['admin', 'reviewer']:
        query = select(Project)
    else:
        query = select(Project).where(Project.owner_id == current_user.id_user)
    result = await db.execute(query)
    projects = result.scalars().all()
    return projects


@project_router.post("/uploadfile/", tags=["Проекты"])
async def upload_file(file: UploadFile = File(...),
                      current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    file_location = f"files/{file.filename}"

    # Сохранение файла
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Создание объекта проекта
    project = Project(
        title=file.filename,
        description='Uploaded file',
        file_path=file_location,
        owner_id=current_user.id_user
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)


    return {"file_path": file_location, "project": project}


@project_router.get("/my_project/{project_id}", response_model=CompleteProjectInfo, tags=["Проекты"])
async def get_my_project(project_id: int,
                         current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id_project == project_id).options(
        joinedload(Project.general_info),
        joinedload(Project.author_info),
        joinedload(Project.project_details),
        joinedload(Project.project_geographies),
        joinedload(Project.team_members),
        joinedload(Project.mentors),
        joinedload(Project.project_results),
        joinedload(Project.task_events),
        joinedload(Project.media_resources),
        joinedload(Project.expenses),
        joinedload(Project.own_funds),
        joinedload(Project.partner_supports),
        joinedload(Project.additional_files)
    )
    result = await db.execute(query)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")
    return project


@project_router.get("/detailed_information/{project_id}", response_model=CompleteProjectInfo, tags=["Проверка"])
async def detailed_project_information(project_id: int,
                                       current_user: User = Depends(get_current_user),
                                       db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id_project == project_id).options(
        joinedload(Project.general_info),
        joinedload(Project.author_info),
        joinedload(Project.project_details),
        joinedload(Project.project_geographies),
        joinedload(Project.team_members),
        joinedload(Project.mentors),
        joinedload(Project.project_results),
        joinedload(Project.task_events),
        joinedload(Project.media_resources),
        joinedload(Project.expenses),
        joinedload(Project.own_funds),
        joinedload(Project.partner_supports),
        joinedload(Project.additional_files)
    )
    result = await db.execute(query)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role not in ['admin', 'reviewer'] and project.owner_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Not authorized to view this project")

    return project


@project_router.post("/add_additional_file/", status_code=status.HTTP_201_CREATED, tags=["Проекты"])
async def add_additional_file(file_data: OtherAdditionalFileCreate,
                              current_user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    # Получаем проект и проверяем права доступа
    project_query = select(GeneralInfo).where(GeneralInfo.project_id == file_data.project_id)
    project_result = await db.execute(project_query)
    project = project_result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="Not authorized to add file to this project")

    # Добавляем информацию о файле
    new_file = OtherAdditionalFile(
        file_name=file_data.file_name,
        file_link=file_data.file_link,
        project_id=file_data.project_id
    )

    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return new_file