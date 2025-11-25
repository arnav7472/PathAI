from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

def create_application() -> FastAPI:
    app = FastAPI(
        title="AI Job Platform API",
        description="A modern job platform with AI-powered resume analysis and job matching",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

# Create app instance
app = create_application()