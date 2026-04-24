"""Phase 10 — Daily Intelligence: summaries, missed tasks, performance insights."""
import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from core.config import MEMORY_DIR
from core.logger import get_logger
from core import tasks as task_mgr, monitor

log = get_logger("intelligence")

INTEL_DIR  = MEMORY_DIR / "shared" / "intelligence"
INTEL_DIR.mkdir(parents=True, exist_ok=True)


# ── Daily summary ─────────────────────────────────────────────────────────────

def generate_daily_summary(date: datetime = None) -> dict:
    if date is None:
        date = datetime.now()

    date_str = date.strftime("%Y-%m-%d")
    day_start = datetime(date.year, date.month, date.day).timestamp()
    day_end   = day_start + 86400

    # Task stats
    all_tasks = task_mgr.list_tasks(limit=500)
    day_tasks = [
        t for t in all_tasks
        if day_start <= (t.get("created_at") or 0) < day_end
    ]
    completed = [t for t in day_tasks if t.get("status") == "done"]
    failed    = [t for t in day_tasks if t.get("status") == "failed"]
    missed    = [
        t for t in all_tasks
        if t.get("due_at") and day_start <= t["due_at"] < day_end
        and t.get("status") not in ("done", "cancelled")
    ]

    # System perf
    perf = monitor.averages(minutes=1440)
    peak = monitor.peaks(minutes=1440)

    summary = {
        "date":        date_str,
        "generated_at": time.time(),
        "tasks": {
            "created":   len(day_tasks),
            "completed": len(completed),
            "failed":    len(failed),
            "missed_deadlines": len(missed),
            "completion_rate": (
                round(len(completed) / len(day_tasks) * 100, 1)
                if day_tasks else 0
            ),
        },
        "missed_tasks": [
            {"id": t["id"], "title": t["title"], "due": t.get("due_at")}
            for t in missed
        ],
        "system": {
            "avg_cpu":  perf.get("cpu"),
            "avg_ram":  perf.get("ram_pct"),
            "peak_cpu": peak.get("cpu"),
            "peak_ram": peak.get("ram_pct"),
        },
        "insights": _generate_insights(day_tasks, completed, failed, perf, peak),
    }

    _save_summary(date_str, summary)
    log.info(f"Daily summary generated for {date_str}")
    return summary


def _generate_insights(day_tasks, completed, failed, perf, peak) -> list[str]:
    insights = []

    if not day_tasks:
        insights.append("No tasks were created today.")
        return insights

    rate = len(completed) / len(day_tasks) * 100 if day_tasks else 0
    if rate >= 80:
        insights.append(f"Excellent day — {rate:.0f}% task completion rate.")
    elif rate >= 50:
        insights.append(f"Decent progress — {rate:.0f}% completion. Room to improve.")
    else:
        insights.append(f"Low completion rate ({rate:.0f}%). Consider breaking tasks into smaller pieces.")

    if failed:
        insights.append(f"{len(failed)} task(s) failed. Review errors in logs.")

    cpu = perf.get("cpu")
    if cpu and cpu > 70:
        insights.append(f"High avg CPU usage ({cpu:.0f}%). System was under heavy load.")

    ram = perf.get("ram_pct")
    if ram and ram > 80:
        insights.append(f"RAM pressure detected (avg {ram:.0f}%). Consider closing unused apps.")

    peak_cpu = peak.get("cpu")
    if peak_cpu and peak_cpu > 95:
        insights.append(f"CPU spiked to {peak_cpu:.0f}% — check for runaway processes.")

    return insights


def _save_summary(date_str: str, summary: dict) -> None:
    path = INTEL_DIR / f"summary_{date_str}.json"
    path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")


def load_summary(date_str: str) -> dict:
    path = INTEL_DIR / f"summary_{date_str}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def recent_summaries(days: int = 7) -> list[dict]:
    summaries = []
    for i in range(days):
        d = datetime.now() - timedelta(days=i)
        s = load_summary(d.strftime("%Y-%m-%d"))
        if s:
            summaries.append(s)
    return summaries


# ── Scheduled daily run ───────────────────────────────────────────────────────

def _schedule_daily() -> None:
    """Run daily summary at midnight."""
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(
            hour=0, minute=1, second=0, microsecond=0
        )
        sleep_secs = (next_midnight - now).total_seconds()
        log.info(f"Next daily summary in {sleep_secs/3600:.1f}h")
        time.sleep(sleep_secs)
        try:
            generate_daily_summary()
        except Exception as e:
            log.error(f"Daily summary error: {e}")


def start_scheduler() -> None:
    t = threading.Thread(target=_schedule_daily, daemon=True, name="intel-scheduler")
    t.start()
    log.info("Daily intelligence scheduler started")
