"""
Universe IDE - Log Aggregator Module

Centralized logging.
"""

from typing import Any, Dict, List
import time
from collections import deque


# ============================================================================
# LOG ENTRY
# ============================================================================

class LogEntry:
    """Log entry"""
    
    def __init__(self, level: str, message: str, source: str = "app"):
        self.level = level
        self.message = message
        self.source = source
        self.timestamp = time.time()


# ============================================================================
# LOG AGGREGATOR
# ============================================================================

class LogAggregator:
    """Log aggregator"""
    
    def __init__(self, max_logs: int = 1000):
        self.max_logs = max_logs
        self.logs = deque(maxlen=max_logs)
        
    def log(self, level: str, message: str, source: str = "app"):
        entry = LogEntry(level, message, source)
        self.logs.append(entry)
        return entry
        
    def search(self, query: str) -> List[LogEntry]:
        return [l for l in self.logs if query.lower() in l.message.lower()]
        
    def get_by_level(self, level: str) -> List[LogEntry]:
        return [l for l in self.logs if l.level == level]


# Global
_aggregator = None

def get_log_aggregator() -> LogAggregator:
    global _aggregator
    if _aggregator is None:
        _aggregator = LogAggregator()
    return _aggregator


__all__ = ["LogEntry", "LogAggregator", "get_log_aggregator"]