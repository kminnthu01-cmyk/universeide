"""
Universe IDE - AI Code Review

Intelligent code review system.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional


# ============================================================================
# REVIEW TYPES
# ============================================================================

class ReviewSeverity(Enum):
    """Issue severity"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"


class ReviewCategory(Enum):
    """Issue category"""
    BUG = "bug"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    BEST_PRACTICE = "best_practice"
    DOCUMENTATION = "documentation"


@dataclass
class ReviewIssue:
    """Code review issue"""
    line: int
    column: int
    severity: ReviewSeverity
    category: ReviewCategory
    message: str
    suggestion: str = ""
    code: str = ""


@dataclass
class ReviewResult:
    """Review result"""
    issues: List[ReviewIssue] = field(default_factory=list)
    score: int = 100
    summary: str = ""
    duration_ms: int = 0


# ============================================================================
# RULES
# ============================================================================

class ReviewRules:
    """Code review rules"""
    
    # Security patterns
    SECURITY = [
        (r"password\s*=\s*['\"][^'\"]+['\"]", "Hardcoded password", ReviewSeverity.ERROR, ReviewCategory.SECURITY),
        (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Hardcoded API key", ReviewSeverity.ERROR, ReviewCategory.SECURITY),
        (r"token\s*=\s*['\"][^'\"]+['\"]", "Hardcoded token", ReviewSeverity.ERROR, ReviewCategory.SECURITY),
        (r"os\.system\(", "os.system() is unsafe", ReviewSeverity.WARNING, ReviewCategory.SECURITY),
        (r"eval\(", "eval() is unsafe", ReviewSeverity.ERROR, ReviewCategory.SECURITY),
        (r"exec\(", "exec() is unsafe", ReviewSeverity.ERROR, ReviewCategory.SECURITY),
    ]
    
    # Performance patterns
    PERFORMANCE = [
        (r"for .* in range\(len\(", "Use enumerate() instead", ReviewSeverity.WARNING, ReviewCategory.PERFORMANCE),
        (r"\.append\(.+\)\n.*\.append\(.+)", "Use extend() instead", ReviewSeverity.INFO, ReviewCategory.PERFORMANCE),
        (r"\.keys\(\)", "Unnecessary .keys()", ReviewSeverity.INFO, ReviewCategory.PERFORMANCE),
    ]
    
    # Style patterns
    STYLE = [
        (r"[ \t]+$", "Trailing whitespace", ReviewSeverity.INFO, ReviewCategory.STYLE),
        (r"\t", "Use spaces instead of tabs", ReviewSeverity.INFO, ReviewCategory.STYLE),
        (r"print\(", "Use logging instead", ReviewSeverity.INFO, ReviewCategory.STYLE),
    ]
    
    # Best practices
    BEST_PRACTICE = [
        (r"except:\s*pass", "Bare except with pass", ReviewSeverity.WARNING, ReviewCategory.BEST_PRACTICE),
        (r"global ", "Avoid global variables", ReviewSeverity.INFO, ReviewCategory.BEST_PRACTICE),
        (r"raise NotImplementedError", "Implement method", ReviewSeverity.INFO, ReviewCategory.BEST_PRACTICE),
        (r"raise Exception\(", "Use specific exceptions", ReviewSeverity.INFO, ReviewCategory.BEST_PRACTICE),
    ]
    
    # Documentation
    DOCUMENTATION = [
        (r"def \w+\([^)]*\):\s*$", "Missing docstring", ReviewSeverity.INFO, ReviewCategory.DOCUMENTATION),
        (r"class \w+:\s*$", "Missing docstring", ReviewSeverity.INFO, ReviewCategory.DOCUMENTATION),
    ]
    
    # Bugs
    BUGS = [
        (r"if .+ == True:", "Use 'if x:' instead", ReviewSeverity.WARNING, ReviewCategory.BUG),
        (r"if .+ == False:", "Use 'if not x:' instead", ReviewSeverity.WARNING, ReviewCategory.BUG),
    ]


# ============================================================================
# LINTER
# ============================================================================

class CodeLinter:
    """Code linter with rules"""
    
    def __init__(self):
        self.rules = ReviewRules()
        
    def lint(self, code: str) -> ReviewResult:
        """Lint code"""
        import time
        start = time.perf_counter()
        
        issues = []
        lines = code.split("\n")
        
        # Check each rule category
        all_rules = [
            self.rules.SECURITY,
            self.rules.PERFORMANCE,
            self.rules.STYLE,
            self.rules.BEST_PRACTICE,
            self.rules.DOCUMENTATION,
            self.rules.BUGS,
        ]
        
        for line_num, line in enumerate(lines, 1):
            for rule_group in all_rules:
                for pattern, message, severity, category in rule_group:
                    if re.search(pattern, line):
                        issues.append(ReviewIssue(
                            line=line_num,
                            column=line.find(pattern) + 1 if pattern in line else 0,
                            severity=severity,
                            category=category,
                            message=message,
                            code=line.strip(),
                        ))
                        
        duration = int((time.perf_counter() - start) * 1000)
        
        # Calculate score
        score = 100
        for issue in issues:
            if issue.severity == ReviewSeverity.ERROR:
                score -= 10
            elif issue.severity == ReviewSeverity.WARNING:
                score -= 5
            else:
                score -= 1
                
        return ReviewResult(
            issues=issues,
            score=max(0, score),
            summary=f"Found {len(issues)} issues",
            duration_ms=duration,
        )


# ============================================================================
# AI CODE REVIEWER
# ============================================================================

class AICodeReviewer:
    """AI-powered code review"""
    
    def __init__(self):
        self.linter = CodeLinter()
        
    def review(self, code: str, language: str = "python") -> ReviewResult:
        """Review code"""
        # Run linter
        result = self.linter.lint(code)
        
        # Add AI-powered suggestions
        # Check for common patterns
        if "for i in range(len(" in code:
            result.issues.append(ReviewIssue(
                line=0,
                column=0,
                severity=ReviewSeverity.SUGGESTION,
                category=ReviewCategory.BEST_PRACTICE,
                message="Use enumerate() for indexed iteration",
                suggestion="for i, item in enumerate(collection):",
            ))
            
        if "try:" in code and "except:" in code:
            result.issues.append(ReviewIssue(
                line=0,
                column=0,
                severity=ReviewSeverity.INFO,
                category=ReviewCategory.BEST_PRACTICE,
                message="Specify exception type in except",
                suggestion="except SpecificException:",
            ))
            
        return result
        
    def suggest_improvements(self, code: str) -> List[str]:
        """Suggest improvements"""
        suggestions = []
        
        # Function without type hints
        if "def " in code and "->" not in code:
            suggestions.append("Add return type hints")
            
        # Missing type hints for parameters
        if re.search(r"def \w+\([^)]*\):", code):
            suggestions.append("Add parameter type hints")
            
        # No docstrings
        if '"""' not in code and "'''" not in code:
            suggestions.append("Add docstrings")
            
        return suggestions
        
    def security_scan(self, code: str) -> List[ReviewIssue]:
        """Security-focused scan"""
        issues = []
        
        # Sensitive data patterns
        patterns = [
            (r"password\s*=\s*['\"]", "hardcoded password"),
            (r"api[_-]?key\s*=\s*['\"]", "hardcoded API key"),
            (r"secret\s*=\s*['\"]", "hardcoded secret"),
            (r"token\s*=\s*['\"]", "hardcoded token"),
            (r"private[_-]?key\s*=\s*['\"]", "hardcoded private key"),
        ]
        
        for pattern, issue_type in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(ReviewIssue(
                    line=0,
                    column=0,
                    severity=ReviewSeverity.ERROR,
                    category=ReviewCategory.SECURITY,
                    message=f"Potential {issue_type}",
                    suggestion="Use environment variables",
                ))
                
        return issues
        
    def performance_check(self, code: str) -> List[ReviewIssue]:
        """Performance check"""
        issues = []
        
        # Inefficient patterns
        if "range(len(" in code:
            issues.append(ReviewIssue(
                line=0,
                column=0,
                severity=ReviewSeverity.WARNING,
                category=ReviewCategory.PERFORMANCE,
                message="Inefficient iteration",
                suggestion="Use enumerate() or direct iteration",
            ))
            
        return issues


# ============================================================================
# REVIEW REPORTER
# ============================================================================

class ReviewReporter:
    """Format review results"""
    
    @staticmethod
    def as_text(result: ReviewResult) -> str:
        """Format as text"""
        lines = [f"Code Review - Score: {result.score}/100"]
        lines.append("=" * 40)
        
        if not result.issues:
            lines.append("No issues found! ✅")
            return "\n".join(lines)
            
        # Group by severity
        errors = [i for i in result.issues if i.severity == ReviewSeverity.ERROR]
        warnings = [i for i in result.issues if i.severity == ReviewSeverity.WARNING]
        
        for issue in errors + warnings:
            prefix = "❌" if issue.severity == ReviewSeverity.ERROR else "⚠️ "
            lines.append(f"{prefix} {issue.message}")
            if issue.line > 0:
                lines.append(f"   Line {issue.line}")
            if issue.suggestion:
                lines.append(f"   💡 {issue.suggestion}")
                
        lines.append("")
        lines.append(f"Duration: {result.duration_ms}ms")
        
        return "\n".join(lines)
        
    @staticmethod
    def as_json(result: ReviewResult) -> dict:
        """Format as JSON"""
        return {
            "score": result.score,
            "issues": [
                {
                    "line": i.line,
                    "column": i.column,
                    "severity": i.severity.value,
                    "category": i.category.value,
                    "message": i.message,
                    "suggestion": i.suggestion,
                }
                for i in result.issues
            ],
            "summary": result.summary,
            "duration_ms": result.duration_ms,
        }
        
    @staticmethod
    def as_markdown(result: ReviewResult) -> str:
        """Format as markdown"""
        lines = [f"# Code Review - Score: {result.score}/100"]
        lines.append("")
        
        if result.issues:
            for issue in result.issues:
                severity = issue.severity.value.upper()
                lines.append(f"### {severity}: {issue.message}")
                lines.append(f"- Line: {issue.line or 'N/A'}")
                if issue.suggestion:
                    lines.append(f"- Suggestion: {issue.suggestion}")
                lines.append("")
        else:
            lines.append("No issues found! ✅")
            
        return "\n".join(lines)


# Global
_reviewer = None

def get_code_reviewer() -> AICodeReviewer:
    """Get code reviewer"""
    global _reviewer
    if _reviewer is None:
        _reviewer = AICodeReviewer()
    return _reviewer


__all__ = [
    "ReviewSeverity",
    "ReviewCategory",
    "ReviewIssue",
    "ReviewResult",
    "ReviewRules",
    "CodeLinter",
    "AICodeReviewer",
    "ReviewReporter",
    "get_code_reviewer",
]