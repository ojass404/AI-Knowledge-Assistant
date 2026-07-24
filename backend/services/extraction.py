import json
import re
import os
from urllib import response
from groq import Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

from services.vectordb import search_documents


def extract_information(question: str, fields: list[str]) -> dict:
    """
    Extract structured information from the uploaded PDF.
    """

    # Better retrieval query
    search_query = question + " " + " ".join(fields)

    results = search_documents(search_query)

    # Build context
    context = ""

    for chunk in results[:8]:
        context += f"""
Document:
{chunk['filename']}

Page:
{chunk['page']}

Content:
{chunk['text']}

-----------------------------
"""

    prompt = f"""
You are an expert PDF information extraction assistant.

Below is the retrieved context from a PDF.

{context}

Extract ONLY the following fields:

{", ".join(fields)}

Rules:

1. Return ONLY valid JSON.
2. Every requested field MUST appear.
3. If a value is missing, return null.
4. If multiple values exist, return a JSON array.
5. Never invent information.
6. Do not explain anything.
7. Do not use markdown.
"""

    response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
    messages=[
        {
            "role": "system",
            "content": "You are an expert PDF information extraction assistant. Always return valid JSON only."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

    text = response.choices[0].message.content

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return {
            "error": "No JSON found.",
            "raw_response": text
        }

    try:
        data = json.loads(match.group(0))

        for field in fields:
            if field not in data:
                data[field] = None

            if isinstance(data[field], str):
                data[field] = data[field].strip()

        return data

    except Exception:
        return {
            "error": "Invalid JSON.",
            "raw_response": text
        }