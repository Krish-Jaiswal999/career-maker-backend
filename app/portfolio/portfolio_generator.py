"""
Portfolio Generator
- HTML template rendering
- Theme selection
- Portfolio generation
"""

from typing import Dict, List
from jinja2 import Template

class PortfolioGenerator:
    """Generates personalized portfolios"""
    
    def __init__(self):
        self.templates = {
            "faang": self._get_faang_template(),
            "startup": self._get_startup_template(),
            "researcher": self._get_researcher_template(),
            "minimal": self._get_minimal_template()
        }
    
    def generate_portfolio(self, user_data: Dict, template_type: str = "faang") -> Dict:
        """Generate portfolio HTML"""
        
        if template_type not in self.templates:
            template_type = "faang"
        
        template = self.templates[template_type]
        
        html_content = template.render(
            name=user_data.get("name", "Your Name"),
            email=user_data.get("email", "your@email.com"),
            phone=user_data.get("phone", "+1 (555) 000-0000"),
            location=user_data.get("location", "City, State"),
            bio=user_data.get("bio", "Software Developer"),
            skills=user_data.get("skills", []),
            projects=user_data.get("projects", []),
            experience=user_data.get("experience", []),
            education=user_data.get("education", []),
            github=user_data.get("github_url", "https://github.com"),
            linkedin=user_data.get("linkedin_url", "https://linkedin.com"),
            github_url=user_data.get("github_url", "#"),
            linkedin_url=user_data.get("linkedin_url", "#")
        )
        
        return {
            "template_type": template_type,
            "html_content": html_content,
            "css_content": self._get_css_for_template(template_type)
        }
    
    def _get_faang_template(self) -> Template:
        """FAANG-style portfolio template"""
        return Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} - Software Engineer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
        header { margin-bottom: 40px; border-bottom: 2px solid #000; padding-bottom: 20px; }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .contact { display: flex; gap: 20px; font-size: 0.9em; }
        .section { margin-bottom: 40px; }
        h2 { font-size: 1.5em; margin: 30px 0 15px 0; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
        .skill-tag { display: inline-block; background: #f0f0f0; padding: 5px 10px; margin: 5px 5px 5px 0; border-radius: 3px; font-size: 0.9em; }
        .project { margin-bottom: 25px; }
        .project-title { font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
        .project-skills { font-size: 0.9em; color: #666; margin: 5px 0; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ name }}</h1>
            <p>{{ bio }}</p>
            <div class="contact">
                <span>📧 {{ email }}</span>
                <span>📱 {{ phone }}</span>
                <span>📍 {{ location }}</span>
                <span><a href="{{ github_url }}">GitHub</a></span>
                <span><a href="{{ linkedin_url }}">LinkedIn</a></span>
            </div>
        </header>
        
        {% if skills %}
        <section class="section">
            <h2>Technical Skills</h2>
            <div>
                {% for skill in skills %}
                <span class="skill-tag">{{ skill }}</span>
                {% endfor %}
            </div>
        </section>
        {% endif %}
        
        {% if projects %}
        <section class="section">
            <h2>Featured Projects</h2>
            {% for project in projects %}
            <div class="project">
                <div class="project-title">{{ project.title }}</div>
                <p>{{ project.description }}</p>
                <div class="project-skills">
                    {% for skill in project.skills %}
                    <span class="skill-tag">{{ skill }}</span>
                    {% endfor %}
                </div>
                {% if project.link %}
                <p><a href="{{ project.link }}">View Project →</a></p>
                {% endif %}
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        {% if experience %}
        <section class="section">
            <h2>Experience</h2>
            {% for exp in experience %}
            <div style="margin-bottom: 20px;">
                <strong>{{ exp.title }}</strong> @ {{ exp.company }}
                <p style="font-size: 0.9em; color: #666;">{{ exp.duration }}</p>
                <p>{{ exp.description }}</p>
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        {% if education %}
        <section class="section">
            <h2>Education</h2>
            {% for edu in education %}
            <div style="margin-bottom: 15px;">
                <strong>{{ edu.degree }}</strong> in {{ edu.field }}
                <p style="font-size: 0.9em; color: #666;">{{ edu.institution }} • {{ edu.year }}</p>
            </div>
            {% endfor %}
        </section>
        {% endif %}
    </div>
</body>
</html>
        """)
    
    def _get_startup_template(self) -> Template:
        """Startup-style portfolio template"""
        return Template("""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{{ name }} — Startup Portfolio</title>
    <style>
        :root{--accent:#ff6b6b;--muted:#f7fafc}
        body{font-family:Inter,system-ui,Arial,sans-serif;background:linear-gradient(120deg,#0f172a 0%, #08112a 60%);color:#eef2ff}
        .frame{max-width:1100px;margin:40px auto;padding:28px}
        header{display:flex;align-items:center;gap:24px}
        .avatar{width:96px;height:96px;background:rgba(255,255,255,0.06);border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:700}
        h1{font-size:2.1rem;margin:0}
        .meta{color:rgba(255,255,255,0.8)}
        .grid{display:grid;grid-template-columns:1fr 380px;gap:26px;margin-top:28px}
        .card{background:linear-gradient(180deg,rgba(255,255,255,0.03),transparent);padding:22px;border-radius:12px}
        .skills{display:flex;flex-wrap:wrap;gap:8px}
        .pill{background:rgba(255,255,255,0.06);padding:6px 10px;border-radius:999px;font-size:0.9rem}
        .projects .proj{padding:14px;border-radius:10px;background:rgba(0,0,0,0.18);margin-bottom:12px}
        a.button{display:inline-block;padding:8px 12px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none}
        .sidebar .contact a{color:#fff}
    </style>
</head>
<body>
    <div class="frame">
        <header>
            <div class="avatar">{{ name.split(' ')[0][0] if name else 'U' }}</div>
            <div>
                <h1>{{ name }}</h1>
                <div class="meta">{{ bio }}</div>
                <div style="margin-top:8px"><a class="button" href="mailto:{{ email }}">Contact</a></div>
            </div>
        </header>

        <div class="grid">
            <div>
                <div class="card">
                    <h2>About</h2>
                    <p style="color:#dbeafe">{{ bio }}</p>
                </div>

                <div class="card projects" style="margin-top:16px">
                    <h2>Projects</h2>
                    {% for project in projects %}
                    <div class="proj">
                        <strong>{{ project.title }}</strong>
                        <p style="color:#c7d2fe">{{ project.description }}</p>
                        {% if project.link %}<a href="{{ project.link }}" style="color:#fff;">View</a>{% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>

            <aside class="sidebar">
                <div class="card contact">
                    <h3>Contact</h3>
                    <div><a href="mailto:{{ email }}">{{ email }}</a></div>
                    <div>{{ phone }}</div>
                    <div><a href="{{ linkedin_url }}">LinkedIn</a></div>
                    <div><a href="{{ github_url }}">GitHub</a></div>
                </div>

                <div class="card" style="margin-top:16px">
                    <h3>Skills</h3>
                    <div class="skills">
                        {% for skill in skills %}<span class="pill">{{ skill }}</span>{% endfor %}
                    </div>
                </div>
            </aside>
        </div>
    </div>
</body>
</html>
                """)
    
    def _get_researcher_template(self) -> Template:
        """Academic/Research portfolio template"""
        return Template("""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ name }} — Research Portfolio</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        body{font-family: 'Merriweather', serif;max-width:900px;margin:40px auto;padding:28px;color:#111;background:#fff}
        header{border-bottom:2px solid #e6eef8;padding-bottom:14px}
        h1{font-size:2rem;margin:0}
        .affil{color:#51628f}
        .pub{margin:18px 0;padding-left:12px;border-left:3px solid #c7d2fe}
        .meta{color:#525252;font-size:0.95rem}
        .grid{display:flex;gap:20px}
        .left{flex:2}
        .right{flex:1;background:#f7fbff;padding:18px;border-radius:8px}
    </style>
</head>
<body>
    <header>
        <h1>{{ name }}</h1>
        <div class="affil">{{ current_title or '' }} {{ ' — ' + (current_company or '') if current_company else '' }}</div>
        <p class="meta">{{ bio }}</p>
    </header>

    <div style="margin-top:22px" class="grid">
        <div class="left">
            <section>
                <h2>Selected Publications & Research</h2>
                {% for project in projects %}
                <article class="pub">
                    <h3>{{ project.title }}</h3>
                    <p>{{ project.description }}</p>
                    {% if project.link %}<div><a href="{{ project.link }}">Read more</a></div>{% endif %}
                </article>
                {% endfor %}
            </section>

            <section style="margin-top:18px">
                <h2>Experience</h2>
                {% for exp in experience %}
                <div style="margin-bottom:12px">
                    <strong>{{ exp.title }}</strong> — <em>{{ exp.company }}</em>
                    <div style="color:#555">{{ exp.description }}</div>
                </div>
                {% endfor %}
            </section>
        </div>

        <aside class="right">
            <h3>Contact & Links</h3>
            <div><a href="mailto:{{ email }}">{{ email }}</a></div>
            <div>{{ phone }}</div>
            <div><a href="{{ linkedin_url }}">LinkedIn</a></div>
            <div style="margin-top:12px"><strong>Skills</strong>
                <div style="margin-top:8px">{% for skill in skills %}<div style="font-size:0.92rem">• {{ skill }}</div>{% endfor %}</div>
            </div>
        </aside>
    </div>
</body>
</html>
                """)
    
    def _get_minimal_template(self) -> Template:
        """Minimal portfolio template"""
        return Template("""
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{{ name }}</title>
    <style>
        body{font-family:Arial,Helvetica,sans-serif;color:#111;background:#fff}
        .wrap{max-width:820px;margin:40px auto;padding:30px}
        .left{float:left;width:30%;padding-right:20px;border-right:1px solid #eee}
        .right{margin-left:32%}
        h1{margin:0 0 6px 0}
        .small{color:#666;font-size:0.95rem}
        ul{padding-left:18px}
    </style>
</head>
<body>
    <div class="wrap">
        <div class="left">
            <h1>{{ name }}</h1>
            <div class="small">{{ current_title or '' }}<br>{{ current_company or '' }}</div>
            <hr style="margin:12px 0">
            <div class="small">Contact:<br><a href="mailto:{{ email }}">{{ email }}</a><br>{{ phone }}</div>
            <h3 style="margin-top:18px">Skills</h3>
            <ul>{% for s in skills %}<li>{{ s }}</li>{% endfor %}</ul>
        </div>

        <div class="right">
            <section>
                <h2>About</h2>
                <p>{{ bio }}</p>
            </section>

            <section>
                <h2>Experience</h2>
                {% for exp in experience %}
                <div style="margin-bottom:12px"><strong>{{ exp.title }}</strong><div class="small">{{ exp.company }} • {{ exp.years }}</div><p>{{ exp.description }}</p></div>
                {% endfor %}
            </section>

            <section>
                <h2>Projects</h2>
                {% for project in projects %}
                <div style="margin-bottom:10px"><strong>{{ project.title }}</strong> — {{ project.description }}</div>
                {% endfor %}
            </section>
        </div>
        <div style="clear:both"></div>
    </div>
</body>
</html>
                """)
    
    def _get_css_for_template(self, template_type: str) -> str:
        """Get CSS for the template"""
        return """
/* Tailwind-inspired responsive CSS */
@media (max-width: 768px) {
    .container { padding: 20px; }
    h1 { font-size: 2em; }
    .contact { flex-direction: column; }
}
        """
