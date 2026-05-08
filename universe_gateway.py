"""
Universe IDE - API Gateway Module

API gateway with rate limiting.
"""

from typing import Any, Callable, Dict, List, Optional
import time


# ============================================================================
# ROUTE
# ============================================================================

class Route:
    """API route"""
    
    def __init__(self, path: str, handler: Callable, methods: List[str] = None):
        self.path = path
        self.handler = handler
        self.methods = methods or ["GET"]


# ============================================================================
# GATEWAY
# ============================================================================

class APIGateway:
    """API Gateway"""
    
    def __init__(self):
        self.routes = {}
        self.middleware = []
        
    def add_route(self, route: Route):
        self.routes[route.path] = route
        
    def add_middleware(self, middleware: Callable):
        self.middleware.append(middleware)
        
    def handle(self, path: str, method: str) -> Optional[Dict]:
        # Apply middleware
        for mw in self.middleware:
            result = mw(path, method)
            if result:
                return result
                
        # Find route
        if path in self.routes:
            route = self.routes[path]
            if method in route.methods:
                return {"status": "ok", "handler": route.handler.__name__}
                
        return {"status": "not_found"}


# ============================================================================
# GATEWAY SERVER
# ============================================================================

class GatewayServer:
    """Run gateway"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.gateway = APIGateway()
        
    def start(self):
        return {"port": self.port, "routes": len(self.gateway.routes)}


# Global
_gateway = None

def get_gateway() -> APIGateway:
    global _gateway
    if _gateway is None:
        _gateway = APIGateway()
    return _gateway


__all__ = ["Route", "APIGateway", "GatewayServer", "get_gateway"]