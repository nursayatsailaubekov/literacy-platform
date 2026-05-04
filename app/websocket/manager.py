"""WebSocket connection manager for real-time notifications."""
from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """Manage WebSocket connections for real-time notifications."""

    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, child_id: int):
        """Accept a new WebSocket connection for a child."""
        await websocket.accept()
        if child_id not in self.active_connections:
            self.active_connections[child_id] = []
        self.active_connections[child_id].append(websocket)

    def disconnect(self, websocket: WebSocket, child_id: int):
        """Remove a WebSocket connection."""
        if child_id in self.active_connections:
            self.active_connections[child_id].remove(websocket)
            if not self.active_connections[child_id]:
                del self.active_connections[child_id]

    async def send_notification(self, child_id: int, message: dict):
        """Send a notification to all connections for a child."""
        if child_id in self.active_connections:
            for connection in self.active_connections[child_id]:
                await connection.send_json(message)

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_json(message)


manager = ConnectionManager()
