"""
Universe IDE - Deploy Module

Deployment.
"""

from typing import Any, Dict


# ============================================================================
# DEPLOYMENT
# ============================================================================

class Deployment:
    """Deployment"""
    
    def __init__(self):
        self.environments = {}
        
    def deploy(self, env: str, config: Dict):
        self.environments[env] = config
        
    def get_status(self, env: str) -> Dict:
        return self.environments.get(env, {})


__all__ = ["Deployment"]