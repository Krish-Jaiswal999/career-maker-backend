"""
Authentication & User Management API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

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

# Password Reset Endpoints

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    """
    Request password reset - sends OTP to email
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If email exists, OTP has been sent"}
    
    # Generate OTP and send email
    otp = AuthService.generate_otp()
    user.reset_otp = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    user.otp_attempts = 0
    db.commit()
    
    # Send OTP email
    from app.email_service import EmailService
    email_service = EmailService()
    email_service.send_otp_email(user.email, otp, user.full_name)
    
    return {"message": "If email exists, OTP has been sent"}

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    """
    Verify OTP sent to user's email
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check OTP
    if not user.reset_otp or not user.otp_expiry:
        raise HTTPException(status_code=400, detail="No password reset request found")
    
    if datetime.utcnow() > user.otp_expiry:
        user.reset_otp = None
        user.otp_expiry = None
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired. Request a new one.")
    
    if user.otp_attempts >= 3:
        raise HTTPException(status_code=429, detail="Too many failed attempts. Request a new OTP.")
    
    if user.reset_otp != otp:
        user.otp_attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    return {"message": "OTP verified successfully", "verified": True}

@router.post("/reset-password")
def reset_password(email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    """
    Reset password using verified OTP
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify OTP
    if not user.reset_otp or not user.otp_expiry:
        raise HTTPException(status_code=400, detail="No password reset request found")
    
    if datetime.utcnow() > user.otp_expiry:
        user.reset_otp = None
        user.otp_expiry = None
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired. Request a new one.")
    
    if user.reset_otp != otp:
        user.otp_attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Validate new password
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    # Update password
    user.password_hash = AuthService.hash_password(new_password)
    user.reset_otp = None
    user.otp_expiry = None
    user.otp_attempts = 0
    db.commit()
    
    # Send confirmation email
    from app.email_service import EmailService
    email_service = EmailService()
    email_service.send_password_reset_confirmation(user.email, user.full_name)
    
    return {"message": "Password reset successfully"}
