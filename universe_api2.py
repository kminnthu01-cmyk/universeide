"""
Universe IDE - Developer API

REST API for external integrations.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


# ============================================================================
# API RESPONSE
# ============================================================================

@dataclass
class APIResponse:
    success: bool
    data: Any = None
    error: str = ""


# ============================================================================
# REST API
# ============================================================================

class RESTAPI:
    """REST API"""
    
    def __init__(self):
        self.routes = {}
        
    def route(self, path: str, method: str = "GET"):
        """Decorator for routes"""
        def decorator(func):
            self.routes[f"{method}:{path}"] = func
            return func
        return decorator
        
    def handle(self, method: str, path: str, data: dict = None) -> APIResponse:
        """Handle request"""
        key = f"{method}:{path}"
        
        if key in self.routes:
            try:
                result = self.routes[key](data or {})
                return APIResponse(success=True, data=result)
            except Exception as e:
                return APIResponse(success=False, error=str(e))
                
        return APIResponse(success=False, error="Not found")


# ============================================================================
# ENDPOINTS
# ============================================================================

class Endpoints:
    """API endpoints"""
    
    def __init__(self, api: RESTAPI):
        self.api = api
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup endpoints"""
        
        @self.api.route("/agents", "GET")
        def get_agents(data):
            from universe_ide import cosmos
            return {"count": cosmos(10).num_agents}
            
        @self.api.route("/agents", "POST")
        def create_agent(data):
            return {"id": "agent-1", "status": "created"}
            
        @self.api.route("/messages", "GET")
        def get_messages(data):
            return {"messages": []}
            
        @self.api.route("/messages", "POST")
        def send_message(data):
            return {"id": "msg-1", "status": "sent"}
            
        @self.api.route("/knowledge", "GET")
        def get_knowledge(data):
            return {"entries": []}
            
        @self.api.route("/knowledge", "POST")
        def store_knowledge(data):
            return {"status": "stored"}


# Global
_api = None

def get_api() -> RESTAPI:
    global _api
    if _api is None:
        _api = RESTAPI()
        Endpoints(_api)
    return _api


__all__ = [
    "APIResponse",
    "RESTAPI",
    "Endpoints",
    "get_api",
]