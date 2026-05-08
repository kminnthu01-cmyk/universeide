#!/usr/bin/env python3
"""
Universe IDE - Universal Launcher

Works on Windows, macOS, Linux.
Usage: python run.py [command]
"""

import os
import subprocess
import sys


def get_venv_python():
    """Get Python path in virtual environment"""
    if sys.platform == "win32" or os.name == "nt":
        return ".venv\\Scripts\\python.exe"
    return ".venv/bin/python"


def main():
    """Main launcher"""
    # Check if venv exists
    venv_python = get_venv_python()
    
    if not os.path.exists(venv_python):
        print("Setting up virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
        
        # Install dependencies
        print("Installing dependencies...")
        if sys.platform == "win32" or os.name == "nt":
            subprocess.run([".venv\\Scripts\\pip.exe", "install", "-e", "."])
        else:
            subprocess.run([".venv/bin/pip", "install", "-e", "."])
    
    # Get command
    cmd = sys.argv[1:] if len(sys.argv) > 1 else ["--help"]
    
    # Run in venv
    if cmd == ["--help"] or not cmd:
        print("""
🪐 Universe IDE - Quick Start

Commands:
  python run.py              # Start interactive
  python run.py cosmos       # Create universe
  python run.py test        # Run tests
  python run.py ui           # Open UI
  python run.py --help       # Show this help
        """)
        return
        
    if cmd[0] == "cosmos":
        result = subprocess.run(
            [venv_python, "-c", "from universe_ide import cosmos; print(cosmos(1000))"],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        
    elif cmd[0] == "test":
        subprocess.run([venv_python, "-m", "pytest", "tests/", "-v"])
        
    elif cmd[0] == "ui":
        import webbrowser
        webbrowser.open("universe_ide_ui.html")
        print("Opened UI in browser")
        
    else:
        print(f"Unknown command: {cmd[0]}")
        print("Run: python run.py --help")


if __name__ == "__main__":
    main()