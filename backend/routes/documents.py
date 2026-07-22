import os

from fastapi import APIRouter
from services.vectordb import delete_document
from config import UPLOAD_FOLDER

router = APIRouter()


@router.get("/documents")
def list_documents():

    files = []

    for filename in sorted(os.listdir(UPLOAD_FOLDER)):

        path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if os.path.isfile(path):

            files.append({

                "filename": filename,

                "size_kb": round(
                    os.path.getsize(path) / 1024,
                    2
                )

            })

    return {

        "count": len(files),

        "documents": files

    }

@router.delete("/documents/{filename}")
def remove_document(filename: str):

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.exists(path):

        os.remove(path)

    delete_document(filename)

    return {

        "message":"Document removed"

    }

@router.delete("/documents")
def clear_documents():

    for filename in os.listdir(UPLOAD_FOLDER):

        path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if os.path.isfile(path):

            os.remove(path)

    from services.vectordb import collection

    collection.delete()

    return {

        "message":"Knowledge base cleared"

    }