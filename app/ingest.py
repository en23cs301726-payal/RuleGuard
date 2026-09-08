from pathlib import Path
import json
import re

import numpy as np
import pandas as pd
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = BASE_DIR / "app" / "index"

INDEX_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# LOAD EMBEDDING MODEL
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# --------------------------------------------------
# STORAGE
# --------------------------------------------------

chunks = []


# --------------------------------------------------
# HELPER: ADD CHUNK
# --------------------------------------------------

def add_chunk(text, source, section):
    text = text.strip()

    if len(text) < 30:
        return

    chunks.append({
        "text": text,
        "source": source,
        "section": section
    })


# --------------------------------------------------
# READ MARKDOWN FILES
# --------------------------------------------------

def process_markdown(path):
    print(f"Reading Markdown: {path.name}")

    text = path.read_text(encoding="utf-8")

    # Split whenever a Markdown heading appears
    parts = re.split(r"(?=^##\s+)", text, flags=re.MULTILINE)

    for part in parts:
        part = part.strip()

        if not part:
            continue

        lines = part.splitlines()

        section = "General"

        if lines:
            first_line = lines[0].strip()

            if first_line.startswith("##"):
                section = first_line.lstrip("#").strip()

        add_chunk(
            text=part,
            source=path.name,
            section=section
        )


# --------------------------------------------------
# READ CSV FILE
# --------------------------------------------------

def process_csv(path):
    print(f"Reading CSV: {path.name}")

    df = pd.read_csv(path)

    for _, row in df.iterrows():

        values = []

        for column in df.columns:
            value = str(row[column])
            values.append(f"{column}: {value}")

        text = " | ".join(values)

        policy_id = str(row.get("policy_id", "CSV"))

        add_chunk(
            text=text,
            source=path.name,
            section=policy_id
        )


# --------------------------------------------------
# READ PDF FILE
# --------------------------------------------------

def process_pdf(path):
    print(f"Reading PDF: {path.name}")

    reader = PdfReader(str(path))

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text:
            continue

        add_chunk(
            text=text,
            source=path.name,
            section=f"Page {page_number}"
        )


# --------------------------------------------------
# PROCESS ALL FILES
# --------------------------------------------------

print("\nProcessing corpus...\n")

for path in DATA_DIR.iterdir():

    if path.suffix.lower() == ".md":
        process_markdown(path)

    elif path.suffix.lower() == ".csv":
        process_csv(path)

    elif path.suffix.lower() == ".pdf":
        process_pdf(path)


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

unique_chunks = []

seen = set()

for chunk in chunks:

    key = (
        chunk["source"],
        chunk["section"],
        chunk["text"]
    )

    if key not in seen:
        seen.add(key)
        unique_chunks.append(chunk)

chunks = unique_chunks


# --------------------------------------------------
# CREATE EMBEDDINGS
# --------------------------------------------------

print(f"\nTotal passages: {len(chunks)}")

texts = [chunk["text"] for chunk in chunks]

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

print("Embeddings created.")


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

metadata_path = INDEX_DIR / "chunks.json"
embeddings_path = INDEX_DIR / "embeddings.npy"

with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

np.save(embeddings_path, embeddings)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\n===================================")
print("RuleGuard ingestion complete!")
print("===================================")

print(f"Passages: {len(chunks)}")
print(f"Embedding dimensions: {embeddings.shape[1]}")

print(f"\nSaved:")
print(metadata_path)
print(embeddings_path)