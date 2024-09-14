from sqlalchemy import Column, Integer, ForeignKey, Float, Text, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Criterion(Base):
    __tablename__ = 'criteria'

    id_criterion = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

    reviews = relationship("Review", back_populates="criterion_ref")

class Review(Base):
    __tablename__ = 'reviews'

    id_review = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('users.id_user'), nullable=False)
    criterion_id = Column(Integer, ForeignKey('criteria.id_criterion'), nullable=False)  # Обновлено
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    project = relationship("Project", back_populates="reviews")
    reviewer = relationship("User", back_populates="reviews")
    criterion_ref = relationship("Criterion", back_populates="reviews")  # Связь с Criterion

