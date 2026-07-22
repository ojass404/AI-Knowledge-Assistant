import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.documents import router as documents_router

from config import UPLOAD_FOLDER

from models.schemas import (
    Question,
    ExtractionRequest
)

from routes.upload import router as upload_router
from routes.export import router as export_router
from routes.summarize import router as summarize_router

from services.parser import extract_text
from services.chunker import create_chunks
from services.embedding import embed_chunks
from services.vectordb import (
    search_documents,
    show_all
)
from services.rag import (
    ask_question,
    conversation_history
)
from services.extraction import extract_information

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="AI Knowledge Assistant"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Create Upload Folder
# --------------------------------------------------

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# --------------------------------------------------
# Register Routers
# --------------------------------------------------

app.include_router(upload_router)
app.include_router(documents_router)
app.include_router(export_router)
app.include_router(summarize_router)

# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to AI Knowledge Assistant!"
    }

# --------------------------------------------------
# Hello API
# --------------------------------------------------

@app.get("/hello")
def hello():

    return {
        "message": "Hello Ojas!"
    }

# --------------------------------------------------
# Student API
# --------------------------------------------------

@app.get("/student/{name}")
def student(name: str):

    return {
        "Student": name
    }

# --------------------------------------------------
# Square API
# --------------------------------------------------

@app.get("/square")
def square(number: int):

    return {
        "square": number * number
    }

# --------------------------------------------------
# Read Uploaded PDF
# --------------------------------------------------

@app.get("/pdf/{filename}")
def read_pdf(filename: str):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    pages = extract_text(file_path)

    return {

        "filename": filename,

        "pages": pages

    }

# --------------------------------------------------
# View Chunks
# --------------------------------------------------

@app.get("/chunks/{filename}")
def view_chunks(filename: str):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    pages = extract_text(file_path)

    chunks = create_chunks(
        pages,
        filename          # ✅ Correct
    )

    return {
        "filename": filename,
        "total_chunks": len(chunks),
        "chunks": chunks
    }

# --------------------------------------------------
# View ChromaDB
# --------------------------------------------------

@app.get("/database")
def database():

    data = show_all()

    return {

        "total_documents": len(data["documents"]),

        "documents": data["documents"][:3]

    }

# --------------------------------------------------
# Semantic Search
# --------------------------------------------------

@app.post("/search")
def search(question: Question):

    return search_documents(
        question.question
    )

# --------------------------------------------------
# Chat
# --------------------------------------------------

@app.post("/chat")
def chat(question: Question):

    return ask_question(
        question.question
    )

# --------------------------------------------------
# Clear Chat
# --------------------------------------------------

@app.post("/clear-chat")
def clear_chat():

    conversation_history.clear()

    return {

        "message": "Chat history cleared"

    }

# --------------------------------------------------
# Extract Information
# --------------------------------------------------

@app.post("/extract")
def extract(request: ExtractionRequest):

    return extract_information(

        request.question,

        request.fields

    )