# Create a test file: test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing environment variables:")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_ANON_KEY: {'***' if os.getenv('SUPABASE_ANON_KEY') else 'None'}")
print(f"GROQ_API_KEY: {'***' if os.getenv('GROQ_API_KEY') else 'None'}")
print(f"REDIS_URL: {os.getenv('REDIS_URL')}")

# Check if .env file exists
import os.path
print(f".env file exists: {os.path.exists('.env')}")
print(f"Current directory: {os.getcwd()}")