from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    project_id: int
    criterion_id: int
    score: float
    feedback: Optional[str]

class ReviewResponse(BaseModel):
    project_id: int
    score: int
    feedback: Optional[str]
    status: str

    class Config:
        from_attributes = True

