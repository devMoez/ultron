"""
Ultron Master System — Main Entry Point
Runs the full boot sequence then starts the dashboard.
"""
import sys
import time
from pathlib import Path

# Add ultron-system to path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.logger import get_logger
from core.startup import boot
from core.config import DASHBOARD_PORT

log = get_logger("main")


def main():
    log.info("Ultron Master System starting...")

    # Run full boot sequence (phases 1-12)
    results = boot()

    # Print boot report
    print("\n" + "=" * 50)
    print("  ULTRON MASTER - BOOT REPORT")
    print("=" * 50)
    for phase, status in results.items():
        icon = "OK" if status.startswith("ok") else "!!"
        print(f"  [{icon}]  {phase:<15} {status}")
    print("=" * 50)
    print(f"\n  Dashboard: http://127.0.0.1:{DASHBOARD_PORT}")
    print("=" * 50 + "\n")

    # Start dashboard (blocking)
    import uvicorn
    from dashboard import app
    uvicorn.run(app, host="127.0.0.1", port=DASHBOARD_PORT, log_level="warning")


if __name__ == "__main__":
    main()
