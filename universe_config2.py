"""
Universe IDE - Config Module

Configuration management.
"""

from typing import Any, Dict


# ============================================================================
# CONFIG
# ============================================================================

class Config:
    """Config"""
    
    def __init__(self):
        self.settings = {}
        
    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)
        
    def set(self, key: str, value: Any):
        self.settings[key] = value


# Global
_config = None

def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config


__all__ = ["Config", "get_config"]