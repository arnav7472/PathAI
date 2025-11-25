from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # JWT Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secure-secret-key-2024-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # Add your production frontend URL here
    ]

settings = Settings()