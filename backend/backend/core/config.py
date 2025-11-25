from dotenv import load_dotenv
import os
import sys

load_dotenv()

class Settings:
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # JWT Configuration - Use default for demo, but should be set in production
    SECRET_KEY = os.getenv("SECRET_KEY", "demo-secret-key-change-in-production-2024")
    if SECRET_KEY == "demo-secret-key-change-in-production-2024":
        print("WARNING: Using default SECRET_KEY. Set SECRET_KEY in .env for production!")
    
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # CORS Configuration - Restricted to specific origins for security
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # Add your production frontend URL here
    ]

settings = Settings()