"""
Universe IDE - Lambda Module

Serverless functions.
"""

from typing import Any, Callable, Dict
import time


# ============================================================================
# LAMBDA FUNCTION
# ============================================================================

class LambdaFunction:
    """Lambda function"""
    
    def __init__(self, name: str, handler: Callable):
        self.name = name
        self.handler = handler
        self.invocations = 0
        
    def invoke(self, event: Dict) -> Any:
        self.invocations += 1
        return self.handler(event)


# ============================================================================
# LAMBDA RUNTIME
# ============================================================================

class LambdaRuntime:
    """Lambda runtime"""
    
    def __init__(self):
        self.functions = {}
        
    def register(self, name: str, handler: Callable):
        self.functions[name] = LambdaFunction(name, handler)
        
    def invoke(self, name: str, event: Dict) -> Any:
        if name in self.functions:
            return self.functions[name].invoke(event)
        return None


# Global
_runtime = None

def get_lambda_runtime() -> LambdaRuntime:
    global _runtime
    if _runtime is None:
        _runtime = LambdaRuntime()
    return _runtime


__all__ = ["LambdaFunction", "LambdaRuntime", "get_lambda_runtime"]