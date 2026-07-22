import chromadb

from services.embedding import generate_embedding

# --------------------------------------------------
# ChromaDB Client
# --------------------------------------------------

import os
import chromadb

DB_PATH = os.path.join("backend", "chroma_db")

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name="pdf_chunks"
)

# --------------------------------------------------
# Store Embeddings
# --------------------------------------------------

def store_embeddings(embedded_chunks):

    for chunk in embedded_chunks:

        collection.add(

            ids=[f"{chunk['filename']}_{chunk['chunk_id']}"],

            embeddings=[chunk["embedding"]],

            documents=[chunk["text"]],

            metadatas=[
                {
                    "filename": chunk["filename"],
                    "page": chunk["page"],
                    "length": chunk["length"]
                }
            ]

        )

# --------------------------------------------------
# Semantic Search
# --------------------------------------------------

def search_documents(query, n_results=5):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    output = []

    for doc, meta, distance in zip(
        documents,
        metadatas,
        distances
    ):

        confidence = max(0, min(1, 1 - distance))

    output.append({

        "filename": meta.get("filename", "Unknown"),

        "page": meta.get("page", 0),

        "length": meta.get("length", 0),

        "text": doc,

        "distance": distance,

        "score": confidence

    })

    # Sort by smallest distance (best match first)
    output.sort(
        key=lambda x: x["distance"]
    )

    return output

# --------------------------------------------------
# View Database
# --------------------------------------------------

def show_all():

    return collection.get()

def delete_document(filename):

    collection.delete(

        where={

            "filename": filename

        }

    )

import chromadb

client = chromadb.PersistentClient(path="chroma_db")

COLLECTION_NAME = "pdf_chunks"

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def reset_collection():
    global collection

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )