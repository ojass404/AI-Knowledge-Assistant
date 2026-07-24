import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = "uploads"
CHROMA_DB_PATH = "chroma_db"
MAX_SEARCH_RESULTS = 5

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"