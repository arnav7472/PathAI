from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from routes.auth import get_current_user
from difflib import SequenceMatcher

router = APIRouter(prefix="/candidates", tags=["candidates"])

# In-memory candidates database
candidates_db = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "resume": "Senior Python developer with 5 years experience. Expertise in FastAPI, Django, PostgreSQL, Docker, Kubernetes, AWS. Strong in microservices architecture and CI/CD pipelines.",
        "email": "alice@example.com"
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "resume": "Full-stack developer proficient in React, Node.js, JavaScript. Experience with MongoDB, MySQL, REST APIs. 3 years in web development and UX optimization.",
        "email": "bob@example.com"
    },
    {
        "id": 3,
        "name": "Carol Davis",
        "resume": "DevOps engineer with Docker, Kubernetes, Terraform, CI/CD expertise. AWS and Azure cloud platforms. 4 years infrastructure and deployment automation.",
        "email": "carol@example.com"
    },
    {
        "id": 4,
        "name": "David Wilson",
        "resume": "Junior Python developer with Django experience. Learning FastAPI and PostgreSQL. Git and basic Docker knowledge. 1 year professional experience.",
        "email": "david@example.com"
    }
]

class CandidateFindRequest(BaseModel):
    job_description: str
    limit: Optional[int] = 10

class CandidateResponse(BaseModel):
    id: int
    name: str
    resume: str
    email: str
    match_score: float
    skill_match: float
    text_similarity: float
    matching_skills: List[str]
    missing_skills: List[str]

def extract_skills_from_text(text: str) -> List[str]:
    """Extract potential skills from text"""
    tech_skills = [
        "python", "javascript", "java", "c++", "c#", "go", "rust", "php", "ruby",
        "react", "angular", "vue", "django", "flask", "fastapi", "node", "express",
        "mysql", "postgresql", "mongodb", "redis", "sql", "nosql",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "git", "jenkins", "ci/cd", "rest", "graphql", "api", "microservices", "ux"
    ]
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in tech_skills:
        if skill in text_lower:
            found_skills.append(skill.title())
    
    return list(set(found_skills))

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts"""
    ratio = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    return round(ratio * 100, 2)

def calculate_skill_match(candidate_skills: List[str], job_skills: List[str]) -> float:
    """Calculate skill match percentage"""
    if not job_skills:
        return 0.0
    
    candidate_set = set(candidate_skills)
    job_set = set(job_skills)
    
    matching = candidate_set & job_set
    match_ratio = len(matching) / len(job_set)
    
    return round(match_ratio * 100, 2)

@router.post("/find", response_model=dict)
async def find_candidates(request: CandidateFindRequest, current_user: dict = Depends(get_current_user)):
    """Find best matching candidates for a job description"""
    
    if not request.job_description or len(request.job_description.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Job description must be at least 10 characters long"
        )
    
    job_skills = extract_skills_from_text(request.job_description)
    ranked_candidates = []
    
    for candidate in candidates_db:
        # Extract candidate skills
        candidate_skills = extract_skills_from_text(candidate['resume'])
        
        # Calculate skill match score (70% weight)
        skill_score = calculate_skill_match(candidate_skills, job_skills)
        
        # Calculate text similarity score (30% weight)
        text_score = calculate_text_similarity(
            request.job_description,
            candidate['resume']
        )
        
        # Weighted combined score
        combined_score = (skill_score * 0.7) + (text_score * 0.3)
        
        # Find matching and missing skills
        matching_skills = list(set(job_skills) & set(candidate_skills))
        missing_skills = list(set(job_skills) - set(candidate_skills))
        
        ranked_candidates.append({
            "id": candidate['id'],
            "name": candidate['name'],
            "resume": candidate['resume'],
            "email": candidate['email'],
            "match_score": round(combined_score, 2),
            "skill_match": skill_score,
            "text_similarity": text_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills
        })
    
    # Sort by match score descending
    ranked_candidates.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Apply limit
    limited_results = ranked_candidates[:request.limit]
    
    return {
        "status": "success",
        "job_description": request.job_description,
        "job_skills": job_skills,
        "total_candidates": len(candidates_db),
        "matched_candidates": len(limited_results),
        "candidates": limited_results
    }

@router.get("/", response_model=dict)
async def get_all_candidates(current_user: dict = Depends(get_current_user)):
    """Get all candidates"""
    return {
        "status": "success",
        "total_candidates": len(candidates_db),
        "candidates": candidates_db
    }

@router.get("/{candidate_id}", response_model=dict)
async def get_candidate(candidate_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific candidate by ID"""
    for candidate in candidates_db:
        if candidate['id'] == candidate_id:
            return {
                "status": "success",
                "candidate": candidate
            }
    
    raise HTTPException(status_code=404, detail="Candidate not found")
