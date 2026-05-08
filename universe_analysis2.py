"""
Universe IDE - Code Analysis

Static code analysis and linting.
"""

import ast
import re
from typing import Any, Dict, List


# ============================================================================
# LINTER
# ============================================================================

class Linter:
    """Code linter"""
    
    RULES = {
        "no_print": r"print\(",
        "no_tabs": r"\t",
        "no_any": r": Any",
        "snake_case": r"[A-Z]",
    }
    
    @classmethod
    def lint(cls, code: str) -> List[Dict]:
        issues = []
        
        for rule, pattern in cls.RULES.items():
            matches = re.finditer(pattern, code)
            for match in matches:
                issues.append({
                    "rule": rule,
                    "line": code[:match.start()].count("\\n") + 1,
                    "message": f"Found {rule}",
                })
                
        return issues
    
    @classmethod
    def fix(cls, code: str) -> str:
        """Auto-fix issues"""
        # Remove print statements
        code = re.sub(r'print\([^)]+\\)', '# print removed', code)
        # Replace tabs with spaces
        code = code.replace("\\t", "    ")
        return code


# ============================================================================
# ANALYZER
# ============================================================================

class Analyzer:
    """Analyze code quality"""
    
    @staticmethod
    def analyze(code: str) -> Dict:
        lines = code.split("\\n")
        
        return {
            "lines": len(lines),
            "chars": len(code),
            "functions": code.count("def "),
            "classes": code.count("class "),
            "imports": code.count("import "),
            "comments": code.count("#"),
        }
    
    @staticmethod
    def complexity(code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        keywords = ["if", "elif", "for", "while", "and", "or"]
        
        for keyword in keywords:
            complexity += code.count(keyword)
            
        return complexity
    
    @staticmethod
    def suggestions(code: str) -> List[str]:
        """Generate suggestions"""
        suggestions = []
        
        if "print(" in code:
            suggestions.append("Use logging instead of print()")
            
        if len(code) > 1000:
            suggestions.append("Consider splitting into modules")
            
        if Analyzer.complexity(code) > 10:
            suggestions.append("High complexity - consider refactoring")
            
        return suggestions


# ============================================================================
# METRICS
# ============================================================================

class CodeMetrics:
    """Code quality metrics"""
    
    @staticmethod
    def score(code: str) -> float:
        """Calculate quality score (0-100)"""
        score = 100.0
        
        # Deduct for issues
        score -= code.count("print(") * 5
        score -= Linter.lint(code).__len__() * 2
        
        # Deduct for complexity
        complexity = Analyzer.complexity(code)
        if complexity > 10:
            score -= (complexity - 10) * 2
            
        return max(0.0, score)
    
    @staticmethod
    def grade(score: float) -> str:
        """Convert score to grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


__all__ = ["Linter", "Analyzer", "CodeMetrics"]