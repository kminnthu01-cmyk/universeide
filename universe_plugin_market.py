"""
Universe IDE - Plugin Marketplace

Plugin discovery, installation, and management.
"""

import asyncio
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional


# ============================================================================
# PLUGIN TYPES
# ============================================================================

class PluginType(Enum):
    """Plugin type"""
    EDITOR = "editor"
    THEME = "theme"
    LANGUAGE = "language"
    INTEGRATION = "integration"
    AI = "ai"
    CUSTOM = "custom"


class PluginStatus(Enum):
    """Plugin status"""
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    UPDATE_AVAILABLE = "update_available"


@dataclass
class PluginManifest:
    """Plugin manifest"""
    id: str
    name: str
    version: str
    description: str
    author: str
    repository: str = ""
    type: PluginType = PluginType.CUSTOM
    dependencies: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    min_version: str = "1.0.0"
    python_version: str = ">=3.11"


@dataclass
class Plugin:
    """Plugin instance"""
    manifest: PluginManifest
    status: PluginStatus = PluginStatus.DISABLED
    installed_at: datetime = None
    enabled_at: datetime = None
    config: dict = field(default_factory=dict)


# ============================================================================
# PLUGIN REGISTRY
# ============================================================================

class PluginRegistry:
    """Central plugin registry"""
    
    def __init__(self):
        self.plugins: dict[str, Plugin] = {}
        
    def register(self, plugin: Plugin):
        """Register plugin"""
        self.plugins[plugin.manifest.id] = plugin
        
    def get(self, plugin_id: str) -> Optional[Plugin]:
        """Get plugin"""
        return self.plugins.get(plugin_id)
        
    def list(self, status: PluginStatus = None, plugin_type: PluginType = None) -> List[Plugin]:
        """List plugins with filters"""
        results = []
        
        for plugin in self.plugins.values():
            if status and plugin.status != status:
                continue
            if plugin_type and plugin.manifest.type != plugin_type:
                continue
            results.append(plugin)
            
        return results
        
    def search(self, query: str) -> List[Plugin]:
        """Search plugins"""
        query_lower = query.lower()
        results = []
        
        for plugin in self.plugins.values():
            manifest = plugin.manifest
            
            # Search name, description, keywords
            if (query_lower in manifest.name.lower() or
                query_lower in manifest.description.lower() or
                any(query_lower in kw.lower() for kw in manifest.keywords)):
                results.append(plugin)
                
        return results


# ============================================================================
# MARKETPLACE
# ============================================================================

class PluginMarketplace:
    """Official plugin marketplace"""
    
    # Curated plugins (mock data)
    FEATURED_PLUGINS = [
        {
            "id": "copilot",
            "name": "GitHub Copilot",
            "description": "AI pair programmer",
            "author": "GitHub",
            "type": "ai",
            "rating": 4.8,
            "downloads": 1000000,
        },
        {
            "id": "prettier", 
            "name": "Prettier",
            "description": "Code formatter",
            "author": "Prettier",
            "type": "editor",
            "rating": 4.9,
            "downloads": 5000000,
        },
        {
            "id": "eslint",
            "name": "ESLint",
            "description": "JavaScript linter",
            "author": "ESLint",
            "type": "editor",
            "rating": 4.7,
            "downloads": 3000000,
        },
        {
            "id": "gitlens",
            "name": "GitLens",
            "description": "Git supercharged",
            "author": "GitKraken",
            "type": "integration",
            "rating": 4.8,
            "downloads": 800000,
        },
        {
            "id": "docker",
            "name": "Docker",
            "description": "Docker support",
            "author": "Microsoft",
            "type": "integration",
            "rating": 4.6,
            "downloads": 600000,
        },
    ]
    
    def __init__(self):
        self.cache: dict = {}
        
    def get_featured(self) -> List[dict]:
        """Get featured plugins"""
        return self.FEATURED_PLUGINS
        
    def search(self, query: str) -> List[dict]:
        """Search marketplace"""
        query_lower = query.lower()
        
        results = []
        for plugin in self.FEATURED_PLUGINS:
            if (query_lower in plugin["name"].lower() or
                query_lower in plugin["description"].lower()):
                results.append(plugin)
                
        return results
        
    def get_details(self, plugin_id: str) -> Optional[dict]:
        """Get plugin details"""
        for plugin in self.FEATURED_PLUGINS:
            if plugin["id"] == plugin_id:
                return plugin
        return None


# ============================================================================
# PLUGIN MANAGER
# ============================================================================

class PluginManager:
    """Manage plugin lifecycle"""
    
    def __init__(self):
        self.registry = PluginRegistry()
        self.marketplace = PluginMarketplace()
        self.hooks: dict[str, List[Callable]] = {}
        
    def install(self, manifest: PluginManifest) -> bool:
        """Install plugin"""
        # Check dependencies
        for dep_id in manifest.dependencies:
            if not self.registry.get(dep_id):
                return False  # Missing dependency
                
        plugin = Plugin(
            manifest=manifest,
            status=PluginStatus.INSTALLED,
            installed_at=datetime.now(),
        )
        
        self.registry.register(plugin)
        return True
        
    def enable(self, plugin_id: str) -> bool:
        """Enable plugin"""
        plugin = self.registry.get(plugin_id)
        
        if not plugin:
            return False
            
        plugin.status = PluginStatus.ENABLED
        plugin.enabled_at = datetime.now()
        
        # Run enable hooks
        self._run_hooks(f"{plugin_id}_enabled")
        
        return True
        
    def disable(self, plugin_id: str) -> bool:
        """Disable plugin"""
        plugin = self.registry.get(plugin_id)
        
        if not plugin:
            return False
            
        plugin.status = PluginStatus.DISABLED
        
        return True
        
    def uninstall(self, plugin_id: str) -> bool:
        """Uninstall plugin"""
        plugin = self.registry.get(plugin_id)
        
        if not plugin:
            return False
            
        # Don't allow if other plugins depend on this
        for p in self.registry.plugins.values():
            if plugin_id in p.manifest.dependencies:
                return False  # Other plugins depend on this
                
        del self.registry.plugins[plugin_id]
        
        return True
        
    def register_hook(self, event: str, callback: Callable):
        """Register event hook"""
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
        
    def _run_hooks(self, event: str):
        """Run event hooks"""
        if event in self.hooks:
            for callback in self.hooks[event]:
                callback()


# ============================================================================
# EXTENSION LOADER
# ============================================================================

class ExtensionLoader:
    """Load plugin extensions"""
    
    def __init__(self):
        self.extensions: dict[str, Callable] = {}
        
    def register_extension(self, name: str, func: Callable):
        """Register extension function"""
        self.extensions[name] = func
        
    def call_extension(self, name: str, *args, **kwargs) -> Any:
        """Call extension"""
        if name in self.extensions:
            return self.extensions[name](*args, **kwargs)
        return None
        
    def list_extensions(self) -> List[str]:
        """List extensions"""
        return list(self.extensions.keys())


# ============================================================================
# PLUGIN API
# ============================================================================

class PluginAPI:
    """API for plugin developers"""
    
    def __init__(self, manager: PluginManager):
        self.manager = manager
        
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return default
        
    def set_config(self, key: str, value: Any):
        """Set config value"""
        pass
        
    def get_workspace_path(self) -> str:
        """Get workspace path"""
        return "."
        
    def create_command(self, name: str, handler: Callable):
        """Register command"""
        self.manager.register_hook(f"command_{name}", handler)
        
    def add_status_bar_item(self, item: dict):
        """Add status bar item"""
        pass  # Would add to UI


# Global
_pm = None

def get_plugin_manager() -> PluginManager:
    """Get plugin manager"""
    global _pm
    if _pm is None:
        _pm = PluginManager()
    return _pm


__all__ = [
    "PluginType",
    "PluginStatus",
    "PluginManifest",
    "Plugin",
    "PluginRegistry",
    "PluginMarketplace",
    "PluginManager",
    "ExtensionLoader",
    "PluginAPI",
    "get_plugin_manager",
]