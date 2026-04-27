# This file handles codebase ingestion into ChromaDB for semantic code retrieval.
"""
RAG Ingest — chunks your repo into ~1000-token snippets and stores them in ChromaDB.

Usage:
    python swarm/rag/ingest.py [repo_root]

Defaults to the opencode repo root if no arg given.
"""
import argparse
import os
import sys
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

import chromadb
from chromadb.utils import embedding_functions

# ── Config ────────────────────────────────────────────────────────────────────
CHROMA_PATH  = SWARM_ROOT / "memory" / "chroma"
COLLECTION   = "codebase"
CHUNK_TOKENS = 1000      # approximate token target per chunk (1 token ≈ 4 chars)
CHUNK_CHARS  = CHUNK_TOKENS * 4
OVERLAP_CHARS = 200       # overlap between chunks to preserve context

INCLUDE_EXTS = {
    ".py", ".ts", ".tsx", ".js", ".jsx",
    ".go", ".rs", ".java", ".c", ".cpp", ".h",
    ".md", ".txt", ".toml", ".json", ".yaml", ".yml",
}
EXCLUDE_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", "coverage", ".turbo",
    "chroma",  # don't ingest the DB itself
}


def _should_include(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return False
    return path.suffix.lower() in INCLUDE_EXTS


def _chunk_text(text: str, file_path: str) -> list[dict]:
    """Split text into overlapping chunks. Returns list of {id, text, metadata}."""
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        chunk = text[start:end]
        chunks.append({
            "id":   f"{file_path}::{idx}",
            "text": chunk,
            "meta": {"file": file_path, "chunk": idx},
        })
        start = end - OVERLAP_CHARS
        idx += 1
    return chunks


def ingest(repo_root: str | Path, reset: bool = False) -> int:
    """
    Ingest all code files from repo_root into ChromaDB.
    Returns number of chunks stored.
    """
    repo_root = Path(repo_root).resolve()
    print(f"[ingest] Scanning {repo_root}")

    # Init Chroma (persistent local DB)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    ef = embedding_functions.DefaultEmbeddingFunction()  # local all-MiniLM-L6-v2

    if reset and COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
        print(f"[ingest] Cleared existing collection '{COLLECTION}'")

    col = client.get_or_create_collection(
        name=COLLECTION,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    files = [p for p in repo_root.rglob("*") if p.is_file() and _should_include(p)]
    print(f"[ingest] Found {len(files)} files to index")

    total_chunks = 0
    batch_ids, batch_docs, batch_metas = [], [], []
    BATCH_SIZE = 100

    for fpath in files:
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        rel = str(fpath.relative_to(repo_root)).replace("\\", "/")
        for chunk in _chunk_text(text, rel):
            batch_ids.append(chunk["id"])
            batch_docs.append(chunk["text"])
            batch_metas.append(chunk["meta"])
            total_chunks += 1

            if len(batch_ids) >= BATCH_SIZE:
                col.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
                batch_ids, batch_docs, batch_metas = [], [], []

    if batch_ids:
        col.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

    print(f"[ingest] Done — {total_chunks} chunks stored in '{COLLECTION}'")
    return total_chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest codebase into ChromaDB")
    parser.add_argument("repo_root", nargs="?", default=str(SWARM_ROOT.parent))
    parser.add_argument("--reset", action="store_true", help="Wipe collection before ingest")
    args = parser.parse_args()
    ingest(args.repo_root, reset=args.reset)
