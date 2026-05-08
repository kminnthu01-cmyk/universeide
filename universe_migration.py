"""
Universe IDE - Migration Module

Database migrations.
"""

from typing import Any, Callable, Dict, List
import time


# ============================================================================
# MIGRATION
# ============================================================================

class Migration:
    """Database migration"""
    
    def __init__(self, version: str, up: Callable, down: Callable):
        self.version = version
        self.up = up
        self.down = down
        self.applied = False
        self.applied_at = None
        
    def apply(self):
        self.up()
        self.applied = True
        self.applied_at = time.time()
        
    def rollback(self):
        self.down()
        self.applied = False


# ============================================================================
# MIGRATION MANAGER
# ============================================================================

class MigrationManager:
    """Migration manager"""
    
    def __init__(self):
        self.migrations = []
        
    def add(self, migration: Migration):
        self.migrations.append(migration)
        
    def migrate(self):
        for m in self.migrations:
            if not m.applied:
                m.apply()


__all__ = ["Migration", "MigrationManager"]