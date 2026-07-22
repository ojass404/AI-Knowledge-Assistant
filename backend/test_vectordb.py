from backend.services.parser import extract_text

from backend.services.chunker import create_chunks

from backend.services.embedding import embed_chunks

from backend.services.vectordb import store_embeddings

pages = extract_text("/Users/ojasmahajan/Public/Projects/AI-Knowledge-Assistant/backend/uploads/Decentralized Micro-Credential Verification Framework.pdf")

chunks = create_chunks(pages)

embedded = embed_chunks(chunks)

store_embeddings(embedded)

print("Stored Successfully!")