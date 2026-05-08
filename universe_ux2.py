"""
Universe IDE - UX Experience

Enhanced user experience features.
"""

import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# COMMAND PALETTE
# ============================================================================

class CommandPalette:
    """Quick command search"""
    
    def __init__(self):
        self.commands = []
        self.history = deque(maxlen=50)
        
    def register(self, command: str, action: Callable, shortcut: str = ""):
        self.commands.append({
            "id": str(uuid.uuid4())[:8],
            "command": command,
            "action": action,
            "shortcut": shortcut,
        })
        
    def search(self, query: str) -> List[Dict]:
        query = query.lower()
        return [c for c in self.commands if query in c["command"].lower()]
        
    def execute(self, command_id: str) -> Any:
        for cmd in self.commands:
            if cmd["id"] == command_id:
                return cmd["action"]()
        return None


# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

class KeyboardManager:
    """Manage keyboard shortcuts"""
    
    def __init__(self):
        self.shortcuts = {}
        
    def register(self, key: str, action: Callable):
        """Register shortcut"""
        self.shortcuts[key] = action
        
    def handle(self, key: str) -> bool:
        """Handle key press"""
        if key in self.shortcuts:
            self.shortcuts[key]()
            return True
        return False
    
    DEFAULT = {
        "ctrl+s": "save",
        "ctrl+o": "open", 
        "ctrl+n": "new",
        "ctrl+p": "command_palette",
        "ctrl+shift+p": "command_palette",
        "ctrl+b": "toggle_sidebar",
        "ctrl+j": "toggle_terminal",
        "ctrl+`": "toggle_terminal",
        "f1": "command_palette",
    }


# ============================================================================
# ANIMATIONS
# ============================================================================

class Animator:
    """UI Animations"""
    
    EFFECTS = {
        "fade": "opacity: 0 -> 1",
        "slide": "transform: translateX",
        "scale": "transform: scale",
        "bounce": "animation: bounce",
    }
    
    @staticmethod
    def css(effect: str, duration: float = 0.3) -> str:
        return f"animation: {effect} {duration}s ease"


# ============================================================================
# TOAST NOTIFICATIONS
# ============================================================================

class Toast:
    """Toast notifications"""
    
    def __init__(self):
        self.toasts = []
        
    def show(self, message: str, type: str = "info", duration: float = 3.0):
        toast = {
            "id": str(uuid.uuid4())[:8],
            "message": message,
            "type": type,
            "duration": duration,
            "timestamp": datetime.now(),
        }
        self.toasts.append(toast)
        return toast
        
    def dismiss(self, toast_id: str):
        self.toasts = [t for t in self.toasts if t["id"] != toast_id]
        
    def get_active(self) -> List[Dict]:
        return self.toasts


# ============================================================================
# CONTEXT MENU
# ============================================================================

class ContextMenu:
    """Right-click menu"""
    
    def __init__(self):
        self.items = []
        
    def add_item(self, label: str, action: Callable, shortcut: str = ""):
        self.items.append({
            "label": label,
            "action": action,
            "shortcut": shortcut,
        })
        
    def add_separator(self):
        self.items.append({"separator": True})
        
    def render(self) -> List[str]:
        lines = []
        for item in self.items:
            if "separator" in item:
                lines.append("<hr/>")
            else:
                shortcut = item.get("shortcut", "")
                label = item["label"]
                lines.append(f"{label} {shortcut}")
        return lines


# ============================================================================
# DRAG AND DROP
# ============================================================================

class DragDrop:
    """Drag and drop support"""
    
    def __init__(self):
        self.dragging = None
        self.drop_targets = []
        
    def start_drag(self, item: Any):
        self.dragging = item
        
    def add_target(self, target: str, handler: Callable):
        self.drop_targets.append({
            "target": target,
            "handler": handler,
        })
        
    def handle_drop(self, target: str) -> bool:
        for t in self.drop_targets:
            if t["target"] == target:
                t["handler"](self.dragging)
                return True
        return False


# ============================================================================
# AUTOCOMPLETE
# ============================================================================

class Autocomplete:
    """Code autocomplete"""
    
    COMPLETIONS = {
        "python": {
            "def ": "def function_name(params):\\n    pass",
            "class ": "class ClassName:\\n    def __init__(self):\\n        pass",
            "for ": "for item in items:\\n    pass",
            "if ": "if condition:\\n    pass",
        },
        "javascript": {
            "function ": "function name(params) {\\n  \\n}",
            "const ": "const name = value;",
            "class ": "class Name {\\n  constructor() {\\n    \\n  }\\n}",
        },
    }
    
    def __init__(self):
        self.custom = {}
        
    def get_completions(self, prefix: str, language: str = "python") -> List[str]:
        # Built-in
        completions = self.COMPLETIONS.get(language, {})
        
        # Custom
        completions.update(self.custom.get(language, {}))
        
        return [v for k, v in completions.items() if k.startswith(prefix)]


# ============================================================================
# MULTI-CURSOR
# ============================================================================

class MultiCursor:
    """Multiple cursors"""
    
    def __init__(self):
        self.cursors = []
        
    def add_cursor(self, line: int, column: int):
        self.cursors.append({"line": line, "column": column})
        
    def remove_cursor(self, index: int):
        if 0 <= index < len(self.cursors):
            self.cursors.pop(index)
            
    def get_cursors(self) -> List[Dict]:
        return self.cursors.copy()


# ============================================================================
# FOLDING
# ============================================================================

class CodeFolding:
    """Code folding"""
    
    def __init__(self):
        self.folds = {}
        
    def add_fold(self, start: int, end: int, label: str = ""):
        fold_id = str(uuid.uuid4())[:8]
        self.folds[fold_id] = {
            "start": start,
            "end": end,
            "label": label,
        }
        return fold_id
        
    def toggle(self, fold_id: str):
        if fold_id in self.folds:
            fold = self.folds[fold_id]
            fold["collapsed"] = not fold.get("collapsed", False)
            
    def is_collapsed(self, fold_id: str) -> bool:
        return self.folds.get(fold_id, {}).get("collapsed", False)


# ============================================================================
# MINIMAP
# ============================================================================

class Minimap:
    """Code minimap"""
    
    def __init__(self):
        self.code = ""
        self.markers = []
        
    def set_code(self, code: str):
        self.code = code
        
    def add_marker(self, line: int, color: str = "red"):
        self.markers.append({"line": line, "color": color})
        
    def get_preview(self) -> str:
        #缩略图预览
        lines = self.code.split('\n')
        return '\n'.join(lines[:10])


# ============================================================================
# SEARCH PANEL
# ============================================================================

class SearchPanel:
    """Search and replace"""
    
    def __init__(self):
        self.query = ""
        self.replace = ""
        self.options = {
            "case_sensitive": False,
            "whole_word": False,
            "regex": False,
            "replace_all": False,
        }
        
    def set_query(self, query: str):
        self.query = query
        
    def find_next(self, code: str, from_index: int = 0) -> Optional[int]:
        if self.options.get("case_sensitive"):
            return code.find(self.query, from_index)
        else:
            return code.lower().find(self.query.lower(), from_index)
            
    def replace_next(self, code: str) -> str:
        idx = self.find_next(code)
        if idx >= 0:
            return code[:idx] + self.replace + code[idx + len(self.query):]
        return code
        
    def replace_all(self, code: str) -> str:
        if self.options.get("replace_all"):
            return code.replace(self.query, self.replace)
        return code


# ============================================================================
# BRANCH VIEW
# ============================================================================

class BranchView:
    """Git branch view"""
    
    def __init__(self):
        self.branches = []
        self.current = "main"
        
    def set_branches(self, branches: List[str]):
        self.branches = branches
        
    def switch(self, branch: str):
        if branch in self.branches:
            self.current = branch
            return True
        return False
        
    def get_current(self) -> str:
        return self.current


# Global instances
_toast = None

def get_toast() -> Toast:
    global _toast
    if _toast is None:
        _toast = Toast()
    return _toast


__all__ = [
    "CommandPalette",
    "KeyboardManager",
    "Animator", 
    "Toast",
    "ContextMenu",
    "DragDrop",
    "Autocomplete",
    "MultiCursor",
    "CodeFolding",
    "Minimap",
    "SearchPanel",
    "BranchView",
    "get_toast",
]