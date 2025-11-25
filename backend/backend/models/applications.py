from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class ApplicationBase(BaseModel):
    job_id: int
    resume_text: str
    cover_letter: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    status: ApplicationStatus
    applied_at: datetime
    ai_analysis: Optional[dict] = None

    class Config:
        from_attributes = True