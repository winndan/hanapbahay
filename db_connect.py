import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("supa_url")
supabase_key = os.getenv("supa_key")

if not supabase_url or not supabase_key:
    raise ValueError("Supabase URL or API Key is missing. Check .env file!")

supabase: Client = create_client(supabase_url, supabase_key)
print("✅ Supabase client initialized successfully")
