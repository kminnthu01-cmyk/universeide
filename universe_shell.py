"""
Universe IDE - Shell Commands

Command palette and shell integration.
"""

import subprocess
from typing import List, Optional


# ============================================================================
# COMMAND PALETTE
# ============================================================================

class CommandPalette:
    """Command palette"""
    
    def __init__(self):
        self.commands = {}
        
    def register(self, id: str, command: str, handler=None):
        """Register command"""
        self.commands[id] = {
            "id": id,
            "command": command,
            "handler": handler,
        }
        
    def get(self, id: str) -> Optional[dict]:
        """Get command"""
        return self.commands.get(id)
        
    def list_commands(self) -> List[dict]:
        """List commands"""
        return list(self.commands.values())


# ============================================================================
# SHELL
# ============================================================================

class Shell:
    """Shell execution"""
    
    def __init__(self):
        self.history = []
        
    def execute(self, cmd: str, timeout: int = 30) -> dict:
        """Execute command"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
            self.history.append({"cmd": cmd, "result": output})
            return output
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def get_history(self) -> List[dict]:
        """Get history"""
        return self.history


# ============================================================================
# BUILDER
# ============================================================================

class CommandBuilder:
    """Build commands"""
    
    COMMON = {
        "git status": "git status",
        "git add .": "git add .",
        "git commit": "git commit -m",
        "git push": "git push origin main",
        "ls -la": "ls -la",
        "pwd": "pwd",
    }
    
    @staticmethod
    def build(cmd: str, args: List[str] = None) -> str:
        """Build command"""
        if args:
            return f"{cmd} {' '.join(args)}"
        return cmd
        
    @staticmethod
    def from_template(template: str, **kwargs) -> str:
        """Build from template"""
        return template.format(**kwargs)


# Global
_shell = None

def get_shell() -> Shell:
    global _shell
    if _shell is None:
        _shell = Shell()
    return _shell


__all__ = [
    "CommandPalette",
    "Shell",
    "CommandBuilder",
    "get_shell",
]