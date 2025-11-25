from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    target_job_title: Optional[str] = None

class ResumeAnalysisResponse(BaseModel):
    status: str
    message: str
    analysis: Dict[str, Any]

class JobRecommendationRequest(BaseModel):
    user_id: int
    limit: Optional[int] = 5

class JobRecommendationResponse(BaseModel):
    status: str
    user_id: int
    recommendations: List[Dict[str, Any]]
    total_jobs_analyzed: int