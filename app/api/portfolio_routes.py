"""
Portfolio & Scraping API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.database.database import get_db
from app.database.models import User, Portfolio, Profile, PortfolioInfo
from app.auth.auth_service import get_current_user, AuthService
from app.portfolio.portfolio_generator import PortfolioGenerator
from app.scraping.scraper import LinkedInScraper, WebScraper

router = APIRouter(prefix="/api", tags=["portfolio"])

@router.post("/generate-portfolio")
def generate_portfolio(
    template_type: str = "faang",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized portfolio"""
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    user_data = {
        "name": current_user.full_name,
        "email": current_user.email,
        "bio": profile.career_goal,
        "skills": profile.current_skills,
        "github_url": profile.github_url or "https://github.com",
        "linkedin_url": profile.linkedin_url or "https://linkedin.com",
        "projects": [],
        "experience": [],
        "education": []
    }
    
    generator = PortfolioGenerator()
    portfolio_data = generator.generate_portfolio(user_data, template_type)
    
    # Save to database
    db_portfolio = Portfolio(
        user_id=current_user.id,
        template_type=template_type,
        html_content=portfolio_data["html_content"],
        css_content=portfolio_data["css_content"],
        sections={}
    )
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    
    return {
        "portfolio_id": db_portfolio.id,
        "template": template_type,
        "html": portfolio_data["html_content"],
        "css": portfolio_data["css_content"]
    }

@router.get("/portfolio")
def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's portfolio"""
    
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return {
        "id": portfolio.id,
        "template": portfolio.template_type,
        "is_published": portfolio.is_published,
        "created_at": portfolio.created_at
    }

# Portfolio Info Schemas
class PortfolioInfoSchema(BaseModel):
    phone: str
    city: str
    state: str
    country: str
    professional_summary: Optional[str] = None
    email: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None  # optional link to user's portfolio/website
    twitter_url: Optional[str] = None
    personal_website: Optional[str] = None
    highest_degree: str
    university: str
    major: str
    graduation_year: Optional[int] = None
    additional_certifications: Optional[str] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    total_experience: int = 0
    work_experience: Optional[str] = None
    achievements: Optional[str] = None
    projects: Optional[str] = None
    languages: Optional[str] = None

class PortfolioInfoResponse(PortfolioInfoSchema):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/portfolio-info")
async def get_portfolio_info(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get portfolio information for current user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        token_data = AuthService.verify_token(token)
        user = db.query(User).filter(User.email == token_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    portfolio_info = db.query(PortfolioInfo).filter(
        PortfolioInfo.user_id == user_id
    ).first()
    
    if not portfolio_info:
        raise HTTPException(status_code=404, detail="Portfolio information not found")
    
    return portfolio_info

@router.post("/portfolio-info")
async def save_portfolio_info(
    portfolio_data: PortfolioInfoSchema,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Save or update portfolio information for current user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        token_data = AuthService.verify_token(token)
        user = db.query(User).filter(User.email == token_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find existing portfolio info or create new one
    portfolio_info = db.query(PortfolioInfo).filter(
        PortfolioInfo.user_id == user_id
    ).first()
    
    if portfolio_info:
        # Update existing
        for field, value in portfolio_data.dict().items():
            setattr(portfolio_info, field, value)
        portfolio_info.updated_at = datetime.utcnow()
    else:
        # Create new
        portfolio_info = PortfolioInfo(
            user_id=user_id,
            **portfolio_data.dict()
        )
        db.add(portfolio_info)
    
    try:
        db.commit()
        db.refresh(portfolio_info)
        return portfolio_info
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save portfolio: {str(e)}")

@router.delete("/portfolio-info")
async def delete_portfolio_info(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Delete portfolio information for current user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        token_data = AuthService.verify_token(token)
        user = db.query(User).filter(User.email == token_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    portfolio_info = db.query(PortfolioInfo).filter(
        PortfolioInfo.user_id == user_id
    ).first()
    
    if not portfolio_info:
        raise HTTPException(status_code=404, detail="Portfolio information not found")
    
    try:
        db.delete(portfolio_info)
        db.commit()
        return {"message": "Portfolio information deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete portfolio: {str(e)}")


@router.post("/generate-portfolio-html")
async def generate_portfolio_html(
    data: dict,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Generate portfolio HTML from portfolio info"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.replace("Bearer ", "")
        token_data = AuthService.verify_token(token)
        user = db.query(User).filter(User.email == token_data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    # Get portfolio info
    portfolio_info = db.query(PortfolioInfo).filter(
        PortfolioInfo.user_id == user_id
    ).first()
    
    if not portfolio_info:
        raise HTTPException(status_code=404, detail="Portfolio information not found. Please fill out your portfolio information first.")
    
    # Get user for name
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate HTML
    template_type = data.get('template', 'faang')

    # Build user_data for PortfolioGenerator
    # Normalize projects, experience, skills
    projects = []
    if portfolio_info.projects:
        if isinstance(portfolio_info.projects, list):
            projects = portfolio_info.projects
        else:
            # split lines into simple project entries
            lines = [l.strip() for l in str(portfolio_info.projects).splitlines() if l.strip()]
            for ln in lines:
                projects.append({"title": ln if len(ln) < 60 else ln[:57] + '...', "description": ln, "skills": []})

    experience = []
    if portfolio_info.work_experience:
        if isinstance(portfolio_info.work_experience, list):
            experience = portfolio_info.work_experience
        else:
            lines = [l.strip() for l in str(portfolio_info.work_experience).splitlines() if l.strip()]
            if len(lines) == 1:
                experience = [{"title": portfolio_info.current_title or "", "company": portfolio_info.current_company or "", "duration": f"{portfolio_info.total_experience} years" if portfolio_info.total_experience else "", "description": lines[0]}]
            else:
                for ln in lines:
                    experience.append({"title": portfolio_info.current_title or "", "company": portfolio_info.current_company or "", "duration": f"{portfolio_info.total_experience} years" if portfolio_info.total_experience else "", "description": ln})

    # Skills from Profile (if available)
    skills = []
    try:
        from app.database.models import Profile
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        if profile and profile.current_skills:
            skills = profile.current_skills if isinstance(profile.current_skills, list) else []
    except Exception:
        skills = []

    user_data = {
        "name": user.full_name or user.username or "",
        "email": portfolio_info.email or user.email,
        "phone": portfolio_info.phone or "",
        "location": f"{portfolio_info.city or ''}, {portfolio_info.state or ''}".strip(', '),
        "bio": portfolio_info.professional_summary or f"{user.full_name} is a {portfolio_info.current_title or 'professional'}.",
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": [{"degree": portfolio_info.highest_degree or "", "field": portfolio_info.major or "", "institution": portfolio_info.university or "", "year": portfolio_info.graduation_year}] if (portfolio_info.highest_degree or portfolio_info.university) else [] ,
        "github_url": portfolio_info.github_url or user.github_url or "#",
        "linkedin_url": portfolio_info.linkedin_url or user.linkedin_url or "#"
    }

    generator = PortfolioGenerator()
    portfolio_generated = generator.generate_portfolio(user_data, template_type)
    html_content = portfolio_generated.get("html_content")
    css_content = portfolio_generated.get("css_content")
    
    # Save portfolio record
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).first()
    
    if portfolio:
        portfolio.template_type = template_type
        portfolio.html_content = html_content
        portfolio.css_content = css_content
        portfolio.updated_at = datetime.utcnow()
    else:
        portfolio = Portfolio(
            user_id=user_id,
            template_type=template_type,
            html_content=html_content,
            css_content=css_content
        )
        db.add(portfolio)
    
    try:
        db.commit()
        db.refresh(portfolio)
        return {
            "id": portfolio.id,
            "template": template_type,
            "html": html_content
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate portfolio: {str(e)}")


def _generate_portfolio_html(user, portfolio_info, template_type='faang', db=None):
    """Generate HTML from portfolio info"""
    
    # Build contact info
    phone_html = f"<a href='tel:{portfolio_info.phone}'>{portfolio_info.phone}</a>" if portfolio_info.phone else ""
    linkedin_html = f"<a href='{portfolio_info.linkedin_url}'>LinkedIn</a>" if portfolio_info.linkedin_url else ""
    github_html = f"<a href='{portfolio_info.github_url}'>GitHub</a>" if portfolio_info.github_url else ""
    email_html = f"<a href='mailto:{portfolio_info.email}'>{portfolio_info.email}</a>"
    
    # Build sections
    summary_html = ""
    if portfolio_info.professional_summary:
        summary_html = f'''
        <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
            <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">About</h2>
            <p>{portfolio_info.professional_summary}</p>
        </section>
        '''
    else:
        # Auto-generate a short professional summary if none provided
        try:
            from app.database.models import Profile
            profile = db.query(Profile).filter(Profile.user_id == user.id).first() if db is not None else None
            skills = profile.current_skills if profile and isinstance(profile.current_skills, list) else []
        except Exception:
            skills = []

        gen_summary = f"{user.full_name} is a {portfolio_info.current_title or 'driven professional'} with {portfolio_info.total_experience} years of experience in {portfolio_info.major or 'their field'}."
        if skills:
            gen_summary += ' Skilled in ' + ', '.join(skills[:6]) + '.'
        gen_summary += ' Passionate about building impactful solutions and continuously learning.'

        summary_html = f'''
        <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
            <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">About</h2>
            <p>{gen_summary}</p>
        </section>
        '''
    
    # Experience
    experience_html = ""
    work_exp = portfolio_info.work_experience
    work_list = []
    # Normalize work_experience: accept list[dict] or string (multi-line)
    if work_exp:
        if isinstance(work_exp, list):
            work_list = work_exp
        elif isinstance(work_exp, str):
            # Treat the whole string as a single experience description if detailed,
            # otherwise split lines and create simple entries
            lines = [l.strip() for l in work_exp.splitlines() if l.strip()]
            if len(lines) == 1:
                work_list = [{
                    'title': portfolio_info.current_title or '',
                    'company': portfolio_info.current_company or '',
                    'years': f"{portfolio_info.total_experience} years" if portfolio_info.total_experience else '',
                    'description': lines[0]
                }]
            else:
                # Multiple lines -> create entries with description from each line
                for ln in lines:
                    work_list.append({
                        'title': portfolio_info.current_title or '',
                        'company': portfolio_info.current_company or '',
                        'years': f"{portfolio_info.total_experience} years" if portfolio_info.total_experience else '',
                        'description': ln
                    })

    if work_list:
        exp_items = ""
        for exp in work_list:
            title = exp.get('title', '') if isinstance(exp, dict) else ''
            company = exp.get('company', '') if isinstance(exp, dict) else ''
            years = exp.get('years', '') if isinstance(exp, dict) else ''
            description = exp.get('description', '') if isinstance(exp, dict) else str(exp)
            exp_items += f'''
            <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #ddd;">
                <div style="font-weight: bold; font-size: 1.1em;">{title}</div>
                <div style="color: #667eea; font-weight: 600;">{company}</div>
                <div style="color: #666; font-style: italic;">{years}</div>
                <p>{description}</p>
            </div>
            '''

        experience_html = f'''
        <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
            <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">Experience</h2>
            {exp_items}
        </section>
        '''
    
    # Education
    education_html = f'''
    <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
        <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">Education</h2>
        <div style="margin-bottom: 20px;">
            <div style="font-weight: bold; font-size: 1.1em;">{portfolio_info.highest_degree}</div>
            <div style="color: #667eea; font-weight: 600;">{portfolio_info.university}</div>
            <div style="color: #666;">Major: {portfolio_info.major}</div>
            {f"<div style='color: #666;'>Graduation: {portfolio_info.graduation_year}</div>" if portfolio_info.graduation_year else ""}
        </div>
    </section>
    '''
    
    # Skills - Try to get from database
    skills_html = ""
    try:
        from app.database.models import Profile
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        if profile and profile.current_skills:
            skills = profile.current_skills if isinstance(profile.current_skills, list) else []
            skills_items = "".join([f'<span style="background: #667eea; color: white; padding: 8px 15px; border-radius: 20px; margin: 5px; display: inline-block;">{skill}</span>' for skill in skills])
            skills_html = f'''
            <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
                <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">Skills</h2>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    {skills_items}
                </div>
            </section>
            '''
    except:
        pass
    
    # Achievements
    achievements_html = ""
    ach = portfolio_info.achievements
    ach_list = []
    if ach:
        if isinstance(ach, list):
            ach_list = ach
        elif isinstance(ach, str):
            lines = [l.strip() for l in ach.splitlines() if l.strip()]
            ach_list = [{'title': ln, 'description': ''} for ln in lines]

    if ach_list:
        achievement_items = ""
        for achievement in ach_list:
            title = achievement.get('title', '') if isinstance(achievement, dict) else str(achievement)
            description = achievement.get('description', '') if isinstance(achievement, dict) else ''
            achievement_items += f'''
            <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #ddd;">
                <div style="font-weight: bold; font-size: 1.1em;">{title}</div>
                <p>{description}</p>
            </div>
            '''
        
        achievements_html = f'''
        <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
            <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">Achievements</h2>
            {achievement_items}
        </section>
        '''
    
    # Languages
    languages_html = ""
    langs = portfolio_info.languages
    lang_list = []
    if langs:
        if isinstance(langs, list):
            lang_list = langs
        elif isinstance(langs, str):
            lines = [l.strip() for l in langs.splitlines() if l.strip()]
            lang_list = [{'language': ln, 'proficiency': ''} for ln in lines]

    if lang_list:
        lang_items = ""
        for lang in lang_list:
            language = lang.get('language', '') if isinstance(lang, dict) else str(lang)
            proficiency = lang.get('proficiency', '') if isinstance(lang, dict) else ''
            lang_items += f'''
            <div style="margin-bottom: 10px;">
                <strong>{language}</strong>{(' - ' + proficiency) if proficiency else ''}
            </div>
            '''
        
        languages_html = f'''
        <section style="background: #f8f9fa; padding: 30px; border-radius: 8px; margin-bottom: 40px;">
            <h2 style="font-size: 1.5em; color: #667eea; margin-bottom: 15px;">Languages</h2>
            {lang_items}
        </section>
        '''
    
    # Main HTML
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{user.full_name} - Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 20px; }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
            margin-bottom: 40px;
            border-radius: 8px;
        }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .contact-info {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .contact-info a {{
            color: white;
            text-decoration: none;
            border-bottom: 2px solid white;
            padding-bottom: 5px;
        }}
        section {{ margin-bottom: 40px; }}
        h2 {{ font-size: 1.8em; color: #667eea; margin-bottom: 20px; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        footer {{
            text-align: center;
            padding: 30px;
            color: #666;
            margin-top: 50px;
            border-top: 2px solid #eee;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{user.full_name}</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">{portfolio_info.current_title or 'Professional'} {f"at {portfolio_info.current_company}" if portfolio_info.current_company else ""}</p>
        <div class="contact-info">
            {email_html}
            {phone_html}
            {linkedin_html}
            {github_html}
        </div>
    </header>
    
    <div class="container">
        {summary_html}
        {experience_html}
        {education_html}
        {skills_html}
        {achievements_html}
        {languages_html}
    </div>
    
    <footer>
        <p>&copy; 2024 {user.full_name}. All rights reserved.</p>
    </footer>
</body>
</html>
    '''
    
    return html_content
