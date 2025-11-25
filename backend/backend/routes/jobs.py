from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..models.jobs import JobResponse
from .auth import get_current_user

class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    requirements: List[str]
    location: Optional[str] = None
    salary_range: Optional[str] = None

router = APIRouter(prefix="/jobs", tags=["jobs"])

# In-memory jobs database
jobs_db = []
job_id_counter = 1

@router.get("/", response_model=dict)
async def get_jobs(current_user: dict = Depends(get_current_user)):
    return {
        "status": "success",
        "data": jobs_db,
        "total": len(jobs_db)
    }

@router.post("/", response_model=dict)
async def create_job(job_data: JobCreate, current_user: dict = Depends(get_current_user)):
    global job_id_counter
    new_job = {
        "id": job_id_counter,
        "title": job_data.title,
        "company": job_data.company,
        "description": job_data.description,
        "requirements": job_data.requirements,
        "location": job_data.location,
        "salary_range": job_data.salary_range,
        "posted_by": current_user['id'],
        "is_active": True
    }
    job_id_counter += 1
    jobs_db.append(new_job)
    
    return {
        "status": "success",
        "message": "Job created successfully",
        "data": new_job
    }