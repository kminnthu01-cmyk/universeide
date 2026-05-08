# Universe IDE - Linux/macOS Installation Guide

## Linux (Ubuntu/Debian)

### Prerequisites

```bash
sudo apt update
sudo apt install python3.13 python3-pip git
```

### Step 1: Clone

```bash
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
```

### Step 2: Virtual Environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install

```bash
pip install -e .
```

### Step 4: Run Tests

```bash
pytest tests/ -v
```

### Step 5: Quick Start

```bash
python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

### Step 6: Open UI

```bash
open universe_ide_ui.html  # macOS
xdg-open universe_ide_ui.html  # Linux
```

---

## macOS

### Prerequisites

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.13
```

### Step 1: Clone

```bash
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
```

### Step 2: Virtual Environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install

```bash
pip install -e .
```

### Step 4: Run Tests

```bash
pytest tests/ -v
```

### Step 5: Quick Start

```bash
python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

### Step 6: Open UI

```bash
open universe_ide_ui.html
```

---

## Desktop App

### Run Desktop UI

```bash
python universe_desktop.py
```

### VSCode Extension

```bash
# Install
code --install-extension extension/

# Or manually copy extension/ to ~/.vscode/extensions/
```

---

## Common Issues

### Permission Denied

```bash
# Fix pip
python3 -m pip install --user -e .
```

### SSL Certificate Error

```bash
# Update certificates
/Applications/Python\ 3.13/Install\ Certificates.command
```

### Old Python

```bash
# Use pyenv
brew install pyenv
pyenv install 3.13.0
pyenv global 3.13.0
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `source .venv/bin/activate` | Activate |
| `python -c "..."` | Run one-liner |
| `pytest tests/ -v` | Run tests |
| `open universe_ide_ui.html` | Open UI |

**🪐 Universe IDE on Linux/macOS**