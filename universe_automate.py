from typing import Any, Callable, Dict, List

"""
Universe IDE - Automation Library

Automate common tasks.
"""

import os
import shutil
from typing import Callable, Dict, List


# ============================================================================
# TASK AUTOMATION
# ============================================================================

class TaskAutomation:
    """Automate repetitive tasks"""
    
    def __init__(self):
        self.tasks = {}
        
    def register(self, name: str, task: Callable):
        self.tasks[name] = task
        
    def run(self, name: str) -> Any:
        if name in self.tasks:
            return self.tasks[name]()
        return None
    
    def list_tasks(self) -> List[str]:
        return list(self.tasks.keys())


# ============================================================================
# BATCH OPERATIONS
# ============================================================================

class BatchOperations:
    """Batch file operations"""
    
    @staticmethod
    def copy_files(source: List[str], dest_dir: str):
        os.makedirs(dest_dir, exist_ok=True)
        
        for src in source:
            if os.path.exists(src):
                shutil.copy2(src, dest_dir)
                
    @staticmethod
    def delete_files(pattern: str):
        import glob
        files = glob.glob(pattern)
        
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
                
    @staticmethod
    def rename_files(directory: str, old_ext: str, new_ext: str):
        for f in os.listdir(directory):
            if f.endswith(old_ext):
                src = os.path.join(directory, f)
                dst = os.path.join(directory, f[:-len(old_ext)] + new_ext)
                os.rename(src, dst)


# ============================================================================
# FILE WATCHER
# ============================================================================

class FileWatcher:
    """Watch files for changes"""
    
    def __init__(self):
        self.watchers = {}
        
    def watch(self, path: str, callback: Callable):
        self.watchers[path] = callback
        
    def trigger(self, path: str):
        if path in self.watchers:
            self.watchers[path]()


# ============================================================================
# TEMPLATE ENGINE
# ============================================================================

class TemplateEngine:
    """Generate code from templates"""
    
    @staticmethod
    def generate(name: str, **vars) -> str:
        templates = {
            "react_component": '''export function {name}() {{
  return (
    <div className="{name}">
    </div>
  );
}}''',
            "python_script": '''#!/usr/bin/env python3
\"\"\"
{name} - Auto-generated
\"\"\"

def main():
    pass

if __name__ == "__main__":
    main()''',
            "test": '''import pytest

def test_{name}():
    assert True''',
        }
        
        template = templates.get(name, "")
        return template.format(**vars)


# ============================================================================
# DEPLOY AUTOMATION
# ============================================================================

class DeployAutomation:
    """Automated deployment"""
    
    @staticmethod
    def build_and_deploy(target: str):
        steps = {
            "vercel": ["npm run build", "vercel deploy"],
            "docker": ["docker build", "docker push"],
            "aws": ["sam build", "sam deploy"],
        }
        
        return steps.get(target, [])


# ============================================================================
# CLEANUP
# ============================================================================

class Cleanup:
    """Clean project files"""
    
    @staticmethod
    def clean_cache():
        import glob
        patterns = ["__pycache__", "*.pyc", "*.pyo"]
        
        for pattern in patterns:
            for path in glob.glob(pattern, recursive=True):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                elif os.path.isfile(path):
                    os.remove(path)
                    
    @staticmethod
    def clean_build():
        import glob
        patterns = ["build", "dist", "*.egg-info"]
        
        for pattern in glob.glob("*", recursive=True):
            if os.path.isdir(pattern) and pattern in patterns:
                shutil.rmtree(pattern)


__all__ = ["TaskAutomation", "BatchOperations", "FileWatcher", "TemplateEngine", "DeployAutomation", "Cleanup"]