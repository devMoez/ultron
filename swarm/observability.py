# This file handles all LLM call logging for Ultron — token usage, latency, errors.
"""
JSONL observability for litellm callbacks.
Every LLM call is appended as a single JSON line to logs/llm_calls.jsonl
"""
import json
import time
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "llm_calls.jsonl"


def log_llm_call(kwargs, completion_response=None, start_time=None, end_time=None):
    """
    litellm success_callback / failure_callback signature.
    Appends one JSON line per call to logs/llm_calls.jsonl.
    """
    try:
        entry = {
            "ts":          time.time(),
            "model":       kwargs.get("model", "unknown"),
            "tier":        _extract_tier(kwargs),
            "input_tokens":  0,
            "output_tokens": 0,
            "latency_ms":    0,
            "success":       completion_response is not None,
            "error":         None,
        }

        if start_time and end_time:
            entry["latency_ms"] = int((end_time - start_time) * 1000)

        if completion_response:
            usage = getattr(completion_response, "usage", None)
            if usage:
                entry["input_tokens"]  = getattr(usage, "prompt_tokens",     0)
                entry["output_tokens"] = getattr(usage, "completion_tokens", 0)
        else:
            # failure path — kwargs may contain exception info
            entry["error"] = str(kwargs.get("exception", "unknown error"))

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception:
        pass  # never let observability crash the main flow


def _extract_tier(kwargs: dict) -> str:
    """Infer tier from model name for log grouping."""
    model = kwargs.get("model", "")
    if "r1" in model or "reasoning" in model:
        return "reasoning"
    if "flash" in model or "mini" in model:
        return "vision"
    if "pro-exp" in model or "longctx" in model:
        return "longctx"
    return "quick"


def tail(n: int = 50) -> list[dict]:
    """Return the last n log entries as dicts — useful for the TUI dashboard."""
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(l) for l in lines[-n:] if l]


def summary() -> dict:
    """Return aggregate stats: total calls, tokens, cost estimate, errors."""
    entries = tail(n=100_000)
    if not entries:
        return {"calls": 0, "input_tokens": 0, "output_tokens": 0, "errors": 0}
    return {
        "calls":         len(entries),
        "input_tokens":  sum(e.get("input_tokens",  0) for e in entries),
        "output_tokens": sum(e.get("output_tokens", 0) for e in entries),
        "errors":        sum(1 for e in entries if not e.get("success")),
        "avg_latency_ms": int(sum(e.get("latency_ms", 0) for e in entries) / len(entries)),
    }
