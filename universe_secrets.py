"""
Universe IDE - Secret Manager Module

Secrets management.
"""

from typing import Any, Dict
import os


# ============================================================================
# SECRET
# ============================================================================

class Secret:
    """Secret"""
    
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.version = 1


# ============================================================================
# SECRET MANAGER
# ============================================================================

class SecretManager:
    """Secret manager"""
    
    def __init__(self):
        self.secrets = {}
        
    def store(self, key: str, value: str):
        self.secrets[key] = Secret(key, value)
        
    def get(self, key: str) -> str:
        if key in self.secrets:
            return self.secrets[key].value
        return os.environ.get(key, "")
        
    def delete(self, key: str) -> bool:
        if key in self.secrets:
            del self.secrets[key]
            return True
        return False


# Global
_manager = None

def get_secret_manager() -> SecretManager:
    global _manager
    if _manager is None:
        _manager = SecretManager()
    return _manager


__all__ = ["Secret", "SecretManager", "get_secret_manager"]