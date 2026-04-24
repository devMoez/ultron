"""Phase 5 — System Monitor: 24h ring buffer, alerts, real-time metrics."""
import subprocess
import threading
import time
from collections import deque
from typing import Optional, Callable
import psutil
from core.logger import get_logger

log = get_logger("monitor")

# 24h at 1 sample/30s = 2880 samples
RING_SIZE = 2880
SAMPLE_INTERVAL = 30  # seconds

_ring: deque = deque(maxlen=RING_SIZE)
_ring_lock = threading.Lock()

_alert_handlers: list[Callable] = []
_alert_thresholds = {
    "cpu":  90.0,   # %
    "ram":  90.0,   # %
    "disk": 95.0,   # %
    "gpu":  95.0,   # %
}


# ── Sampling ──────────────────────────────────────────────────────────────────

def _gpu_pct() -> Optional[float]:
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=2,
        )
        if r.returncode == 0:
            return float(r.stdout.strip().split("\n")[0])
    except Exception:
        pass
    return None


def snapshot() -> dict:
    cpu   = psutil.cpu_percent(interval=1)
    mem   = psutil.virtual_memory()
    disk  = psutil.disk_usage("/")
    net   = psutil.net_io_counters()
    gpu   = _gpu_pct()
    return {
        "ts":        time.time(),
        "cpu":       cpu,
        "ram_pct":   mem.percent,
        "ram_used":  mem.used,
        "ram_total": mem.total,
        "disk_pct":  disk.percent,
        "disk_used": disk.used,
        "disk_total":disk.total,
        "net_sent":  net.bytes_sent,
        "net_recv":  net.bytes_recv,
        "gpu":       gpu,
    }


def latest() -> Optional[dict]:
    with _ring_lock:
        return _ring[-1] if _ring else None


def history(minutes: int = 60) -> list[dict]:
    cutoff = time.time() - minutes * 60
    with _ring_lock:
        return [s for s in _ring if s["ts"] >= cutoff]


def history_all() -> list[dict]:
    with _ring_lock:
        return list(_ring)


# ── Alert system ──────────────────────────────────────────────────────────────

def set_threshold(metric: str, value: float) -> None:
    _alert_thresholds[metric] = value


def on_alert(callback: Callable) -> None:
    _alert_handlers.append(callback)


def _check_alerts(sample: dict) -> None:
    checks = {
        "cpu":  sample.get("cpu"),
        "ram":  sample.get("ram_pct"),
        "disk": sample.get("disk_pct"),
        "gpu":  sample.get("gpu"),
    }
    for metric, val in checks.items():
        if val is None:
            continue
        threshold = _alert_thresholds.get(metric, 100)
        if val >= threshold:
            alert = {
                "ts":      sample["ts"],
                "metric":  metric,
                "value":   val,
                "threshold": threshold,
            }
            log.warning(f"ALERT: {metric}={val:.1f}% >= {threshold}%")
            for cb in _alert_handlers:
                try:
                    cb(alert)
                except Exception:
                    pass


# ── Background loop ───────────────────────────────────────────────────────────

_running = False

def _monitor_loop() -> None:
    while _running:
        try:
            s = snapshot()
            with _ring_lock:
                _ring.append(s)
            _check_alerts(s)
        except Exception as e:
            log.error(f"Monitor error: {e}")
        time.sleep(SAMPLE_INTERVAL)


def start() -> None:
    global _running
    if _running:
        return
    _running = True
    t = threading.Thread(target=_monitor_loop, daemon=True, name="sys-monitor")
    t.start()
    log.info(f"System monitor started (interval={SAMPLE_INTERVAL}s, ring={RING_SIZE})")


def stop() -> None:
    global _running
    _running = False


# ── Stats helpers ─────────────────────────────────────────────────────────────

def averages(minutes: int = 60) -> dict:
    samples = history(minutes)
    if not samples:
        return {}
    def avg(key):
        vals = [s[key] for s in samples if s.get(key) is not None]
        return round(sum(vals) / len(vals), 2) if vals else None
    return {
        "cpu":      avg("cpu"),
        "ram_pct":  avg("ram_pct"),
        "disk_pct": avg("disk_pct"),
        "gpu":      avg("gpu"),
        "samples":  len(samples),
        "window_min": minutes,
    }


def peaks(minutes: int = 1440) -> dict:
    samples = history(minutes)
    if not samples:
        return {}
    def peak(key):
        vals = [s[key] for s in samples if s.get(key) is not None]
        return round(max(vals), 2) if vals else None
    return {
        "cpu":      peak("cpu"),
        "ram_pct":  peak("ram_pct"),
        "disk_pct": peak("disk_pct"),
        "gpu":      peak("gpu"),
    }
