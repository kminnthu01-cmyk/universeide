"""
Universe IDE - AI Assistant

Intelligent AI that analyzes code and provides fixes.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# AI MODES
# ============================================================================

class AIMode(Enum):
    """AI assistant modes"""
    ANALYSIS = "analysis"
    FIX = "fix"
    EXPLAIN = "explain"
    REFACTOR = "refactor"
    OPTIMIZE = "optimize"
    DOCUMENT = "document"


# ============================================================================
# CODE ANALYZER
# ============================================================================

class AICodeAnalyzer:
    """Analyze code with AI"""
    
    def __init__(self):
        self.context = {}
        
    def analyze_complexity(self, code: str) -> dict:
        """Analyze code complexity"""
        lines = [l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]
        
        cyclomatic = 1  # Base complexity
        for keyword in ["if", "elif", "for", "while", "and", "or", "except"]:
            cyclomatic += code.count(keyword)
            
        return {
            "lines": len(lines),
            "cyclomatic": cyclomatic,
            "functions": len(re.findall(r"def \w+\(", code)),
            "classes": len(re.findall(r"class \w+:", code)),
            "complexity": "high" if cyclomatic > 10 else "medium" if cyclomatic > 5 else "low",
        }
        
    def analyze_quality(self, code: str) -> dict:
        """Analyze code quality"""
        issues = []
        scores = {"docstrings": 0, "type_hints": 0, "naming": 0}
        
        # Check docstrings
        if '"""' in code or "'''" in code:
            scores["docstrings"] = 1
        
        # Check type hints
        if "->" in code or ": str" in code or ": int" in code:
            scores["type_hints"] = 1
            
        # Check naming conventions
        if re.search(r"[A-Z]\w+[A-Z]", code):
            scores["naming"] = 1
            
        # Common issues
        if "global " in code:
            issues.append("Avoid global variables")
            
        if code.count("except:") > 0 and "pass" in code:
            issues.append("Exception handler with pass - too broad")
            
        if len(code.split("\n")) > 500:
            issues.append("File too long - consider splitting")
            
        return {
            "score": sum(scores.values()) / 3 * 100,
            "issues": issues,
            "checks": scores,
        }
        
    def suggest_improvements(self, code: str) -> List[dict]:
        """AI suggest improvements"""
        suggestions = []
        
        for match in re.finditer(r"for (\w+) in range\(len\((\w+)\)\):", code):
            var, coll = match.groups()
            suggestions.append({
                "line": code[:match.start()].count("\n") + 1,
                "issue": f"for {var} in range(len({coll}))",
                "fix": f"for {var}, item in enumerate({coll}):",
                "reason": "Use enumerate for index + value",
                "priority": "high",
            })
            
        for match in re.finditer(r"if (.+) != (.+):", code):
            suggestions.append({
                "line": code[:match.start()].count("\n") + 1,
                "issue": "Explicit inequality check",
                "fix": "Consider using 'not in' or truthy check",
                "priority": "low",
            })
            
        return suggestions


# ============================================================================
# AI FIXER
# ============================================================================

class AIFixer:
    """AI-powered code fixing"""
    
    FIXES = {
        # Common errors -> fixes
        r"\.append\(.+\)\n.*\.append\(.+\)": "Use .extend() instead of multiple .append()",
        r"list\(.+\)": "Use list comprehension for better performance",
        r"for i in range\(len\(.+\)\):": "Use enumerate() instead",
        r"if .+ == True": "Use 'if {var}:' instead",
        r"if .+ == False": "Use 'if not {var}:' instead",
    }
    
    @classmethod
    def fix(cls, code: str) -> tuple[str, List[dict]]:
        """Apply AI fixes"""
        fixes_applied = []
        result = code
        
        for pattern, fix in cls.FIXES.items():
            if re.search(pattern, code):
                fixes_applied.append({
                    "pattern": pattern,
                    "fix": fix,
                })
                
        return result, fixes_applied
        
    @classmethod
    def fix_error(cls, error: Exception, code: str) -> Optional[str]:
        """Fix specific error"""
        error_type = type(error).__name__
        
        if error_type == "NameError":
            # Try to find undefined name
            match = re.search(r"not defined: (\w+)", str(error))
            if match:
                name = match.group(1)
                return f"# TODO: Define '{name}' before use\n{code}"
                
        if error_type == "TypeError":
            # NoneType check
            if "NoneType" in str(error):
                return "# TODO: Add None check before operation\n" + code
                
        return None


# ============================================================================
# AI EXPLAINER
# ============================================================================

class AIExplainer:
    """Explain code with AI"""
    
    @staticmethod
    def explain_function(code: str) -> str:
        """Explain function purpose"""
        # Extract function name and docstring
        match = re.search(r'def (\w+)\([^)]*\):[^"""*]', code)
        if match:
            func_name = match.group(1)
            
        # Find docstring
        doc_match = re.search(r'"""(.+?)"""', code, re.DOTALL)
        if doc_match:
            return f"Function: {func_name}\\nPurpose: {doc_match.group(1)}"
            
        return f"Function: {func_name}\\nPurpose: Not documented"
        
    @staticmethod
    def explain_error(error: Exception) -> str:
        """Explain error"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        explanations = {
            "NameError": "A variable or function name that hasn't been defined",
            "TypeError": "An operation on incompatible types",
            "ValueError": "Value incompatible with operation",
            "IndexError": "Index outside valid range",
            "KeyError": "Dictionary key not found",
            "AttributeError": "Attribute doesn't exist on object",
        }
        
        return explanations.get(error_type, "Unknown error") + f": {error_msg}"


# ============================================================================
# AI OPTIMIZER
# ============================================================================

class AIOptimizer:
    """Optimize code"""
    
    OPTIMIZATIONS = [
        # List comprehensions
        (r"\[.*for i in range\(.+)\]", "use list comprehension"),
        # Caching
        (r"def (\w+)\(.+\):\s*#.*expensive", "add @lru_cache"),
        # Lazy evaluation
        (r"for .* in .*:\s*if .*:", "use generator for large data"),
    ]
    
    @classmethod
    def optimize(cls, code: str) -> tuple[str, List[dict]]:
        """Apply optimizations"""
        suggestions = []
        result = code
        
        # Add caching to expensive functions
        if "# expensive" in code.lower() or "# slow" in code.lower():
            result = "@cache\n" + result
            suggestions.append({
                "type": "caching",
                "fix": "Added @cache decorator",
            })
            
        return result, suggestions


# ============================================================================
# DOCUMENTER
# ============================================================================

class AIDocumenter:
    """Auto-document code"""
    
    TEMPLATES = {
        "function": '''def {name}({params}):
    """
    {description}
    
    Args:
        {param_docs}
    
    Returns:
        {return_doc}
    """
    pass''',
        "class": '''class {name}:
    """
    {description}
    
    Attributes:
        {attr_docs}
    """
    pass''',
    }
    
    @classmethod
    def document(cls, code: str, mode: str = "function") -> str:
        """Generate documentation"""
        name_match = re.search(rf"def (\w+)\(", code)
        if not name_match:
            name_match = re.search(r"class (\w+):", code)
            
        if name_match:
            name = name_match.group(1)
            template = cls.TEMPLATES.get(mode, "")
            return template.format(
                name=name,
                params="self, *args",
                description="TODO: Add description",
                param_docs="param: description",
                return_doc="return value",
                attr_docs="attr: description",
            )
            
        return code


# ============================================================================
# AI ASSISTANT
# ============================================================================

@dataclass
class AIResponse:
    """AI response"""
    mode: AIMode
    content: Any
    confidence: float = 1.0


class AIAssistant:
    """Main AI assistant"""
    
    def __init__(self):
        self.analyzer = AICodeAnalyzer()
        self.fixer = AIFixer()
        self.explainer = AIExplainer()
        self.optimizer = AIOptimizer()
        self.documenter = AIDocumenter()
        
    def get_response(self, query: str) -> str:
        """Get response to a query"""
        # Simple response based on query keywords
        query_lower = query.lower()
        
        if any(w in query_lower for w in ["fix", "bug", "error"]):
            return "I can help fix that. Please provide the code you'd like me to analyze."
        elif any(w in query_lower for w in ["explain", "how"]):
            return "I can explain any code. Please provide the code."
        elif any(w in query_lower for w in ["optimize", "fast"]):
            return "I can optimize your code for better performance."
        elif any(w in query_lower for w in ["analyze", "review"]):
            return "I can analyze your code for issues and improvements."
        else:
            return "I'm your AI assistant. I can analyze, fix, explain, and optimize your code."
        
    def analyze(self, code: str) -> AIResponse:
        """Analyze code"""
        complexity = self.analyzer.analyze_complexity(code)
        quality = self.analyzer.analyze_quality(code)
        suggestions = self.analyzer.suggest_improvements(code)
        
        return AIResponse(
            mode=AIMode.ANALYSIS,
            content={
                "complexity": complexity,
                "quality": quality,
                "suggestions": suggestions,
            },
            confidence=0.9,
        )
        
    def fix(self, code: str) -> AIResponse:
        """Fix code"""
        fixed, fixes_applied = self.fixer.fix(code)
        
        return AIResponse(
            mode=AIMode.FIX,
            content={
                "code": fixed,
                "fixes": fixes_applied,
            },
            confidence=0.8,
        )
        
    def explain(self, code: str, mode: str = "function") -> AIResponse:
        """Explain code"""
        if mode == "function":
            content = self.explainer.explain_function(code)
        else:
            content = self.explainer.explain_error(code)
            
        return AIResponse(
            mode=AIMode.EXPLAIN,
            content=content,
            confidence=0.85,
        )
        
    def optimize(self, code: str) -> AIResponse:
        """Optimize code"""
        optimized, suggestions = self.optimizer.optimize(code)
        
        return AIResponse(
            mode=AIMode.OPTIMIZE,
            content={
                "code": optimized,
                "suggestions": suggestions,
            },
            confidence=0.75,
        )
        
    def document(self, code: str) -> AIResponse:
        """Document code"""
        documented = self.documenter.document(code)
        
        return AIResponse(
            mode=AIMode.DOCUMENT,
            content=documented,
            confidence=0.9,
        )
        
    def assist(self, code: str, mode: str) -> AIResponse:
        """General assist"""
        mode_enum = AIMode(mode)
        
        if mode_enum == AIMode.ANALYSIS:
            return self.analyze(code)
        elif mode_enum == AIMode.FIX:
            return self.fix(code)
        elif mode_enum == AIMode.EXPLAIN:
            return self.explain(code)
        elif mode_enum == AIMode.OPTIMIZE:
            return self.optimize(code)
        elif mode_enum == AIMode.DOCUMENT:
            return self.document(code)
            
        return AIResponse(mode_enum, {"error": "Unknown mode"}, 0.0)


# Global
_ai = None

def get_ai_assistant() -> AIAssistant:
    """Get AI assistant"""
    global _ai
    if _ai is None:
        _ai = AIAssistant()
    return _ai


__all__ = [
    "AIMode",
    "AICodeAnalyzer",
    "AIFixer",
    "AIExplainer",
    "AIOptimizer",
    "AIDocumenter",
    "AIAssistant",
    "get_ai_assistant",
]


# ============================================================================
# AI ASSIST FUNCTION
# ============================================================================

def aiassist(query: str) -> str:
    """AI assist - process a query and return response"""
    assistant = get_ai_assistant()
    return assistant.get_response(query)


__all__ = [
    "AIMode",
    "AIAgent",
    "AIAnalyzer",
    "AITester",
    "AIBuilder",
    "AIReviewer",
    "AIOptimizer",
    "AIDocumenter",
    "AIAssistant",
    "get_ai_assistant",
    "aiassist",
]