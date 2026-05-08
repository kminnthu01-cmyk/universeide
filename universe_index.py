"""
Universe IDE - Index Module

Database indexing.
"""

from typing import Any, Dict, List


# ============================================================================
# INDEX
# ============================================================================

class Index:
    """Index"""
    
    def __init__(self, name: str, fields: List[str]):
        self.name = name
        self.fields = fields
        self.data = {}
        
    def add(self, key: str, value: Any):
        self.data[key] = value
        
    def get(self, key: str) -> Any:
        return self.data.get(key)


# ============================================================================
# INDEX MANAGER
# ============================================================================

class IndexManager:
    """Index manager"""
    
    def __init__(self):
        self.indexes = {}
        
    def create(self, name: str, fields: List[str]) -> Index:
        idx = Index(name, fields)
        self.indexes[name] = idx
        return idx


__all__ = ["Index", "IndexManager"]