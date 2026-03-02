from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
import hashlib
import secrets

from app.database.database import get_db
from app.database.models import User
from app.schemas import TokenData
from app.email_service import EmailService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        # Hash with SHA256 first (standard for bcrypt's 72-byte limit)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # Then bcrypt hash the SHA256 result (64 bytes)
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password_hash.encode(), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # Hash the plain password the same way
        password_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        try:
            return bcrypt.checkpw(password_hash.encode(), hashed_password.encode())
        except Exception:
            return False
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        return token_data
    
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    @staticmethod
    def create_password_reset_request(user: User) -> bool:
        """
        Create a password reset OTP for user
        
        Args:
            user: User object to create OTP for
            
        Returns:
            True if successful
        """
        from app.database.database import SessionLocal
        
        try:
            db = SessionLocal()
            otp = AuthService.generate_otp()
            user.reset_otp = otp
            user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
            user.otp_attempts = 0
            db.commit()
            
            # Send OTP email
            email_service = EmailService()
            email_service.send_otp_email(user.email, otp, user.full_name)
            
            db.close()
            return True
        except Exception as e:
            print(f"Error creating password reset: {str(e)}")
            return False
    
    @staticmethod
    def verify_otp(user: User, otp: str) -> bool:
        """
        Verify OTP for password reset
        
        Args:
            user: User object
            otp: OTP to verify
            
        Returns:
            True if OTP is valid and not expired
        """
        if not user.reset_otp or not user.otp_expiry:
            return False
        
        if datetime.utcnow() > user.otp_expiry:
            return False
        
        if user.otp_attempts >= 3:
            return False
        
        return user.reset_otp == otp
    
    @staticmethod
    def clear_otp(user: User) -> None:
        """Clear OTP and expiry from user"""
        from app.database.database import SessionLocal
        
        db = SessionLocal()
        user.reset_otp = None
        user.otp_expiry = None
        user.otp_attempts = 0
        db.commit()
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    token_data = AuthService.verify_token(token)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
