"""
Universe IDE - Metrics Module

System metrics collection.
"""

from typing import Any, Dict, List
import time
from collections import deque


# ============================================================================
# SYSTEM METRICS
# ============================================================================

class SystemMetrics:
    """System metrics"""
    
    def __init__(self):
        self.cpu = deque(maxlen=60)
        self.memory = deque(maxlen=60)
        self.requests = deque(maxlen=60)
        
    def record_cpu(self, value: float):
        self.cpu.append({"value": value, "time": time.time()})
        
    def record_memory(self, value: float):
        self.memory.append({"value": value, "time": time.time()})
        
    def record_request(self, latency: float):
        self.requests.append({"value": latency, "time": time.time()})
        
    def get_cpu(self) -> Dict:
        if not self.cpu:
            return {"avg": 0, "current": 0}
        values = [c["value"] for c in self.cpu]
        return {"avg": sum(values)/len(values), "current": values[-1]}
        
    def get_memory(self) -> Dict:
        if not self.memory:
            return {"avg": 0, "current": 0}
        values = [c["value"] for c in self.memory]
        return {"avg": sum(values)/len(values), "current": values[-1]}
        
    def get_requests(self) -> Dict:
        if not self.requests:
            return {"avg": 0, "count": 0}
        values = [c["value"] for c in self.requests]
        return {"avg": sum(values)/len(values), "count": len(values)}


# Global
_metrics = None

def get_metrics() -> SystemMetrics:
    global _metrics
    if _metrics is None:
        _metrics = SystemMetrics()
    return _metrics


__all__ = ["SystemMetrics", "get_metrics"]