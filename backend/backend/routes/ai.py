from fastapi import APIRouter, Depends
from ..models.ai import ResumeAnalysisRequest, ResumeAnalysisResponse
from ..utils.ai_helpers import (
    extract_skills_from_text,
    analyze_resume_strengths,
    calculate_job_match_score,
)
from .auth import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])

# Common in-demand tech skills
IN_DEMAND_SKILLS = [
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
    "React", "Angular", "Vue", "Node", "Python", "Java",
    "Docker", "Kubernetes", "CI/CD", "Microservices"
]

@router.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest, current_user: dict = Depends(get_current_user)):
    try:
        if len(request.resume_text.strip()) < 10:
            return ResumeAnalysisResponse(
                status="error",
                message="Resume text too short",
                analysis={}
            )
        
        # Extract skills
        extracted_skills = extract_skills_from_text(request.resume_text)
        
        # Analyze strengths and weaknesses
        strength_analysis = analyze_resume_strengths(extracted_skills)
        
        # Calculate missing skills dynamically
        extracted_skills_set = set(extracted_skills)
        in_demand_set = set(IN_DEMAND_SKILLS)
        missing_skills = list(in_demand_set - extracted_skills_set)
        
        # Calculate job match score based on skills
        match_score = calculate_job_match_score(extracted_skills, IN_DEMAND_SKILLS)
        
        # Generate improvement suggestions based on missing skills
        improvement_suggestions = []
        if "AWS" not in extracted_skills_set or "Azure" not in extracted_skills_set or "GCP" not in extracted_skills_set:
            improvement_suggestions.append("Learn cloud platforms like AWS, Azure, or GCP")
        if "Docker" not in extracted_skills_set or "Kubernetes" not in extracted_skills_set:
            improvement_suggestions.append("Gain experience with containerization (Docker, Kubernetes)")
        if "CI/CD" not in extracted_skills_set:
            improvement_suggestions.append("Improve your understanding of CI/CD pipelines")
        if "Microservices" not in extracted_skills_set:
            improvement_suggestions.append("Learn about microservices architecture")
        if not improvement_suggestions:
            improvement_suggestions.append("Continue expanding your technical skill set")
        
        analysis_result = {
            "extracted_skills": extracted_skills,
            "strengths": strength_analysis["strengths"],
            "weaknesses": strength_analysis["weaknesses"],
            "missing_skills": missing_skills[:10],  # Top 10 missing skills
            "job_match_score": match_score,
            "improvement_suggestions": improvement_suggestions,
            "experience_level": "Mid-level" if len(extracted_skills) >= 5 else "Entry-level" if len(extracted_skills) >= 2 else "Beginner"
        }
        
        return ResumeAnalysisResponse(
            status="success",
            message="Resume analyzed successfully",
            analysis=analysis_result
        )
        
    except Exception as e:
        return ResumeAnalysisResponse(
            status="error",
            message=f"Analysis failed: {str(e)}",
            analysis={}
        )