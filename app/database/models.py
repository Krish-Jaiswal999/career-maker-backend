from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Password reset OTP fields
    reset_otp = Column(String, nullable=True)  # One-time password for password reset
    otp_expiry = Column(DateTime, nullable=True)  # When OTP expires (10 minutes from generation)
    otp_attempts = Column(Integer, default=0)  # Track failed OTP attempts
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    roadmaps = relationship("Roadmap", back_populates="user")
    projects = relationship("UserProject", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")
    portfolio_info = relationship("PortfolioInfo", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    career_goal = Column(Text)
    current_skills = Column(JSON)  # ["Python", "JavaScript", ...]
    years_experience = Column(Integer, default=0)
    linkedin_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")

class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    goal = Column(String)
    phases = Column(JSON)  # Complex nested structure
    completed_phases = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="roadmaps")

class UserProject(Base):
    __tablename__ = "user_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    skills = Column(JSON)  # ["Python", "Flask", ...]
    status = Column(String, default="not-started")  # not-started, in-progress, completed
    github_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="projects")

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    template_type = Column(String)  # faang, startup, researcher, open-source
    html_content = Column(Text)
    css_content = Column(Text, nullable=True)
    sections = Column(JSON)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="portfolios")

class LinkedInProfile(Base):
    __tablename__ = "linkedin_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    profile_url = Column(String, unique=True, index=True)
    name = Column(String)
    headline = Column(String)
    education = Column(JSON)
    experience = Column(JSON)
    skills = Column(JSON)
    certifications = Column(JSON)
    analysis = Column(JSON)
    scraped_at = Column(DateTime, default=datetime.utcnow)

class ProgressTracker(Base):
    __tablename__ = "progress_tracker"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_name = Column(String)
    proficiency_level = Column(String)  # beginner, intermediate, advanced, expert
    completed_projects = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PortfolioInfo(Base):
    __tablename__ = "portfolio_info"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Personal Information
    phone = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    professional_summary = Column(Text, nullable=True)
    
    # Contact & Social
    email = Column(String)
    linkedin_url = Column(String, nullable=True)  # optional
    github_url = Column(String, nullable=True)    # optional
    portfolio_url = Column(String, nullable=True)  # optional; make website link optional per requirement
    twitter_url = Column(String, nullable=True)   # optional
    personal_website = Column(String, nullable=True)  # optional
    
    # Education
    highest_degree = Column(String)  # High School, Bachelor, Master, PhD
    university = Column(String)
    major = Column(String)
    graduation_year = Column(Integer, nullable=True)
    additional_certifications = Column(JSON, nullable=True)  # [{name, issuer, date}]
    
    # Professional Experience
    current_title = Column(String, nullable=True)
    current_company = Column(String, nullable=True)
    total_experience = Column(Integer, default=0)  # Years
    work_experience = Column(JSON, nullable=True)  # [{title, company, years, description}]
    
    # Achievements & Awards
    achievements = Column(JSON, nullable=True)  # [{title, description, date}]
    projects = Column(JSON, nullable=True)  # [{name, description, skills, link}]
    
    # Languages
    languages = Column(JSON, nullable=True)  # [{language, proficiency}]
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="portfolio_info")
