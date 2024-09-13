from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]
    file_path: str

class Project(BaseModel):
    id_project: int
    title: str
    description: Optional[str]
    file_path: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
