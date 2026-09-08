from pathlib import Path
import json

import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
INDEX_DIR = BASE_DIR / "index"

CHUNKS_FILE = INDEX_DIR / "chunks.json"
EMBEDDINGS_FILE = INDEX_DIR / "embeddings.npy"


# -----------------------------
# Load saved data
# -----------------------------

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = np.load(EMBEDDINGS_FILE)


# -----------------------------
# Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Search function
# -----------------------------

def search(query, top_k=5):

    # Convert the question into an embedding
    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Calculate cosine similarity.
    # Because both vectors are normalized,
    # their dot product equals cosine similarity.
    scores = embeddings @ query_embedding

    # Get the indexes of the highest scores
    top_indexes = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indexes:

        chunk = chunks[index]

        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "section": chunk["section"],
            "similarity": float(scores[index])
        })

    return results


# -----------------------------
# Test the search engine
# -----------------------------

if __name__ == "__main__":

    question = input("\nAsk RuleGuard a question: ")

    results = search(question, top_k=5)

    print("\n========== SEARCH RESULTS ==========\n")

    for i, result in enumerate(results, start=1):

        print(f"Result {i}")
        print(f"Source: {result['source']}")
        print(f"Section: {result['section']}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Text: {result['text']}")
        print("-" * 70)