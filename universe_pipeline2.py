"""
Universe IDE - Pipeline Module

Data pipeline.
"""

from typing import Any, Callable, Dict, List


# ============================================================================
# PIPELINE
# ============================================================================

class Pipeline:
    """Data pipeline"""
    
    def __init__(self):
        self.stages = []
        
    def stage(self, handler: Callable):
        self.stages.append(handler)
        
    def execute(self, data: Any) -> Any:
        result = data
        for stage in self.stages:
            result = stage(result)
        return result


# Global
_pipeline = None

def get_pipeline() -> Pipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline()
    return _pipeline


__all__ = ["Pipeline", "get_pipeline"]