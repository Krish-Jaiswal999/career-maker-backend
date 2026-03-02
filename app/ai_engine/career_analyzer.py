"""
AI Engine for Career Path Analysis
- Career goal understanding
- Skill gap detection
- Industry path mapping
"""

from typing import List, Dict
import json

class CareerAnalyzer:
    """Analyzes career goals and current skills"""
    
    def __init__(self):
        # Skill variant mapping - maps variants to their canonical form
        self.skill_aliases = {
            # SQL variants
            "mysql": "SQL",
            "postgresql": "SQL",
            "postgres": "SQL",
            "oracle": "SQL",
            "mssql": "SQL",
            "sql server": "SQL",
            "mariadb": "SQL",
            
            # Deep Learning frameworks
            "tensorflow": "Deep Learning",
            "pytorch": "Deep Learning",
            "keras": "Deep Learning",
            
            # Frontend frameworks
            "react": "Frontend Framework",
            "vue": "Frontend Framework",
            "angular": "Frontend Framework",
            "svelte": "Frontend Framework",
            
            # Cloud platforms
            "aws": "Cloud Platform",
            "gcp": "Cloud Platform",
            "google cloud": "Cloud Platform",
            "azure": "Cloud Platform",
            "microsoft azure": "Cloud Platform",
            
            # Container tools
            "docker": "Container",
            "kubernetes": "Container",
            "k8s": "Container",
            
            # NoSQL databases
            "mongodb": "NoSQL",
            "cassandra": "NoSQL",
            "dynamodb": "NoSQL",
            "redis": "NoSQL",
            
            # Machine Learning libraries
            "scikit-learn": "Machine Learning",
            "scikit_learn": "Machine Learning",
            "sklearn": "Machine Learning",
            "xgboost": "Machine Learning",
            "lightgbm": "Machine Learning",
            
            # Data Processing
            "pandas": "Data Processing",
            "numpy": "Data Processing",
            "scipy": "Data Processing",
            
            # API Frameworks
            "fastapi": "API Framework",
            "flask": "API Framework",
            "django": "API Framework",
            "express": "API Framework",
            "node.js": "API Framework",
            "nodejs": "API Framework",
        }
        
        self.skill_categories = {
            "programming_languages": ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
            "frameworks": ["FastAPI", "Flask", "Django", "React", "Vue", "Angular"],
            "databases": ["PostgreSQL", "MongoDB", "Redis", "MySQL", "Cassandra"],
            "ml_frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "XGBoost"],
            "data_tools": ["Pandas", "NumPy", "Spark", "Hadoop"],
            "devops": ["Docker", "Kubernetes", "AWS", "GCP", "Terraform"],
            "soft_skills": ["Leadership", "Communication", "Project Management", "Problem Solving"]
        }
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize a skill to its canonical form (handles aliases/variants)"""
        skill_lower = skill.lower()
        if skill_lower in self.skill_aliases:
            return self.skill_aliases[skill_lower]
        return skill
    
    def detect_skill_gaps(self, career_goal: str, current_skills: List[str]) -> Dict:
        """Detect skills needed for the career goal"""
        
        career_skill_map = {
            "machine learning engineer": ["Python", "Deep Learning", "Statistics", "SQL", "Data Processing"],
            "machine learning": ["Python", "Deep Learning", "Statistics", "SQL", "Data Processing"],
            "ml engineer": ["Python", "Deep Learning", "Statistics", "SQL", "Data Processing"],
            "ml engineering": ["Python", "Deep Learning", "Statistics", "SQL", "Data Processing"],
            "data scientist": ["Python", "SQL", "Data Processing", "Machine Learning", "Data Visualization"],
            "data science": ["Python", "SQL", "Data Processing", "Machine Learning", "Data Visualization"],
            "full stack developer": ["JavaScript", "Frontend Framework", "API Framework", "SQL", "Container"],
            "fullstack": ["JavaScript", "Frontend Framework", "API Framework", "SQL", "Container"],
            "backend engineer": ["Python", "API Framework", "SQL", "NoSQL", "Cloud Platform"],
            "backend": ["Python", "API Framework", "SQL", "NoSQL", "Cloud Platform"],
            "devops engineer": ["Container", "Cloud Platform", "Linux", "CI/CD", "Infrastructure as Code"],
            "devops": ["Container", "Cloud Platform", "Linux", "CI/CD", "Infrastructure as Code"],
            "frontend engineer": ["JavaScript", "Frontend Framework", "CSS", "HTML", "TypeScript"],
            "frontend": ["JavaScript", "Frontend Framework", "CSS", "HTML", "TypeScript"],
            "cloud architect": ["Cloud Platform", "Container", "Infrastructure as Code", "Database Design", "Security"],
            "cloud": ["Cloud Platform", "Container", "Infrastructure as Code", "Database Design", "Security"],
        }
        
        goal_lower = career_goal.lower()
        needed_skills = career_skill_map.get(goal_lower, ["Python", "JavaScript", "SQL"])
        
        # Normalize current skills to their canonical forms
        normalized_current = set()
        for skill in current_skills:
            normalized = self.normalize_skill(skill)
            normalized_current.add(normalized.lower())
        
        # Find gaps - compare normalized needed skills with normalized current skills
        gaps = []
        needed_set = set()
        for skill in needed_skills:
            skill_lower = skill.lower()
            needed_set.add(skill_lower)
            if skill_lower not in normalized_current:
                gaps.append(skill)
        
        return {
            "career_goal": career_goal,
            "current_skills": current_skills,
            "skill_gaps": gaps,
            "proficiency_gaps": len(gaps),
            "completion_percentage": ((len(normalized_current) / len(needed_set)) * 100) if needed_set else 0
        }
    
    def map_career_trajectory(self, goal: str) -> Dict:
        """Map the career trajectory for the goal"""
        
        trajectories = {
            "machine learning engineer": ["Python Basics", "ML Fundamentals", "Deep Learning", "Advanced NLP", "ML Systems Design"],
            "machine learning": ["Python Basics", "ML Fundamentals", "Deep Learning", "Advanced NLP", "ML Systems Design"],
            "ml engineer": ["Python Basics", "ML Fundamentals", "Deep Learning", "Advanced NLP", "ML Systems Design"],
            "ml engineering": ["Python Basics", "ML Fundamentals", "Deep Learning", "Advanced NLP", "ML Systems Design"],
            "full stack developer": ["Frontend Basics", "Backend Fundamentals", "Database Design", "DevOps", "System Design"],
            "fullstack": ["Frontend Basics", "Backend Fundamentals", "Database Design", "DevOps", "System Design"],
            "data scientist": ["Python & SQL", "Statistics", "Data Visualization", "Machine Learning", "Big Data Tools"],
            "data science": ["Python & SQL", "Statistics", "Data Visualization", "Machine Learning", "Big Data Tools"],
            "backend engineer": ["Python Web Dev", "Database Design", "Microservices", "System Design", "Cloud Deployment"],
            "backend": ["Python Web Dev", "Database Design", "Microservices", "System Design", "Cloud Deployment"],
            "frontend engineer": ["HTML/CSS Basics", "JavaScript Fundamentals", "React/Framework", "State Management", "Advanced UI/UX"],
            "frontend": ["HTML/CSS Basics", "JavaScript Fundamentals", "React/Framework", "State Management", "Advanced UI/UX"],
            "devops engineer": ["Linux Basics", "Docker/Containers", "Kubernetes", "CI/CD Pipelines", "Infrastructure as Code"],
            "devops": ["Linux Basics", "Docker/Containers", "Kubernetes", "CI/CD Pipelines", "Infrastructure as Code"],
            "cloud architect": ["Cloud Fundamentals", "AWS/Azure Services", "Architecture Patterns", "Security", "Cost Optimization"],
            "cloud": ["Cloud Fundamentals", "AWS/Azure Services", "Architecture Patterns", "Security", "Cost Optimization"],
        }
        
        goal_lower = goal.lower()
        steps = trajectories.get(goal_lower, ["Foundation", "Intermediate", "Advanced", "Expert"])
        
        return {
            "career_goal": goal,
            "trajectory_steps": steps,
            "total_steps": len(steps)
        }

class RoadmapGenerator:
    """Generates personalized learning roadmaps"""
    
    def __init__(self):
        self.phase_durations = {
            "Foundation": "4-6 weeks",
            "Intermediate": "8-12 weeks",
            "Advanced": "12-16 weeks",
            "Expert": "Ongoing"
        }
        # Map skills to realistic project ideas
        self.skill_projects = {
            "Python": ["Build a CLI Tool", "Web Scraper", "Data Analysis Script"],
            "JavaScript": ["Interactive Web App", "DOM Manipulation Project", "Browser Games"],
            "Frontend Framework": ["Todo App", "Weather Dashboard", "Social Media Feed UI"],
            "API Framework": ["REST API Backend", "User Authentication System", "Microservice"],
            "SQL": ["Complex Queries", "Database Design", "Data Reporting"],
            "Deep Learning": ["Image Classification Model", "Neural Network", "Time Series Prediction"],
            "Container": ["Containerize Application", "Multi-container Setup", "Docker Compose"],
            "Cloud Platform": ["Deploy on Cloud", "Serverless Functions", "Data Pipeline"],
            "NoSQL": ["NoSQL Database Design", "Document Queries", "Data Migration"],
            "Statistics": ["Statistical Analysis", "Hypothesis Testing", "Data Visualization"],
            "Machine Learning": ["Predictive Model", "Feature Engineering", "Model Comparison"],
            "Data Processing": ["Data Cleaning", "Feature Engineering", "Data Pipeline"],
            "Data Visualization": ["Dashboard Creation", "Interactive Charts", "Data Storytelling"],
            "CI/CD": ["Automated Testing", "Deployment Pipeline", "Monitoring Setup"],
            "Infrastructure as Code": ["IaC Configuration", "Terraform Scripts", "Helm Charts"],
            "TypeScript": ["Type-Safe App", "Type Definitions", "Typed Library"],
            "HTML": ["Semantic Markup", "Accessible Pages", "Web Components"],
            "CSS": ["Responsive Design", "CSS Grid Layout", "Animation Effects"],
            "Linux": ["Shell Scripting", "System Administration", "Process Management"],
        }
    
    def generate_roadmap(self, career_goal: str, current_skills: List[str], years_exp: int) -> Dict:
        """Generate a detailed roadmap"""
        
        analyzer = CareerAnalyzer()
        gaps = analyzer.detect_skill_gaps(career_goal, current_skills)
        
        roadmap = {
            "goal": career_goal,
            "phases": self._create_phases(career_goal, gaps["skill_gaps"]),
            "total_duration": self._estimate_duration(len(gaps["skill_gaps"])),
            "milestone_count": 4,
            "projects_count": 8
        }
        
        return roadmap
    
    def _create_phases(self, goal: str, skill_gaps: List[str]) -> List[Dict]:
        """Create individual phases for the roadmap"""
        
        phases = []
        
        # Foundation Phase
        phases.append({
            "phase_number": 1,
            "phase_name": "Foundation",
            "duration": "4-6 weeks",
            "skills": skill_gaps[:2] if skill_gaps else ["Fundamentals"],
            "projects": self._get_projects_for_skills(skill_gaps[:2] if skill_gaps else ["Python"]),
            "resources": ["YouTube Tutorial", "Official Documentation"],
            "milestones": ["Complete basic tutorials", "First mini-project"],
            "order": 1
        })
        
        # Intermediate Phase
        if len(skill_gaps) > 2:
            phases.append({
                "phase_number": 2,
                "phase_name": "Intermediate",
                "duration": "8-12 weeks",
                "skills": skill_gaps[2:4] if len(skill_gaps) > 4 else skill_gaps[2:],
                "projects": self._get_projects_for_skills(skill_gaps[2:4] if len(skill_gaps) > 4 else skill_gaps[2:]),
                "resources": ["Udemy Course", "Blog Posts"],
                "milestones": ["Build intermediate project", "Contribute to open source"],
                "order": 2
            })
        
        # Advanced Phase
        if len(skill_gaps) > 4:
            phases.append({
                "phase_number": 3,
                "phase_name": "Advanced",
                "duration": "12-16 weeks",
                "skills": skill_gaps[4:],
                "projects": self._get_projects_for_skills(skill_gaps[4:]),
                "resources": ["Research Papers", "Advanced Courses"],
                "milestones": ["Advanced project completion", "System design"],
                "order": 3
            })
        
        return phases
    
    def _get_projects_for_skills(self, skills: List[str]) -> List[str]:
        """Get relevant project recommendations for given skills"""
        projects = set()
        
        for skill in skills:
            # Check if skill is in the map (case-insensitive)
            for key, project_list in self.skill_projects.items():
                if key.lower() == skill.lower():
                    projects.update(project_list[:2])  # Add top 2 projects per skill
                    break
        
        # Return up to 3 unique projects
        return list(projects)[:3] if projects else ["Build a practical project with your new skills"]
    
    def _estimate_duration(self, gap_count: int) -> str:
        """Estimate total learning duration"""
        months = gap_count * 2  # 2 months per skill approximately
        return f"{months}-{months + 4} weeks"
