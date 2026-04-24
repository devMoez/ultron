"""Phase 2 — 7-Layer Memory Engine."""
import json
import time
import threading
from pathlib import Path
from typing import Any, Optional
from core.config import MEMORY_DIR
from core.logger import get_logger

log = get_logger("memory")

LAYERS = {
    "global":   MEMORY_DIR / "global",
    "personal": MEMORY_DIR / "personal",
    "project":  MEMORY_DIR / "projects",
    "shared":   MEMORY_DIR / "shared",
    "semantic": MEMORY_DIR / "semantic",
    "temporal": MEMORY_DIR / "temporal",
    "action":   MEMORY_DIR / "action",
}
for _p in LAYERS.values():
    _p.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()


# ── Core I/O ──────────────────────────────────────────────────────────────────

def _path(layer: str, key: str) -> Path:
    if layer not in LAYERS:
        raise ValueError(f"Unknown memory layer: {layer}")
    return LAYERS[layer] / f"{key}.json"


def write(layer: str, key: str, value: Any, meta: Optional[dict] = None) -> None:
    """Write a value to a memory layer."""
    p = _path(layer, key)
    entry = {
        "key": key,
        "layer": layer,
        "value": value,
        "updated_at": time.time(),
        "meta": meta or {},
    }
    with _lock:
        p.write_text(json.dumps(entry, indent=2, default=str), encoding="utf-8")
    log.debug(f"memory.write {layer}/{key}")


def read(layer: str, key: str, default: Any = None) -> Any:
    """Read a value from a memory layer."""
    p = _path(layer, key)
    if not p.exists():
        return default
    try:
        with _lock:
            data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("value", default)
    except Exception as e:
        log.error(f"memory.read {layer}/{key}: {e}")
        return default


def delete(layer: str, key: str) -> bool:
    p = _path(layer, key)
    if p.exists():
        p.unlink()
        return True
    return False


def list_keys(layer: str) -> list[str]:
    return [p.stem for p in LAYERS[layer].glob("*.json")]


def search(query: str, layers: Optional[list[str]] = None) -> list[dict]:
    """Simple keyword search across memory layers."""
    results = []
    targets = layers or list(LAYERS.keys())
    q = query.lower()
    for layer in targets:
        for p in LAYERS[layer].glob("*.json"):
            try:
                raw = p.read_text(encoding="utf-8")
                if q in raw.lower():
                    data = json.loads(raw)
                    results.append({
                        "layer": layer,
                        "key": p.stem,
                        "value": data.get("value"),
                        "updated_at": data.get("updated_at"),
                    })
            except Exception:
                pass
    results.sort(key=lambda x: x.get("updated_at") or 0, reverse=True)
    return results


def dump_layer(layer: str) -> dict:
    """Return all key-value pairs in a layer."""
    out = {}
    for key in list_keys(layer):
        out[key] = read(layer, key)
    return out


# ── Temporal memory (auto-expire) ────────────────────────────────────────────

def write_temporal(key: str, value: Any, ttl_seconds: int = 3600) -> None:
    write("temporal", key, value, meta={"expires_at": time.time() + ttl_seconds})


def read_temporal(key: str, default: Any = None) -> Any:
    p = _path("temporal", key)
    if not p.exists():
        return default
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        expires = data.get("meta", {}).get("expires_at", 0)
        if time.time() > expires:
            p.unlink()
            return default
        return data.get("value", default)
    except Exception:
        return default


def purge_expired() -> int:
    """Remove expired temporal memories. Returns count removed."""
    removed = 0
    for p in LAYERS["temporal"].glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            expires = data.get("meta", {}).get("expires_at", float("inf"))
            if time.time() > expires:
                p.unlink()
                removed += 1
        except Exception:
            pass
    return removed


# ── Action memory (append-only log) ──────────────────────────────────────────

ACTION_LOG = MEMORY_DIR / "action" / "action_log.jsonl"

def log_action(action: str, details: Optional[dict] = None) -> None:
    entry = {
        "ts": time.time(),
        "action": action,
        "details": details or {},
    }
    with _lock:
        with open(ACTION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")


def recent_actions(n: int = 50) -> list[dict]:
    if not ACTION_LOG.exists():
        return []
    try:
        lines = ACTION_LOG.read_text(encoding="utf-8").splitlines()
        return [json.loads(l) for l in lines[-n:] if l.strip()]
    except Exception:
        return []


# ── Semantic memory (tag-indexed facts) ──────────────────────────────────────

def write_semantic(key: str, fact: str, tags: Optional[list[str]] = None) -> None:
    write("semantic", key, {"fact": fact, "tags": tags or []})


def search_semantic(tag: str) -> list[dict]:
    results = []
    for p in LAYERS["semantic"].glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            val = data.get("value", {})
            if tag in val.get("tags", []):
                results.append({"key": p.stem, **val})
        except Exception:
            pass
    return results
