from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    email: Optional[str] = None

# Profile Schemas
class ProfileCreate(BaseModel):
    career_goal: str
    current_skills: List[str]
    years_experience: int = 0
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class ProfileUpdate(BaseModel):
    career_goal: Optional[str] = None
    current_skills: Optional[List[str]] = None
    years_experience: Optional[int] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class ProfileOut(ProfileCreate):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Roadmap Schemas
class RoadmapPhase(BaseModel):
    phase: str
    skills: List[str]
    projects: List[str]
    resources: List[str]
    duration: str
    order: int

class RoadmapCreate(BaseModel):
    goal: str

class RoadmapOut(BaseModel):
    id: int
    user_id: int
    goal: str
    phases: List[RoadmapPhase]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project Schemas
class ProjectCreate(BaseModel):
    title: str
    description: str
    skills: List[str]

class ProjectUpdate(BaseModel):
    status: str
    github_link: Optional[str] = None

class ProjectOut(ProjectCreate):
    id: int
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Portfolio Schemas
class PortfolioCreate(BaseModel):
    template_type: str

class PortfolioOut(BaseModel):
    id: int
    user_id: int
    template_type: str
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Progress Tracker
class ProgressTrackerOut(BaseModel):
    id: int
    user_id: int
    skill_name: str
    proficiency_level: str
    completed_projects: int
    
    class Config:
        from_attributes = True
