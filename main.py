from backend.backend.app import app
from backend.backend.routes import auth as auth_routes
from backend.backend.routes import jobs as jobs_routes
from backend.backend.routes import ai as ai_routes
from backend.backend.routes import candidates as candidates_routes

# Include routers
app.include_router(auth_routes.router)
app.include_router(jobs_routes.router)
app.include_router(ai_routes.router)
app.include_router(candidates_routes.router)

@app.get("/")
async def root():
    return {
        "message": "AI Job Platform API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running smoothly"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)