from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.auth.auth import get_current_user
from src.auth.models import User
from src.projects.models import Project
from src.review.models import Review
from src.database import async_session
from src.review.schemas import ReviewBase

review_router = APIRouter()


async def get_db():
    async with async_session() as session:
        yield session


@review_router.post("/", response_model=ReviewBase, tags=["Проверка"])
async def create_review_criterion(
        review: ReviewBase,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.role != 'reviewer':
        raise HTTPException(status_code=403, detail="У Вас нет прав для оценки проекта")

    query = select(Project).where(Project.id_project == review.project_id).options(joinedload(Project.reviews))
    result = await db.execute(query)
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Стараница не найдена")

    new_review_data = review.dict()
    new_review_data.pop('status', None)  # Удаляем статус, если он есть
    new_review_data.update({
        "reviewer_id": current_user.id_user
    })

    new_review = Review(**new_review_data)

    project.reviews.append(new_review)

    # Обновляем статус проекта
    project.status = 'Оценено'

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return ReviewBase(
        project_id=new_review.project_id,
        team_experience=new_review.team_experience,
        project_relevance=new_review.project_relevance,
        solution_uniqueness=new_review.solution_uniqueness,
        implementation_scale=new_review.implementation_scale,
        development_potential=new_review.development_potential,
        project_transparency=new_review.project_transparency,
        feasibility_and_effectiveness=new_review.feasibility_and_effectiveness,
        additional_resources=new_review.additional_resources,
        planned_expenses=new_review.planned_expenses,
        budget_realism=new_review.budget_realism,
        feedback=new_review.feedback,
        status=project.status
    )