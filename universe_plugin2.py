"""
Universe IDE - Advanced Plugin System

Extensible plugin architecture.
"""

import importlib
import os
import sys
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type


# ============================================================================
# PLUGIN
# ============================================================================

@dataclass
class Plugin:
    """Plugin definition"""
    id: str
    name: str
    version: str
    description: str
    hooks: List[str] = field(default_factory=list)
    handler: Optional[Callable] = None
    enabled: bool = True


# ============================================================================
# PLUGIN MANAGER
# ============================================================================

class PluginManager:
    """Manage plugins"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.hooks: Dict[str, List[str]] = {}
        
    def register(
        self,
        name: str,
        version: str,
        description: str,
        hooks: List[str],
        handler: Callable = None
    ) -> str:
        plugin_id = str(uuid.uuid4())[:12]
        
        plugin = Plugin(
            id=plugin_id,
            name=name,
            version=version,
            description=description,
            hooks=hooks,
            handler=handler,
        )
        
        self.plugins[plugin_id] = plugin
        
        # Register hooks
        for hook in hooks:
            if hook not in self.hooks:
                self.hooks[hook] = []
            self.hooks[hook].append(plugin_id)
            
        return plugin_id
        
    def enable(self, plugin_id: str) -> bool:
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = True
            return True
        return False
        
    def disable(self, plugin_id: str) -> bool:
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = False
            return True
        return False
        
    def get(self, plugin_id: str) -> Optional[Plugin]:
        return self.plugins.get(plugin_id)
        
    def list_enabled(self) -> List[Plugin]:
        return [p for p in self.plugins.values() if p.enabled]
        
    def call_hook(self, hook: str, *args, **kwargs) -> List[Any]:
        results = []
        
        if hook not in self.hooks:
            return results
            
        for plugin_id in self.hooks[hook]:
            plugin = self.plugins.get(plugin_id)
            if plugin and plugin.enabled and plugin.handler:
                try:
                    result = plugin.handler(*args, **kwargs)
                    results.append(result)
                except Exception:
                    pass
                    
        return results


# ============================================================================
# HOOKS
# ============================================================================

class Hooks:
    """Built-in hooks"""
    
    PRE_START = "pre_start"
    POST_START = "post_start"
    PRE_STOP = "pre_stop"
    POST_STOP = "post_stop"
    PRE_BUILD = "pre_build"
    POST_BUILD = "post_build"
    PRE_DEPLOY = "pre_deploy"
    POST_DEPLOY = "post_deploy"
    ON_ERROR = "on_error"


# ============================================================================
# LOADER
# ============================================================================

class PluginLoader:
    """Load plugins from files"""
    
    def __init__(self, manager: PluginManager):
        self.manager = manager
        
    def load_file(self, path: str) -> Optional[str]:
        try:
            # Load module
            spec = importlib.util.spec_from_file_location("plugin", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get plugin info
            name = getattr(module, "PLUGIN_NAME", "unknown")
            version = getattr(module, "PLUGIN_VERSION", "1.0.0")
            description = getattr(module, "PLUGIN_DESCRIPTION", "")
            hooks = getattr(module, "PLUGIN_HOOKS", [])
            handler = getattr(module, "plugin_main", None)
            
            return self.manager.register(
                name, version, description, hooks, handler
            )
            
        except Exception:
            return None
        
    def load_directory(self, directory: str) -> List[str]:
        loaded = []
        
        if not os.path.exists(directory):
            return loaded
            
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                path = os.path.join(directory, filename)
                plugin_id = self.load_file(path)
                if plugin_id:
                    loaded.append(plugin_id)
                    
        return loaded


# ============================================================================
# EXTENSION
# ============================================================================

class Extension:
    """Code extension"""
    
    @staticmethod
    def extend_class(
        target_class: Type,
        methods: Dict[str, Callable]
    ):
        """Extend a class with new methods"""
        for name, method in methods.items():
            setattr(target_class, name, method)
            
    @staticmethod
    def extend_function(
        target: Callable,
        wrapper: Callable
    ) -> Callable:
        """Wrap a function"""
        return wrapper


# Global
_plugin_manager = None

def get_plugin_manager() -> PluginManager:
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


__all__ = [
    "Plugin",
    "PluginManager",
    "Hooks",
    "PluginLoader",
    "Extension",
    "get_plugin_manager",
]