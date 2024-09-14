from sqlalchemy import Column, Integer, ForeignKey, Float, Text, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Review(Base):
    __tablename__ = 'reviews'

    id_review = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('users.id_user'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Оценка по критериям
    team_experience = Column(Integer, nullable=False)  # Опыт и компетенции команды проекта
    project_relevance = Column(Integer, nullable=False)  # Актуальность и социальная значимость проекта
    solution_uniqueness = Column(Integer, nullable=False)  # Уникальность и адресность предложенного решения проблемы
    implementation_scale = Column(Integer, nullable=False)  # Масштаб реализации проекта
    development_potential = Column(Integer, nullable=False)  # Перспектива развития и потенциал проекта
    project_transparency = Column(Integer, nullable=False)  # Информационная открытость проекта
    feasibility_and_effectiveness = Column(Integer, nullable=False)  # Реализуемость проекта и его результативность
    additional_resources = Column(Integer, nullable=False)  # Собственный вклад и дополнительные ресурсы проекта
    planned_expenses = Column(Integer, nullable=False)  # Планируемые расходы на реализацию проекта
    budget_realism = Column(Integer, nullable=False)  # Реалистичность бюджета проекта

    #Фитбек по проекту
    feedback = Column(Text, nullable=False)

    project = relationship("Project", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")
