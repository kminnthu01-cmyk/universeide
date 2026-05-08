# Universe IDE - Windows Installation Guide

## Windows 10/11

### Prerequisites

- Windows 10 version 1903+ or Windows 11
- Python 3.13+
- Git for Windows

### Step 1: Install Python

Download from: https://www.python.org/downloads/

```
✅ Check "Add Python to PATH"
✅ Check "Install pip"
```

Verify:
```cmd
python --version
```

### Step 2: Install Git

Download from: https://git-scm.com/download/win

### Step 3: Clone Repository

```cmd
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
```

### Step 4: Create Virtual Environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```cmd
pip install -e .
```

### Step 6: Run Tests

```cmd
pytest tests/ -v
```

### Step 7: Run Universe IDE

```cmd
# Create 1000 agents
python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

### Step 8: Open UI

```cmd
start universe_ide_ui.html
```

---

## Desktop App

### Option 1: Run Desktop App

```cmd
python universe_desktop.py
```

### Option 2: VSCode Extension

```cmd
# Install extension
code --install-extension extension/
```

---

## Common Issues

### Python Not Found

Add to PATH:
```
C:\Python313\
C:\Python313\Scripts\
```

### pip Not Recognized

```cmd
python -m pip install -e .
```

### Slow Performance

Use PowerShell:
```powershell
# Set performance mode
powercfg /setactive scheme_min
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `.venv\Scripts\activate` | Activate environment |
| `python -c "..."` | Run one-liner |
| `pytest tests/ -v` | Run tests |
| `start universe_ide_ui.html` | Open UI |

**🪐 Universe IDE on Windows**