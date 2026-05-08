"""
Universe IDE - Extension System

Public API for extending Universe IDE.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# EXTENSION TYPES
# ============================================================================

class ExtensionPoint(Enum):
    """Extension points"""
    COMMAND = "command"
    COMPLETION = "completion"
    DIAGNOSTIC = "diagnostic"
    HOVER = "hover"
    DEFINITION = "definition"
    ACTION = "action"
    SIDEBAR = "sidebar"
    STATUSBAR = "statusbar"
    MENU = "menu"
    KEYMAP = "keymap"


@dataclass
class Extension:
    """Extension definition"""
    id: str
    name: str
    version: str
    description: str
    author: str
    extension_points: List[ExtensionPoint] = field(default_factory=list)
    contributes: dict = field(default_factory=dict)


# ============================================================================
# COMMANDS
# ============================================================================

class Commands:
    """Registered commands"""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        
    def register(self, id: str, handler: Callable, description: str = ""):
        """Register command"""
        self.commands[id] = handler
        
    def execute(self, id: str, *args, **kwargs) -> Any:
        """Execute command"""
        if id in self.commands:
            return self.commands[id](*args, **kwargs)
        raise ValueError(f"Unknown command: {id}")
        
    def list_commands(self) -> List[str]:
        """List commands"""
        return list(self.commands.keys())


# ============================================================================
# KEYMAP
# ============================================================================

@dataclass
class KeyBinding:
    """Key binding"""
    key: str
    command: str
    when: str = "editorTextFocus"


class Keymap:
    """Key mappings"""
    
    DEFAULT = [
        KeyBinding(key="Cmd+S", command="save"),
        KeyBinding(key="Cmd+P", command="quickOpen"),
        KeyBinding(key="Cmd+Shift+P", command="commandPalette"),
        KeyBinding(key="Cmd+B", command="toggleSidebar"),
        KeyBinding(key="Cmd+`", command="toggleTerminal"),
        KeyBinding(key="F5", command="run"),
        KeyBinding(key="F6", command="debug"),
    ]
    
    def __init__(self):
        self.custom: List[KeyBinding] = []
        
    def add_binding(self, binding: KeyBinding):
        """Add key binding"""
        self.custom.append(binding)
        
    def get_binding(self, key: str) -> Optional[str]:
        """Get command for key"""
        # Check custom first
        for b in self.custom:
            if b.key == key:
                return b.command
                
        # Check defaults
        for b in self.DEFAULT:
            if b.key == key:
                return b.command
                
        return None


# ============================================================================
# ACTIONS
# ============================================================================

class Actions:
    """Registered actions"""
    
    def __init__(self):
        self.actions: Dict[str, Callable] = {}
        
    def register(self, id: str, handler: Callable):
        """Register action"""
        self.actions[id] = handler
        
    def execute(self, id: str, context: dict = None):
        """Execute action"""
        if id in self.actions:
            self.actions[id](context or {})
            
    def get_actions(self) -> List[str]:
        """List actions"""
        return list(self.actions.keys())


# ============================================================================
# MENUS
# ============================================================================

@dataclass
class MenuItem:
    """Menu item"""
    id: str
    label: str
    command: str = ""
    submenu: List["MenuItem"] = field(default_factory=list)


class Menu:
    """Menu definitions"""
    
    MAIN_MENU = {
        "file": MenuItem(id="file", label="File", submenu=[
            MenuItem(id="newFile", label="New File", command="newFile"),
            MenuItem(id="openFile", label="Open File", command="openFile"),
            MenuItem(id="save", label="Save", command="save"),
        ]),
        "edit": MenuItem(id="edit", label="Edit", submenu=[
            MenuItem(id="undo", label="Undo", command="undo"),
            MenuItem(id="redo", label="Redo", command="redo"),
        ]),
        "view": MenuItem(id="view", label="View", submenu=[
            MenuItem(id="toggleSidebar", label="Toggle Sidebar", command="toggleSidebar"),
            MenuItem(id="toggleTerminal", label="Toggle Terminal", command="toggleTerminal"),
        ]),
        "run": MenuItem(id="run", label="Run", submenu=[
            MenuItem(id="runFile", label="Run File", command="run"),
            MenuItem(id="debugFile", label="Debug File", command="debug"),
        ]),
    }
    
    def get_menu(self, name: str) -> Optional[MenuItem]:
        """Get menu"""
        return self.MAIN_MENU.get(name)


# ============================================================================
# SIDEBAR
# ============================================================================

class SidebarPanel:
    """Sidebar panel"""
    
    def __init__(self, id: str, title: str, icon: str = ""):
        self.id = id
        self.title = title
        self.icon = icon
        self.content: Any = None


class SidebarManager:
    """Manage sidebar panels"""
    
    def __init__(self):
        self.panels: Dict[str, SidebarPanel] = {}
        self.active: Optional[str] = None
        
    def register(self, panel: SidebarPanel):
        """Register panel"""
        self.panels[panel.id] = panel
        
    def show(self, panel_id: str):
        """Show panel"""
        if panel_id in self.panels:
            self.active = panel_id
            
    def get_active(self) -> Optional[SidebarPanel]:
        """Get active panel"""
        if self.active:
            return self.panels.get(self.active)
        return None


# ============================================================================
# STATUS BAR
# ============================================================================

@dataclass
class StatusBarItem:
    """Status bar item"""
    id: str
    text: str
    alignment: str = "left"  # left or right
    command: str = ""


class StatusBarManager:
    """Manage status bar"""
    
    def __init__(self):
        self.items: List[StatusBarItem] = []
        
    def add_item(self, item: StatusBarItem):
        """Add item"""
        self.items.append(item)
        
    def update_item(self, id: str, text: str):
        """Update item text"""
        for item in self.items:
            if item.id == id:
                item.text = text
                break
                
    def get_items(self, alignment: str = None) -> List[StatusBarItem]:
        """Get items"""
        if alignment:
            return [i for i in self.items if i.alignment == alignment]
        return self.items


# ============================================================================
# EXTENSION HOST
# ============================================================================

class ExtensionHost:
    """Host for extensions"""
    
    def __init__(self):
        self.commands = Commands()
        self.keymap = Keymap()
        self.actions = Actions()
        self.menu = Menu()
        self.sidebar = SidebarManager()
        self.status_bar = StatusBarManager()
        self._context: dict = {}
        
    def register_command(self, id: str, handler: Callable, description: str = ""):
        """Register command"""
        self.commands.register(id, handler, description)
        
    def register_action(self, id: str, handler: Callable):
        """Register action"""
        self.actions.register(id, handler)
        
    def register_keybinding(self, key: str, command: str):
        """Register keybinding"""
        self.keymap.add_binding(KeyBinding(key=key, command=command))
        
    def register_panel(self, id: str, title: str, icon: str = "", content: Any = None):
        """Register sidebar panel"""
        panel = SidebarPanel(id, title, icon)
        panel.content = content
        self.sidebar.register(panel)
        
    def set_context(self, key: str, value: Any):
        """Set context"""
        self._context[key] = value
        
    def get_context(self, key: str) -> Any:
        """Get context"""
        return self._context.get(key)
        
    def execute_command(self, command_id: str, *args, **kwargs) -> Any:
        """Execute command"""
        return self.commands.execute(command_id, *args, **kwargs)


# Global
_ext_host = None

def get_extension_host() -> ExtensionHost:
    """Get extension host"""
    global _ext_host
    if _ext_host is None:
        _ext_host = ExtensionHost()
        # Register default commands
        _default_commands = [
            ("save", lambda: print("Saved!")),
            ("newFile", lambda: print("New file")),
            ("quickOpen", lambda: print("Quick open")),
            ("commandPalette", lambda: print("Palette")),
            ("toggleSidebar", lambda: print("Sidebar")),
            ("toggleTerminal", lambda: print("Terminal")),
            ("run", lambda: print("Run")),
            ("debug", lambda: print("Debug")),
        ]
        for cmd, handler in _default_commands:
            _ext_host.register_command(cmd, handler)
            
    return _ext_host


__all__ = [
    "ExtensionPoint",
    "Extension",
    "Commands",
    "KeyBinding",
    "Keymap",
    "Actions",
    "Menu",
    "MenuItem",
    "SidebarPanel",
    "SidebarManager",
    "StatusBarItem",
    "StatusBarManager",
    "ExtensionHost",
    "get_extension_host",
]