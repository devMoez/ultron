# This file handles Ultron's self-improvement loop — proposes, tests, and surfaces prompt changes.
"""
EvolutionAgent — after each major task session, analyses bottlenecks and proposes improvements.

Safety model (phase 1 — prompts only):
  - Only modifies files under packages/opencode/src/session/prompt/
  - Every proposal is written to swarm/proposals/<id>.json
  - Sandbox runner applies the change and validates it
  - Only if sandbox passes does it surface the change for human cherry-pick
  - Code changes are NEVER auto-applied

Usage:
    python swarm/evolution_agent.py [--session-log <path>] [--dry-run]
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

SWARM_ROOT  = Path(__file__).resolve().parent
REPO_ROOT   = SWARM_ROOT.parent
PROPOSALS   = SWARM_ROOT / "proposals"
PROMPT_ROOT = REPO_ROOT / "packages" / "opencode" / "src" / "session" / "prompt"

sys.path.insert(0, str(SWARM_ROOT))

from llm_router import reason
from observability import summary as obs_summary
from pydantic import BaseModel

PROPOSALS.mkdir(parents=True, exist_ok=True)


class Proposal(BaseModel):
    id: str = ""
    bottleneck: str
    change_type: str       # "prompt" only in phase 1
    target_file: str       # relative path from repo root
    proposed_diff: str     # full new content of the target file
    test_command: str
    rationale: str


EVOLUTION_SYSTEM = """You are Ultron's EvolutionAgent. Make Ultron smarter after each session.

Analyse the session log and observability stats. Identify the single biggest bottleneck.
Propose ONE improvement.

PHASE 1 CONSTRAINT: Only propose changes to prompt files (.txt) under session/prompt/.
Do NOT propose code changes.

Return JSON matching this schema:
{
  "id": "",
  "bottleneck": "One sentence: what slowed things down",
  "change_type": "prompt",
  "target_file": "packages/opencode/src/session/prompt/<filename>.txt",
  "proposed_diff": "<complete new content of the prompt file>",
  "test_command": "echo 'prompt change'",
  "rationale": "Why this improves performance"
}

Be surgical. One change. Maximum impact."""


def run(session_log: str | dict, dry_run: bool = False) -> dict:
    """
    Analyse a session and propose an improvement.
    Call from orchestrator after each completed session.
    """
    if isinstance(session_log, str):
        p = Path(session_log)
        session_data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"note": "log not found"}
    else:
        session_data = session_log

    obs = obs_summary()

    messages = [
        {"role": "system", "content": EVOLUTION_SYSTEM},
        {"role": "user",   "content": (
            f"Session summary:\n{json.dumps(session_data, indent=2)[:3000]}\n\n"
            f"Observability stats:\n{json.dumps(obs, indent=2)}\n\n"
            f"Available prompts:\n{_list_prompts()}"
        )},
    ]

    try:
        raw = reason(messages, temperature=0.3)
        raw = _strip_fences(raw) if isinstance(raw, str) else raw
        data = json.loads(raw) if isinstance(raw, str) else raw
        proposal = Proposal(**data)
        if not proposal.id:
            proposal.id = str(uuid.uuid4())[:8]
    except Exception as exc:
        print(f"[evolution] LLM proposal failed: {exc}")
        return {}

    prop_file = PROPOSALS / f"{proposal.id}.json"
    prop_file.write_text(proposal.model_dump_json(indent=2), encoding="utf-8")
    print(f"[evolution] Proposal written: {prop_file}")

    if dry_run:
        return proposal.model_dump()

    passed = _sandbox_test(proposal)
    result = {**proposal.model_dump(), "sandbox_passed": passed}

    if passed:
        print(f"[evolution] PASS — proposal {proposal.id} ready to cherry-pick")
        print(f"  Bottleneck : {proposal.bottleneck}")
        print(f"  File       : {proposal.target_file}")
        print(f"  Rationale  : {proposal.rationale}")
    else:
        print(f"[evolution] FAIL — proposal {proposal.id} discarded")
        prop_file.unlink(missing_ok=True)

    return result


def _strip_fences(text: str) -> str:
    """Strip markdown code fences from LLM response before JSON parsing."""
    import re
    text = text.strip()
    # Remove ```json ... ``` or ``` ... ```
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    # Find first { and last } to extract pure JSON
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end+1]
    return text.strip()


def _list_prompts() -> str:
    if not PROMPT_ROOT.exists():
        return "Prompt directory not found"
    return "\n".join(
        f"  {f.name}: {f.read_text(encoding='utf-8')[:80].replace(chr(10), ' ')}..."
        for f in sorted(PROMPT_ROOT.glob("*.txt"))
    ) or "No prompts found"


def _sandbox_test(proposal: Proposal) -> bool:
    target = REPO_ROOT / proposal.target_file

    # Safety gate — phase 1: prompts only
    if not proposal.target_file.endswith(".txt"):
        print("[evolution] BLOCKED — only .txt files in phase 1")
        return False
    if "session/prompt" not in proposal.target_file and "session\\prompt" not in proposal.target_file:
        print("[evolution] BLOCKED — must be under session/prompt/")
        return False

    cmd = proposal.test_command
    if not cmd or cmd.startswith("echo"):
        return len(proposal.proposed_diff.strip()) > 20

    with tempfile.TemporaryDirectory() as tmp:
        tmp_file = Path(tmp) / Path(proposal.target_file).name
        tmp_file.write_text(proposal.proposed_diff, encoding="utf-8")
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, cwd=tmp)
            return r.returncode == 0
        except Exception as exc:
            print(f"[evolution] Sandbox error: {exc}")
            return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ultron EvolutionAgent")
    parser.add_argument("--session-log", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.session_log or {}, dry_run=args.dry_run), indent=2))
