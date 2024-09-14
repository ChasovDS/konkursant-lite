from sqlalchemy import Column, String, Integer, Text, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database import Base

class Project(Base):
    __tablename__ = 'projects'

    id_project = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    file_path = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id_user'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    status = Column(String, default='pending', nullable=False)

    owner = relationship("User", back_populates="projects")
    reviews = relationship("Review", back_populates="project")
