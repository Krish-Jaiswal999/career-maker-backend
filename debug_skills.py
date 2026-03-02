from app.database.database import SessionLocal
from app.database.models import Profile, Roadmap
from app.ai_engine.career_analyzer import CareerAnalyzer, RoadmapGenerator

db = SessionLocal()
profile = db.query(Profile).first()

if profile:
    print('=== DATABASE ===')
    print('Skills in DB:', profile.current_skills)
    print('Goal in DB:', profile.career_goal)
    
    print('\n=== SKILL GAP ANALYSIS ===')
    analyzer = CareerAnalyzer()
    gaps = analyzer.detect_skill_gaps(profile.career_goal, profile.current_skills)
    print('Detected gaps:', gaps['skill_gaps'])
    
    print('\n=== ROADMAP GENERATION ===')
    gen = RoadmapGenerator()
    roadmap = gen.generate_roadmap(profile.career_goal, profile.current_skills, 2)
    print('Phase 1 skills to learn:', roadmap['phases'][0]['skills'])
    
    print('\n=== DATABASE ROADMAP ===')
    db_roadmap = db.query(Roadmap).first()
    if db_roadmap:
        print('Stored Phase 1 skills:', db_roadmap.phases[0]['skills'])
    else:
        print('No roadmap in database yet')
