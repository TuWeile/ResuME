from datetime import datetime
import time
from typing import List, Optional
from pydantic import BaseModel, Field

# Mainly Replaced [] with None for Optional[str/int] 
class Address(BaseModel):
    street: str = ""
    city: str = ""
    state: str = ""
    zip: str = ""
    country: str = ""


class PersonalInfo(BaseModel):
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    # address: Address = None
    date_of_birth: str = ""


class Experience(BaseModel):
    company: str = ""
    position: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    responsibilities: str = ""
    details: Optional[str] = None


class Education(BaseModel):
    institution: str = ""
    degree: str = ""
    major: str = ""
    minor: Optional[str] = None
    gpa: Optional[int] = None
    max_gpa: Optional[int] = None
    honours: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    details: Optional[str] = None


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = []
    role: str = ""
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Certification(BaseModel):
    title: str = ""
    achievement: str = ""
    date: Optional[str] = None


# not in use atm.
class Attachment(BaseModel):
    type: str
    file_name: str
    file_url: str
    uploaded_at: str


# not in use atm.
class Behavioural(BaseModel):
    question: str
    answer: str


class User(BaseModel):
    id: str = "" # = Field(alias="index_id")  // what does this do
    personalInfo: PersonalInfo = None
    address: Address = None
    experiences: Optional[List[Experience]] = []
    educations: Optional[List[Education]] = []
    projects: Optional[List[Project]] = []
    certifications: Optional[List[Certification]] = []
    biography: Optional[str] = ""
    motivations: Optional[str] = ""
    strengths: Optional[str] = ""
    weaknesses: Optional[str] = ""
    # attachments: Optional[List[Attachment]] = None
    linkedin: Optional[str] = ""
    website: Optional[str] = ""
    # behavioural: Optional[List[Behavioural]] = None
    behaviouralQuestions: Optional[List[str]] = []
    behaviouralAnswers: Optional[List[str]] = []
    skills: Optional[str] = ""
    created_at: int = int(time.time())
    deleted_by: int = int(time.time() + 172800)

    class Config:
        allow_population_by_field_name = True




class UserUpdateSearch(BaseModel):
    # id: Optional[str] # = Field(alias="index_id")  // what does this do
    personal_info: Optional[PersonalInfo] = None
    address: Optional[Address] = None
    experiences: Optional[List[Experience]] = None
    educations: Optional[List[Education]] = None
    projects: Optional[List[Project]] = None
    certifications: Optional[List[Certification]] = None
    biography: Optional[str] = None
    motivations: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    # attachments: Optional[List[Attachment]] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    # behavioural: Optional[List[Behavioural]] = None
    skills: Optional[str] = None
    # created_at: Optional[int]
    # deleted_by: Optional[int]

    class Config:
        allow_population_by_field_name = True

