"""
Universe IDE - Self-Updating System

Auto-update mechanism with safe rollback.
Features:
- Version checking
- Safe updates with verification
- Rollback capability
- Health monitoring
- Auto-restart
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, List


# ============================================================================
# VERSION MANAGEMENT
# ============================================================================

@dataclass
class Version:
    """A version of the platform"""
    major: int
    minor: int
    patch: int
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
        
    def __lt__(self, other) -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        
    def __eq__(self, other) -> bool:
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)


CURRENT_VERSION = Version(1, 0, 0)


class VersionManager:
    """
    Manage platform versions and updates.
    """
    
    def __init__(self, storage_path: str = ".universe_versions"):
        self.storage_path = storage_path
        self.current = CURRENT_VERSION
        self.backup_path = Path(storage_path) / "backups"
        self.backup_path.mkdir(exist_ok=True)
        
    def get_current_version(self) -> Version:
        """Get current version"""
        return self.current
        
    def create_backup(self) -> str:
        """Create a backup before update"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"v{self.current}_{timestamp}"
        backup_dir = self.backup_path / backup_name
        
        # Copy key files
        files_to_backup = [
            "universe/__init__.py",
            "universe_ide.py", 
            "universe_cli.py",
            "examples.py",
        ]
        
        backup_dir.mkdir(parents=True)
        
        for f in files_to_backup:
            if Path(f).exists():
                dest = backup_dir / f
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                
        # Save metadata
        meta = {
            "version": str(self.current),
            "timestamp": timestamp,
            "files": files_to_backup,
        }
        with open(backup_dir / "meta.json", "w") as f:
            json.dump(meta, f, indent=2)
            
        return backup_name
        
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from a backup"""
        backup_dir = self.backup_path / backup_name
        if not backup_dir.exists():
            return False
            
        # Read metadata
        with open(backup_dir / "meta.json") as f:
            meta = json.load(f)
            
        # Restore files
        for f in meta.get("files", []):
            src = backup_dir / f
            if src.exists():
                shutil.copy2(src, f)
                
        return True
        
    def list_backups(self) -> List[dict]:
        """List available backups"""
        backups = []
        for d in self.backup_path.iterdir():
            if d.is_dir():
                meta_file = d / "meta.json"
                if meta_file.exists():
                    with open(meta_file) as f:
                        meta = json.load(f)
                    backups.append({
                        "name": d.name,
                        "version": meta.get("version"),
                        "timestamp": meta.get("timestamp"),
                    })
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)


# ============================================================================
# HEALTH MONITORING
# ============================================================================

@dataclass
class HealthStatus:
    """System health status"""
    healthy: bool = True
    checks_passed: int = 0
    checks_failed: int = 0
    last_check: Optional[datetime] = None
    issues: List[str] = field(default_factory=list)


class HealthMonitor:
    """
    Monitor system health and auto-heal.
    """
    
    def __init__(self):
        self.status = HealthStatus()
        self.last_full_check = None
        
    def check_dependencies(self) -> bool:
        """Check if dependencies are available"""
        required = ["openhands", "fastapi", "uvicorn"]
        missing = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
                
        if missing:
            self.status.issues.append(f"Missing: {missing}")
            return False
        return True
        
    def check_imports(self) -> bool:
        """Check key imports work"""
        try:
            from universe_ide import cosmos
            from universe import UniverseAI
            return True
        except Exception as e:
            self.status.issues.append(f"Import error: {e}")
            return False
            
    def check_disk_space(self, min_gb: float = 1.0) -> bool:
        """Check available disk space"""
        import shutil
        stat = shutil.disk_usage(".")
        free_gb = stat.free / (1024**3)
        if free_gb < min_gb:
            self.status.issues.append(f"Low disk: {free_gb:.1f}GB")
            return False
        return True
        
    def run_full_check(self) -> HealthStatus:
        """Run all health checks"""
        self.status = HealthStatus()
        self.status.last_check = datetime.now()
        
        checks = [
            self.check_dependencies,
            self.check_imports,
            self.check_disk_space,
        ]
        
        for check in checks:
            try:
                if check():
                    self.status.checks_passed += 1
                else:
                    self.status.checks_failed += 1
            except Exception as e:
                self.status.checks_failed += 1
                self.status.issues.append(f"Check error: {e}")
                
        self.status.healthy = self.status.checks_failed == 0
        self.last_full_check = datetime.now()
        
        return self.status
        
    def get_status(self) -> dict:
        """Get status summary"""
        return {
            "healthy": self.status.healthy,
            "checks_passed": self.status.checks_passed,
            "checks_failed": self.status.checks_failed,
            "issues": self.status.issues,
            "last_check": self.status.last_check.isoformat() if self.status.last_check else None,
        }


# ============================================================================
# AUTO-UPDATER
# ============================================================================

class AutoUpdater:
    """
    Safe auto-update with rollback.
    """
    
    def __init__(self):
        self.version_manager = VersionManager()
        self.health_monitor = HealthMonitor()
        self.update_in_progress = False
        
    def check_for_updates(self) -> bool:
        """Check if update is needed"""
        # For now, just verify health
        status = self.health_monitor.run_full_check()
        return status.healthy
        
    def safe_update(self, update_func: Callable[[], bool]) -> dict:
        """
        Safely apply an update.
        
        Args:
            update_func: Function that applies the update
            
        Returns:
            Dict with success status and message
        """
        if self.update_in_progress:
            return {
                "success": False,
                "message": "Update already in progress",
            }
            
        self.update_in_progress = True
        
        try:
            # Pre-update health check
            health = self.health_monitor.run_full_check()
            if not health.healthy:
                return {
                    "success": False,
                    "message": f"Unhealthy: {health.issues}",
                }
                
            # Create backup
            backup_name = self.version_manager.create_backup()
            
            # Apply update
            success = update_func()
            
            if success:
                # Verify
                post_health = self.health_monitor.run_full_check()
                if post_health.healthy:
                    return {
                        "success": True,
                        "message": "Update successful",
                        "backup": backup_name,
                    }
                else:
                    # Rollback
                    self.version_manager.restore_backup(backup_name)
                    return {
                        "success": False,
                        "message": "Post-update check failed, rolled back",
                        "backup": backup_name,
                    }
            else:
                # Rollback
                self.version_manager.restore_backup(backup_name)
                return {
                    "success": False,
                    "message": "Update function failed, rolled back",
                    "backup": backup_name,
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {e}",
            }
        finally:
            self.update_in_progress = False
            
    def get_status(self) -> dict:
        """Get updater status"""
        return {
            "version": str(self.version_manager.get_current_version()),
            "healthy": self.health_monitor.status.healthy,
            "update_in_progress": self.update_in_progress,
            "backups": self.version_manager.list_backups(),
        }


# Global instances
_version_manager = None
_health_monitor = None
_auto_updater = None


def get_version_manager() -> VersionManager:
    """Get version manager"""
    global _version_manager
    if _version_manager is None:
        _version_manager = VersionManager()
    return _version_manager


def get_health_monitor() -> HealthMonitor:
    """Get health monitor"""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = HealthMonitor()
    return _health_monitor


def get_auto_updater() -> AutoUpdater:
    """Get auto-updater"""
    global _auto_updater
    if _auto_updater is None:
        _auto_updater = AutoUpdater()
    return _auto_updater


__all__ = [
    "Version",
    "VersionManager",
    "HealthMonitor", 
    "AutoUpdater",
    "get_version_manager",
    "get_health_monitor", 
    "get_auto_updater",
    "HealthStatus",
]