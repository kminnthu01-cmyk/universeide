"""
Universe IDE - Health Module

Health checks.
"""

from typing import Any, Dict
import time


# ============================================================================
# HEALTH CHECK
# ============================================================================

class HealthCheck:
    """Health checker"""
    
    def __init__(self):
        self.components = {}
        
    def register(self, name: str, check: callable):
        self.components[name] = check
        
    def check_all(self) -> Dict:
        results = {}
        for name, check in self.components.items():
            try:
                results[name] = check()
            except:
                results[name] = False
        return results
        
    def is_healthy(self) -> bool:
        results = self.check_all()
        return all(results.values())


# Global
_health = None

def get_health() -> HealthCheck:
    global _health
    if _health is None:
        _health = HealthCheck()
    return _health


__all__ = ["HealthCheck", "get_health"]