from backend.services.parser import extract_text
from backend.services.chunker import create_chunks
from backend.services.embedding import embed_chunks

pages = extract_text("/Users/ojasmahajan/Public/Projects/AI-Knowledge-Assistant/backend/uploads/Decentralized Micro-Credential Verification Framework.pdf")

chunks = create_chunks(pages)

embedded = embed_chunks(chunks)

print("Pages:", len(pages))
print("Chunks:", len(chunks))
print("Embeddings:", len(embedded))

print("\nEmbedding Length:")

print(len(embedded[0]["embedding"]))