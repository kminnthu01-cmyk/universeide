"""
Universe IDE - Unified IDE Experience

Combines editor + terminal + AI into seamless experience.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# IDE STATE
# ============================================================================

class IDEState(Enum):
    """IDE states"""
    IDLE = "idle"
    EDITING = "editing"
    RUNNING = "running"
    DEBUGGING = "debugging"
    STREAMING = "streaming"


# ============================================================================
# PROJECT
# ============================================================================

@dataclass
class Project:
    """Code project"""
    name: str
    path: str
    files: Dict[str, str] = field(default_factory=dict)
    language: str = "python"
    created: datetime = field(default_factory=datetime.now)


# ============================================================================
# WORKSPACE
# ============================================================================

class Workspace:
    """
    Unified workspace managing editor, terminal, and AI.
    """
    
    def __init__(self):
        self.state = IDEState.IDLE
        self.current_project: Optional[Project] = None
        self.open_files: List[str] = []
        self.active_file: Optional[str] = None
        
        # Initialize components
        try:
            from universe_editor import CodeEditor, get_editor
            from universe_terminal import TerminalEmulator, get_terminal
            from universe_ide import cosmos
            
            self.editor = get_editor()
            self.terminal = get_terminal()
            self.universe = cosmos(10)
        except ImportError:
            self.editor = None
            self.terminal = None
            self.universe = None
            
    def create_project(self, name: str, path: str) -> Project:
        """Create new project"""
        project = Project(name=name, path=path)
        self.current_project = project
        self.state = IDEState.EDITING
        return project
        
    def add_file(self, filename: str, content: str = ""):
        """Add file to project"""
        if self.current_project:
            self.current_project.files[filename] = content
            self.open_files.append(filename)
            self.active_file = filename
            
    def open_file(self, filename: str):
        """Open file"""
        if filename in self.current_project.files:
            self.active_file = filename
            if self.editor:
                self.editor.set_code(self.current_project.files[filename])
                
    def save_file(self):
        """Save current file"""
        if self.active_file and self.current_project and self.editor:
            self.current_project.files[self.active_file] = self.editor.get_code()
            
    def run_file(self) -> dict:
        """Run current file"""
        if not self.terminal:
            return {"error": "Terminal not available"}
            
        self.state = IDEState.RUNNING
        self.terminal.start()
        
        # Send run command
        self.terminal.send_command(f"python {self.active_file}")
        
        return {"status": "running", "file": self.active_file}
        
    def debug_file(self) -> dict:
        """Debug current file"""
        self.state = IDEState.DEBUGGING
        return {"status": "debugging", "file": self.active_file}
        
    def get_status(self) -> dict:
        """Get workspace status"""
        return {
            "state": self.state.value,
            "project": self.current_project.name if self.current_project else None,
            "open_files": len(self.open_files),
            "active_file": self.active_file,
        }


# ============================================================================
# UNIFIED IDE
# ============================================================================

class UnifiedIDE:
    """
    The ultimate unified IDE experience.
    """
    
    def __init__(self):
        self.workspace = Workspace()
        self.projects: Dict[str, Project] = {}
        self.start_time = datetime.now()
        
    def new_project(self, name: str) -> Project:
        """Create new project"""
        project = self.workspace.create_project(name, f"./{name}")
        self.projects[name] = project
        return project
        
    def open_project(self, name: str) -> Optional[Project]:
        """Open existing project"""
        return self.projects.get(name)
        
    def list_projects(self) -> List[str]:
        """List all projects"""
        return list(self.projects.keys())
        
    def get_ai_assistance(self, prompt: str) -> str:
        """Get AI assistance"""
        if self.workspace.universe:
            task = self.workspace.universe.create_task(prompt)
            return f"AI: {task.description}"
        return "AI not available"
        
    def code_completion(self, prefix: str) -> List[str]:
        """Get code completions"""
        if self.workspace.editor:
            from universe_editor import AutoCompleter
            completer = AutoCompleter()
            return [c["insert"] for c in completer.get_completions(prefix)]
        return []
        
    def run_terminal(self, command: str) -> str:
        """Run terminal command"""
        if self.workspace.terminal:
            self.workspace.terminal.send_command(command)
            return self.workspace.terminal.read_output()
        return ""


# ============================================================================
# IDE COMMANDS
# ============================================================================

@dataclass
class IDECommand:
    """IDE command"""
    name: str
    handler: Callable
    shortcut: str = ""
    description: str = ""


class IDECommandRegistry:
    """Registry of IDE commands"""
    
    def __init__(self):
        self.commands: Dict[str, IDECommand] = {}
        
    def register(
        self, 
        name: str, 
        handler: Callable,
        shortcut: str = "",
        description: str = "",
    ):
        """Register command"""
        self.commands[name] = IDECommand(name, handler, shortcut, description)
        
    def get(self, name: str) -> Optional[IDECommand]:
        """Get command"""
        return self.commands.get(name)
        
    def list_all(self) -> List[IDECommand]:
        """List all commands"""
        return list(self.commands.values())


# ============================================================================
# KEYBINDINGS
# ============================================================================

KEYBINDINGS = {
    "Ctrl+S": "save_file",
    "Ctrl+O": "open_file", 
    "Ctrl+N": "new_file",
    "Ctrl+R": "run_file",
    "Ctrl+D": "debug_file",
    "Ctrl+P": "quick_open",
    "Ctrl+Shift+P": "command_palette",
    "Ctrl+B": "toggle_sidebar",
    "Ctrl+`": "toggle_terminal",
    "Ctrl+/": "toggle_comment",
    "F5": "run_debug",
    "F6": "run_without_debug",
    "F7": "format_code",
}


# Global
_ide = None

def get_unified_ide() -> UnifiedIDE:
    """Get unified IDE"""
    global _ide
    if _ide is None:
        _ide = UnifiedIDE()
    return _ide


__all__ = [
    "IDEState",
    "Project",
    "Workspace",
    "UnifiedIDE",
    "IDECommand",
    "IDECommandRegistry",
    "KEYBINDINGS",
    "get_unified_ide",
]