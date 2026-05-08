"""
Universe IDE - Package Module

Package management.
"""

from typing import Any, Dict, List


# ============================================================================
# PACKAGE
# ============================================================================

class Package:
    """Package"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.dependencies = []
        
    def add_dependency(self, dep: str):
        self.dependencies.append(dep)


# ============================================================================
# PACKAGE MANAGER
# ============================================================================

class PackageManager:
    """Package manager"""
    
    def __init__(self):
        self.packages = {}
        
    def install(self, package: Package):
        self.packages[package.name] = package


__all__ = ["Package", "PackageManager"]