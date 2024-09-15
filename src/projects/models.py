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
    status = Column(String, default='Ожидает проверки', nullable=False)

    owner = relationship("User", back_populates="projects")
    reviews = relationship("Review", back_populates="project")

    other_additional_files = relationship("OtherAdditionalFile", back_populates="project")
    # Relationships to the new models
    general_info = relationship("GeneralInfo", back_populates="project", uselist=False)
    author_info = relationship("AuthorInfo", back_populates="project", uselist=False)
    project_details = relationship("ProjectDetails", back_populates="project", uselist=False)
    project_geography = relationship("ProjectGeography", back_populates="project", uselist=False)
    team_members = relationship("TeamMember", back_populates="project")
    mentors = relationship("Mentor", back_populates="project")
    project_results = relationship("ProjectResult", back_populates="project")
    task_events = relationship("TaskEvent", back_populates="project")
    media_resources = relationship("MediaResource", back_populates="project")
    expenses = relationship("Expense", back_populates="project")
    own_funds = relationship("OwnFund", back_populates="project")
    partner_supports = relationship("PartnerSupport", back_populates="project")
    additional_files = relationship("AdditionalFile", back_populates="project")



 # Models for "General Information" Tab


class GeneralInfo(Base):
    __tablename__ = 'general_info'

    id_general_info = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    project_title = Column(String, nullable=False)
    region = Column(String, nullable=False)
    logo_path = Column(String)  # path to the logo file
    contacts = Column(Text, nullable=False)
    implementation_scale = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="general_info")


class AuthorInfo(Base):
    __tablename__ = 'author_info'

    id_author_info = Column(Integer, primary_key=True, index=True)
    experience = Column(Text, nullable=False)
    functionality_description = Column(Text, nullable=False)
    registration_address = Column(String, nullable=False)
    resume_path = Column(String)  # path to the resume file
    video_link = Column(String)  # URL to the video
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="author_info")


 # Models for "About the Project" Tab


class ProjectDetails(Base):
    __tablename__ = 'project_details'

    id_project_details = Column(Integer, primary_key=True, index=True)
    brief_info = Column(Text, nullable=False)
    problem_description = Column(Text, nullable=False)
    target_groups = Column(Text, nullable=False)
    main_goal = Column(Text, nullable=False)
    successful_experiences = Column(Text, nullable=False)
    development_perspectives = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="project_details")


class ProjectGeography(Base):
    __tablename__ = 'project_geography'

    id_project_geography = Column(Integer, primary_key=True, index=True)
    region_or_district = Column(String, nullable=False)
    address = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="project_geography")


 # Models for "Team" Tab


class TeamMember(Base):
    __tablename__ = 'team_members'

    id_team_member = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    resume_path = Column(String)  # path to the resume file
    competencies = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="team_members")


class Mentor(Base):
    __tablename__ = 'mentors'

    id_mentor = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    resume_path = Column(String)  # path to the resume file
    competencies = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="mentors")


 # Models for "Results" Tab


class ProjectResult(Base):
    __tablename__ = 'project_results'

    id_project_result = Column(Integer, primary_key=True, index=True)
    planned_date = Column(DateTime, nullable=False)
    event_count = Column(Integer, nullable=False)
    event_unit = Column(String, nullable=False)
    last_event_date = Column(DateTime, nullable=False)
    participant_count = Column(Integer, nullable=False)
    participant_unit = Column(String, nullable=False)
    publication_count = Column(Integer, nullable=False)
    publication_unit = Column(String, nullable=False)
    view_count = Column(Integer, nullable=False)
    view_unit = Column(String, nullable=False)
    social_effect = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="project_results")


 # Models for "Calendar Plan" Tab


class TaskEvent(Base):
    __tablename__ = 'task_events'

    id_task_event = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    event_name = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=False)
    event_description = Column(Text, nullable=False)
    unique_participants = Column(Integer, nullable=False)
    repeating_participants = Column(Integer, nullable=False)
    publication_count = Column(Integer, nullable=False)
    view_count = Column(Integer, nullable=False)
    additional_info = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="task_events")


 # Models for "Media" Tab


class MediaResource(Base):
    __tablename__ = 'media_resources'

    id_media_resource = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String, nullable=False)
    publication_month = Column(String, nullable=False)
    planned_views = Column(Integer, nullable=False)
    resource_links = Column(Text, nullable=False)
    chosen_format_reason = Column(Text, nullable=False)
    media_plan_path = Column(String)  # path to the detailed media plan file
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="media_resources")


 # Models for "Expenses" Tab


class Expense(Base):
    __tablename__ = 'expenses'

    id_expense = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    expense_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="expenses")


 # Models for "Co-financing" Tab


class OwnFund(Base):
    __tablename__ = 'own_funds'

    id_own_fund = Column(Integer, primary_key=True, index=True)
    expense_list = Column(Text, nullable=False)
    amount_rub = Column(Float, nullable=False)
    file_path = Column(String)  # path to the file
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="own_funds")


class PartnerSupport(Base):
    __tablename__ = 'partner_supports'

    id_partner_support = Column(Integer, primary_key=True, index=True)
    partner_name = Column(String, nullable=False)
    support_type = Column(String, nullable=False)
    expense_list = Column(Text, nullable=False)
    amount_rub = Column(Float, nullable=False)
    file_path = Column(String)  # path to the file
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="partner_supports")


 # Models for "Additional Files" Tab


class AdditionalFile(Base):
    __tablename__ = 'additional_files'

    id_additional_file = Column(Integer, primary_key=True, index=True)
    file_description = Column(Text, nullable=False)
    file_path = Column(String, nullable=False)  # path to the file
    project_id = Column(Integer, ForeignKey('projects.id_project'), nullable=False)

    project = relationship("Project", back_populates="additional_files")


class OtherAdditionalFile(Base):
    __tablename__ = 'other_additional_files'

    id_file = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_link = Column(String, nullable=False)  # ссылка на файл
    project_id = Column(Integer, ForeignKey('general_info.project_id'), nullable=False)  # связываем с проектом

    general_info = relationship("GeneralInfo", back_populates="other_additional_files")