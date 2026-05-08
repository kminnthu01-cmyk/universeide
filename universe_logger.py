"""
Universe IDE - Logger Module

Logging.
"""

from typing import Any


# ============================================================================
# LOGGER
# ============================================================================

class Logger:
    """Logger"""
    
    def __init__(self, name: str = "universe"):
        self.name = name
        
    def info(self, message: str):
        print(f"[INFO] {message}")
        
    def error(self, message: str):
        print(f"[ERROR] {message}")
        
    def debug(self, message: str):
        print(f"[DEBUG] {message}")


__all__ = ["Logger"]