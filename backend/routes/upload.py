import os
import shutil

from fastapi import APIRouter, UploadFile, File

from config import UPLOAD_FOLDER

from services.parser import extract_text
from services.chunker import create_chunks
from services.embedding import embed_chunks
from services.vectordb import (
    store_embeddings,
    reset_collection
)
from services.rag import conversation_history

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Clear previous chat
    conversation_history.clear()

    # Clear previous embeddings
    reset_collection()

    # Delete old PDFs
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            os.remove(os.path.join(UPLOAD_FOLDER, filename))

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text(file_path)

    chunks = create_chunks(
        pages,
        file.filename
    )

    embedded = embed_chunks(chunks)

    store_embeddings(embedded)

    return {
        "message": "PDF uploaded successfully",
        "pages": len(pages),
        "chunks": len(chunks),
        "embeddings": len(embedded)
    }