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


@review_router.post("/create_review/{project_id}", response_model=ReviewBase, tags=["Проверка"])
async def create_review_for_project(
        project_id: int,
        review: ReviewBase,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.role != 'reviewer':
        raise HTTPException(status_code=403, detail="У Вас нет прав для оценки проекта")

    # Найти проект по project_id
    query = select(Project).where(Project.id_project == project_id).options(joinedload(Project.reviews))
    result = await db.execute(query)
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Создаем отзыв
    new_review_data = review.dict()
    new_review_data.pop('status', None)  # Удаляем статус, если он есть
    new_review_data.update({
        "reviewer_id": current_user.id_user,
        "project_id": project_id  # Устанавливаем project_id из маршрута
    })

    new_review = Review(**new_review_data)  # Здесь project_id будет с правильным значением

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

@review_router.get("/{project_id}", response_model=list[ReviewBase], tags=["Проверка"])
async def get_project_reviews(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # Найти проект по project_id
    query = select(Project).where(Project.id_project == project_id).options(joinedload(Project.reviews))
    result = await db.execute(query)
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    # Проверяем роль пользователя
    if current_user.role != 'reviewer' and project.owner_id != current_user.id_user:
        raise HTTPException(status_code=403, detail="У вас нет доступа к этому проекту")

    # Генерируем список отзывов в формате ReviewBase
    return [
        ReviewBase(
            project_id=review.project_id,
            team_experience=review.team_experience,
            project_relevance=review.project_relevance,
            solution_uniqueness=review.solution_uniqueness,
            implementation_scale=review.implementation_scale,
            development_potential=review.development_potential,
            project_transparency=review.project_transparency,
            feasibility_and_effectiveness=review.feasibility_and_effectiveness,
            additional_resources=review.additional_resources,
            planned_expenses=review.planned_expenses,
            budget_realism=review.budget_realism,
            feedback=review.feedback,
            status=project.status  # Статус проекта
        ) for review in project.reviews
    ]


@review_router.get("/verified_projects/", response_model=list[ReviewBase], tags=["Проверка"])
async def get_verified_projects(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # Проверка прав доступа
    if current_user.role not in ['reviewer', 'admin']:
        raise HTTPException(status_code=403, detail="У вас нет доступа к этой информации")

    # Получение проектов с отзывами
    query = select(Project).options(joinedload(Project.reviews))
    result = await db.execute(query)
    projects = result.unique().scalars().all()  # Добавлен unique()

    # Формирование списка отзывов
    verified_reviews = []
    for project in projects:
        for review in project.reviews:
            verified_reviews.append(ReviewBase(
                project_id=review.project_id,
                team_experience=review.team_experience,
                project_relevance=review.project_relevance,
                solution_uniqueness=review.solution_uniqueness,
                implementation_scale=review.implementation_scale,
                development_potential=review.development_potential,
                project_transparency=review.project_transparency,
                feasibility_and_effectiveness=review.feasibility_and_effectiveness,
                additional_resources=review.additional_resources,
                planned_expenses=review.planned_expenses,
                budget_realism=review.budget_realism,
                feedback=review.feedback,
                status=project.status  # Статус проекта
            ))

    return verified_reviews

