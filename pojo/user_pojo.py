from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    country: str


class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Address
    date_of_birth: datetime


class Experience(BaseModel):
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    responsibilities: str
    details: Optional[str] = None


class Education(BaseModel):
    institution: str
    degree: str
    major: str
    minor: Optional[str] = None
    gpa: Optional[int] = None
    max_gpa: Optional[int] = None
    honours: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    details: Optional[str] = None


class Project(BaseModel):
    name: str
    description: str
    technologies: List[str]
    role: str
    url: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None


class Certification(BaseModel):
    title: str
    achievement: str
    date: datetime


class Attachment(BaseModel):
    type: str
    file_name: str
    file_url: str
    uploaded_at: datetime


class Behavioural(BaseModel):
    question: str
    answer: str


class User(BaseModel):
    id: str # = Field(alias="index_id")  // what does this do
    personal_info: PersonalInfo
    experiences: Optional[List[Experience]] = None
    educations: Optional[List[Education]] = None
    projects: Optional[List[Project]] = None
    certifications: Optional[List[Certification]] = None
    biography: Optional[str] = None
    motivations: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    behavioural: Optional[List[Behavioural]] = None
    skills: Optional[str] = None
    created_at: int
    deleted_by: int

    class Config:
        allow_population_by_field_name = True


class UserUpdateSearch(BaseModel):
    # id: Optional[str] # = Field(alias="index_id")  // what does this do
    personal_info: Optional[PersonalInfo] = None
    experiences: Optional[List[Experience]] = None
    educations: Optional[List[Education]] = None
    projects: Optional[List[Project]] = None
    certifications: Optional[List[Certification]] = None
    biography: Optional[str] = None
    motivations: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    behavioural: Optional[List[Behavioural]] = None
    skills: Optional[str] = None
    # created_at: Optional[int]
    # deleted_by: Optional[int]

    class Config:
        allow_population_by_field_name = True
