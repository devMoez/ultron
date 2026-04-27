# This file handles all LLM routing for the Ultron swarm — one place to swap models.
"""
Universal LLM Router using litellm.
Maps task types to optimal models with automatic fallback.
"""
import json
import os
import time
from typing import Any

import litellm
from litellm import completion
from pydantic import BaseModel

# ── Observability callback ────────────────────────────────────────────────────
from observability import log_llm_call

litellm.success_callback = [log_llm_call]
litellm.failure_callback = [log_llm_call]

# ── Model Map ─────────────────────────────────────────────────────────────────
# Override any model via env vars, e.g. ULTRON_REASONING_MODEL=openai/gpt-4o
MODEL_MAP = {
    # Deep reasoning, planning, self-improvement (1M ctx, cheap)
    "reasoning": os.environ.get("ULTRON_REASONING_MODEL", "deepseek/deepseek-r1"),
    # Fast code edits, tool calls, JSON output (blazing fast, cheap)
    "quick":     os.environ.get("ULTRON_QUICK_MODEL",     "deepseek/deepseek-chat"),
    # Vision — screenshots, UI understanding
    "vision":    os.environ.get("ULTRON_VISION_MODEL",    "gemini/gemini-2.0-flash"),
    # Long-context synthesis — summarising large codebases
    "longctx":   os.environ.get("ULTRON_LONGCTX_MODEL",   "gemini/gemini-2.0-pro-exp"),
}

# Fallback chain: if primary model fails, try these in order
FALLBACK_MAP = {
    "reasoning": ["deepseek/deepseek-chat",    "openai/gpt-4o-mini"],
    "quick":     ["openai/gpt-4o-mini",        "groq/llama3-70b-8192"],
    "vision":    ["openai/gpt-4o-mini",        "gemini/gemini-2.0-flash"],
    "longctx":   ["deepseek/deepseek-r1",      "openai/gpt-4o"],
}

# Default generation params per tier
DEFAULTS = {
    "reasoning": {"temperature": 0.2, "max_tokens": 8192},
    "quick":     {"temperature": 0.0, "max_tokens": 4096},
    "vision":    {"temperature": 0.1, "max_tokens": 2048},
    "longctx":   {"temperature": 0.1, "max_tokens": 8192},
}


def call(
    tier: str,
    messages: list[dict],
    response_format: type[BaseModel] | None = None,
    **kwargs: Any,
) -> str:
    """
    Call the LLM for a given tier. Returns the text content of the response.

    Args:
        tier:            One of 'reasoning', 'quick', 'vision', 'longctx'
        messages:        OpenAI-format message list
        response_format: Optional Pydantic model for structured JSON output
        **kwargs:        Override any litellm parameter

    Returns:
        str — the assistant message content
    """
    model = MODEL_MAP.get(tier, MODEL_MAP["quick"])
    params = {**DEFAULTS.get(tier, {}), **kwargs}

    if response_format is not None:
        params["response_format"] = response_format

    try:
        resp = completion(
            model=model,
            messages=messages,
            fallbacks=FALLBACK_MAP.get(tier, []),
            **params,
        )
        return resp.choices[0].message.content or ""
    except Exception as exc:
        raise RuntimeError(f"LLM call failed (tier={tier}, model={model}): {exc}") from exc


def call_json(tier: str, messages: list[dict], schema: type[BaseModel], **kwargs) -> BaseModel:
    """
    Convenience wrapper — call LLM and parse result into a Pydantic model.
    Uses JSON mode automatically.
    """
    raw = call(tier, messages, response_format=schema, **kwargs)
    # litellm may return raw JSON string when response_format is a Pydantic model
    if isinstance(raw, str):
        return schema.model_validate_json(raw)
    return raw  # type: ignore[return-value]


# ── Convenience shortcuts ─────────────────────────────────────────────────────

def reason(messages: list[dict], **kw) -> str:
    """Deep reasoning — use for planning, self-improvement, complex analysis."""
    return call("reasoning", messages, **kw)


def quick(messages: list[dict], **kw) -> str:
    """Fast, cheap — use for JSON extraction, simple code, tool calls."""
    return call("quick", messages, **kw)


def vision(messages: list[dict], image_url: str | None = None, **kw) -> str:
    """Vision — use for screenshot or image understanding."""
    if image_url:
        # inject image into last user message
        for msg in reversed(messages):
            if msg["role"] == "user":
                msg["content"] = [
                    {"type": "text",      "text": msg["content"]},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ]
                break
    return call("vision", messages, **kw)


def longctx(messages: list[dict], **kw) -> str:
    """Long-context synthesis — use for large codebase / doc summarisation."""
    return call("longctx", messages, **kw)
