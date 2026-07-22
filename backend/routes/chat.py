from fastapi import APIRouter

from models.schemas import Question

from services.rag import ask_question


router = APIRouter()


@router.post("/chat")
def chat(request: Question):

    result = ask_question(request.question)

    return result