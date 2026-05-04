"""WebSocket routes for real-time notifications."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.websocket.manager import manager
from app.core.security import decode_token
from app.services.child_service import ChildService

router = APIRouter()


@router.websocket("/ws/notifications/{child_id}")
async def websocket_notifications(
    websocket: WebSocket,
    child_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    """WebSocket endpoint for real-time notifications."""
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))

        ChildService.verify_child_ownership(db, child_id, user_id)

        await manager.connect(websocket, child_id)

        try:
            while True:
                data = await websocket.receive_text()

        except WebSocketDisconnect:
            manager.disconnect(websocket, child_id)

    except Exception as e:
        await websocket.close(code=1008)
