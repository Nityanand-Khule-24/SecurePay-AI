from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Find .env in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL loaded:", bool(SUPABASE_URL))
print("KEY loaded:", bool(SUPABASE_KEY))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are not set.")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("Supabase connection initialized successfully....")