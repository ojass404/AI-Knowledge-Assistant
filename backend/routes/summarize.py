from fastapi import APIRouter

from services.summarizer import summarize_document

from pydantic import BaseModel


router = APIRouter()


class SummaryRequest(BaseModel):
    summary_type: str = "bullet"


@router.post("/summarize")
def summarize(request: SummaryRequest):
    return summarize_document(request.summary_type)