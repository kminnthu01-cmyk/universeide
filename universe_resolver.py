"""
Universe IDE - Resolver Module

Service discovery.
"""

from typing import Any, Dict


# ============================================================================
# RESOLVER
# ============================================================================

class Resolver:
    """Resolver"""
    
    def __init__(self):
        self.services = {}
        
    def register(self, name: str, address: str):
        self.services[name] = address
        
    def resolve(self, name: str) -> str:
        return self.services.get(name)


__all__ = ["Resolver"]