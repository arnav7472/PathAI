from fastapi import APIRouter, Depends
from models.ai import ResumeAnalysisRequest, ResumeAnalysisResponse
from utils.ai_helpers import extract_skills_from_text, analyze_resume_strengths, calculate_job_match_score
from routes.auth import get_current_user

router = APIRouter(prefix="/ai", tags=["ai"])

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
        
        # Generate improvement suggestions
        improvement_suggestions = [
            "Learn cloud platforms like AWS, Azure, or GCP",
            "Gain experience with containerization (Docker, Kubernetes)",
            "Improve your understanding of CI/CD pipelines",
            "Learn about microservices architecture"
        ]
        
        analysis_result = {
            "extracted_skills": extracted_skills,
            "strengths": strength_analysis["strengths"],
            "weaknesses": strength_analysis["weaknesses"],
            "missing_skills": ["AWS", "Docker", "Kubernetes", "React", "Node.js"],
            "job_match_score": 72,
            "improvement_suggestions": improvement_suggestions,
            "experience_level": "Mid-level" if len(extracted_skills) >= 5 else "Entry-level"
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