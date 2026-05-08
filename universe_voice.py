"""
Universe IDE - Voice Control

Voice-based command interface.
speech_recognition and pyttsx3 are optional dependencies.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional

# Try imports, but allow module to load without them
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    sr = None
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    pyttsx3 = None
    PYTTSX3_AVAILABLE = False


# ============================================================================
# VOICE COMMANDS
# ============================================================================

class VoiceCommand(Enum):
    """Voice commands"""
    CREATE = "create universe"
    STATUS = "show status"
    DEPLOY = "deploy task"
    HELP = "help"
    STOP = "stop"
    START = "start"


# ============================================================================
# VOICE RECOGNIZER
# ============================================================================

class VoiceRecognizer:
    """
    Voice-to-text recognition.
    """
    
    def __init__(self):
        if SPEECH_RECOGNITION_AVAILABLE and sr:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        else:
            self.recognizer = None
            self.microphone = None
            
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input"""
        if not self.recognizer:
            return None
            
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=timeout)
                
            text = self.recognizer.recognize_google(audio)
            return text
            
        except:
            return None
            
    def parse_command(self, text: str) -> VoiceCommand:
        """Parse command from text"""
        text = text.lower()
        
        for cmd in VoiceCommand:
            if cmd.value in text:
                return cmd
                
        return None


# ============================================================================
# VOICE CONTROLLER
# ============================================================================

class VoiceController:
    """
    Voice-based control.
    """
    
    def __init__(self):
        self.recognizer = VoiceRecognizer()
        self.listening = False
        self.handlers: dict[VoiceCommand, Callable] = {}
        
    def register(self, command: VoiceCommand, handler: Callable):
        """Register command handler"""
        self.handlers[command] = handler
        
    async def start_listening(self):
        """Start voice listening loop"""
        self.listening = True
        print("🎤 Voice control started. Say a command...")
        
        while self.listening:
            text = self.recognizer.listen()
            
            if text:
                print(f"  Heard: {text}")
                cmd = self.recognizer.parse_command(text)
                
                if cmd and cmd in self.handlers:
                    await self.handlers[cmd]()
                    
            await asyncio.sleep(0.5)
            
    def stop_listening(self):
        """Stop listening"""
        self.listening = False


# ============================================================================
# TEXT TO SPEECH
# ============================================================================

class TextToSpeech:
    """
    Text-to-speech output.
    """
    
    def __init__(self):
        if PYTTSX3_AVAILABLE and pyttsx3:
            self.engine = pyttsx3.init()
        else:
            self.engine = None
            
    def speak(self, text: str):
        """Speak text"""
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
                
    def speak_async(self, text: str):
        """Speak async"""
        asyncio.create_task(self._speak(text))
        
    async def _speak(self, text: str):
        """Internal async speak"""
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()


# ============================================================================
# VOICE MODE
# ============================================================================

class VoiceMode:
    """Full voice mode"""
    
    def __init__(self):
        self.controller = VoiceController()
        self.tts = TextToSpeech()
        
    async def run(self):
        """Run voice mode"""
        # Register default handlers
        self.controller.register(VoiceCommand.STATUS, lambda: print("Status: Running"))
        self.controller.register(VoiceCommand.CREATE, lambda: print("Creating universe"))
        
        await self.controller.start_listening()


# Global
_voice = None

def get_voice_mode() -> VoiceMode:
    """Get voice mode"""
    global _voice
    if _voice is None:
        _voice = VoiceMode()
    return _voice


__all__ = [
    "VoiceCommand",
    "VoiceRecognizer",
    "VoiceController",
    "TextToSpeech",
    "VoiceMode",
    "get_voice_mode",
]