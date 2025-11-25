from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str] = []
    location: Optional[str] = None
    salary_range: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    posted_by: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True

class JobRecommendation(BaseModel):
    job_id: int
    title: str
    company: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]