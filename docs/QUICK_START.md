# Universe IDE - Easy Installation Guide

## 🪐 One-Command Setup (Works on All Platforms)

### Quick Start

```bash
# 1. Clone
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide

# 2. Install (auto-detects platform)
uv sync

# 3. Run
uv run python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

---

## Platform-Specific

### Windows

```powershell
# PowerShell
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
python -m venv .venv
.venv\Scripts\pip install -e .
.venv\Scripts\python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

### macOS

```bash
# Terminal
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

### Linux

```bash
# Bash
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

---

## Using Launcher

```bash
# Clone and run
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide

# Use launcher
python run.py cosmos      # Create universe
python run.py test       # Run tests
python run.py ui          # Open UI
```

---

## Docker

```bash
git clone https://github.com/kminnthu01-cmyk/universeide.git
cd universeide
docker build -t universe-ide .
docker run universe-ide
```

---

## No Install Required

```bash
# Just run with uv (no venv needed)
uv run python -c "from universe_ide import cosmos; print(cosmos(1000))"
```

---

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| Python | 3.13+ |
| Git | Any |
| Memory | 512MB |

**🪐 Works on Windows, macOS, Linux - Zero Config**