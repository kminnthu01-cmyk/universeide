"""
Universe IDE - Plugin System

Extensible plugin architecture for the platform.
"""

import importlib
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Optional


# ============================================================================
# PLUGIN INTERFACE
# ============================================================================

class Plugin(ABC):
    """Base plugin interface"""
    
    name: str = "base"
    version: str = "1.0.0"
    description: str = ""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin"""
        return True
        
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute plugin functionality"""
        pass
        
    @abstractmethod
    def shutdown(self):
        """Cleanup resources"""


# ============================================================================
# PLUGIN MANAGER
# ============================================================================

@dataclass
class PluginMetadata:
    """Plugin metadata"""
    name: str
    version: str
    description: str
    author: str = "unknown"
    enabled: bool = True
    loaded_at: Optional[datetime] = None


class PluginManager:
    """
    Manage plugins for Universe IDE.
    """
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: dict[str, Plugin] = {}
        self.metadata: dict[str, PluginMetadata] = {}
        
    def load_plugin(self, plugin_class: type, *args, **kwargs) -> bool:
        """Load a plugin"""
        try:
            plugin = plugin_class(*args, **kwargs)
            if plugin.initialize():
                self.plugins[plugin.name] = plugin
                self.metadata[plugin.name] = PluginMetadata(
                    name=plugin.name,
                    version=plugin.version,
                    description=plugin.description,
                    loaded_at=datetime.now(),
                )
                return True
        except Exception as e:
            print(f"Failed to load plugin: {e}")
        return False
        
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin"""
        if name in self.plugins:
            self.plugins[name].shutdown()
            del self.plugins[name]
            del self.metadata[name]
            return True
        return False
        
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name"""
        return self.plugins.get(name)
        
    def list_plugins(self) -> list[dict]:
        """List all plugins"""
        return [
            {"name": m.name, "version": m.version, "enabled": m.enabled}
            for m in self.metadata.values()
        ]


# ============================================================================
# BUILT-IN PLUGINS
# ============================================================================

class CodeReviewPlugin(Plugin):
    """AI-powered code review plugin"""
    
    name = "code_review"
    version = "1.0.0"
    description = "AI-powered code review"
    
    def initialize(self) -> bool:
        print(f"  Initializing {self.name} plugin...")
        return True
        
    def execute(self, code: str) -> dict:
        """Review code"""
        issues = []
        
        # Simple checks
        if "eval(" in code:
            issues.append({"severity": "high", "message": "Avoid eval()"})
        if "exec(" in code:
            issues.append({"severity": "high", "message": "Avoid exec()"})
        if "password" in code.lower() and "=" in code:
            issues.append({"severity": "medium", "message": "Hardcoded password"})
            
        return {"issues": issues, "score": max(0, 100 - len(issues) * 20)}
        
    def shutdown(self):
        print(f"  Shutting down {self.name} plugin")


class SecurityScanPlugin(Plugin):
    """Security scanning plugin"""
    
    name = "security_scan"
    version = "1.0.0"
    description = "Security vulnerability scanner"
    
    def initialize(self) -> bool:
        print(f"  Initializing {self.name} plugin...")
        return True
        
    def execute(self, code: str) -> dict:
        """Scan for vulnerabilities"""
        vulnerabilities = []
        
        checks = [
            (r"eval\s*\(", "Code injection", "critical"),
            (r"os\.system\s*\(", "Command injection", "high"),
            (r"pickle\.loads?\s*\(", "Unsafe deserialization", "high"),
            (r"hashlib\.md5\s*\(", "Weak crypto", "medium"),
            (r"R\.pop\s*\(\s*0\s*\)", "Inefficient list operation", "low"),
        ]
        
        import re
        for pattern, desc, severity in checks:
            if re.search(pattern, code):
                vulnerabilities.append({
                    "type": desc,
                    "severity": severity,
                    "pattern": pattern,
                })
                
        return {
            "vulnerabilities": vulnerabilities,
            "risk_score": sum(
                {"critical": 30, "high": 20, "medium": 10, "low": 5}.get(v["severity"], 0)
                for v in vulnerabilities
            )
        }
        
    def shutdown(self):
        print(f"  Shutting down {self.name} plugin")


class PerformanceProfilingPlugin(Plugin):
    """Performance profiling plugin"""
    
    name = "performance_profiler"
    version = "1.0.0"
    description = "Performance profiling"
    
    def initialize(self) -> bool:
        print(f"  Initializing {self.name} plugin...")
        return True
        
    def execute(self, code: str) -> dict:
        """Profile code performance"""
        issues = []
        
        # Simple checks
        if "for" in code and "range(len(" in code:
            issues.append({"type": "len in loop", "suggestion": "Use enumerate()"})
        if "+=" in code and "for" in code:
            issues.append({"type": "string concat in loop", "suggestion": "Use list join()"})
            
        return {"issues": issues, "recommendations": len(issues) == 0}
        
    def shutdown(self):
        print(f"  Shutting down {self.name} plugin")


class DocumentationPlugin(Plugin):
    """Auto-documentation plugin"""
    
    name = "documentation"
    version = "1.0.0"
    description = "Auto-generate documentation"
    
    def initialize(self) -> bool:
        print(f"  Initializing {self.name} plugin...")
        return True
        
    def execute(self, code: str) -> dict:
        """Generate docs"""
        import re
        
        functions = re.findall(r'def (\w+)\([^)]*\):', code)
        classes = re.findall(r'class (\w+)\(', code)
        
        return {
            "functions": functions,
            "classes": classes,
            "doc_coverage": len(functions) if functions else 0,
        }
        
    def shutdown(self):
        print(f"  Shutting down {self.name} plugin")


# ============================================================================
# PLUGIN REGISTRY
# ============================================================================

class PluginRegistry:
    """Registry of available plugins"""
    
    @staticmethod
    def get_available() -> dict:
        """Get all available plugins"""
        return {
            "code_review": CodeReviewPlugin,
            "security_scan": SecurityScanPlugin,
            "performance_profiler": PerformanceProfilingPlugin,
            "documentation": DocumentationPlugin,
        }


# GLOBAL
_plugin_manager = None

def get_plugin_manager() -> PluginManager:
    """Get global plugin manager"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


__all__ = [
    "Plugin",
    "PluginManager", 
    "PluginMetadata",
    "PluginRegistry",
    "CodeReviewPlugin",
    "SecurityScanPlugin", 
    "PerformanceProfilingPlugin",
    "DocumentationPlugin",
    "get_plugin_manager",
]