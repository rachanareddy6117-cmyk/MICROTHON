from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ...firewall.telemetry import telemetry_hub

router = APIRouter(tags=["WebSocket Event Streaming"])

@router.websocket("/ws/events")
async def websocket_event_stream(websocket: WebSocket):
    await websocket.accept()
    queue = telemetry_hub.subscribe()
    try:
        await websocket.send_json({"type": "CONNECTED", "message": "PQC-Migrate Live Telemetry Stream"})
        while True:
            event = await queue.get()
            await websocket.send_json(event)
    except WebSocketDisconnect:
        telemetry_hub.unsubscribe(queue)
