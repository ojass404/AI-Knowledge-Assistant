from pydantic import BaseModel


class Question(BaseModel):
    question: str


class ExtractionRequest(BaseModel):
    question: str
    fields: list[str]


class SummaryRequest(BaseModel):
    summary_type: str