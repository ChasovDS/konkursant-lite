
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import get_current_user
from src.auth.models import User
from src.projects.models import Project
from src.database import async_session
from src.projects import schemas


project_router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@project_router.post("/", response_model=schemas.Project)
async def create_project(
    project: schemas.ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_project = models.Project(**project.dict(), owner_id=current_user.id_user)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project

@project_router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"file_path": file_location}
