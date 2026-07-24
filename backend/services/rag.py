from groq import Groq

from config import GROQ_API_KEY, MODEL_NAME

from services.vectordb import search_documents

# --------------------------------------------------
# Initialize Groq Client
# --------------------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)

# --------------------------------------------------
# Conversation History
# --------------------------------------------------

conversation_history = []

# --------------------------------------------------
# Ask Question
# --------------------------------------------------

def ask_question(question):

    global conversation_history

    results = search_documents(question)

    # -----------------------------
    # Build Context
    # -----------------------------

    context = ""

    for chunk in results:

        context += f"""
Document:
{chunk['filename']}

Page:
{chunk['page']}

Content:
{chunk['text']}

-----------------------------
"""

    # -----------------------------
    # Prompt
    # -----------------------------

    messages = [
        {
            "role": "system",
            "content": """
You are an AI Knowledge Assistant.

Answer naturally.

Use ONLY the retrieved context.

If the answer is not present in the context,
reply politely that the information is not available
in the uploaded document.

Do NOT make up facts.

Do NOT answer in JSON unless the user explicitly asks.

Explain concepts in normal English.

Use bullet points whenever appropriate.
"""
        }
    ]

    messages.extend(conversation_history)

    messages.append(
        {
            "role": "user",
            "content": f"""
Context:

{context}

Question:

{question}
"""
        }
    )

    # -----------------------------
    # Generate Response
    # -----------------------------

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=messages,

        temperature=0.3,

        max_tokens=1024

    )

    answer = response.choices[0].message.content

    # -----------------------------
    # Save Conversation
    # -----------------------------

    conversation_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    conversation_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return {

        "answer": answer,

        "sources": results

    }