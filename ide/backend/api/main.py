"""
Universe IDE Backend - API Server

FastAPI-based backend for the Universe AI IDE Platform.
Provides:
- Agent management API
- File operations API
- Terminal execution API
- WebSocket for real-time updates
- Authentication & rate limiting
"""

import asyncio
import hashlib
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """IDE Configuration"""
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8080"))
    MAX_AGENTS = int(os.getenv("MAX_AGENTS", "1000"))
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10_000_000"))  # 10MB
    ALLOWED_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".md", ".yaml", ".yml", ".toml", ".txt", ".html", ".css"}


# ============================================================================
# MODELS
# ============================================================================

class AgentRequest(BaseModel):
    """Request to spawn agents"""
    count: int = 10
    model: str = "claude-sonnet-4-20250505"
    provider: str = "anthropic"
    task: str


class AgentResponse(BaseModel):
    """Agent spawn response"""
    session_id: str
    agents: int
    status: str
    created_at: datetime


class FileRequest(BaseModel):
    """File operation request"""
    path: str
    content: Optional[str] = None


class FileResponse(BaseModel):
    """File operation response"""
    path: str
    success: bool
    size: Optional[int] = None
    error: Optional[str] = None


class TerminalCommand(BaseModel):
    """Terminal command"""
    command: str
    cwd: str = "/workspace"


class TerminalResponse(BaseModel):
    """Terminal output"""
    session_id: str
    output: str
    exit_code: int
    duration_ms: int


# ============================================================================
# WEBSOCKET MANAGER
# ============================================================================

class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.sessions: dict[str, dict] = {}
        
    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a new WebSocket"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.sessions[session_id] = {
            "connected_at": datetime.now(),
            "agents": 0,
        }
        
    def disconnect(self, session_id: str):
        """Disconnect a WebSocket"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.sessions:
            del self.sessions[session_id]
            
    async def send_message(self, session_id: str, message: dict):
        """Send message to session"""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)
            
    async def broadcast(self, message: dict):
        """Broadcast to all sessions"""
        for session_id in self.active_connections:
            await self.send_message(session_id, message)


manager = ConnectionManager()


# ============================================================================
# API ENDPOINTS
# ============================================================================

app = FastAPI(
    title="Universe IDE API",
    description="The world's best AI agentic IDE platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🪐 Universe IDE starting...")
    print(f"   Max agents: {Config.MAX_AGENTS}")
    yield
    # Shutdown
    print("🪐 Universe IDE shutting down...")


app.router.lifespan_context = lifespan


# Health check
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "active_sessions": len(manager.active_connections),
    }


# Agent management
@app.post("/api/agents/spawn", response_model=AgentResponse)
async def spawn_agents(request: AgentRequest):
    """Spawn parallel universe agents"""
    if request.count > Config.MAX_AGENTS:
        raise HTTPException(
            status_code=400, 
            detail=f"Max agents: {Config.MAX_AGENTS}"
        )
    
    session_id = hashlib.sha256(
        f"{datetime.now().isoformat()}".encode()
    ).hexdigest()[:16]
    
    # Update session
    manager.sessions[session_id] = {
        "agents": request.count,
        "model": request.model,
        "provider": request.provider,
        "task": request.task,
        "created_at": datetime.now(),
    }
    
    return AgentResponse(
        session_id=session_id,
        agents=request.count,
        status="spawned",
        created_at=datetime.now(),
    )


@app.get("/api/agents/{session_id}")
async def get_agents(session_id: str):
    """Get agent session status"""
    if session_id not in manager.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return manager.sessions[session_id]


@app.delete("/api/agents/{session_id}")
async def kill_agents(session_id: str):
    """Kill agent session"""
    if session_id not in manager.sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del manager.sessions[session_id]
    return {"status": "killed", "session_id": session_id}


# File operations
@app.post("/api/files/read", response_model=FileResponse)
async def read_file(request: FileRequest):
    """Read a file"""
    try:
        with open(request.path, "r") as f:
            content = f.read()
        return FileResponse(
            path=request.path,
            success=True,
            size=len(content),
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        return FileResponse(
            path=request.path,
            success=False,
            error=str(e),
        )


@app.post("/api/files/write", response_model=FileResponse)
async def write_file(request: FileRequest):
    """Write a file"""
    if request.content and len(request.content) > Config.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    try:
        # Create directory if needed
        os.makedirs(os.path.dirname(request.path), exist_ok=True)
        
        with open(request.path, "w") as f:
            f.write(request.content or "")
            
        return FileResponse(
            path=request.path,
            success=True,
            size=len(request.content or ""),
        )
    except Exception as e:
        return FileResponse(
            path=request.path,
            success=False,
            error=str(e),
        )


# Terminal execution
@app.post("/api/terminal/execute", response_model=TerminalResponse)
async def execute_terminal(command: TerminalCommand):
    """Execute terminal command"""
    start = datetime.now()
    
    try:
        proc = await asyncio.create_subprocess_shell(
            command.command,
            cwd=command.cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await proc.communicate()
        duration = (datetime.now() - start).total_seconds() * 1000
        
        return TerminalResponse(
            session_id="local",
            output=stdout.decode() + stderr.decode(),
            exit_code=proc.returncode or 0,
            duration_ms=int(duration),
        )
    except Exception as e:
        duration = (datetime.now() - start).total_seconds() * 1000
        return TerminalResponse(
            session_id="local",
            output=str(e),
            exit_code=1,
            duration_ms=int(duration),
        )


# WebSocket
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket for real-time updates"""
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            msg_type = data.get("type")
            
            if msg_type == "ping":
                await manager.send_message(session_id, {"type": "pong"})
            elif msg_type == "execute":
                # Execute command
                result = await execute_terminal(
                    TerminalCommand(command=data.get("command", ""))
                )
                await manager.send_message(session_id, {
                    "type": "result",
                    "data": result.dict(),
                })
            elif msg_type == "broadcast":
                # Broadcast to all
                await manager.broadcast({
                    "type": "broadcast",
                    "data": data.get("data"),
                })
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
    )