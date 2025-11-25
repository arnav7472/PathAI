import re
from typing import List, Dict, Any

# Define skill categories
BACKEND_SKILLS = {"Python", "Java", "Go", "Node", "Django", "Flask", "FastAPI", "Express", "Ruby", "Php"}
FRONTEND_SKILLS = {"React", "Angular", "Vue", "Javascript", "Typescript"}
DEVOPS_SKILLS = {"Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform", "Jenkins", "CI/CD"}
DATABASE_SKILLS = {"MySQL", "PostgreSQL", "MongoDB", "Redis", "SQL", "Nosql"}

# Common tech skills dictionary
TECH_SKILLS = [
    "python", "javascript", "java", "c++", "c#", "go", "rust", "php", "ruby", "typescript",
    "react", "angular", "vue", "django", "flask", "fastapi", "node", "express",
    "mysql", "postgresql", "mongodb", "redis", "sql", "nosql",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "git", "jenkins", "ci/cd", "rest", "graphql", "api", "microservices", "ux"
]

def extract_skills_from_text(text: str) -> List[str]:
    """Extract potential skills from resume text"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in TECH_SKILLS:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def analyze_resume_strengths(skills: List[str], experience_years: int = None) -> Dict[str, Any]:
    """Analyze resume strengths based on skills"""
    strengths = []
    weaknesses = []
    
    user_skills_set = set(skills)
    
    # Analyze strengths
    if user_skills_set & BACKEND_SKILLS:
        strengths.append("Strong backend development skills")
    if user_skills_set & FRONTEND_SKILLS:
        strengths.append("Frontend development experience")
    if user_skills_set & DEVOPS_SKILLS:
        strengths.append("DevOps and cloud platform knowledge")
    if user_skills_set & DATABASE_SKILLS:
        strengths.append("Database design and management experience")
    
    # Analyze weaknesses (missing important skills)
    if not user_skills_set & BACKEND_SKILLS and not user_skills_set & FRONTEND_SKILLS:
        weaknesses.append("Limited programming language experience")
    if not user_skills_set & DEVOPS_SKILLS:
        weaknesses.append("Limited cloud and deployment experience")
    
    return {
        "strengths": strengths,
        "weaknesses": weaknesses
    }

def calculate_job_match_score(user_skills: List[str], job_skills: List[str]) -> float:
    """Calculate match score between user skills and job requirements"""
    if not job_skills:
        return 0.0
    
    user_skills_set = set(user_skills)
    job_skills_set = set(job_skills)
    
    matching_skills = user_skills_set & job_skills_set
    match_ratio = len(matching_skills) / len(job_skills_set)
    
    return round(match_ratio * 100, 2)