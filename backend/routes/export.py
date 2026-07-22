from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import uuid
import os

router = APIRouter()

EXPORT_FOLDER = "exports"

os.makedirs(EXPORT_FOLDER, exist_ok=True)


class ExportRequest(BaseModel):

    title: str

    content: str


@router.post("/export/pdf")
def export_pdf(request: ExportRequest):

    filename = f"{uuid.uuid4()}.pdf"

    filepath = os.path.join(
        EXPORT_FOLDER,
        filename
    )

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filepath)

    story = []

    story.append(
        Paragraph(
            f"<b>{request.title}</b>",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            request.content.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    return FileResponse(

        filepath,

        media_type="application/pdf",

        filename="AI_Knowledge_Assistant.pdf"

    )