import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get Supabase URL and Key from environment variables
url: str = os.getenv('supa_url')
key: str = os.getenv('supa_key')

# Check if the environment variables are loaded correctly
if not url or not key:
    raise ValueError("Supabase URL or Key not found in environment variables.")

# Create Supabase client
supabase: Client = create_client(url, key)
print("Supabase client initialized successfully.")  # Debugging line