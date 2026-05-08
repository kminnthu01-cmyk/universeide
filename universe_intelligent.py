"""
Universe IDE - Intelligent Features

AI-powered intelligent coding assistance.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================================
# SMART SUGGESTIONS
# ============================================================================

class SmartSuggestion:
    """AI-powered code suggestion"""
    
    def __init__(
        self,
        suggestion_type: str,
        code: str,
        confidence: float,
        explanation: str,
    ):
        self.type = suggestion_type
        self.code = code
        self.confidence = confidence
        self.explanation = explanation


# ============================================================================
# CODE INTELLIGENCE
# ============================================================================

class CodeIntelligence:
    """
    Intelligent code analysis and suggestions.
    """
    
    # Common patterns with improvements
    CODE_PATTERNS = {
        # Inefficient -> Efficient
        (r"for i in range\(len\(.+)\):", r"\1[i]"): 
            "Use enumerate() instead of range(len())",
        (r"\.append\(.+\)\n.*\.append\(.+\)", r"extend([\1, \2])"):
            "Use extend() for multiple appends",
        (r"if .+ in .+:.*\n.*return .+", r"return .+ if .+ else .+"):
            "Use ternary operator",
        (r"\.keys\(\)", r""):
            "Explicit iteration not needed in Python 3",
    }
    
    def __init__(self):
        self.context = {}
        
    def analyze(self, code: str) -> List[SmartSuggestion]:
        """Analyze code and suggest improvements"""
        suggestions = []
        
        # Check for common patterns
        for pattern, replacement in self.CODE_PATTERNS.items():
            if re.search(pattern[0], code):
                suggestions.append(SmartSuggestion(
                    suggestion_type="optimization",
                    code=replacement,
                    confidence=0.9,
                    explanation=self.CODE_PATTERNS[(pattern, replacement)],
                ))
                
        return suggestions
        
    def predict_imports(self, code: str) -> List[str]:
        """Predict needed imports"""
        imports = []
        
        # Simple prediction based on usage
        if "requests" in code or "urlopen" in code:
            imports.append("import requests")
            
        if "json" in code:
            imports.append("import json")
            
        if "re" in code:
            imports.append("import re")
            
        if "asyncio" in code:
            imports.append("import asyncio")
            
        return imports
        
    def suggest_tests(self, code: str) -> List[str]:
        """Suggest test cases"""
        tests = []
        
        # Find functions
        functions = re.findall(r"def (\w+)\((.*?)\):", code)
        
        for name, params in functions:
            tests.append(f"def test_{name}():")
            tests.append(f"    # TODO: test {name}({params})")
            tests.append(f"    pass")
            tests.append("")
            
        return tests


# ============================================================================
# SMART CODE SNIPPETS
# ============================================================================

class SmartSnippets:
    """
    Intelligent code snippets.
    """
    
    SNIPPETS = {
        "api": '''async def api_request(url: str, method: str = "GET") -> dict:
    """Make API request"""
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url) as response:
            return await response.json()''',
            
        "retry": '''async def retry_request(func, max_retries: int = 3, delay: float = 1.0):
    """Retry failed requests"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(delay * 2 ** attempt)''',
            
        "cache": '''from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(param):
    """Cached expensive function"""
    # expensive computation
    return result''',
            
        "debounce": '''import asyncio

async def debounce(wait_ms: int):
    """Debounce rapid calls"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(wait_ms / 1000)
            return await func(*args, **kwargs)
        return wrapper
    return decorator''',
            
        "rate_limit": '''import asyncio
from collections import deque
from time import time

class RateLimiter:
    """Rate limiter"""
    def __init__(self, max_calls: int, window_ms: int):
        self.max_calls = max_calls
        self.window = window_ms / 1000
        self.calls = deque()
        
    async def __aenter__(self):
        now = time()
        while len(self.calls) >= self.max_calls:
            if now - self.calls[0] < self.window:
                await asyncio.sleep(self.calls[0] + self.window - now)
            self.calls.popleft()
        self.calls.append(now)''',
    }
    
    def get(self, name: str) -> str:
        """Get snippet"""
        return self.SNIPPETS.get(name, "")
        
    def list_all(self) -> List[str]:
        """List all snippets"""
        return list(self.SNIPPETS.keys())


# ============================================================================
# REFACTORING ENGINE
# ============================================================================

class RefactoringEngine:
    """
    Automatic code refactoring.
    """
    
    def refactor(
        self, 
        code: str, 
        target: str
    ) -> Tuple[str, List[str]]:
        """Refactor code"""
        changes = []
        result = code
        
        if target == "dict-comprehension":
            # {k: v for k, v in items} -> original
            # Already optimal
            pass
            
        elif target == "namedtuple":
            # class -> namedtuple
            classes = re.findall(r"class (\w+):(.*?)", code, re.DOTALL)
            for name, body in classes:
                changes.append(f"Consider namedtuple for {name}")
                
        elif target == "dataclass":
            # class with __init__ -> @dataclass
            if "__init__" in code:
                changes.append("Use @dataclass decorator")
                
        return result, changes


# ============================================================================
# CODE METRICS
# ============================================================================

class CodeMetrics:
    """
    Calculate code quality metrics.
    """
    
    @staticmethod
    def cyclomatic_complexity(code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        
        # Count decision points
        decision_keywords = [
            "if", "elif", "for", "while", "and", "or", 
            "except", "case", "when"
        ]
        
        for keyword in decision_keywords:
            complexity += code.count(keyword)
            
        return complexity
        
    @staticmethod
    def halstead_metrics(code: str) -> dict:
        """Calculate Halstead metrics"""
        operators = len(re.findall(r"[+\-*/=<>!&|]+", code))
        operands = len(re.findall(r"\b\w+\b", code))

        n1 = operators  # unique operators
        n2 = operands  # unique operands

        if n1 > 0 and n2 > 0:
            volume = (n1 + n2) * (n1 + n2).bit_length()
            difficulty = n1 / 2 * (n2 / n1 if n1 > 0 else 0)
        else:
            volume = 0
            difficulty = 0

        return {
            "operators": operators,
            "operands": operands,
            "volume": volume,
            "difficulty": difficulty,
        }
        
    @staticmethod
    def maintainability_index(code: str) -> float:
        """Calculate maintainability index (0-100)"""
        lines = len(code.split("\n"))
        complexity = CodeMetrics.cyclomatic_complexity(code)
        
        # Simple MI calculation
        mi = 171 - 5.2 * (complexity / 10) - 0.23 * (lines / 100) * 100 / 171
        
        return max(0, min(100, mi))


# Global
_intelligence = None

def get_intelligence() -> CodeIntelligence:
    """Get code intelligence"""
    global _intelligence
    if _intelligence is None:
        _intelligence = CodeIntelligence()
    return _intelligence


__all__ = [
    "SmartSuggestion",
    "CodeIntelligence",
    "SmartSnippets",
    "RefactoringEngine",
    "CodeMetrics",
    "get_intelligence",
]