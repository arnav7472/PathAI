from .config import settings

# Initialize Supabase client (optional for demo)
supabase = None
try:
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        from supabase import create_client, Client
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        print("Supabase client initialized successfully")
    else:
        print("Supabase not configured - using in-memory storage for demo")
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")
    supabase = None

def get_supabase():
    return supabase