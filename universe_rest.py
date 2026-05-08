"""
Universe IDE - REST API Enhanced
"""

import uuid
from typing import Any, Dict


# ============================================================================
# REQUEST/RESPONSE
# ============================================================================

class Request:
    def __init__(self, method: str, path: str, body=None):
        self.method = method
        self.path = path
        self.body = body


class Response:
    def __init__(self, status=200, body=None):
        self.status = status
        self.body = body


# ============================================================================
# ROUTER
# ============================================================================

class Router:
    def __init__(self):
        self.routes = {}
        
    def add(self, path, method, handler):
        self.routes[f"{method}:{path}"] = handler
    
    def get(self, path):
        def decorator(handler):
            self.add(path, "GET", handler)
            return handler
        return decorator
    
    def post(self, path):
        def decorator(handler):
            self.add(path, "POST", handler)
            return handler
        return decorator
    
    def resolve(self, path, method):
        return self.routes.get(f"{method}:{path}")


# ============================================================================
# API SERVER
# ============================================================================

class APIServer:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.router = Router()
    
    def start(self):
        return {"host": self.host, "port": self.port}
    
    async def handle(self, request):
        handler = self.router.resolve(request.path, request.method)
        if handler:
            return await handler(request)
        return Response(404, {"error": "Not found"})


# ============================================================================
# OPENAPI
# ============================================================================

class OpenAPIGenerator:
    def __init__(self):
        self.info = {"title": "Universe API", "version": "1.0.0"}
        
    def generate(self, routes):
        paths = {}
        for key, handler in routes.items():
            path = key.split(":")[1]
            paths[path] = {"get": {"operationId": handler.__name__}}
        return {"openapi": "3.0.0", "info": self.info, "paths": paths}


__all__ = ["Request", "Response", "Router", "APIServer", "OpenAPIGenerator"]
