"""
Universe IDE - Visual Code Analysis

Visual understanding of code and UI.
"""

import base64
import hashlib
import io
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ============================================================================
# UI ANALYZER
# ============================================================================

class UIAnalyzer:
    """Analyze UI elements"""
    
    COMPONENTS = {
        'button': ['<button', 'Button', 'QPushButton', 'tk.Button'],
        'input': ['<input>', 'Input', 'TextField', 'Entry'],
        'container': ['<div>', 'Container', 'Frame', 'Panel'],
        'list': ['<ul>', '<ol>', 'ListBox', 'ListView'],
        'table': ['<table>', 'Table', 'DataGrid'],
        'image': ['<img>', 'Image', 'Picture'],
        'link': ['<a>', 'Link', 'Hyperlink'],
    }
    
    def analyze(self, code: str) -> dict:
        """Analyze UI code"""
        components = []
        
        for comp_type, patterns in self.COMPONENTS.items():
            for pattern in patterns:
                if pattern in code:
                    components.append(comp_type)
                    break
        
        return {
            'components': components,
            'component_count': len(components),
            'type': self._detect_type(code),
        }
    
    def _detect_type(self, code: str) -> str:
        """Detect UI type"""
        code_lower = code.lower()
        
        if 'react' in code_lower or 'vue' in code_lower:
            return 'web_framework'
        elif 'tkinter' in code_lower or 'qt' in code_lower:
            return 'desktop'
        elif 'flutter' in code_lower or 'react-native' in code_lower:
            return 'mobile'
        elif 'html' in code_lower or 'css' in code_lower:
            return 'web_html'
            
        return 'unknown'


# ============================================================================
# CODE VISUALIZER
# ============================================================================

class CodeVisualizer:
    """Visualize code structure"""
    
    def visualize(self, code: str) -> dict:
        """Create visual representation"""
        lines = code.split('\n')
        
        # Map lines to visual elements
        visual = []
        
        for i, line in enumerate(lines):
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            
            # Determine type
            if content.startswith('#') or content.startswith('//'):
                vtype = 'comment'
            elif content.startswith('def '):
                vtype = 'function'
            elif content.startswith('class '):
                vtype = 'class'
            elif content.startswith('import '):
                vtype = 'import'
            elif content.startswith('if '):
                vtype = 'conditional'
            elif content.startswith('for '):
                vtype = 'loop'
            else:
                vtype = 'code'
            
            visual.append({
                'line': i + 1,
                'indent': indent,
                'type': vtype,
                'content': content[:50],
            })
        
        return {
            'lines': len(lines),
            'structure': visual,
            'depth': max(v['indent'] for v in visual) if visual else 0,
        }
    
    def render_ascii(self, code: str) -> str:
        """Render as ASCII art"""
        vis = self.visualize(code)
        
        lines = []
        for v in vis['structure'][:30]:  # First 30 lines
            prefix = '  ' * v['indent']
            
            symbols = {
                'comment': '#',
                'function': 'f',
                'class': 'C',
                'import': 'i',
                'conditional': '?',
                'loop': '~',
                'code': '.',
            }
            
            symbol = symbols.get(v['type'], '.')
            lines.append(f"{v['line']:3d} {prefix}{symbol} {v['content']}")
        
        return '\n'.join(lines)


# ============================================================================
# COLOR SCHEME
# ============================================================================

class ColorScheme:
    """Code colorization"""
    
    DEFAULT = {
        'keyword': '#569cd6',
        'string': '#ce9178',
        'comment': '#6a9955',
        'function': '#dcdcaa',
        'class': '#4ec9b0',
        'number': '#b5cea8',
        'operator': '#d4d4d4',
    }
    
    def colorize(self, code: str, theme: str = 'default') -> str:
        """Colorize code (generates HTML)"""
        colors = self.DEFAULT
        
        html = ['<pre style="background:#1e1e1e;color:#d4d4d4;font-family:monospace;">']
        
        lines = code.split('\n')
        
        for line in lines:
            # Simple highlighting
            colored = self._highlight_line(line, colors)
            html.append(colored)
        
        html.append('</pre>')
        
        return '\n'.join(html)
    
    def _highlight_line(self, line: str, colors: dict) -> str:
        """Highlight single line"""
        # Simple keyword highlighting
        keywords = ['def', 'class', 'if', 'else', 'for', 'return', 'import']
        
        for kw in keywords:
            if kw in line:
                line = line.replace(kw, f'<span style="color:{colors["keyword"]}">{kw}</span>')
        
        # Escape HTML
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        return f'<div>{line}</div>'


# ============================================================================
# LAYOUT ANALYZER
# ============================================================================

class LayoutAnalyzer:
    """Analyze code layout"""
    
    def analyze(self, code: str) -> dict:
        """Analyze layout"""
        lines = code.split('\n')
        
        # Indentation patterns
        indents = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
        
        return {
            'file_length': len(lines),
            'avg_indent': sum(indents) / max(1, len(indents)),
            'max_indent': max(indents) if indents else 0,
            'structure_score': self._score_structure(code),
        }
    
    def _score_structure(self, code: str) -> float:
        """Score code structure"""
        score = 0.5
        
        # Check for consistent indentation
        if '    ' in code:  # 4 spaces
            score += 0.1
            
        # Check for docstrings
        if '"""' in code or "'''" in code:
            score += 0.1
            
        # Check for type hints
        if '->' in code:
            score += 0.1
            
        # Check for comments
        if '#' in code or '//' in code:
            score += 0.1
            
        return min(1.0, score)


# Global
_visual = None

def get_visual_ai() -> LayoutAnalyzer:
    """Get visual AI"""
    global _visual
    if _visual is None:
        _visual = LayoutAnalyzer()
    return _visual


__all__ = [
    "UIAnalyzer",
    "CodeVisualizer",
    "ColorScheme", 
    "LayoutAnalyzer",
    "get_visual_ai",
]