"""
Universe IDE - Template System

Project templates and generators.
"""

import os
import shutil
from dataclasses import dataclass, field
from typing import Any, Optional


# ============================================================================
# TEMPLATE DEFINITION
# ============================================================================

@dataclass
class Template:
    """Project template"""
    name: str
    description: str
    files: dict[str, str] = field(default_factory=dict)
    config: dict = field(default_factory=dict)


# ============================================================================
# TEMPLATE REGISTRY
# ============================================================================

class TemplateRegistry:
    """Registry of project templates"""
    
    @staticmethod
    def get_all() -> dict[str, Template]:
        """Get all templates"""
        return {
            "webapp": Template(
                name="Web Application",
                description="Full-stack web application",
                files={
                    "app.py": '''from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
''',
                    "requirements.txt": "flask>=2.0",
                    "README.md": "# Web App\\n\\nFlask web application",
                },
            ),
            "api": Template(
                name="REST API",
                description="FastAPI REST API",
                files={
                    "main.py": '''from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
''',
                    "requirements.txt": "fastapi>=0.100",
                },
            ),
            "agent": Template(
                name="AI Agent",
                description="OpenHands AI Agent",
                files={
                    "agent.py": '''from universe_ide import cosmos
universe = cosmos(10)
print("Agent ready")
''',
                    "requirements.txt": "universe-ide",
                },
            ),
            "cli": Template(
                name="CLI Tool",
                description="Command-line tool",
                files={
                    "main.py": '''#!/usr/bin/env python3
import click

@click.command()
def main():
    print("Hello!")

if __name__ == "__main__":
    main()
''',
                    "requirements.txt": "click>=8.0",
                },
            ),
            "data": Template(
                name="Data Pipeline",
                description="Data processing pipeline",
                files={
                    "pipeline.py": '''import pandas as pd

def process():
    df = pd.DataFrame()
    return df

if __name__ == "__main__":
    process()
''',
                    "requirements.txt": "pandas>=2.0",
                },
            ),
            "ml": Template(
                name="ML Project",
                description="Machine learning project",
                files={
                    "train.py": '''import numpy as np
print("ML ready")
''',
                    "requirements.txt": "numpy>=1.24",
                },
            ),
        }
        
    @staticmethod
    def get(name: str) -> Optional[Template]:
        """Get template by name"""
        return TemplateRegistry.get_all().get(name)


# ============================================================================
# PROJECT GENERATOR
# ============================================================================

class ProjectGenerator:
    """
    Generate projects from templates.
    """
    
    def __init__(self):
        self.registry = TemplateRegistry()
        
    def generate(
        self, 
        template_name: str, 
        output_dir: str,
        variables: dict = None
    ) -> bool:
        """Generate project"""
        template = self.registry.get(template_name)
        
        if not template:
            return False
            
        variables = variables or {}
        
        # Create directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate files
        for filename, content in template.files.items():
            # Apply variables
            for key, value in variables.items():
                content = content.replace(f"{{{key}}}", str(value))
                
            filepath = os.path.join(output_dir, filename)
            
            # Create file
            with open(filepath, "w") as f:
                f.write(content)
                
        return True
        
    def list_templates(self) -> list[dict]:
        """List available templates"""
        templates = self.registry.get_all()
        
        return [
            {
                "name": t.name,
                "description": t.description,
            }
            for t in templates.values()
        ]


# Global
_generator = None

def get_generator() -> ProjectGenerator:
    """Get project generator"""
    global _generator
    if _generator is None:
        _generator = ProjectGenerator()
    return _generator


__all__ = [
    "Template",
    "TemplateRegistry",
    "ProjectGenerator",
    "get_generator",
]