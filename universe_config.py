"""
Universe IDE - Configuration Management

Dynamic configuration system.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


# ============================================================================
# CONFIG STRUCTURE
# ============================================================================

@dataclass
class ConfigValue:
    """Configuration value"""
    value: Any
    type: str = "string"
    default: Any = None
    description: str = ""
    validated: bool = False


class Config:
    """
    Configuration manager.
    """
    
    DEFAULTS = {
        "universe.default_agents": 100,
        "universe.max_agents": 1000,
        "universe.default_model": "claude-sonnet-4-20250505",
        "universe.default_provider": "anthropic",
        
        "performance.cache_size": 1000,
        "performance.gc_threshold": 50000,
        "performance.parallel_workers": 8,
        
        "stability.max_errors": 100,
        "stability.health_check_interval": 60,
        "stability.checkpoint_limit": 10,
        
        "security.api_key_enabled": True,
        "security.rate_limit_requests": 100,
        "security.rate_limit_window": 60,
        
        "ux.theme": "cosmic",
        "ux.notifications_enabled": True,
        "ux.onboarding_completed": False,
        
        "logging.level": "INFO",
        "logging.file": "universe.log",
    }
    
    def __init__(self):
        self.values: dict[str, ConfigValue] = {}
        
        # Load defaults
        for key, value in self.DEFAULTS.items():
            self.values[key] = ConfigValue(
                value=value,
                type=type(value).__name__,
                default=value,
            )
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        if key in self.values:
            return self.values[key].value
        return default
        
    def set(self, key: str, value: Any):
        """Set config value"""
        if key in self.values:
            self.values[key].value = value
        else:
            self.values[key] = ConfigValue(value=value)
            
    def get_all(self) -> dict:
        """Get all config"""
        return {k: v.value for k, v in self.values.items()}
        
    def validate(self) -> dict:
        """Validate config"""
        results = {}
        
        for key, cv in self.values.items():
            results[key] = cv.validated
            
        return results


# ============================================================================
# ENVIRONMENT
# ============================================================================

class EnvConfig:
    """
    Environment-based configuration.
    """
    
    PREFIX = "UNIVERSE_"
    
    @classmethod
    def load(cls) -> dict:
        """Load from environment"""
        config = {}
        
        for key, value in os.environ.items():
            if key.startswith(cls.PREFIX):
                config_key = key[len(cls.PREFIX):].lower()
                config[config_key] = value
                
        return config
        
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get environment value"""
        env_key = cls.PREFIX + key.upper()
        return os.environ.get(env_key, default)


# ============================================================================
# CONFIG MANAGER
# ============================================================================

class ConfigManager:
    """
    Unified configuration.
    """
    
    def __init__(self):
        self.config = Config()
        self.env = EnvConfig()
        
    def load_env(self):
        """Load environment config"""
        env_config = self.env.load()
        
        for key, value in env_config.items():
            self.config.set(f"env.{key}", value)
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        # Check env first
        env_value = self.env.get(key)
        if env_value is not None:
            return env_value
            
        # Check config
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set config value"""
        self.config.set(key, value)


# Global
_config = None

def get_config() -> ConfigManager:
    """Get config manager"""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config


__all__ = [
    "ConfigValue",
    "Config",
    "EnvConfig",
    "ConfigManager",
    "get_config",
]