"""
Universe IDE - Feature Flag Module

Feature flags.
"""

from typing import Any, Callable, Dict


# ============================================================================
# FEATURE FLAG
# ============================================================================

class FeatureFlag:
    """Feature flag"""
    
    def __init__(self, name: str, enabled: bool = False):
        self.name = name
        self.enabled = enabled
        self.rules = {}
        
    def enable(self):
        self.enabled = True
        
    def disable(self):
        self.enabled = False
        
    def is_enabled(self) -> bool:
        return self.enabled


# ============================================================================
# Feature Store
# ============================================================================

class FeatureStore:
    """Feature store"""
    
    def __init__(self):
        self.flags = {}
        
    def create(self, name: str, enabled: bool = False) -> FeatureFlag:
        flag = FeatureFlag(name, enabled)
        self.flags[name] = flag
        return flag
        
    def get(self, name: str) -> FeatureFlag:
        return self.flags.get(name)
        
    def is_enabled(self, name: str) -> bool:
        flag = self.flags.get(name)
        return flag.enabled if flag else False


# Global
_store = None

def get_feature_store() -> FeatureStore:
    global _store
    if _store is None:
        _store = FeatureStore()
    return _store


__all__ = ["FeatureFlag", "FeatureStore", "get_feature_store"]