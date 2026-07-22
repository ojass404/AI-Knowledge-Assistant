from backend.services.parser import extract_text
from backend.services.chunker import create_chunks

pages = extract_text("/Users/ojasmahajan/Public/Projects/AI-Knowledge-Assistant/backend/uploads/Decentralized Micro-Credential Verification Framework.pdf")

chunks = create_chunks(pages)

print("Total Pages:", len(pages))
print("Total Chunks:", len(chunks))

print("\nFirst Chunk:")
print(chunks[0])

print("\nSecond Chunk:")
print(chunks[1])