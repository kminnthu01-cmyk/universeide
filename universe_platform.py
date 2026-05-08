"""
Universe IDE - Cross-Platform Support

Easy installation for all platforms.
"""

import os
import platform
import subprocess
import sys
from typing import Optional


# ============================================================================
# PLATFORM DETECTION
# ============================================================================

def get_platform() -> str:
    """Detect current platform"""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return system


def is_python_installed() -> bool:
    """Check if Python is installed"""
    try:
        result = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


# ============================================================================
# PLATFORM-SPECIFIC INSTALL
# ============================================================================

class PlatformInstaller:
    """Install Universe IDE on any platform"""
    
    @staticmethod
    def install_python() -> str:
        """Get Python install instructions"""
        system = get_platform()
        
        if system == "windows":
            return "Download Python 3.13 from python.org"
        elif system == "macos":
            return "brew install python@3.13"
        else:
            return "sudo apt install python3.13"
            
    @staticmethod
    def install_uv() -> str:
        """Get uv install command"""
        system = get_platform()
        
        if system == "windows":
            return "irm https://astral.sh/uv/install.ps1 | iex"
        elif system == "macos":
            return "brew install uv"
        else:
            return "curl -LsSf https://astral.sh/uv/install.sh | sh"


# ============================================================================
# QUICK START
# ============================================================================

class QuickStart:
    """One-command setup for all platforms"""
    
    @staticmethod
    def install_command() -> str:
        """Get install command for current platform"""
        system = get_platform()
        
        if system == "windows":
            return """
# Windows (PowerShell)
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
python -m venv .venv
.venv\\Scripts\\pip install -e .
python -c "from universe_ide import cosmos; print(cosmos(1000))"
"""
        elif system == "macos":
            return """
# macOS
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -c "from universe_ide import cosmos; print(cosmos(1000))"
"""
        else:
            return """
# Linux
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -c "from universe_ide import cosmos; print(cosmos(1000))"
"""
            
    @staticmethod
    def run_command() -> str:
        """Get run command for current platform"""
        system = get_platform()
        
        if system == "windows":
            return ".venv\\Scripts\\python -c \"from universe_ide import cosmos; print(cosmos(1000))\""
        else:
            return "./venv/bin/python -c \"from universe_ide import cosmos; print(cosmos(1000))\""


# ============================================================================
# BINARY RELEASES (Future)
# ============================================================================

class BinaryRelease:
    """Platform-specific binaries"""
    
    @staticmethod
    def get_download_url() -> Optional[str]:
        """Get download URL for current platform"""
        system = get_platform()
        
        # Placeholder for binary releases
        urls = {
            "windows": "https://github.com/.../universe-ide-windows.exe",
            "macos": "https://github.com/.../universe-ide-macos",
            "linux": "https://github.com/.../universe-ide-linux",
        }
        
        return urls.get(system)


# ============================================================================
# DOCKER
# ============================================================================

class DockerSetup:
    """Docker installation"""
    
    DOCKERFILE = '''
FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY . .
RUN uv sync

CMD ["python", "-c", "from universe_ide import cosmos; print(cosmos(1000))"]
'''
    
    @staticmethod
    def get_file() -> str:
        return DockerSetup.DOCKERFILE


# ============================================================================
# UNMANAGED INSTALL
# ============================================================================

def quick_install() -> str:
    """Universal quick install (works on all platforms)"""
    return f"""
# One-command setup (works on all platforms)
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide

# Use uv (works on Windows, macOS, Linux)
uv sync

# Run
uv run python -c "from universe_ide import cosmos; print(cosmos(1000))"
"""


# ============================================================================
# GUI LAUNCHER
# ============================================================================

class PlatformConfig:
    """Platform-specific config"""
    
    @staticmethod
    def get_editor_config() -> dict:
        """Get platform-specific editor settings"""
        system = get_platform()
        
        configs = {
            "windows": {
                "shell": "powershell",
                "path_separator": "\\\\",
                "line_ending": "crlf",
            },
            "macos": {
                "shell": "zsh",
                "path_separator": "/",
                "line_ending": "lf",
            },
            "linux": {
                "shell": "bash",
                "path_separator": "/",
                "line_ending": "lf",
            },
        }
        
        return configs.get(system, configs["linux"])


__all__ = [
    "get_platform",
    "PlatformInstaller", 
    "QuickStart",
    "BinaryRelease",
    "DockerSetup",
    "quick_install",
    "PlatformConfig",
]