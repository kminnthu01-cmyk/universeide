"""
Universe IDE - Code Generation

AI-powered intelligent code generation.
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


# ============================================================================
# LANGUAGE SUPPORT
# ============================================================================

class Language(Enum):
    """Programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"
    Csharp = "c#"
    HTML = "html"
    CSS = "css"
    SQL = "sql"


# ============================================================================
# CODE TEMPLATES
# ============================================================================

CODE_TEMPLATES = {
    Language.PYTHON: {
        "flask": '''from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
''',
        "fastapi": '''from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
        "class": '''class {name}:
    def __init__(self):
        pass
        
    def method(self):
        pass
''',
    },
    Language.JAVASCRIPT: {
        "express": '''const express = require("express");
const app = express();

app.get("/", (req, res) => {{
    res.send("Hello");
}});

app.listen(3000, () => console.log("Server running"));
''',
        "react": '''import React from "react";

export default function App() {{
    return <div>Hello World!</div>;
}}
''',
    },
    Language.TYPESCRIPT: {
        "class": '''class {name} {{
    constructor() {{
        // init
    }}
    
    method(): void {{
        // code
    }}
}}
''',
    },
}


# ============================================================================
# CODE GENERATOR
# ============================================================================

class CodeGenerator:
    """
    Intelligent code generation.
    """
    
    def __init__(self):
        self.templates = CODE_TEMPLATES
        
    def generate(
        self, 
        language: Language, 
        template: str,
        variables: dict = None
    ) -> str:
        """Generate code from template"""
        variables = variables or {}
        
        # Get template
        lang_templates = self.templates.get(language, {})
        code = lang_templates.get(template, "")
        
        # Replace variables
        for key, value in variables.items():
            code = code.replace(f"{{{key}}}", value)
            
        return code
        
    def list_templates(self, language: Language) -> list[str]:
        """List available templates"""
        return list(self.templates.get(language, {}).keys())
        
    def generate_from_prompt(
        self, 
        prompt: str, 
        language: Language = Language.PYTHON
    ) -> str:
        """Generate code from natural language prompt"""
        # Simple prompt parsing
        prompt = prompt.lower()
        
        # Detect template
        if "class" in prompt and "python" in prompt:
            name = self._extract_name(prompt, "MyClass")
            return self.generate(Language.PYTHON, "class", {"name": name})
            
        if "flask" in prompt:
            return self.generate(Language.PYTHON, "flask")
            
        if "fastapi" in prompt:
            return self.generate(Language.PYTHON, "fastapi")
            
        # Default
        return "# Generated code\\n" + f"print('{prompt}')"
        
    def _extract_name(self, prompt: str, default: str) -> str:
        """Extract name from prompt"""
        words = prompt.split()
        for i, w in enumerate(words):
            if w == "name" or w == "called":
                if i + 1 < len(words):
                    return words[i + 1].strip(".,!?")
        return default


# ============================================================================
# CODE COMPLETION
# ============================================================================

class CodeCompletion:
    """
    Intelligent code completion.
    """
    
    def __init__(self):
        self.completions: dict = {}
        
    def add_completion(self, context: str, completion: str):
        """Add completion"""
        self.completions[context] = completion
        
    def complete(self, context: str, prefix: str) -> str:
        """Get completion"""
        # Simple prefix match
        for key, value in self.completions.items():
            if key.startswith(prefix):
                return value
                
        return ""


# ============================================================================
# CODE REFACTORING
# ============================================================================

class CodeRefactor:
    """
    Code refactoring suggestions.
    """
    
    @staticmethod
    def suggest_refactor(code: str) -> list[dict]:
        """Suggest refactorings"""
        suggestions = []
        
        # Check for long functions
        lines = code.split("\\n")
        if len(lines) > 100:
            suggestions.append({
                "type": "function_too_long",
                "message": "Function has >100 lines. Consider splitting.",
            })
            
        # Check for global variables
        if "global " in code:
            suggestions.append({
                "type": "global_variables",
                "message": "Avoid global variables. Use classes instead.",
            })
            
        return suggestions


# ============================================================================
# CODE ANALYSIS
# ============================================================================

class CodeAnalysis:
    """
    Static code analysis.
    """
    
    @staticmethod
    def analyze(code: str) -> dict:
        """Analyze code"""
        lines = code.split("\\n")
        
        return {
            "lines": len(lines),
            "blank_lines": sum(1 for l in lines if not l.strip()),
            "code_lines": sum(1 for l in lines if l.strip() and not l.strip().startswith("#")),
            "comments": sum(1 for l in lines if l.strip().startswith("#")),
            "functions": code.count("def "),
            "classes": code.count("class "),
        }


# Global
_generator = None

def get_code_generator() -> CodeGenerator:
    """Get code generator"""
    global _generator
    if _generator is None:
        _generator = CodeGenerator()
    return _generator


__all__ = [
    "Language",
    "CODE_TEMPLATES",
    "CodeGenerator",
    "CodeCompletion",
    "CodeRefactor",
    "CodeAnalysis",
    "get_code_generator",
]