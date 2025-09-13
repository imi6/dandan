"""WebSocket endpoints"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

router = APIRouter()


class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept and store a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: dict, client_id: str):
        """Send a message to a specific client"""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients"""
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except:
                # Client might be disconnected
                pass


# Create a global connection manager
manager = ConnectionManager()


@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time communication
    
    Supports:
    - MD5 calculation progress
    - Real-time danmaku
    - Video sync
    """
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                msg_type = message.get("type")
                
                if msg_type == "ping":
                    # Respond to ping
                    await manager.send_personal_message(
                        {"type": "pong"},
                        client_id
                    )
                
                elif msg_type == "md5_progress":
                    # Broadcast MD5 calculation progress
                    await manager.send_personal_message(
                        {
                            "type": "md5_progress",
                            "progress": message.get("progress", 0),
                            "video_id": message.get("video_id")
                        },
                        client_id
                    )
                
                elif msg_type == "danmaku":
                    # Broadcast danmaku to all clients
                    await manager.broadcast({
                        "type": "danmaku",
                        "content": message.get("content"),
                        "sender": client_id
                    })
                
                elif msg_type == "sync":
                    # Video sync message
                    await manager.broadcast({
                        "type": "sync",
                        "time": message.get("time"),
                        "playing": message.get("playing"),
                        "sender": client_id
                    })
                
                else:
                    # Echo unknown messages back
                    await manager.send_personal_message(
                        {"type": "error", "message": f"Unknown message type: {msg_type}"},
                        client_id
                    )
                    
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {"type": "error", "message": "Invalid JSON"},
                    client_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        # Notify others about disconnection
        await manager.broadcast({
            "type": "user_disconnected",
            "client_id": client_id
        })