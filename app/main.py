"""
Main FastAPI Application
Career Path Planner Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()

from app.database.database import engine, Base
from app.database.models import User, Profile, Roadmap, UserProject, Portfolio, LinkedInProfile, ProgressTracker, PortfolioInfo
from app.api import auth_routes, ai_routes, portfolio_routes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GenAI Career Path Planner",
    description="AI-powered career path planning and roadmap generation",
    version="1.0.0"
)

# CORS middleware
# For development/testing allow all origins to avoid preflight issues.
# In production set ALLOWED_ORIGINS in .env and restore stricter policy.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(ai_routes.router)
app.include_router(portfolio_routes.router)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to GenAI Career Path Planner API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/auth/signup, /api/auth/login, /api/auth/me, /api/auth/profile",
            "ai": "/api/analyze-career, /api/generate-roadmap, /api/user-roadmap",
            "portfolio": "/api/generate-portfolio, /api/portfolio",
            "resources": "/api/learning-resources/{skill}, /api/trending-projects/{language}"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
