"""
Universe IDE - Version Control

Git-like version control for projects.
"""

import os
import shutil
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# ============================================================================
# REPOSITORY
# ============================================================================

class Repository:
    """Version control repository"""
    
    def __init__(self, path: str):
        self.path = path
        self.commits = deque(maxlen=100)
        self.branches = ["main"]
        self.current_branch = "main"
        
    def init(self) -> bool:
        """Initialize repository"""
        # Create .universe directory
        meta_dir = os.path.join(self.path, ".universe")
        os.makedirs(meta_dir, exist_ok=True)
        
        return True
    
    def commit(self, message: str, files: List[str]) -> str:
        """Create commit"""
        commit_id = str(time.time())[:12]
        
        commit = {
            "id": commit_id,
            "message": message,
            "files": files,
            "branch": self.current_branch,
            "timestamp": time.time(),
        }
        
        self.commits.append(commit)
        return commit_id
    
    def log(self, count: int = 10) -> List[Dict]:
        """Get commit history"""
        return list(self.commits)[-count:]
    
    def branch(self, name: str) -> bool:
        """Create branch"""
        if name not in self.branches:
            self.branches.append(name)
            return True
        return False
    
    def checkout(self, name: str) -> bool:
        """Switch branch"""
        if name in self.branches:
            self.current_branch = name
            return True
        return False


# ============================================================================
# DIFF
# ============================================================================

class Diff:
    """Compare changes"""
    
    @staticmethod
    def compare(file1: str, file2: str) -> str:
        """Compare two files"""
        with open(file1) as f1, open(file2) as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            
        # Simple diff
        result = []
        for i, (l1, l2) in enumerate(zip(lines1, lines2)):
            if l1 != l2:
                result.append(f"Line {i}: {l1} -> {l2}")
                
        return "\n".join(result) if result else "No differences"


# ============================================================================
# SNAPSHOT
# ============================================================================

class Snapshot:
    """Project snapshots"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.snapshots = {}
        
    def create(self, name: str) -> str:
        """Create snapshot"""
        snapshot_path = os.path.join(self.base_path, ".snapshots", name)
        
        # Copy project
        shutil.copytree(self.base_path, snapshot_path)
        
        self.snapshots[name] = {
            "path": snapshot_path,
            "time": time.time(),
        }
        
        return name
    
    def restore(self, name: str) -> bool:
        """Restore snapshot"""
        if name in self.snapshots:
            snapshot = self.snapshots[name]
            shutil.copytree(snapshot["path"], self.base_path, dirs_exist_ok=True)
            return True
        return False
    
    def list_snapshots(self) -> List[str]:
        return list(self.snapshots.keys())


# Global
_repo = None

def get_repo(path: str = ".") -> Repository:
    global _repo
    if _repo is None:
        _repo = Repository(path)
    return _repo


__all__ = ["Repository", "Diff", "Snapshot", "get_repo"]