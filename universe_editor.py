"""
Universe IDE - Smart Code Editor

In-browser code editor with syntax highlighting.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# SYNTAX HIGHLIGHTING
# ============================================================================

class SyntaxTheme(Enum):
    """Editor themes"""
    DARK = "dark"
    LIGHT = "light"
    MONOKAI = "monokai"
    DRACULA = "dracula"


# Token types for syntax highlighting
TOKEN_TYPES = {
    "keyword": ["def", "class", "if", "else", "for", "while", "return", "import", "from", "as", "try", "except", "with", "async", "await", "True", "False", "None"],
    "string": ["'", '"', '"""', "'''"],
    "number": ["0-9"],
    "comment": ["#"],
    "function": ["def ", "async def "],
    "class": ["class "],
    "operator": ["+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">="],
}


@dataclass
class Token:
    """Syntax token"""
    token_type: str
    value: str
    start: int
    end: int


class SyntaxHighlighter:
    """
    Syntax highlighting engine.
    """
    
    THEMES = {
        SyntaxTheme.DARK: {
            "keyword": "#ff79c6",
            "string": "#f1fa8c", 
            "number": "#bd93f9",
            "comment": "#6272a4",
            "function": "#50fa7b",
            "class": "#8be9fd",
            "operator": "#ff79c6",
            "background": "#282a36",
            "foreground": "#f8f8f2",
        },
        SyntaxTheme.MONOKAI: {
            "keyword": "#f92672",
            "string": "#e6db74",
            "number": "#ae81ff",
            "comment": "#75715e",
            "function": "#a6e22e",
            "class": "#66d9ef",
            "operator": "#f92672",
            "background": "#272822",
            "foreground": "#f8f8f0",
        },
    }
    
    def __init__(self, theme: SyntaxTheme = SyntaxTheme.DARK):
        self.theme = theme
        self.colors = self.THEMES.get(theme, self.THEMES[SyntaxTheme.DARK])
        
    def tokenize(self, code: str) -> list[Token]:
        """Tokenize code"""
        tokens = []
        
        # Python keywords
        keyword_pattern = r'\b(def|class|if|else|for|while|return|import|from|as|try|except|with|async|await|True|False|None|and|or|not|in|is|pass|break|continue|raise|yield|lambda|global|nonlocal|assert)\b'
        for match in re.finditer(keyword_pattern, code):
            tokens.append(Token("keyword", match.group(), match.start(), match.end()))
            
        # Strings
        string_pattern = r'(""".*?"""|\'\'\'.*?\'\'\')|"[^"]*"|\'[^\']*\''
        for match in re.finditer(string_pattern, code, re.DOTALL):
            tokens.append(Token("string", match.group(), match.start(), match.end()))
            
        # Comments
        comment_pattern = r'#[^\n]*'
        for match in re.finditer(comment_pattern, code):
            tokens.append(Token("comment", match.group(), match.start(), match.end()))
            
        # Numbers
        number_pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(number_pattern, code):
            tokens.append(Token("number", match.group(), match.start(), match.end()))
            
        return sorted(tokens, key=lambda t: t.start)
        
    def highlight(self, code: str) -> str:
        """Generate highlighted HTML"""
        tokens = self.tokenize(code)
        
        # Build highlighted code
        result = []
        last_end = 0
        
        # Sort all match positions
        all_tokens = []
        for t in tokens:
            all_tokens.append((t.start, "start", t))
            all_tokens.append((t.end, "end", t))
            
        all_tokens.sort(key=lambda x: x[0])
        
        # Simple line-by-line highlighting
        lines = code.split("\n")
        highlighted_lines = []
        
        for line in lines:
            # Check for keywords
            for kw in ["def ", "class ", "async "]:
                if kw in line:
                    highlighted_lines.append(f'<span style="color:{self.colors.get("function")}">{line}</span>')
                    break
            else:
                # Check for comments
                if "#" in line:
                    idx = line.index("#")
                    highlighted_lines.append(f'{line[:idx]}<span style="color:{self.colors.get("comment")}">{line[idx:]}</span>')
                else:
                    highlighted_lines.append(line)
                    
        return "\n".join(highlighted_lines)


# ============================================================================
# CODE EDITOR
# ============================================================================

class CodeEditor:
    """
    Full-featured code editor.
    """
    
    def __init__(
        self,
        language: str = "python",
        theme: SyntaxTheme = SyntaxTheme.DARK,
    ):
        self.language = language
        self.highlighter = SyntaxHighlighter(theme)
        self.code = ""
        self.cursor_position = 0
        self.selection_start = 0
        self.selection_end = 0
        self.undo_stack: list[str] = []
        self.redo_stack: list[str] = []
        
    def set_code(self, code: str):
        """Set code"""
        if self.code:
            self.undo_stack.append(self.code)
        self.code = code
        
    def get_code(self) -> str:
        """Get code"""
        return self.code
        
    def insert(self, text: str):
        """Insert text at cursor"""
        before = self.code[:self.cursor_position]
        after = self.code[self.cursor_position:]
        self.code = before + text + after
        self.cursor_position += len(text)
        
    def delete(self, count: int = 1):
        """Delete at cursor"""
        start = max(0, self.cursor_position - count)
        end = min(len(self.code), self.cursor_position + count)
        self.code = self.code[:start] + self.code[end:]
        
    def undo(self):
        """Undo last change"""
        if self.undo_stack:
            self.redo_stack.append(self.code)
            self.code = self.undo_stack.pop()
            
    def redo(self):
        """Redo last undone change"""
        if self.redo_stack:
            self.undo_stack.append(self.code)
            self.code = self.redo_stack.pop()
            
    def get_html(self) -> str:
        """Get highlighted HTML"""
        return self.highlighter.highlight(self.code)
        
    def get_tokens(self) -> list[Token]:
        """Get tokens"""
        return self.highlighter.tokenize(self.code)


# ============================================================================
# AUTO-COMPLETION
# ============================================================================

class AutoCompleter:
    """
    Intelligent auto-completion.
    """
    
    COMPLETIONS = {
        "python": {
            "def ": "def function_name(params):\n    pass",
            "class ": "class ClassName:\n    def __init__(self):\n        pass",
            "import ": "import module",
            "from ": "from module import",
            "async def ": "async def function_name(params):\n    pass",
            "if ": "if condition:\n    pass",
            "for ": "for item in iterable:\n    pass",
            "while ": "while condition:\n    pass",
            "try ": "try:\n    pass\nexcept Exception:\n    pass",
            "with ": "with open('file') as f:\n    pass",
            "@ ": "@decorator\ndef function():\n    pass",
        },
    }
    
    def __init__(self, language: str = "python"):
        self.language = language
        self.completions = self.COMPLETIONS.get(language, {})
        
    def get_completions(self, prefix: str) -> list[dict]:
        """Get completions for prefix"""
        results = []
        
        for key, value in self.completions.items():
            if key.startswith(prefix):
                results.append({
                    "label": key.strip(),
                    "insert": value,
                    "detail": "snippet",
                })
                
        return results[:10]


# Global
_editor = None

def get_editor(
    language: str = "python",
    theme: SyntaxTheme = SyntaxTheme.DARK,
) -> CodeEditor:
    """Get code editor"""
    global _editor
    if _editor is None:
        _editor = CodeEditor(language, theme)
    return _editor


__all__ = [
    "SyntaxTheme",
    "Token",
    "SyntaxHighlighter",
    "CodeEditor",
    "AutoCompleter",
    "get_editor",
]