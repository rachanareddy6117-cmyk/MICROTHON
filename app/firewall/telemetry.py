import asyncio
from typing import List, Dict, Any

class FirewallTelemetryHub:
    """
    Real-time pub/sub broadcaster for firewall handshake events, policy alerts, and telemetry.
    Supports WebSocket event streaming.
    """
    def __init__(self):
        self._subscribers: List[asyncio.Queue] = []

    def subscribe(self) -> asyncio.Queue:
        q = asyncio.Queue()
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        if q in self._subscribers:
            self._subscribers.remove(q)

    async def broadcast_event(self, event: Dict[str, Any]):
        for q in self._subscribers:
            try:
                await q.put(event)
            except Exception:
                pass

telemetry_hub = FirewallTelemetryHub()
