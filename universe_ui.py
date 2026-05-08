"""
Universe IDE - Modern UI Components

Beautiful, responsive UI components.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# THEME
# ============================================================================

class Theme:
    """Color themes"""
    
    DARK = {
        "background": "#1e1e1e",
        "surface": "#252526",
        "primary": "#007acc",
        "secondary": "#3c3c3c",
        "text": "#cccccc",
        "accent": "#0e639c",
        "success": "#4ec9b0",
        "warning": "#dcdcaa",
        "error": "#f14c4c",
    }
    
    LIGHT = {
        "background": "#ffffff",
        "surface": "#f3f3f3",
        "primary": "#0066b8",
        "secondary": "#e0e0e0",
        "text": "#333333",
        "accent": "#0078d4",
        "success": "#16825d",
        "warning": "#795e26",
        "error": "#d73a49",
    }
    
    UNIVERSE = {
        "background": "#0a0a1a",
        "surface": "#12122a",
        "primary": "#7c3aed",
        "secondary": "#1e1e3a",
        "text": "#e0e0ff",
        "accent": "#a78bfa",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
    }


# ============================================================================
# COMPONENT
# ============================================================================

@dataclass
class Component:
    """UI Component"""
    id: str
    type: str
    props: Dict = field(default_factory=dict)
    children: List = field(default_factory=list)


# ============================================================================
# BUTTON
# ============================================================================

class Button:
    """Button component"""
    
    VARIANTS = ["primary", "secondary", "ghost", "danger"]
    SIZES = ["sm", "md", "lg"]
    
    @staticmethod
    def render(
        label: str,
        variant: str = "primary",
        size: str = "md",
        onclick: Callable = None
    ) -> str:
        return f'<button class="btn btn-{variant} btn-{size}">{label}</button>'


# ============================================================================
# INPUT
# ============================================================================

class Input:
    """Input component"""
    
    TYPES = ["text", "password", "email", "number"]
    
    @staticmethod
    def render(
        placeholder: str = "",
        type: str = "text",
        value: str = ""
    ) -> str:
        return f'<input type="{type}" placeholder="{placeholder}" value="{value}"/>'


# ============================================================================
# CARD
# ============================================================================

class Card:
    """Card component"""
    
    @staticmethod
    def render(title: str, content: str) -> str:
        return f'''
<div class="card">
  <div class="card-header">{title}</div>
  <div class="card-body">{content}</div>
</div>'''


# ============================================================================
# MODAL
# ============================================================================

class Modal:
    """Modal dialog"""
    
    @staticmethod
    def render(title: str, content: str, footer: str = "") -> str:
        return f'''
<div class="modal">
  <div class="modal-content">
    <div class="modal-header">{title}</div>
    <div class="modal-body">{content}</div>
    <div class="modal-footer">{footer}</div>
  </div>
</div>'''


# ============================================================================
# TERMINAL UI
# ============================================================================

class TerminalUI:
    """Terminal emulator UI"""
    
    @staticmethod
    def render(commands: List[str] = None) -> str:
        lines = [
            '<div class="terminal">',
            '<div class="terminal-header">',
            '<span>Universe IDE</span>',
            '</div>',
            '<div class="terminal-body">',
        ]
        
        for cmd in (commands or ["Welcome to Universe IDE"]):
            lines.append(f'<div class="terminal-line">$ {cmd}</div>')
            
        lines.extend([
            '</div>',
            '</div>',
        ])
        
        return '\n'.join(lines)


# ============================================================================
# SIDEBAR
# ============================================================================

class Sidebar:
    """Sidebar component"""
    
    @staticmethod
    def render(items: List[Dict[str, str]]) -> str:
        lines = ['<div class="sidebar">']
        
        for item in items:
            icon = item.get("icon", "")
            label = item.get("label", "")
            lines.append(f'<div class="sidebar-item">{icon} {label}</div>')
            
        lines.append('</div>')
        return '\n'.join(lines)


# ============================================================================
# FILE TREE
# ============================================================================

class FileTree:
    """File tree component"""
    
    @staticmethod
    def render_tree(files: Dict, path: str = "") -> str:
        lines = ['<div class="file-tree">']
        
        for name, content in files.items():
            if isinstance(content, dict):
                lines.append(f'<div class="folder">{name}</div>')
                lines.append(FileTree.render_tree(content, name))
            else:
                icon = "📄" if "." in name else "📁"
                lines.append(f'<div class="file">{icon} {name}</div>')
                
        lines.append('</div>')
        return '\n'.join(lines)


# ============================================================================
# CODE EDITOR UI
# ============================================================================

class CodeEditorUI:
    """Code editor UI"""
    
    @staticmethod
    def render(
        code: str = "",
        language: str = "python",
        line_numbers: bool = True
    ) -> str:
        lines = [
            '<div class="code-editor" data-language="{}">'.format(language),
        ]
        
        if line_numbers:
            for i, line in enumerate(code.split('\n'), 1):
                lines.append(f'<div class="line"><span class="ln">{i}</span>{line}</div>')
        else:
            lines.append(code)
            
        lines.append('</div>')
        
        return '\n'.join(lines)


# ============================================================================
# TABS
# ============================================================================

class Tabs:
    """Tab component"""
    
    @staticmethod
    def render(tabs: List[Dict[str, str]], active: int = 0) -> str:
        lines = ['<div class="tabs">']
        
        for i, tab in enumerate(tabs):
            label = tab.get("label", "")
            active_class = "active" if i == active else ""
            lines.append(f'<div class="tab {active_class}">{label}</div>')
            
        lines.append('</div>')
        return '\n'.join(lines)


# ============================================================================
# NOTIFICATIONS
# ============================================================================

class Notification:
    """Notification component"""
    
    TYPES = ["info", "success", "warning", "error"]
    
    @staticmethod
    def render(message: str, type: str = "info") -> str:
        return f'<div class="notification notification-{type}">{message}</div>'


# ============================================================================
# STATUS BAR
# ============================================================================

class StatusBar:
    """Status bar"""
    
    @staticmethod
    def render(items: List[str]) -> str:
        lines = ['<div class="status-bar">']
        
        for item in items:
            lines.append(f'<span class="status-item">{item}</span>')
            
        lines.append('</div>')
        return '\n'.join(lines)


# ============================================================================
# CSS GENERATOR
# ============================================================================

class CSSGenerator:
    """Generate CSS"""
    
    @staticmethod
    def generate(theme: Dict = None) -> str:
        theme = theme or Theme.UNIVERSE
        
        return f'''
:root {{
  --bg: {theme["background"]};
  --surface: {theme["surface"]};
  --primary: {theme["primary"]};
  --text: {theme["text"]};
}}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}

.btn {{
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}}

.btn-primary {{
  background: var(--primary);
  color: white;
}}

.terminal {{
  background: #0a0a0a;
  color: #00ff00;
  font-family: 'Fira Code', monospace;
  padding: 16px;
  border-radius: 8px;
}}
'''


__all__ = [
    "Theme",
    "Button", 
    "Input",
    "Card",
    "Modal",
    "TerminalUI",
    "Sidebar",
    "FileTree",
    "CodeEditorUI",
    "Tabs",
    "Notification",
    "StatusBar",
    "CSSGenerator",
]