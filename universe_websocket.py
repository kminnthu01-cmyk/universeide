"""
Universe IDE - WebSocket Manager

Real-time WebSocket communication.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# WEBSOCKET MESSAGE
# ============================================================================

class WSMessageType(Enum):
    """WebSocket message types"""
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    MESSAGE = "message"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"


@dataclass
class WSMessage:
    """WebSocket message"""
    msg_type: WSMessageType
    data: Any
    client_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


# ============================================================================
# WEBSOCKET CLIENT
# ============================================================================

class WSClient:
    """WebSocket client"""
    
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.connected = True
        
    def send(self, message: WSMessage):
        """Send message"""
        pass
        
    def close(self):
        """Close connection"""
        self.connected = False


# ============================================================================
# WEBSOCKET SERVER
# ============================================================================

class WSServer:
    """
    WebSocket server.
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8081):
        self.host = host
        self.port = port
        self.clients: dict[str, WSClient] = {}
        self.handlers: dict[WSMessageType, Callable] = {}
        self._running = False
        
    async def connect(self, client_id: str):
        """Connect client"""
        client = WSClient(client_id)
        self.clients[client_id] = client
        await self._handle(WSMessageType.CONNECT, {"client_id": client_id})
        
    async def disconnect(self, client_id: str):
        """Disconnect client"""
        if client_id in self.clients:
            self.clients[client_id].close()
            del self.clients[client_id]
        await self._handle(WSMessageType.DISCONNECT, {"client_id": client_id})
            
    async def send(self, client_id: str, message: WSMessage):
        """Send to client"""
        if client_id in self.clients:
            self.clients[client_id].send(message)
            
    async def broadcast(self, message: WSMessage):
        """Broadcast to all"""
        for client in self.clients.values():
            if client.connected:
                client.send(message)
                
    def register_handler(self, msg_type: WSMessageType, handler: Callable):
        """Register message handler"""
        self.handlers[msg_type] = handler
        
    async def _handle(self, msg_type: WSMessageType, data: dict):
        """Handle message"""
        if msg_type in self.handlers:
            handler = self.handlers[msg_type]
            if asyncio.iscoroutinefunction(handler):
                await handler(data)
            else:
                handler(data)
                
    async def start(self):
        """Start server"""
        self._running = True
        print(f"🔌 WS Server: ws://{self.host}:{self.port}")
        
    async def stop(self):
        """Stop server"""
        self._running = False
        for client in self.clients.values():
            client.close()
        self.clients.clear()


# ============================================================================
# WEBSOCKET CLIENT (BROWSER)
# ============================================================================

class WebSocketClient:
    """WebSocket client for browser"""
    
    def __init__(self, url: str):
        self.url = url
        self.ws = None
        
    async def connect(self):
        """Connect"""
        # In browser context, would use native WebSocket
        pass
        
    async def send(self, data: dict):
        """Send data"""
        pass
        
    async def receive(self) -> Optional[dict]:
        """Receive data"""
        return None


# ============================================================================
# REAL-TIME AGENT UPDATES
# ============================================================================

class RealtimeAgentUpdates:
    """Real-time agent update streaming"""
    
    def __init__(self):
        self.server = WSServer()
        
    async def stream_agent_status(self, agent_id: str):
        """Stream agent status"""
        while True:
            msg = WSMessage(
                msg_type=WSMessageType.MESSAGE,
                data={"agent_id": agent_id, "status": "running"},
            )
            await self.server.broadcast(msg)
            await asyncio.sleep(1)


# Global
_ws_server = None

def get_ws_server() -> WSServer:
    """Get WebSocket server"""
    global _ws_server
    if _ws_server is None:
        _ws_server = WSServer()
    return _ws_server


__all__ = [
    "WSMessageType",
    "WSMessage",
    "WSClient",
    "WSServer",
    "WebSocketClient",
    "RealtimeAgentUpdates",
    "get_ws_server",
]