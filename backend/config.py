import os

UPLOAD_FOLDER = "uploads"

CHROMA_DB_PATH = "chroma_db"

OLLAMA_MODEL = "llama3.2"

MAX_SEARCH_RESULTS = 5

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "llama3.2"

OLLAMA_URL = "http://host.docker.internal:11434"