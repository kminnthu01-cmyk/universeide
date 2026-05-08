"""
Universe IDE - Windows Integration

Windows-specific features and compatibility.
"""

import ctypes
import os
import platform
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


# ============================================================================
# WINDOWS DETECTION
# ============================================================================

class WindowsInfo:
    """Windows system information"""
    
    @staticmethod
    def is_windows() -> bool:
        """Check if Windows"""
        return os.name == 'nt' or platform.system() == 'Windows'
        
    @staticmethod
    def is_admin() -> bool:
        """Check if admin"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
            
    @staticmethod
    def get_version() -> str:
        """Get Windows version"""
        return platform.version()
        
    @staticmethod
    def get_arch() -> str:
        """Get architecture"""
        return platform.machine()


# ============================================================================
# WINDOWS PATHS
# ============================================================================

class WindowsPaths:
    """Windows paths"""
    
    @staticmethod
    def get_appdata() -> str:
        """Get appdata path"""
        return os.environ.get('APPDATA', '')
        
    @staticmethod
    def get_localappdata() -> str:
        """Get local appdata"""
        return os.environ.get('LOCALAPPDATA', '')
        
    @staticmethod
    def get_program_files() -> str:
        """Get program files"""
        return os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        
    @staticmethod
    def get_module_dir() -> str:
        """Get module directory"""
        if WindowsInfo.is_windows():
            return os.path.join(
                WindowsPaths.get_localappdata(),
                'universe-ide'
            )
        return '.universe-ide'


# ============================================================================
# WINDOWS REGISTRY
# ============================================================================

try:
    import winreg
    
    class Registry:
        """Windows registry"""
        
        @staticmethod
        def set_value(key: str, name: str, value: str):
            """Set registry value"""
            try:
                reg = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key)
                winreg.SetValueEx(reg, name, 0, winreg.REG_SZ, value)
                winreg.CloseKey(reg)
                return True
            except:
                return False
                
        @staticmethod
        def get_value(key: str, name: str) -> Optional[str]:
            """Get registry value"""
            try:
                reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key)
                value, _ = winreg.QueryValueEx(reg, name)
                winreg.CloseKey(reg)
                return value
            except:
                return None
                
except ImportError:
    Registry = None


# ============================================================================
# WINKIT INTEGRATION
# ============================================================================

class WinKit:
    """Windows kit integration"""
    
    @staticmethod
    def open_file(path: str):
        """Open file with default app"""
        if WindowsInfo.is_windows():
            os.startfile(path)
            
    @staticmethod
    def open_url(url: str):
        """Open URL in browser"""
        if WindowsInfo.is_windows():
            subprocess.Popen(['start', '', url], shell=True)
            
    @staticmethod
    def show_notification(title: str, message: str):
        """Show Windows notification"""
        # PowerShell notification
        script = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
        $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
        $text = $xml.GetElementsByTagName("text")
        $text.Item(0).AppendChild($xml.CreateTextNode("{title}")) | Out-Null
        $text.Item(1).AppendChild($xml.CreateTextNode("{message}")) | Out-Null
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("UniverseIDE")
        $notifier.Show($toast)
        '''
        
        if WindowsInfo.is_windows():
            try:
                subprocess.Popen(
                    ['powershell', '-Command', script],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except:
                pass


# ============================================================================
# POWERSHELL
# ============================================================================

class PowerShell:
    """PowerShell execution"""
    
    @staticmethod
    def run(script: str) -> tuple[str, str, int]:
        """Run PowerShell script"""
        try:
            result = subprocess.Popen(
                ['powershell', '-Command', script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = result.communicate()
            return (
                stdout.decode('utf-8', errors='ignore'),
                stderr.decode('utf-8', errors='ignore'),
                result.returncode,
            )
        except Exception as e:
            return "", str(e), 1
            
    @staticmethod
    def install_universe():
        """Install Universe IDE via PowerShell"""
        script = "pip install universe-ide"
        return PowerShell.run(script)


# ============================================================================
# WINDOWS SERVICE
# ============================================================================

@dataclass
class WindowsService:
    """Windows service wrapper"""
    name: str
    status: str = "stopped"
    start_type: str = "manual"


class WindowsServiceManager:
    """Manage Windows services"""
    
    @staticmethod
    def is_running(service_name: str) -> bool:
        """Check if service running"""
        if not WindowsInfo.is_windows():
            return False
            
        script = f'(Get-Service -Name "{service_name}" -ErrorAction SilentlyContinue).Status'
        output, _, _ = PowerShell.run(script)
        
        return 'Running' in output
        
    @staticmethod
    def start(service_name: str) -> bool:
        """Start service"""
        if not WindowsInfo.is_windows():
            return False
            
        script = f'Start-Service -Name "{service_name}"'
        _, _, code = PowerShell.run(script)
        
        return code == 0


# ============================================================================
# CONFIG FOR WINDOWS
# ============================================================================

class WindowsConfig:
    """Windows-specific config"""
    
    @staticmethod
    def get_config_path() -> str:
        """Get config path"""
        return os.path.join(
            WindowsPaths.get_localappdata(),
            'universe-ide',
            'config.yaml'
        )
        
    @staticmethod
    def ensure_dirs():
        """Ensure directories exist"""
        if WindowsInfo.is_windows():
            dirs = [
                WindowsPaths.get_module_dir(),
                WindowsPaths.get_localappdata(),
            ]
            for d in dirs:
                os.makedirs(d, exist_ok=True)


# ============================================================================
# WINDOWS MANAGER
# ============================================================================

class WindowsManager:
    """Windows management"""
    
    def __init__(self):
        self.info = WindowsInfo()
        self.paths = WindowsPaths()
        self.config = WindowsConfig()
        
    def get_status(self) -> dict:
        """Get Windows status"""
        return {
            "is_windows": self.info.is_windows(),
            "is_admin": self.info.is_admin(),
            "version": self.info.get_version(),
            "arch": self.info.get_arch(),
        }
        
    def setup(self):
        """Setup for Windows"""
        if self.info.is_windows():
            self.config.ensure_dirs()


# Global
_windows = None

def get_windows() -> WindowsManager:
    """Get Windows manager"""
    global _windows
    if _windows is None:
        _windows = WindowsManager()
    return _windows


__all__ = [
    "WindowsInfo",
    "WindowsPaths", 
    "Registry",
    "WinKit",
    "PowerShell",
    "WindowsService",
    "WindowsServiceManager",
    "WindowsConfig",
    "WindowsManager",
    "get_windows",
]