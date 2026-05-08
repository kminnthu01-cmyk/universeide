"""
Universe IDE - Intelligent Debugger

AI-powered debugging with smart breakpoints and analysis.
"""

import asyncio
import re
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set


# ============================================================================
# DEBUG TYPES
# ============================================================================

class DebugEventType(Enum):
    """Debug event types"""
    BREAKPOINT = "breakpoint"
    WATCH = "watch"
    STEP = "step"
    EXCEPTION = "exception"
    ERROR = "error"


class DebugState(Enum):
    """Debug states"""
    STOPPED = "stopped"
    RUNNING = "running"
    STEPPING = "stepping"
    BREAKPOINT_HIT = "breakpoint_hit"


# ============================================================================
# INTELLIGENT BREAKPOINTS
# ============================================================================

@dataclass
class SmartBreakpoint:
    """AI-powered breakpoint"""
    id: str
    file: str
    line: int
    condition: str = ""
    hit_count: int = 0
    enabled: bool = True
    
    # Smart features
    auto_disable: bool = False
    trace_after: int = 0  # Disable after N hits
    log_message: str = ""


class BreakpointManager:
    """Intelligent breakpoint management"""
    
    def __init__(self):
        self.breakpoints: Dict[str, SmartBreakpoint] = {}
        self.hit_history: List[dict] = []
        
    def add(
        self, 
        file: str, 
        line: int, 
        condition: str = "",
        id: str = None,
    ) -> str:
        """Add breakpoint"""
        bp_id = id or f"bp_{len(self.breakpoints)}"
        self.breakpoints[bp_id] = SmartBreakpoint(
            id=bp_id,
            file=file,
            line=line,
            condition=condition,
        )
        return bp_id
        
    def should_break(self, bp_id: str, context: dict) -> bool:
        """Check if should break"""
        bp = self.breakpoints.get(bp_id)
        if not bp or not bp.enabled:
            return False
            
        # Update hit count
        bp.hit_count += 1
        
        # Check condition
        if bp.condition:
            try:
                result = eval(bp.condition, {}, context)
                if not result:
                    return False
            except:
                return False
                
        # Check auto-disable
        if bp.auto_disable and bp.hit_count >= bp.trace_after:
            bp.enabled = False
            
        return True
        
    def suggest_breakpoints(self, code: str) -> List[dict]:
        """AI suggest smart breakpoints"""
        suggestions = []
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            # Function definitions
            if re.match(r"^\s*def \w+\(", line):
                suggestions.append({
                    "line": i,
                    "reason": "function definition",
                    "confidence": 0.9,
                })
                
            # Loop with function calls
            if "for " in line and "(" in line:
                suggestions.append({
                    "line": i,
                    "reason": "loop with function call",
                    "confidence": 0.7,
                })
                
            # Exception handling
            if re.match(r"^\s*except", line):
                suggestions.append({
                    "line": i,
                    "reason": "exception handler",
                    "confidence": 0.8,
                })
                
        return suggestions


# ============================================================================
# VARIABLE WATCHER
# ============================================================================

@dataclass
class VariableWatch:
    """Variable watch point"""
    name: str
    expression: str
    old_value: Any = None
    changes: List[dict] = field(default_factory=list)


class VariableWatcher:
    """Watch variable changes"""
    
    def __init__(self):
        self.watches: Dict[str, VariableWatch] = {}
        self.scope: dict = {}
        
    def add_watch(self, name: str, expression: str = None):
        """Add watch"""
        expr = expression or name
        self.watches[name] = VariableWatch(
            name=name,
            expression=expr,
        )
        
    def evaluate_all(self):
        """Evaluate all watches"""
        for name, watch in self.watches.items():
            try:
                new_value = eval(watch.expression, {}, self.scope)
                
                if watch.old_value is not None and new_value != watch.old_value:
                    watch.changes.append({
                        "old": watch.old_value,
                        "new": new_value,
                        "time": datetime.now(),
                    })
                    
                watch.old_value = new_value
                
            except Exception as e:
                watch.changes.append({
                    "error": str(e),
                    "time": datetime.now(),
                })
                
    def get_changes(self, name: str) -> List[dict]:
        """Get changes for variable"""
        if name in self.watches:
            return self.watches[name].changes
        return []


# ============================================================================
# STACK ANALYSIS
# ============================================================================

class StackAnalyzer:
    """Analyze call stack"""
    
    @staticmethod
    def get_stack() -> List[dict]:
        """Get current stack"""
        stack = []
        
        for frame in traceback.extract_stack()[:-2]:
            stack.append({
                "file": frame.filename,
                "line": frame.lineno,
                "function": frame.name,
                "code": frame.line,
            })
            
        return stack
        
    @staticmethod
    def find_leaks(stack: List[dict]) -> List[dict]:
        """Find potential memory leaks"""
        leaks = []
        
        # Count function calls
        func_counts: Dict[str, int] = {}
        
        for frame in stack:
            func = frame.get("function", "")
            if func:
                func_counts[func] = func_counts.get(func, 0) + 1
                
        # Functions called too many times
        for func, count in func_counts.items():
            if count > 10:
                leaks.append({
                    "function": func,
                    "reason": f"called {count} times",
                    "severity": "high",
                })
                
        return leaks
        
    @staticmethod
    def suggest_fix(stack: List[dict], error: Exception) -> List[dict]:
        """AI suggest fixes based on stack"""
        suggestions = []
        
        error_type = type(error).__name__
        
        # Analyze stack for common issues
        for frame in stack:
            if "NoneType" in str(frame.get("code", "")):
                suggestions.append({
                    "fix": "Add null check",
                    "line": frame["line"],
                    "confidence": 0.8,
                })
                
            if ".get(" in str(frame.get("code", "")):
                suggestions.append({
                    "fix": "Check key exists before access",
                    "line": frame["line"],
                    "confidence": 0.7,
                })
                
        return suggestions


# ============================================================================
# EXCEPTION INTELLIGENCE
# ============================================================================

class ExceptionIntelligence:
    """Intelligent exception handling"""
    
    # Known patterns with fixes
    PATTERNS = {
        "NameError": [
            ("undefined variable", "Define the variable before use"),
            ("not defined", "Check spelling or import"),
        ],
        "TypeError": [
            ("'NoneType' object", "Check if variable can be None"),
            ("not subscriptable", "Variable type doesn't support indexing"),
            ("not callable", "Variable is not a function"),
        ],
        "AttributeError": [
            ("has no attribute", "Check if attribute exists"),
            ("module has no", "Import the attribute"),
        ],
        "IndexError": [
            ("list index out of range", "Check list length before access"),
            ("index negative", "Index must be non-negative"),
        ],
        "KeyError": [
            ("key", "Use .get() or check key exists"),
        ],
    }
    
    @classmethod
    def analyze(cls, exception: Exception) -> dict:
        """Analyze exception"""
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        suggestions = cls.PATTERNS.get(error_type, [])
        
        matching = []
        for pattern, fix in suggestions:
            if pattern.lower() in error_msg.lower():
                matching.append(fix)
                
        return {
            "type": error_type,
            "message": error_msg,
            "suggestions": matching,
            "stack": StackAnalyzer.get_stack(),
        }
        
    @classmethod
    def suggests_fix(cls, exception: Exception) -> List[str]:
        """Get fix suggestions"""
        analysis = cls.analyze(exception)
        return analysis.get("suggestions", [])


# ============================================================================
# CONDITIONAL DEBUGGING
# ============================================================================

class ConditionalDebugger:
    """Debug with AI conditions"""
    
    def __init__(self):
        self.bp_manager = BreakpointManager()
        self.var_watcher = VariableWatcher()
        
    def debug_function(
        self, 
        func: Callable, 
        *args,
        **kwargs
    ):
        """Debug function execution"""
        # Set up watches for all parameters
        for name, value in kwargs.items():
            self.var_watcher.add_watch(name, name)
            
        # Run with watch
        async def run():
            try:
                self.var_watcher.evaluate_all()
                result = func(*args, **kwargs)
                self.var_watcher.evaluate_all()
                return result
            except Exception as e:
                analysis = ExceptionIntelligence.analyze(e)
                print(f"Debug: {analysis}")
                raise
                
        return run()


# ============================================================================
# ERROR PREDICTION
# ============================================================================

class ErrorPredictor:
    """Predict potential errors"""
    
    @staticmethod
    def predict(code: str) -> List[dict]:
        """Predict errors in code"""
        predictions = []
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            # Missing exception handling
            if "open(" in line or "requests" in line or "fetch" in line:
                predictions.append({
                    "line": i,
                    "error": "IOError",
                    "reason": "No exception handling for I/O",
                    "fix": "Wrap in try/except",
                    "confidence": 0.7,
                })
                
            # Division without check
            if "/" in line and " / " in line:
                predictions.append({
                    "line": i,
                    "error": "ZeroDivisionError",
                    "reason": "Possible division by zero",
                    "fix": "Check divisor != 0",
                    "confidence": 0.5,
                })
                
            # Unclosed resources
            if "open(" in line:
                predictions.append({
                    "line": i,
                    "error": "ResourceWarning",
                    "reason": "File may not be closed",
                    "fix": "Use context manager (with)",
                    "confidence": 0.6,
                })
                
        return predictions


# ============================================================================
# DEBUG REPL
# ============================================================================

class DebugREPL:
    """Interactive debug REPL"""
    
    def __init__(self):
        self.locals: dict = {}
        self.globals: dict = {}
        self.history: List[str] = []
        
    def execute(self, command: str) -> Any:
        """Execute debug command"""
        self.history.append(command)
        
        # Special commands
        if command == "stack":
            return StackAnalyzer.get_stack()
            
        elif command == "locals":
            return self.locals
            
        elif command == "globals":
            return self.globals
            
        elif command.startswith("print "):
            expr = command[6:]
            return eval(expr, self.globals, self.locals)
            
        elif command.startswith("watch "):
            self.locals[command[6:]] = None
            return f"Watching: {command[6:]}"
            
        # Eval expression
        try:
            return eval(command, self.globals, self.locals)
        except:
            try:
                return exec(command, self.globals, self.locals)
            except Exception as e:
                return f"Error: {e}"


# Global
_debugger = None

def get_intelligent_debugger() -> ConditionalDebugger:
    """Get debugger"""
    global _debugger
    if _debugger is None:
        _debugger = ConditionalDebugger()
    return _debugger


__all__ = [
    "DebugEventType",
    "DebugState",
    "SmartBreakpoint",
    "BreakpointManager",
    "VariableWatch",
    "VariableWatcher",
    "StackAnalyzer",
    "ExceptionIntelligence",
    "ConditionalDebugger",
    "ErrorPredictor",
    "DebugREPL",
    "get_intelligent_debugger",
]