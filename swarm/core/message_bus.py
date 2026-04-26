"""
In-memory pub/sub message bus for agent communication.

Channels are plain strings, e.g.:
  "skill.code"    — tasks requiring the 'code' skill
  "agent.planner" — messages directed at the planner agent
  "broadcast"     — all-agent announcements

Usage:
    bus.subscribe("skill.code", my_callback)
    bus.publish("skill.code", {"event": "task_ready", "task_id": "abc"})
    bus.get_log(since=timestamp)   # for UI display
"""
import threading
import time
from collections import defaultdict
from typing import Callable


class MessageBus:
    def __init__(self):
        self._lock        = threading.RLock()
        self._subs:  dict[str, list[Callable]] = defaultdict(list)
        self._log:   list[dict]                = []

    def subscribe(self, channel: str, callback: Callable) -> None:
        with self._lock:
            self._subs[channel].append(callback)

    def unsubscribe(self, channel: str, callback: Callable) -> None:
        with self._lock:
            self._subs[channel] = [cb for cb in self._subs[channel] if cb is not callback]

    def publish(self, channel: str, message: dict) -> int:
        """Broadcast message to all subscribers of channel. Returns count."""
        with self._lock:
            subs = list(self._subs[channel])
            self._record(channel, message)
        notified = 0
        for cb in subs:
            try:
                cb(message)
                notified += 1
            except Exception:
                pass
        return notified

    def get_log(self, since: float = 0.0, limit: int = 200) -> list[dict]:
        with self._lock:
            filtered = [m for m in self._log if m["ts"] > since]
            return filtered[-limit:]

    def channels(self) -> list[str]:
        with self._lock:
            return list(self._subs.keys())

    def _record(self, channel: str, message: dict) -> None:
        entry = {"ts": time.time(), "channel": channel}
        # Include message fields but truncate long strings
        for k, v in message.items():
            entry[k] = v[:200] if isinstance(v, str) and len(v) > 200 else v
        self._log.append(entry)
        if len(self._log) > 1000:
            self._log = self._log[-1000:]


# Process-wide singleton
shared_bus = MessageBus()
