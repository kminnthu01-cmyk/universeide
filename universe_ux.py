"""
Universe IDE - Interactive UI Components

User Experience focused components.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional


# ============================================================================
# UI COMPONENTS
# ============================================================================

class ComponentType(Enum):
    """UI component types"""
    BUTTON = "button"
    INPUT = "input"
    SELECT = "select"
    CHECKBOX = "checkbox"
    SLIDER = "slider"
    TOGGLE = "toggle"
    CARD = "card"
    MODAL = "modal"
    TABS = "tabs"
    TABLE = "table"
    LIST = "list"
    TREE = "tree"
    CHART = "chart"


@dataclass
class Component:
    """UI Component"""
    component_id: str
    type: ComponentType
    label: str
    value: Any = None
    options: list = field(default_factory=list)
    enabled: bool = True
    visible: bool = True
    action: Optional[Callable] = None


# ============================================================================
# THEME
# ============================================================================

class ThemeVariant(Enum):
    """Theme variants"""
    LIGHT = "light"
    DARK = "dark"
    COSMIC = "cosmic"
    NEON = "neon"


class Theme:
    """
    Theme management.
    """
    
    THEMES = {
        ThemeVariant.LIGHT: {
            "bg": "#ffffff",
            "fg": "#1a1a1a",
            "accent": "#6366f1",
            "success": "#22c55e",
            "warning": "#f59e0b",
            "error": "#ef4444",
        },
        ThemeVariant.DARK: {
            "bg": "#0f0f0f",
            "fg": "#fafafa",
            "accent": "#818cf8",
            "success": "#4ade80",
            "warning": "#fbbf24",
            "error": "#f87171",
        },
        ThemeVariant.COSMIC: {
            "bg": "#0a0a1a",
            "fg": "#e0e7ff",
            "accent": "#8b5cf6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444",
        },
        ThemeVariant.NEON: {
            "bg": "#000000",
            "fg": "#00ff00",
            "accent": "#ff00ff",
            "success": "#00ff00",
            "warning": "#ffff00",
            "error": "#ff0000",
        },
    }
    
    def __init__(self, variant: ThemeVariant = ThemeVariant.COSMIC):
        self.variant = variant
        self.colors = self.THEMES[variant]
        
    def get_css(self) -> str:
        """Get CSS variables"""
        return f"""
--bg: {self.colors['bg']};
--fg: {self.colors['fg']};
--accent: {self.colors['accent']};
--success: {self.colors['success']};
--warning: {self.colors['warning']};
--error: {self.colors['error']};
"""
        
    def get_config(self) -> dict:
        """Get theme config"""
        return {
            "variant": self.variant.value,
            "colors": self.colors,
        }


# ============================================================================
# INTERACTIVE TERMINAL
# ============================================================================

class InteractiveTerminal:
    """
    Terminal with autocomplete and suggestions.
    """
    
    def __init__(self):
        self.history: list[str] = []
        self.suggestions: list[str] = []
        self.commands = {
            "help": "Show available commands",
            "status": "Show status",
            "create": "Create universe",
            "deploy": "Deploy task",
            "analyze": "Analyze code",
            "config": "Configure settings",
            "theme": "Change theme",
            "clear": "Clear terminal",
        }
        
    def get_suggestions(self, prefix: str) -> list[str]:
        """Get command suggestions"""
        return [
            cmd for cmd in self.commands.keys()
            if cmd.startswith(prefix.lower())
        ]
        
    def format_help(self) -> str:
        """Format help output"""
        lines = ["Available commands:", ""]
        
        for cmd, desc in self.commands.items():
            lines.append(f"  {cmd:12} - {desc}")
            
        return "\n".join(lines)


# ============================================================================
# WIZARD
# ============================================================================

@dataclass
class WizardStep:
    """Wizard step"""
    step_id: str
    title: str
    description: str
    prompt: str = ""
    validation: Optional[Callable] = None


class SetupWizard:
    """
    Interactive setup wizard.
    """
    
    def __init__(self):
        self.steps: list[WizardStep] = []
        self.current_step = 0
        self.answers: dict = {}
        
    def add_step(self, step: WizardStep):
        """Add step"""
        self.steps.append(step)
        
    def get_current(self) -> Optional[WizardStep]:
        """Get current step"""
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
        
    def next_step(self, answer: Any = None) -> bool:
        """Move to next step"""
        if answer is not None:
            current = self.get_current()
            if current:
                self.answers[current.step_id] = answer
                
        self.current_step += 1
        return self.current_step < len(self.steps)
        
    def is_complete(self) -> bool:
        """Check if complete"""
        return self.current_step >= len(self.steps)
        
    def get_summary(self) -> dict:
        """Get answers summary"""
        return self.answers


# ============================================================================
# NOTIFICATIONS
# ============================================================================

class NotificationType(Enum):
    """Notification types"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    PROGRESS = "progress"


@dataclass
class Notification:
    """Notification"""
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False


class NotificationManager:
    """
    Notification management.
    """
    
    def __init__(self):
        self.notifications: list[Notification] = []
        self.max_notifications = 50
        
    def add(
        self, 
        title: str, 
        message: str,
        notification_type: NotificationType = NotificationType.INFO
    ):
        """Add notification"""
        notif = Notification(
            title=title,
            message=message,
            type=notification_type,
        )
        
        self.notifications.append(notif)
        
        # Trim
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[-self.max_notifications:]
            
    def get_all(self, unread_only: bool = False) -> list[Notification]:
        """Get notifications"""
        notifs = self.notifications
        
        if unread_only:
            notifs = [n for n in notifs if not n.read]
            
        return notifs
        
    def mark_read(self, index: int):
        """Mark as read"""
        if 0 <= index < len(self.notifications):
            self.notifications[index].read = True
            
    def clear(self):
        """Clear all"""
        self.notifications.clear()


# ============================================================================
# ONBOARDING
# ============================================================================

@dataclass
class OnboardingStep:
    """Onboarding step"""
    title: str
    content: str
    action_label: str = "Next"
    

class Onboarding:
    """
    User onboarding flow.
    """
    
    def __init__(self):
        self.steps: list[OnboardingStep] = []
        self.current = 0
        self._init_default_steps()
        
    def _init_default_steps(self):
        """Initialize default steps"""
        self.steps = [
            OnboardingStep(
                title="Welcome to Universe IDE",
                content="The ultimate AI agentic platform for building intelligent applications.",
            ),
            OnboardingStep(
                title="Create Your First Universe",
                content="Use cosmos(n) to create n parallel agents.",
            ),
            OnboardingStep(
                title="Explore Features",
                content="Self-learning, monitoring, security, and more.",
            ),
            OnboardingStep(
                title="You're Ready!",
                content="Start building amazing applications.",
            ),
        ]
        
    def get_current(self) -> Optional[OnboardingStep]:
        """Get current step"""
        if 0 <= self.current < len(self.steps):
            return self.steps[self.current]
        return None
        
    def next(self) -> bool:
        """Next step"""
        if self.current < len(self.steps) - 1:
            self.current += 1
            return True
        return False
        
    def reset(self):
        """Reset"""
        self.current = 0


# ============================================================================
# UX MANAGER
# ============================================================================

class UXManager:
    """
    Unified UX management.
    """
    
    def __init__(self):
        self.theme = Theme(ThemeVariant.COSMIC)
        self.terminal = InteractiveTerminal()
        self.setup_wizard = SetupWizard()
        self.notifications = NotificationManager()
        self.onboarding = Onboarding()
        
    def set_theme(self, variant: ThemeVariant):
        """Set theme"""
        self.theme = Theme(variant)
        
    def show_notification(
        self, 
        title: str, 
        message: str,
        notification_type: NotificationType = NotificationType.INFO
    ):
        """Show notification"""
        self.notifications.add(title, message, notification_type)


# Global
_ux = None

def get_ux() -> UXManager:
    """Get UX manager"""
    global _ux
    if _ux is None:
        _ux = UXManager()
    return _ux


__all__ = [
    "ComponentType",
    "Component",
    "ThemeVariant",
    "Theme",
    "InteractiveTerminal",
    "SetupWizard",
    "NotificationType",
    "Notification",
    "NotificationManager",
    "Onboarding",
    "UXManager",
    "get_ux",
]