# This file handles semantic code retrieval from ChromaDB for agent context injection.
"""
RAG Retriever — given a query, returns the top-k most relevant code snippets.
Agents call retrieve() before any LLM prompt to inject relevant context.
"""
import sys
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = SWARM_ROOT / "memory" / "chroma"
COLLECTION  = "codebase"

_client: chromadb.PersistentClient | None = None
_col = None


def _get_collection():
    global _client, _col
    if _col is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        ef = embedding_functions.DefaultEmbeddingFunction()
        try:
            _col = _client.get_collection(name=COLLECTION, embedding_function=ef)
        except Exception:
            return None  # not ingested yet
    return _col


def retrieve(query: str, k: int = 5) -> list[dict]:
    """
    Return top-k relevant code snippets for the given query.

    Returns list of dicts:
        [{"file": "...", "chunk": 0, "text": "...snippet..."}, ...]
    """
    col = _get_collection()
    if col is None:
        return []

    try:
        results = col.query(query_texts=[query], n_results=min(k, col.count()))
    except Exception:
        return []

    snippets = []
    docs      = results.get("documents",  [[]])[0]
    metas     = results.get("metadatas",  [[]])[0]
    distances = results.get("distances",  [[]])[0]

    for doc, meta, dist in zip(docs, metas, distances):
        snippets.append({
            "file":       meta.get("file", "?"),
            "chunk":      meta.get("chunk", 0),
            "text":       doc,
            "similarity": round(1 - dist, 3),  # cosine: distance → similarity
        })

    return snippets


def format_context(snippets: list[dict], max_chars: int = 6000) -> str:
    """
    Format retrieved snippets into a compact context block for LLM injection.
    Respects max_chars budget to avoid token overflow.
    """
    if not snippets:
        return ""

    lines = ["<relevant_code>"]
    total = 0
    for s in snippets:
        header = f"\n### {s['file']} (similarity={s['similarity']})\n"
        body   = s["text"]
        chunk  = header + body
        if total + len(chunk) > max_chars:
            break
        lines.append(chunk)
        total += len(chunk)
    lines.append("</relevant_code>")
    return "\n".join(lines)


def retrieve_and_format(query: str, k: int = 5, max_chars: int = 6000) -> str:
    """Convenience: retrieve + format in one call."""
    return format_context(retrieve(query, k=k), max_chars=max_chars)
