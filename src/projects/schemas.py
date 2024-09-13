from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]
    file_path: str

class ProjectEvaluation(BaseModel):
    score: float

class Project(BaseModel):
    id_project: int
    title: str
    description: Optional[str]
    file_path: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
    score: Optional[float] = None
    status: str

    class Config:
        from_attributes = True
