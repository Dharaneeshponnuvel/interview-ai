import os
from dotenv import load_dotenv

# Load .env file (this must be at the top)
load_dotenv()

# Debug print to confirm environment variables are loaded
print("Gemini Key Loaded:", bool(os.getenv("GEMINI_API_KEY")))
print("Google Key Loaded:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# === Gemini API ===
# ✅ Read the Gemini key from .env or environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "models/gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/{GEMINI_MODEL}:generateContent"


# === Google Cloud Optional Audio ===
# ✅ Read the *variable name*, not the path directly
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# === Settings ===
MAX_RESUME_CHARS = 20000
DEFAULT_NUM_QUESTIONS = 5
