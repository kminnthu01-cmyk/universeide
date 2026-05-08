"""
Universe IDE - Language Server Protocol

LSP implementation for IDE features.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional


# ============================================================================
# LSP TYPES
# ============================================================================

class LSPMessageType(Enum):
    """LSP message types"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"


@dataclass
class TextDocument:
    """Text document"""
    uri: str
    language_id: str
    version: int
    content: str


@dataclass
class Position:
    """Text position"""
    line: int
    character: int


@dataclass
class Range:
    """Text range"""
    start: Position
    end: Position


@dataclass
class Location:
    """Location"""
    uri: str
    range: Range


@dataclass
class Diagnostic:
    """Diagnostic"""
    range: Range
    severity: int  # 1=error, 2=warning, 3=info
    message: str
    code: str = ""


@dataclass
class CompletionItem:
    """Completion item"""
    label: str
    kind: int = 1  # text
    detail: str = ""
    documentation: str = ""
    insert_text: str = ""
    filter_text: str = ""


# ============================================================================
# LSP METHODS
# ============================================================================

class LSPMethods:
    """LSP method constants"""
    # Initialize
    INITIALIZE = "initialize"
    INITIALIZED = "initialized"
    SHUTDOWN = "shutdown"
    EXIT = "exit"
    
    # Documents
    TEXT_DOCUMENT_DID_OPEN = "textDocument/didOpen"
    TEXT_DOCUMENT_DID_CHANGE = "textDocument/didChange"
    TEXT_DOCUMENT_DID_CLOSE = "textDocument/didClose"
    TEXT_DOCUMENT_DID_SAVE = "textDocument/didSave"
    
    # Diagnostics
    TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS = "textDocument/publishDiagnostics"
    
    # Completion
    TEXT_DOCUMENT_COMPLETION = "textDocument/completion"
    COMPLETION_ITEM_RESOLVE = "completionItem/resolve"
    
    # Definition
    TEXT_DOCUMENT_DEFINITION = "textDocument/definition"
    TEXT_DOCUMENT_TYPE_DEFINITION = "textDocument/typeDefinition"
    
    # References
    TEXT_DOCUMENT_REFERENCES = "textDocument/references"
    
    # Hover
    TEXT_DOCUMENT_HOVER = "textDocument/hover"
    
    # Formatting
    TEXT_DOCUMENT_FORMATTING = "textDocument/formatting"
    TEXT_DOCUMENT_RANGE_FORMATTING = "textDocument/rangeFormatting"
    
    # Rename
    TEXT_DOCUMENT_RENAME = "textDocument/rename"
    TEXT_DOCUMENT_PREPARE_RENAME = "textDocument/prepareRename"
    
    # Symbols
    TEXT_DOCUMENT_SYMBOL = "textDocument/documentSymbol"
    WORKSPACE_SYMBOL = "workspace/symbol"


# ============================================================================
# COMPLETION PROVIDER
# ============================================================================

class CompletionProvider:
    """Provide code completions"""
    
    # Python keywords
    KEYWORDS = [
        "def", "class", "if", "elif", "else", "for", "while", "try",
        "except", "finally", "with", "as", "import", "from", "return",
        "yield", "raise", "pass", "break", "continue", "and", "or", "not",
        "in", "is", "True", "False", "None", "async", "await",
    ]
    
    # Built-ins
    BUILTINS = [
        "print", "len", "range", "enumerate", "zip", "map", "filter",
        "sorted", "reversed", "sum", "min", "max", "abs", "open",
        "isinstance", "issubclass", "hasattr", "getattr", "setattr",
    ]
    
    # Universe IDE
    UNIVERSE = [
        "cosmos", "UniverseAI", "get_message_bus", "get_knowledge_base",
        "get_stream_manager", "get_task_queue", "get_ai_assistant",
        "get_code_reviewer", "get_intelligent_debugger",
    ]
    
    def provide(self, document: TextDocument, position: Position) -> List[CompletionItem]:
        """Provide completions"""
        items = []
        
        # Get current line
        lines = document.content.split("\n")
        if position.line < len(lines):
            line = lines[position.line]
            text_before = line[:position.character]
            
            # Add keywords matching prefix
            for kw in self.KEYWORDS:
                if kw.startswith(text_before) or text_before == "":
                    items.append(CompletionItem(
                        label=kw,
                        kind=14,  # keyword
                        detail="keyword",
                        insert_text=kw,
                    ))
                    
            # Add built-ins
            for bi in self.BUILTINS:
                if bi.startswith(text_before) or text_before == "":
                    items.append(CompletionItem(
                        label=bi,
                        kind=6,  # function
                        detail="builtin",
                        insert_text=bi,
                    ))
                    
            # Add universe
            for u in self.UNIVERSE:
                if u.startswith(text_before) or text_before == "":
                    items.append(CompletionItem(
                        label=u,
                        kind=6,
                        detail="universe",
                        insert_text=u,
                    ))
                    
        return items[:50]  # Limit results


# ============================================================================
# DEFINITION PROVIDER
# ============================================================================

class DefinitionProvider:
    """Provide goto definition"""
    
    # Simple definition map (in production, use AST)
    DEFINITIONS = {
        "cosmos": "universe_ide.py",
        "UniverseAI": "universe_ide.py",
        "cosmos": "universe_ide.py",
    }
    
    def find(self, document: TextDocument, position: Position) -> Optional[Location]:
        """Find definition location"""
        lines = document.content.split("\n")
        
        if position.line < len(lines):
            line = lines[position.line]
            
            # Extract identifier before cursor
            words = line[:position.character].split()[-1]
            
            if words in self.DEFINITIONS:
                return Location(
                    uri=self.DEFINITIONS[words],
                    range=Range(
                        start=Position(0, 0),
                        end=Position(0, 0),
                    ),
                )
                
        return None


# ============================================================================
# REFERENCES PROVIDER
# ============================================================================

class ReferencesProvider:
    """Find references"""
    
    def find(self, document: TextDocument, position: Position) -> List[Location]:
        """Find all references"""
        # Simple implementation
        lines = document.content.split("\n")
        references = []
        
        if position.line < len(lines):
            line = lines[position.line]
            words = line[:position.character].split()[-1]
            
            # Find all occurrences
            for i, l in enumerate(lines):
                if words in l:
                    pos = l.find(words)
                    references.append(Location(
                        uri=document.uri,
                        range=Range(
                            start=Position(i, pos),
                            end=Position(i, pos + len(words)),
                        ),
                    ))
                    
        return references


# ============================================================================
# HOVER PROVIDER
# ============================================================================

class HoverProvider:
    """Provide hover information"""
    
    DOCS = {
        "cosmos": "Create universe with N parallel AI agents.\n\nArgs: num_agents (int)\nReturns: UniverseAI",
        "print": "Print to stdout.\n\nArgs: *objects, sep, end, file",
        "len": "Return length.\n\nArgs: object\nReturns: int",
    }
    
    def provide(self, document: TextDocument, position: Position) -> dict:
        """Provide hover"""
        lines = document.content.split("\n")
        
        if position.line < len(lines):
            line = lines[position.line]
            words = line[:position.character].split()[-1]
            
            if words in self.DOCS:
                return {
                    "contents": self.DOCS[words],
                    "range": Range(
                        start=position,
                        end=position,
                    ),
                }
                
        return {"contents": ""}


# ============================================================================
# DIAGNOSTICS PROVIDER
# ============================================================================

class DiagnosticsProvider:
    """Provide diagnostics"""
    
    def diagnose(self, document: TextDocument) -> List[Diagnostic]:
        """Run diagnostics"""
        diagnostics = []
        lines = document.content.split("\n")
        
        for i, line in enumerate(lines):
            # Check for common issues
            if "    \t" in line:  # Mixed indentation
                start = Position(i, line.find("    \t"))
                end = Position(i, line.find("    \t") + 5)
                diagnostics.append(Diagnostic(
                    range=Range(start=start, end=end),
                    severity=3,
                    message="Mixed indentation",
                ))
                
            if "==" in line and " = " not in line:
                # Likely accidental comparison
                diagnostics.append(Diagnostic(
                    range=Range(
                        start=Position(i, 0),
                        end=Position(i, len(line)),
                    ),
                    severity=2,
                    message="Possible accidentalcomparison",
                ))
                
        return diagnostics


# ============================================================================
# LANGUAGE SERVER
# ============================================================================

class LanguageServer:
    """Language Server Protocol implementation"""
    
    def __init__(self):
        self.capabilities = {
            "completionProvider": {"triggerCharacters": ["."]},
            "definitionProvider": True,
            "referencesProvider": True,
            "hoverProvider": True,
            "diagnosticsProvider": True,
        }
        
        self.completion = CompletionProvider()
        self.definition = DefinitionProvider()
        self.references = ReferencesProvider()
        self.hover = HoverProvider()
        self.diagnostics = DiagnosticsProvider()
        
        self.documents: dict[str, TextDocument] = {}
        
    def initialize(self, params: dict) -> dict:
        """Initialize"""
        return {
            "capabilities": self.capabilities,
            "serverInfo": {
                "name": "Universe IDE Language Server",
                "version": "2.1",
            },
        }
        
    def shutdown(self) -> None:
        """Shutdown"""
        pass
        
    def text_document_completion(
        self, 
        text_document: dict, 
        position: dict
    ) -> List[CompletionItem]:
        """Provide completion"""
        doc = TextDocument(
            uri=text_document.get("uri", ""),
            language_id=text_document.get("languageId", "python"),
            version=text_document.get("version", 1),
            content=text_document.get("text", ""),
        )
        
        pos = Position(
            line=position.get("line", 0),
            character=position.get("character", 0),
        )
        
        return self.completion.provide(doc, pos)
        
    def text_document_definition(
        self, 
        text_document: dict, 
        position: dict
    ) -> Optional[Location]:
        """Provide definition"""
        doc = TextDocument(
            uri=text_document.get("uri", ""),
            language_id=text_document.get("languageId", "python"),
            version=text_document.get("version", 1),
            content=text_document.get("text", ""),
        )
        
        pos = Position(
            line=position.get("line", 0),
            character=position.get("character", 0),
        )
        
        return self.definition.find(doc, pos)
        
    def text_document_hover(
        self, 
        text_document: dict, 
        position: dict
    ) -> dict:
        """Provide hover"""
        doc = TextDocument(
            uri=text_document.get("uri", ""),
            language_id=text_document.get("languageId", "python"),
            version=text_document.get("version", 1),
            content=text_document.get("text", ""),
        )
        
        pos = Position(
            line=position.get("line", 0),
            character=position.get("character", 0),
        )
        
        return self.hover.provide(doc, pos)


# Global
_lsp = None

def get_language_server() -> LanguageServer:
    """Get language server"""
    global _lsp
    if _lsp is None:
        _lsp = LanguageServer()
    return _lsp


__all__ = [
    "LSPMessageType",
    "TextDocument",
    "Position",
    "Range",
    "Location",
    "Diagnostic",
    "CompletionItem",
    "LSPMethods",
    "CompletionProvider",
    "DefinitionProvider",
    "ReferencesProvider",
    "HoverProvider",
    "DiagnosticsProvider",
    "LanguageServer",
    "get_language_server",
]