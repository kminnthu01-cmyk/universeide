"""
Universe IDE - Real-time Analytics

Real-time data processing.
"""

import time
from collections import deque
from dataclasses import dataclass


# ============================================================================
# REAL-TIME ENGINE
# ============================================================================

class RealTimeEngine:
    def __init__(self, window_size: int = 100):
        self.window = deque(maxlen=window_size)
        
    def add(self, data: dict):
        data["timestamp"] = time.time()
        self.window.append(data)
        
    def get_stats(self) -> dict:
        values = [d.get("value", 0) for d in self.window]
        if not values:
            return {"count": 0}
        return {
            "count": len(values),
            "avg": sum(values) / len(values),
            "rate": len(self.window) / (time.time() - self.window[0]["timestamp"]) if len(self.window) > 1 else 0,
        }


# ============================================================================
# STREAM PROCESSOR
# ============================================================================

class StreamProcessor:
    def __init__(self):
        self.engine = RealTimeEngine()
        self.handlers = []
        
    def on_data(self, handler):
        self.handlers.append(handler)
        
    def process(self, data: dict):
        self.engine.add(data)
        for handler in self.handlers:
            handler(data)


# ============================================================================
# DASHBOARD DATA
# ============================================================================

class DashboardData:
    def __init__(self):
        self.data = {}
        
    def update(self, key: str, value):
        if key not in self.data:
            self.data[key] = deque(maxlen=1000)
        self.data[key].append({"value": value, "timestamp": time.time()})
        
    def get(self, key: str) -> list:
        return list(self.data.get(key, []))


_rte = None

def get_realtime():
    global _rte
    if _rte is None:
        _rte = RealTimeEngine()
    return _rte


__all__ = ["RealTimeEngine", "StreamProcessor", "DashboardData", "get_realtime"]
