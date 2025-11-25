from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to fix potential browser issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    name: str
    email: str

class JobCreate(BaseModel):
    title: str
    company: str
    description: str

class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int

@app.get("/")
async def root():
    return {"message": "Server is running successfully!"}

@app.post("/users")
async def create_user(user: UserCreate):
    return {
        "status": "success", 
        "data": {
            "id": 1, 
            "name": user.name, 
            "email": user.email
        }
    }

@app.get("/users")
async def get_users():
    return {"status": "success", "data": [{"id": 1, "name": "Test User", "email": "test@example.com"}]}

@app.post("/jobs")
async def create_job(job: JobCreate):
    return {
        "status": "success",
        "data": {
            "id": 1,
            "title": job.title,
            "company": job.company,
            "description": job.description
        }
    }

@app.get("/jobs")
async def get_jobs():
    return {"status": "success", "data": [{"id": 1, "title": "Test Job", "company": "Test Co"}]}

@app.post("/apply")
async def apply_for_job(application: ApplicationCreate):
    return {
        "status": "success",
        "data": {
            "id": 1,
            "user_id": application.user_id,
            "job_id": application.job_id
        }
    }

@app.get("/applications")
async def get_applications():
    return {"status": "success", "data": [{"id": 1, "user_id": 1, "job_id": 1}]}

print("✅ All routes registered: POST /users, GET /users, POST /jobs, GET /jobs, POST /apply, GET /applications")


