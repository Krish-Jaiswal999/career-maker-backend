"""
NLP and Skill Matching Engine
- Vector similarity search
- Skill embedding
- Career path matching
"""

from typing import List, Dict

class SkillMatcher:
    """Matches skills with career paths and projects"""
    
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
        
        self.skill_taxonomy = {
            "backend": ["Python", "Java", "C#", "Go", "Rust"],
            "frontend": ["JavaScript", "React", "Vue", "Angular", "TypeScript"],
            "fullstack": ["JavaScript", "Python", "React", "Node.js", "PostgreSQL"],
            "data": ["Python", "SQL", "Pandas", "Statistics", "Machine Learning"],
            "ml": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Mathematics"],
            "devops": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
            "mobile": ["React Native", "Swift", "Kotlin", "Flutter"]
        }
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize a skill to its canonical form (handles aliases/variants)"""
        skill_lower = skill.lower()
        if skill_lower in self.skill_aliases:
            return self.skill_aliases[skill_lower]
        return skill
    
    def match_skills_to_career(self, skills: List[str], career_goal: str) -> Dict:
        """Find how well skills match a career goal"""
        
        goal_key = self._normalize_goal(career_goal)
        target_skills = self.skill_taxonomy.get(goal_key, [])
        
        skill_set = set([s.lower() for s in skills])
        target_set = set([s.lower() for s in target_skills])
        
        matched = skill_set.intersection(target_set)
        missing = target_set - skill_set
        
        match_score = (len(matched) / len(target_set)) * 100 if target_set else 0
        
        return {
            "career_goal": career_goal,
            "target_skills": target_skills,
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "match_score": round(match_score, 2),
            "readiness_level": self._calculate_readiness(match_score)
        }
    
    def recommend_projects(self, skills: List[str], career_goal: str) -> List[Dict]:
        """Recommend projects based on skills"""
        
        projects = [
            {
                "title": "Portfolio Website",
                "skills": ["HTML", "CSS", "JavaScript"],
                "difficulty": "beginner",
                "duration": "2 weeks"
            },
            {
                "title": "REST API with FastAPI",
                "skills": ["Python", "FastAPI", "PostgreSQL"],
                "difficulty": "intermediate",
                "duration": "3 weeks"
            },
            {
                "title": "Machine Learning Model",
                "skills": ["Python", "TensorFlow", "Scikit-learn"],
                "difficulty": "intermediate",
                "duration": "4 weeks"
            },
            {
                "title": "Full-stack Application",
                "skills": ["React", "Node.js", "MongoDB"],
                "difficulty": "advanced",
                "duration": "6 weeks"
            },
            {
                "title": "Docker Containerization",
                "skills": ["Docker", "Kubernetes", "DevOps"],
                "difficulty": "intermediate",
                "duration": "2 weeks"
            }
        ]
        
        # Filter projects that match skills
        recommended = []
        skill_set = set([s.lower() for s in skills])
        
        for project in projects:
            project_skill_set = set([s.lower() for s in project["skills"]])
            if skill_set.intersection(project_skill_set):
                recommended.append(project)
        
        return recommended[:5]  # Return top 5
    
    def recommend_resources(self, skill: str) -> List[Dict]:
        """Recommend learning resources for a skill"""
        
        resources_map = {
            "python": [
                {"type": "📚 Course", "title": "Python for Everybody", "link": "https://www.coursera.org/learn/python"},
                {"type": "🎥 YouTube", "title": "Python Tutorial for Beginners", "link": "https://www.youtube.com/watch?v=_uQrJ0TkSuc"},
                {"type": "📖 Book", "title": "Python Crash Course", "link": "https://nostarch.com/python-crash-course-2nd-edition"},
                {"type": "💻 Practice", "title": "LeetCode Python Track", "link": "https://leetcode.com"},
                {"type": "📚 Docs", "title": "Official Python Docs", "link": "https://docs.python.org/3/"}
            ],
            "javascript": [
                {"type": "📚 Course", "title": "The Complete JavaScript Course", "link": "https://www.udemy.com/course/the-complete-javascript-course-2024/"},
                {"type": "🎥 YouTube", "title": "JavaScript Fundamentals", "link": "https://www.youtube.com/watch?v=W6NZfCO5tTE"},
                {"type": "💻 Interactive", "title": "JavaScript.info", "link": "https://javascript.info"},
                {"type": "💻 Practice", "title": "Codewars JavaScript", "link": "https://www.codewars.com"},
                {"type": "📖 Book", "title": "Eloquent JavaScript", "link": "https://eloquentjavascript.net"}
            ],
            "react": [
                {"type": "📚 Docs", "title": "React Official Documentation", "link": "https://react.dev"},
                {"type": "📚 Course", "title": "React - The Complete Guide", "link": "https://www.udemy.com/course/react-the-complete-guide/"},
                {"type": "🎥 YouTube", "title": "React Course by Scrimba", "link": "https://www.youtube.com/watch?v=I6nnRc-XP2M"},
                {"type": "💻 Practice", "title": "React Router Tutorial", "link": "https://reactrouter.com"},
                {"type": "🛠️ Tools", "title": "Create React App", "link": "https://create-react-app.dev"}
            ],
            "tensorflow": [
                {"type": "📚 Course", "title": "TensorFlow for Beginners", "link": "https://www.tensorflow.org/learn"},
                {"type": "🎥 YouTube", "title": "TensorFlow Tutorial", "link": "https://www.youtube.com/watch?v=KakSz1FkQmQ"},
                {"type": "📖 Book", "title": "Hands-On ML with TensorFlow", "link": "https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/"},
                {"type": "📚 Docs", "title": "TensorFlow Official Docs", "link": "https://www.tensorflow.org/api_docs"},
                {"type": "💻 Practice", "title": "TensorFlow Examples", "link": "https://github.com/aymericdamien/TensorFlow-Examples"}
            ],
            "pytorch": [
                {"type": "📚 Course", "title": "PyTorch for Deep Learning", "link": "https://pytorch.org/tutorials/"},
                {"type": "🎥 YouTube", "title": "PyTorch Full Tutorial", "link": "https://www.youtube.com/watch?v=GIsg-ZUy0MY"},
                {"type": "📚 Docs", "title": "PyTorch Documentation", "link": "https://pytorch.org/docs/stable/index.html"},
                {"type": "💻 Practice", "title": "Kaggle PyTorch Projects", "link": "https://www.kaggle.com/code?language=pytorch"},
                {"type": "📖 Book", "title": "Deep Learning with PyTorch", "link": "https://www.manning.com/books/deep-learning-with-pytorch"}
            ],
            "docker": [
                {"type": "📚 Docs", "title": "Docker Official Documentation", "link": "https://docs.docker.com"},
                {"type": "📚 Course", "title": "Docker Mastery", "link": "https://www.udemy.com/course/docker-mastery/"},
                {"type": "🎥 YouTube", "title": "Docker Tutorials", "link": "https://www.youtube.com/watch?v=3c-iBn73dRM"},
                {"type": "💻 Practice", "title": "Docker Labs", "link": "https://www.docker.com/"},
                {"type": "🛠️ Tools", "title": "Docker Hub", "link": "https://hub.docker.com"}
            ],
            "kubernetes": [
                {"type": "📚 Docs", "title": "Kubernetes Official Docs", "link": "https://kubernetes.io/docs/"},
                {"type": "📚 Course", "title": "Kubernetes for Beginners", "link": "https://www.udemy.com/course/kubernetes-for-beginners/"},
                {"type": "🎥 YouTube", "title": "Kubernetes Crash Course", "link": "https://www.youtube.com/watch?v=X48VuDVv0Z0"},
                {"type": "💻 Practice", "title": "Katacoda K8s Labs", "link": "https://www.katacoda.com"},
                {"type": "📖 Book", "title": "Kubernetes in Action", "link": "https://www.manning.com/books/kubernetes-in-action"}
            ],
            "aws": [
                {"type": "📚 Docs", "title": "AWS Learning Path", "link": "https://aws.amazon.com/training/"},
                {"type": "📚 Course", "title": "Ultimate AWS Course", "link": "https://www.udemy.com/course/ultimate-aws-certified-solutions-architect-associate/"},
                {"type": "🎥 YouTube", "title": "AWS Tutorials", "link": "https://www.youtube.com/results?search_query=aws+tutorials"},
                {"type": "💻 Practice", "title": "AWS Free Tier", "link": "https://aws.amazon.com/free/"},
                {"type": "📖 Book", "title": "AWS Solutions Architecture", "link": "https://www.oreilly.com/"}
            ],
            "sql": [
                {"type": "📚 Course", "title": "SQL for Data Analysis", "link": "https://www.udemy.com/course/sql-for-business-analysts/"},
                {"type": "🎥 YouTube", "title": "SQL Tutorial", "link": "https://www.youtube.com/watch?v=19vJtICSIOU"},
                {"type": "💻 Practice", "title": "SQLZoo", "link": "https://www.sqlzoo.net"},
                {"type": "📚 Docs", "title": "PostgreSQL Documentation", "link": "https://www.postgresql.org/docs/"},
                {"type": "💻 Interactive", "title": "Mode SQL Tutorial", "link": "https://mode.com/sql-tutorial/"}
            ],
            "fastapi": [
                {"type": "📚 Docs", "title": "FastAPI Official Documentation", "link": "https://fastapi.tiangolo.com"},
                {"type": "🎥 YouTube", "title": "FastAPI Tutorial", "link": "https://www.youtube.com/watch?v=7t2alSnE2-I"},
                {"type": "📚 Course", "title": "FastAPI on Udemy", "link": "https://www.udemy.com/course/fastapi-the-complete-course/"},
                {"type": "💻 Practice", "title": "Real Python FastAPI", "link": "https://realpython.com/fastapi-python-web-apis/"},
                {"type": "🛠️ Tools", "title": "FastAPI GitHub", "link": "https://github.com/tiangolo/fastapi"}
            ],
            "statistics": [
                {"type": "📚 Course", "title": "Statistics with Python", "link": "https://www.coursera.org/learn/basic-statistics"},
                {"type": "🎥 YouTube", "title": "Statistics Essentials", "link": "https://www.youtube.com/watch?v=xxpc-SQ5BII"},
                {"type": "📖 Book", "title": "Statistical Rethinking", "link": "https://xcelab.net/rm/statistical-rethinking/"},
                {"type": "💻 Practice", "title": "Khan Academy Statistics", "link": "https://www.khanacademy.org/math/statistics-probability"},
                {"type": "💻 Tool", "title": "R Statistical Computing", "link": "https://www.r-project.org"}
            ]
        }
        
        skill_lower = skill.lower()
        if skill_lower in resources_map:
            return resources_map[skill_lower]
        
        # Generic fallback with more comprehensive resources
        return [
            {"type": "🔍 Search", "title": f"Google: Learn {skill}", "link": f"https://www.google.com/search?q=learn+{skill.replace(' ', '+')}"},
            {"type": "📚 Course", "title": f"{skill} on Udemy", "link": "https://www.udemy.com"},
            {"type": "🎥 YouTube", "title": f"{skill} Tutorial", "link": "https://www.youtube.com"},
            {"type": "📖 Books", "title": f"O'Reilly {skill} Books", "link": "https://www.oreilly.com"},
            {"type": "💻 Community", "title": f"Stack Overflow {skill} Tag", "link": "https://stackoverflow.com"}
        ]
    
    def _normalize_goal(self, goal: str) -> str:
        """Normalize career goal to taxonomy key"""
        goal_lower = goal.lower()
        if "machine learning" in goal_lower or "ml" in goal_lower:
            return "ml"
        elif "backend" in goal_lower:
            return "backend"
        elif "frontend" in goal_lower:
            return "frontend"
        elif "full stack" in goal_lower:
            return "fullstack"
        elif "data" in goal_lower:
            return "data"
        elif "devops" in goal_lower:
            return "devops"
        elif "mobile" in goal_lower:
            return "mobile"
        return "fullstack"
    
    def _calculate_readiness(self, score: float) -> str:
        """Calculate readiness level based on match score"""
        if score >= 80:
            return "ready"
        elif score >= 60:
            return "intermediate"
        elif score >= 40:
            return "beginner"
        else:
            return "novice"
