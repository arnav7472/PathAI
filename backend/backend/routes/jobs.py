from fastapi import APIRouter, Depends
from models.jobs import JobResponse
from routes.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])

# In-memory jobs database
jobs_db = []

@router.get("/", response_model=dict)
async def get_jobs(current_user: dict = Depends(get_current_user)):
    return {
        "status": "success",
        "data": jobs_db,
        "total": len(jobs_db)
    }

@router.post("/", response_model=dict)
async def create_job(job_data: dict, current_user: dict = Depends(get_current_user)):
    new_job = {
        "id": len(jobs_db) + 1,
        **job_data,
        "posted_by": current_user['id'],
        "is_active": True
    }
    jobs_db.append(new_job)
    
    return {
        "status": "success",
        "message": "Job created successfully",
        "data": new_job
    }