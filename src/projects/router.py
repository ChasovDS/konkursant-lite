from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from src.auth.auth import get_current_user
from src.auth.models import User
from src.projects.models import Project
from src.database import async_session
from src.projects import schemas
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

@project_router.patch("/{project_id}/evaluate", response_model=schemas.Project, tags=["Проекты"])
async def evaluate_project(project_id: int,
                           evaluation: schemas.ProjectEvaluation,
                           current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    query = select(Project).where(Project.id_project == project_id)
    result = await db.execute(query)
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role != 'reviewer':
        raise HTTPException(status_code=403, detail="Not authorized to evaluate projects")
    project.score = evaluation.score
    project.status = 'evaluated'
    await db.commit()
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
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

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
