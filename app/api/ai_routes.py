"""
AI & Roadmap Generation API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User, Roadmap, Profile
from app.auth.auth_service import get_current_user
from app.schemas import RoadmapCreate
from app.ai_engine.career_analyzer import CareerAnalyzer, RoadmapGenerator
from app.ai_engine.skill_matcher import SkillMatcher

router = APIRouter(prefix="/api", tags=["ai"])

@router.get("/analyze-career")
def analyze_career(
    career_goal: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze career goal and skill gaps"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    analyzer = CareerAnalyzer()
    gaps = analyzer.detect_skill_gaps(career_goal, profile.current_skills)
    trajectory = analyzer.map_career_trajectory(career_goal)
    
    return {
        "analysis": gaps,
        "trajectory": trajectory
    }

@router.post("/generate-roadmap")
def generate_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized learning roadmap"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    generator = RoadmapGenerator()
    roadmap_data = generator.generate_roadmap(
        career_goal=profile.career_goal,
        current_skills=profile.current_skills,
        years_exp=profile.years_experience
    )
    
    # Save roadmap to database
    db_roadmap = Roadmap(
        user_id=current_user.id,
        goal=profile.career_goal,
        phases=roadmap_data["phases"]
    )
    db.add(db_roadmap)
    db.commit()
    db.refresh(db_roadmap)
    
    return {
        "roadmap_id": db_roadmap.id,
        "roadmap": roadmap_data
    }

@router.get("/user-roadmap")
def get_user_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's current roadmap"""
    
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    return {
        "id": roadmap.id,
        "goal": roadmap.goal,
        "phases": roadmap.phases,
        "created_at": roadmap.created_at
    }

@router.get("/match-skills")
def match_skills(
    career_goal: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Match skills to career goal"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    matcher = SkillMatcher()
    match_result = matcher.match_skills_to_career(profile.current_skills, career_goal)
    
    return match_result

@router.post("/recommend-projects")
def recommend_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project recommendations"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    matcher = SkillMatcher()
    projects = matcher.recommend_projects(profile.current_skills, profile.career_goal)
    
    return {"projects": projects}

@router.get("/recommend-resources")
def recommend_resources(
    skill: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get learning resources for a specific skill or all recommended skills"""
    
    matcher = SkillMatcher()
    
    if skill:
        # Get resources for specific skill
        resources = matcher.recommend_resources(skill)
        return {"skill": skill, "resources": resources}
    else:
        # Get resources for all gaps in user's roadmap
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        analyzer = CareerAnalyzer()
        gaps = analyzer.detect_skill_gaps(profile.career_goal, profile.current_skills)
        
        all_resources = {}
        for skill in gaps["skill_gaps"]:
            all_resources[skill] = matcher.recommend_resources(skill)
        
        return {
            "career_goal": profile.career_goal,
            "skills_to_learn": gaps["skill_gaps"],
            "resources": all_resources
        }

@router.get("/learning-path")
def get_learning_path(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive learning path with all resources"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    analyzer = CareerAnalyzer()
    gaps = analyzer.detect_skill_gaps(profile.career_goal, profile.current_skills)
    
    matcher = SkillMatcher()
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).first()
    
    # Build complete learning path with resources for each skill
    skills_with_resources = []
    for skill in gaps["skill_gaps"]:
        skill_data = {
            "skill": skill,
            "resources": matcher.recommend_resources(skill),
            "status": "to-learn"
        }
        skills_with_resources.append(skill_data)
    
    current_skills_data = []
    for skill in profile.current_skills:
        current_skills_data.append({
            "skill": skill,
            "status": "learned"
        })
    
    return {
        "career_goal": profile.career_goal,
        "current_skills": current_skills_data,
        "skills_to_learn": skills_with_resources,
        "total_skills_needed": len(gaps["skill_gaps"]) + len(profile.current_skills),
        "progress_percentage": gaps["completion_percentage"],
        "roadmap": roadmap.phases if roadmap else None
    }
