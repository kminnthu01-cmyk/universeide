"""
Universe IDE - Build Module

Build system.
"""

from typing import Any, Dict


# ============================================================================
# BUILD
# ============================================================================

class Build:
    """Build"""
    
    def __init__(self):
        self.artifacts = {}
        
    def build(self, target: str) -> str:
        self.artifacts[target] = f"artifact_{target}"
        return self.artifacts[target]
        
    def get_artifact(self, target: str) -> str:
        return self.artifacts.get(target)


__all__ = ["Build"]