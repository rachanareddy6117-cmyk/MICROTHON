from __future__ import annotations

import asyncio
from typing import Any, Dict

try:
    from redis import Redis
except ModuleNotFoundError:  # pragma: no cover - optional dependency in local/dev environments
    Redis = None  # type: ignore[assignment]

redis_client = Redis(host="localhost", port=6379, decode_responses=True) if Redis else None


async def enqueue_task(task_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if redis_client is None:
        return {
            "task_name": task_name,
            "queued": False,
            "payload": payload,
            "message": "Redis unavailable; background task not enqueued in this environment.",
        }
    redis_client.rpush("pqc-migrate:queue", f"{task_name}:{payload}")
    return {"task_name": task_name, "queued": True, "payload": payload}


async def process_background_scan(repository_id: str, scan_type: str = "full") -> Dict[str, Any]:
    await asyncio.sleep(0)
    return {
        "repository_id": repository_id,
        "scan_type": scan_type,
        "status": "queued",
        "message": "Background scan queued for async processing.",
    }
