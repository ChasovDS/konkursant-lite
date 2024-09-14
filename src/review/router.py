from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.auth.auth import get_current_user
from src.auth.models import User
from src.projects.models import Project
from src.review.models import Review
from src.database import async_session
from src.review.schemas import ReviewCreate, ReviewResponse

review_router = APIRouter()


async def get_db():
    async with async_session() as session:
        yield session


@review_router.post("/", response_model=ReviewResponse, tags=["Проверка"])
async def create_review_criterion(
        review: ReviewCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.role != 'reviewer':
        raise HTTPException(status_code=403, detail="Not authorized to review projects")

    query = select(Project).where(Project.id_project == review.project_id).options(joinedload(Project.reviews))
    result = await db.execute(query)
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_review = Review(
        project_id=review.project_id,
        reviewer_id=current_user.id_user,
        criterion_id=review.criterion_id,
        score=review.score,
        feedback=review.feedback
    )

    project.reviews.append(new_review)

    # Обновляем статус проекта и средний балл
    project.status = 'evaluated'
    score_sum = sum(r.score for r in project.reviews)
    project.score = score_sum / len(project.reviews)

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return ReviewResponse(
        project_id=new_review.project_id,
        score=new_review.score,
        feedback=new_review.feedback,
        status=project.status
    )
