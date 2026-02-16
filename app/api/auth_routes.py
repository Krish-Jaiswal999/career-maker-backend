"""
Authentication & User Management API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.database import get_db
from app.database.models import User, Profile
from app.schemas import UserCreate, UserLogin, UserOut, Token, ProfileCreate, ProfileOut
from app.auth.auth_service import AuthService, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        password_hash=AuthService.hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = AuthService.create_access_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.from_orm(db_user)
    }

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not AuthService.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = AuthService.create_access_token(
        data={"sub": user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.from_orm(db_user)
    }

@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserOut.from_orm(current_user)

@router.post("/profile", response_model=ProfileOut)
def create_profile(
    profile: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create/update user profile"""
    
    existing_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    
    if existing_profile:
        # Update existing profile
        existing_profile.career_goal = profile.career_goal
        existing_profile.current_skills = profile.current_skills
        existing_profile.years_experience = profile.years_experience
        existing_profile.linkedin_url = profile.linkedin_url
        existing_profile.github_url = profile.github_url
    else:
        # Create new profile
        existing_profile = Profile(
            user_id=current_user.id,
            career_goal=profile.career_goal,
            current_skills=profile.current_skills,
            years_experience=profile.years_experience,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url
        )
        db.add(existing_profile)
    
    db.commit()
    db.refresh(existing_profile)
    
    return ProfileOut.from_orm(existing_profile)

@router.get("/profile", response_model=ProfileOut)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return ProfileOut.from_orm(profile)
