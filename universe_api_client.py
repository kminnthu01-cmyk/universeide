"""
Universe IDE - API Client Module

REST API client.
"""

from typing import Any, Dict, Optional
import json


# ============================================================================
# CLIENT
# ============================================================================

class APIClient:
    """API client"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {}
        
    def set_header(self, key: str, value: str):
        self.headers[key] = value
        
    def get(self, endpoint: str) -> Dict:
        return {"url": f"{self.base_url}/{endpoint}"}
        
    def post(self, endpoint: str, data: Dict) -> Dict:
        return {"url": f"{self.base_url}/{endpoint}", "data": data}
        
    def put(self, endpoint: str, data: Dict) -> Dict:
        return {"url": f"{self.base_url}/{endpoint}", "data": data}
        
    def delete(self, endpoint: str) -> Dict:
        return {"url": f"{self.base_url}/{endpoint}"}


__all__ = ["APIClient"]