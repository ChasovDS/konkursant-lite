from pydantic import BaseModel, HttpUrl
from typing import Optional, List
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
    status: str

    class Config:
        from_attributes = True


class OtherAdditionalFileCreate(BaseModel):
    file_name: str
    file_link: HttpUrl
    project_id: int

    class Config:
        from_attributes = True


class GeneralInfoCreate(BaseModel):
    full_name: str
    project_title: str
    region: str
    logo_path: Optional[str]
    contacts: str
    implementation_scale: str
    start_date: datetime
    end_date: datetime


class GeneralInfo(BaseModel):
    id_general_info: int
    full_name: str
    project_title: str
    region: str
    logo_path: Optional[str]
    contacts: str
    implementation_scale: str
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True


# Схемы для таблицы "Дополнительная информация об авторе проекта"


class AuthorInfoCreate(BaseModel):
    experience: str
    functionality_description: str
    registration_address: str
    resume_path: Optional[str]
    video_link: Optional[HttpUrl]


class AuthorInfo(BaseModel):
    id_author_info: int
    experience: str
    functionality_description: str
    registration_address: str
    resume_path: Optional[str]
    video_link: Optional[HttpUrl]

    class Config:
        from_attributes = True


# Схемы для таблицы "Информация о проекте"


class ProjectDetailsCreate(BaseModel):
    brief_info: str
    problem_description: str
    target_groups: str
    main_goal: str
    successful_experiences: str
    development_perspectives: str


class ProjectDetails(BaseModel):
    id_project_details: int
    brief_info: str
    problem_description: str
    target_groups: str
    main_goal: str
    successful_experiences: str
    development_perspectives: str

    class Config:
        from_attributes = True


# Схемы для таблицы "География проекта"


class ProjectGeographyCreate(BaseModel):
    region_or_district: str
    address: str


class ProjectGeography(BaseModel):
    id_project_geography: int
    region_or_district: str
    address: str

    class Config:
        from_attributes = True


# Схемы для таблицы "Команда"


class TeamMemberCreate(BaseModel):
    full_name: str
    email: str
    role: str
    resume_path: Optional[str]
    competencies: str


class TeamMember(BaseModel):
    id_team_member: int
    full_name: str
    email: str
    role: str
    resume_path: Optional[str]
    competencies: str

    class Config:
        from_attributes = True


# Схемы для таблицы "Наставники"


class MentorCreate(BaseModel):
    full_name: str
    email: str
    role: str
    resume_path: Optional[str]
    competencies: str


class Mentor(BaseModel):
    id_mentor: int
    full_name: str
    email: str
    role: str
    resume_path: Optional[str]
    competencies: str

    class Config:
        from_attributes = True


# Схемы для таблицы "Результаты"


class ProjectResultCreate(BaseModel):
    planned_date: datetime
    event_count: int
    event_unit: str
    last_event_date: datetime
    participant_count: int
    participant_unit: str
    publication_count: int
    publication_unit: str
    view_count: int
    view_unit: str
    social_effect: str


class ProjectResult(BaseModel):
    id_project_result: int
    planned_date: datetime
    event_count: int
    event_unit: str
    last_event_date: datetime
    participant_count: int
    participant_unit: str
    publication_count: int
    publication_unit: str
    view_count: int
    view_unit: str
    social_effect: str

    class Config:
        from_attributes = True


# Схемы для таблицы "Календарный план"


class TaskEventCreate(BaseModel):
    task: str
    event_name: str
    deadline: datetime
    event_description: str
    unique_participants: int
    repeating_participants: int
    publication_count: int
    view_count: int
    additional_info: Optional[str]


class TaskEvent(BaseModel):
    id_task_event: int
    task: str
    event_name: str
    deadline: datetime
    event_description: str
    unique_participants: int
    repeating_participants: int
    publication_count: int
    view_count: int
    additional_info: Optional[str]

    class Config:
        from_attributes = True


# Схемы для таблицы "Медиа"


class MediaResourceCreate(BaseModel):
    resource_type: str
    publication_month: str
    planned_views: int
    resource_links: str
    chosen_format_reason: str
    media_plan_path: Optional[str]


class MediaResource(BaseModel):
    id_media_resource: int
    resource_type: str
    publication_month: str
    planned_views: int
    resource_links: str
    chosen_format_reason: str
    media_plan_path: Optional[str]

    class Config:
        from_attributes = True


# Схемы для таблицы "Расходы"


class ExpenseCreate(BaseModel):
    total_amount: float
    category: str
    expense_type: str
    name: str
    description: str
    quantity: int
    unit_price: float
    amount: float


class Expense(BaseModel):
    id_expense: int
    total_amount: float
    category: str
    expense_type: str
    name: str
    description: str
    quantity: int
    unit_price: float
    amount: float

    class Config:
        from_attributes = True


# Схемы для таблицы "Софинансирование"


class OwnFundCreate(BaseModel):
    expense_list: str
    amount_rub: float
    file_path: Optional[str]


class OwnFund(BaseModel):
    id_own_fund: int
    expense_list: str
    amount_rub: float
    file_path: Optional[str]

    class Config:
        from_attributes = True


class PartnerSupportCreate(BaseModel):
    partner_name: str
    support_type: str
    expense_list: str
    amount_rub: float
    file_path: Optional[str]


class PartnerSupport(BaseModel):
    id_partner_support: int
    partner_name: str
    support_type: str
    expense_list: str
    amount_rub: float
    file_path: Optional[str]

    class Config:
        from_attributes = True


# Схемы для таблицы "Доп. Файлы"


class AdditionalFileCreate(BaseModel):
    file_description: str
    file_path: str


class AdditionalFile(BaseModel):
    id_additional_file: int
    file_description: str
    file_path: str

    class Config:
        from_attributes = True



class CompleteProjectInfo(BaseModel):
    # Поля из Project
    id_project: int
    title: str
    description: Optional[str]
    file_path: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
    status: str

    # Поля из GeneralInfo
    id_general_info: int
    full_name: str
    project_title: str
    region: str
    logo_path: Optional[str]
    contacts: str
    implementation_scale: str
    start_date: datetime
    end_date: datetime

    # Поля из AuthorInfo
    id_author_info: int
    experience: str
    functionality_description: str
    registration_address: str
    resume_path: Optional[str]
    video_link: Optional[HttpUrl]

    # Поля из ProjectDetails
    id_project_details: int
    brief_info: str
    problem_description: str
    target_groups: str
    main_goal: str
    successful_experiences: str
    development_perspectives: str

    # Поля из ProjectGeography
    project_geographies: List[ProjectGeography]  # Список географий проекта

    # Поля из TeamMember
    team_members: List[TeamMember]  # Список участников команды

    # Поля из Mentor
    mentors: List[Mentor]  # Список наставников

    # Поля из ProjectResult
    project_results: List[ProjectResult]  # Список результатов проекта

    # Поля из TaskEvent
    task_events: List[TaskEvent]  # Список событий

    # Поля из MediaResource
    media_resources: List[MediaResource]  # Список медиа ресурсов

    # Поля из Expense
    expenses: List[Expense]  # Список расходов

    # Поля из OwnFund
    own_funds: List[OwnFund]  # Список собственных средств

    # Поля из PartnerSupport
    partner_supports: List[PartnerSupport]  # Список партнерской поддержки

    # Поля из AdditionalFile
    additional_files: List[AdditionalFile]  # Список дополнительных файлов

    class Config:
        from_attributes = True
