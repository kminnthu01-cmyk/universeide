"""
Universe IDE - Monitor Module

System monitoring.
"""

from typing import Any, Dict, List
import time


# ============================================================================
# MONITOR
# ============================================================================

class Monitor:
    """System monitor"""
    
    def __init__(self):
        self.metrics = {}
        self.alerts = []
        
    def record(self, metric: str, value: Any):
        if metric not in self.metrics:
            self.metrics[metric] = []
        self.metrics[metric].append({"value": value, "time": time.time()})
        
    def get(self, metric: str) -> List:
        return self.metrics.get(metric, [])


__all__ = ["Monitor"]