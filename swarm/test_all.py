"""
Ultron Swarm - Full Feature Test Suite
Run: python swarm/test_all.py
"""
import os
import sys
import json
os.environ["LITELLM_LOG"] = "ERROR"

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

PASS = "[PASS]"
FAIL = "[FAIL]"
results = []

def test(name, fn):
    try:
        fn()
        print(f"{PASS} {name}")
        results.append((name, True, None))
    except Exception as e:
        print(f"{FAIL} {name}: {e}")
        results.append((name, False, str(e)))

# ── Test 1: API Keys loaded ────────────────────────────────────────────────────
def t_keys():
    assert os.environ.get("OPENROUTER_API_KEY"), "OPENROUTER_API_KEY not set"
    assert os.environ.get("DEEPSEEK_API_KEY"), "DEEPSEEK_API_KEY not set"

test("API keys loaded from .env", t_keys)

# ── Test 2: LLM Router - quick tier ───────────────────────────────────────────
def t_llm_quick():
    from llm_router import quick
    r = quick([{"role": "user", "content": "Say OK"}], max_tokens=5)
    assert r and len(r.strip()) > 0, "Empty response"

test("LLM Router - quick tier (OpenRouter/DeepSeek)", t_llm_quick)

# ── Test 3: LLM Router - reasoning tier ───────────────────────────────────────
def t_llm_reason():
    from llm_router import reason
    r = reason([{"role": "user", "content": "What is 2+2? Answer with just the number."}], max_tokens=10)
    assert r and "4" in r, f"Expected '4', got: {r}"

test("LLM Router - reasoning tier (deepseek-r1)", t_llm_reason)

# ── Test 4: Observability ─────────────────────────────────────────────────────
def t_obs():
    from observability import log_llm_call, summary
    # Simulate a call entry
    class FakeUsage:
        prompt_tokens = 42
        completion_tokens = 8
    class FakeResp:
        usage = FakeUsage()
    log_llm_call({"model": "openrouter/deepseek/deepseek-chat"}, completion_response=FakeResp())
    s = summary()
    assert s["calls"] >= 1, "No calls logged"
    assert s["input_tokens"] > 0, "No tokens logged"

test("Observability - JSONL logging + summary()", t_obs)

# ── Test 5: RAG retriever (pre-ingest) ────────────────────────────────────────
def t_rag_retriever():
    from rag.retriever import retrieve_and_format
    # Should return empty string if not yet ingested (not an error)
    r = retrieve_and_format("build a REST API")
    assert isinstance(r, str), "Should return string"

test("RAG retriever - graceful empty (not ingested yet)", t_rag_retriever)

# ── Test 6: RAG ingest (small subset) ────────────────────────────────────────
def t_rag_ingest():
    from rag.ingest import ingest
    # Only ingest the swarm/ dir for speed
    count = ingest(os.path.dirname(__file__), reset=True)
    assert count > 0, f"No chunks indexed, got {count}"

test("RAG ingest - swarm/ directory", t_rag_ingest)

# ── Test 7: RAG retrieval after ingest ────────────────────────────────────────
def t_rag_after():
    from rag.retriever import _index, retrieve_and_format
    # Reset singleton so it re-opens after ingest
    import rag.retriever as rr
    rr._index = None
    r = retrieve_and_format("LLM router model mapping")
    assert r and "<relevant_code>" in r, "No results returned after ingest"

test("RAG retrieval - after ingest", t_rag_after)

# ── Test 8: EvolutionAgent dry-run ───────────────────────────────────────────
def t_evolution():
    from evolution_agent import run
    result = run(
        {"task": "build REST API", "duration_sec": 30, "bottleneck": "planning took too long"},
        dry_run=True
    )
    assert result.get("bottleneck"), f"No proposal generated: {result}"
    assert result.get("target_file", "").endswith(".txt"), "Phase-1 safety: must target .txt prompt"

test("EvolutionAgent - dry-run proposal", t_evolution)

# ── Test 9: Planner decomposition (LLM) ──────────────────────────────────────
def t_planner():
    from agents.planner import _call_with_retry
    messages = [
        {"role": "system", "content": "You are Ultron's Planner. Return a Plan JSON."},
        {"role": "user",   "content": "Goal: Build a todo list REST API with tests\nProject path: /tmp/todo\n"},
    ]
    from agents.planner import Plan
    plan = _call_with_retry(messages)
    assert isinstance(plan, Plan), f"Expected Plan, got {type(plan)}"
    assert len(plan.steps) > 0, "Plan has no steps"

test("Planner - LLM decomposition (deepseek-r1)", t_planner)

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "="*50)
passed = sum(1 for _, ok, _ in results if ok)
total  = len(results)
print(f"Results: {passed}/{total} passed")
if passed < total:
    print("\nFailed tests:")
    for name, ok, err in results:
        if not ok:
            print(f"  - {name}: {err}")
print("="*50)
sys.exit(0 if passed == total else 1)
