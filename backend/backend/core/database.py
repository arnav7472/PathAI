from supabase import create_client, Client
from .config import settings

# Initialize Supabase client
try:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    print("✅ Supabase client initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize Supabase client: {e}")
    supabase = None

def get_supabase():
    return supabase