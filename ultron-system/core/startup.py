"""Phase 8 — Auto Start: boot sequence, resume tasks, scan MCPs, start agents."""
import time
from core.logger import get_logger
from core import state, memory, tasks as task_mgr, monitor, recovery, intelligence, optimizer, privacy

log = get_logger("startup")


def boot() -> dict:
    """
    Full Ultron boot sequence.
    Returns dict of boot results per phase.
    """
    results = {}
    started_at = time.time()
    log.info("=" * 50)
    log.info("ULTRON TRACKER SYSTEM - BOOTING")
    log.info("=" * 50)

    # Phase 1 — State
    try:
        state.load()
        state.set("boot_at", started_at)
        results["state"] = "ok"
        log.info("[1] State loaded")
    except Exception as e:
        results["state"] = f"error: {e}"
        log.error(f"[1] State load failed: {e}")

    # Phase 2 — Memory
    try:
        expired = memory.purge_expired()
        results["memory"] = f"ok (purged {expired} expired)"
        log.info(f"[2] Memory ready — purged {expired} expired temporal entries")
    except Exception as e:
        results["memory"] = f"error: {e}"
        log.error(f"[2] Memory init failed: {e}")

    # Phase 4 — Tasks DB
    try:
        task_mgr.init_db()
        task_mgr.start_reminder_watcher()
        stats = task_mgr.stats()
        results["tasks"] = f"ok — {stats['pending']} pending, {stats['done']} done"
        log.info(f"[4] Task DB ready: {stats}")
    except Exception as e:
        results["tasks"] = f"error: {e}"
        log.error(f"[4] Task init failed: {e}")

    # Phase 5 — System monitor
    try:
        monitor.start()
        results["monitor"] = "ok"
        log.info("[5] System monitor started")
    except Exception as e:
        results["monitor"] = f"error: {e}"
        log.error(f"[5] Monitor start failed: {e}")

    # Phase 7 — Recovery: resume interrupted tasks
    try:
        recovery.start_watchdog()
        resumed = recovery.resume_interrupted_tasks()
        results["recovery"] = f"ok — {len(resumed)} tasks resumed"
        log.info(f"[7] Recovery: resumed {len(resumed)} tasks")
    except Exception as e:
        results["recovery"] = f"error: {e}"
        log.error(f"[7] Recovery failed: {e}")

    # Phase 10 — Intelligence scheduler
    try:
        intelligence.start_scheduler()
        results["intelligence"] = "ok"
        log.info("[10] Intelligence scheduler started")
    except Exception as e:
        results["intelligence"] = f"error: {e}"
        log.error(f"[10] Intelligence start failed: {e}")

    # Phase 11 — Privacy
    try:
        privacy.ensure_gitignore()
        # Create default Moez profile if not exists
        if not privacy.get_user("moez"):
            privacy.create_user("moez", display_name="Moez", prefs={
                "theme": "dark",
                "verbosity": "normal",
                "timezone": "Asia/Karachi",
                "language": "en",
                "notify": True,
            })
        results["privacy"] = "ok"
        log.info("[11] Privacy & user system ready")
    except Exception as e:
        results["privacy"] = f"error: {e}"
        log.error(f"[11] Privacy init failed: {e}")

    # Phase 12 — Optimizer
    try:
        optimizer.start()
        results["optimizer"] = "ok"
        log.info("[12] Optimizer started")
    except Exception as e:
        results["optimizer"] = f"error: {e}"
        log.error(f"[12] Optimizer start failed: {e}")

    elapsed = round(time.time() - started_at, 2)
    ok_count = sum(1 for v in results.values() if v.startswith("ok"))
    log.info(f"Boot complete in {elapsed}s — {ok_count}/{len(results)} phases OK")
    log.info("=" * 50)

    state.set("last_boot", started_at)
    state.set("boot_results", results)

    return results
