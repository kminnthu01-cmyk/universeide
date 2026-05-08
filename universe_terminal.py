"""
Universe IDE - Terminal Emulator

Full terminal emulator with shell.
"""

import os
import pty
import select
import signal
import subprocess
import termios
import tty
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple


# ============================================================================
# TERMINAL TYPES
# ============================================================================

class TerminalType(Enum):
    """Terminal types"""
    XTERM = "xterm"
    VT100 = "vt100"
    LINUX = "linux"
    CELESTE = "celeste"


@dataclass
class TerminalSize:
    """Terminal dimensions"""
    rows: int = 24
    cols: int = 80


# ============================================================================
# SHELL MANAGER
# ============================================================================

class ShellManager:
    """
    Manage shell processes.
    """
    
    def __init__(self, shell: str = "/bin/bash"):
        self.shell = shell
        self.process: Optional[subprocess.Popen] = None
        self.master_fd: Optional[int] = None
        
    def start(self, cwd: str = None):
        """Start shell"""
        cwd = cwd or os.getcwd()
        
        # Start pseudo-terminal
        master, slave = pty.openpty()
        
        self.process = subprocess.Popen(
            [self.shell],
            stdin=slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            preexec_fn=os.setsid,
        )
        
        os.close(slave)
        self.master_fd = master
        
    def read(self, size: int = 1024) -> bytes:
        """Read from shell"""
        if not self.master_fd:
            return b""
            
        try:
            return os.read(self.master_fd, size)
        except:
            return b""
            
    def write(self, data: str):
        """Write to shell"""
        if self.master_fd:
            try:
                os.write(self.master_fd, data.encode())
            except:
                pass
                
    def resize(self, rows: int, cols: int):
        """Resize terminal"""
        if self.master_fd:
            try:
                import fcntl
                import struct
                import termios
                fcntl.ioctl(
                    self.master_fd,
                    termios.TIOCSWINSZ,
                    struct.pack("hhhh", rows, cols, 0, 0),
                )
            except:
                pass
                
    def is_alive(self) -> bool:
        """Check if shell is running"""
        if self.process:
            return self.process.poll() is None
        return False
        
    def kill(self):
        """Kill shell"""
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
                
    def close(self):
        """Close shell"""
        if self.master_fd:
            try:
                os.close(self.master_fd)
            except:
                pass
                
        if self.process:
            self.process.wait()


# ============================================================================
# TERMINAL EMULATOR
# ============================================================================

class TerminalEmulator:
    """
    Full terminal emulator.
    """
    
    # ANSI escape codes
    ANSI_CODES = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bg_black": "\033[40m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
    }
    
    def __init__(
        self,
        terminal_type: TerminalType = TerminalType.CELESTE,
        shell: str = "/bin/bash",
    ):
        self.terminal_type = terminal_type
        self.shell_manager = ShellManager(shell)
        self.size = TerminalSize()
        self.history: List[str] = []
        self.max_history = 1000
        self.cursor_visible = True
        self.scrollback = 100
        
    def start(self, cwd: str = None):
        """Start terminal"""
        self.shell_manager.start(cwd)
        print(f"🖥️  Universe Terminal v1.0")
        print(f"    Shell: {self.shell_manager.shell}")
        
    def read_output(self) -> str:
        """Read output"""
        data = self.shell_manager.read()
        return data.decode("utf-8", errors="replace")
        
    def send_command(self, command: str):
        """Send command"""
        self.shell_manager.write(command + "\n")
        
    def send_key(self, key: str):
        """Send key press"""
        self.shell_manager.write(key)
        
    def resize(self, rows: int, cols: int):
        """Resize terminal"""
        self.size = TerminalSize(rows, cols)
        self.shell_manager.resize(rows, cols)
        
    def get_size(self) -> Tuple[int, int]:
        """Get terminal size"""
        return self.size.rows, self.size.cols
        
    def is_alive(self) -> bool:
        """Check if running"""
        return self.shell_manager.is_alive()
        
    def close(self):
        """Close terminal"""
        self.shell_manager.close()


# ============================================================================
# TERMINAL UI
# ============================================================================

TERMINAL_HTML = '''<!DOCTYPE html>
<html>
<head>
<style>
.terminal {{
    background: #0d1117;
    color: #58a6ff;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    padding: 20px;
    border-radius: 8px;
    min-height: 400px;
}}
.prompt {{
    color: #7ee787;
}}
.output {{
    color: #c9d1d9;
    white-space: pre-wrap;
}}
.cursor {{
    display: inline-block;
    width: 8px;
    height: 16px;
    background: #58a6ff;
    animation: blink 1s step-end infinite;
}}
@keyframes blink {{
    50% {{ opacity: 0; }}
}}
</style>
</head>
<body>
<div class="terminal" id="terminal">
<div class="output" id="output"></div>
<span class="prompt">$ </span><span class="cursor">▊</span>
</div>
</body>
</html>'''


# Global
_terminal = None

def get_terminal(
    terminal_type: TerminalType = TerminalType.CELESTE,
) -> TerminalEmulator:
    """Get terminal emulator"""
    global _terminal
    if _terminal is None:
        _terminal = TerminalEmulator(terminal_type)
    return _terminal


__all__ = [
    "TerminalType",
    "TerminalSize",
    "ShellManager",
    "TerminalEmulator",
    "TERMINAL_HTML",
    "get_terminal",
]