"""
Universe IDE - Collaboration

Multiplayer coding with real-time sync.
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# PRESENCE
# ============================================================================

@dataclass
class UserPresence:
    """User presence in session"""
    user_id: str
    username: str
    cursor_position: int = 0
    selection: tuple = field(default_factory=tuple)
    last_active: datetime = field(default_factory=datetime.now)
    color: str = "#6366f1"


# ============================================================================
# REAL-TIME COLLAB
# ============================================================================

class RealtimeCollab:
    """
    Real-time collaborative editing.
    """
    
    def __init__(self):
        self.users: Dict[str, UserPresence] = {}
        self.document: str = ""
        self.version: int = 0
        self.history: List[dict] = []
        self._lock = asyncio.Lock()
        
    async def join(self, user_id: str, username: str):
        """User joins"""
        self.users[user_id] = UserPresence(
            user_id=user_id,
            username=username,
        )
        
    async def leave(self, user_id: str):
        """User leaves"""
        if user_id in self.users:
            del self.users[user_id]
            
    async def edit(
        self, 
        user_id: str, 
        position: int, 
        delete_count: int, 
        insert_text: str
    ):
        """Apply edit"""
        async with self._lock:
            # Apply edit
            before = self.document[:position]
            after = self.document[position + delete_count:]
            self.document = before + insert_text + after
            
            # Record in history
            self.history.append({
                "user_id": user_id,
                "position": position,
                "delete_count": delete_count,
                "insert_text": insert_text,
                "version": self.version,
                "timestamp": time.time(),
            })
            
            self.version += 1
            
    async def get_operations(self, since_version: int) -> List[dict]:
        """Get ops since version"""
        return [
            op for op in self.history 
            if op["version"] > since_version
        ]
        
    async def update_cursor(self, user_id: str, position: int):
        """Update cursor"""
        if user_id in self.users:
            self.users[user_id].cursor_position = position
            self.users[user_id].last_active = datetime.now()
            
    def get_presence(self) -> List[UserPresence]:
        """Get all presence"""
        return list(self.users.values())


# ============================================================================
# SHARED EDITOR
# ============================================================================

class SharedEditor:
    """
    Multiplayer shared editor.
    """
    
    def __init__(self):
        self.collab = RealtimeCollab()
        
    async def create_session(self, document: str = "") -> str:
        """Create session"""
        session_id = f"session_{int(time.time())}"
        self.collab.document = document
        return session_id
        
    async def apply_operation(
        self, 
        session_id: str,
        user_id: str,
        position: int,
        delete_count: int,
        insert_text: str,
    ):
        """Apply operation"""
        await self.collab.edit(user_id, position, delete_count, insert_text)
        
    def get_state(self) -> dict:
        """Get editor state"""
        return {
            "document": self.collab.document,
            "version": self.collab.version,
            "users": [
                {
                    "user_id": u.user_id,
                    "username": u.username,
                    "cursor": u.cursor_position,
                    "color": u.color,
                }
                for u in self.collab.get_presence()
            ],
        }


# ============================================================================
# CODE REVIEW
# ============================================================================

@dataclass
class ReviewComment:
    """Code review comment"""
    comment_id: str
    author: str
    content: str
    path: str
    line: int
    created_at: datetime = field(default_factory=datetime.now)
    resolved: bool = False


class CodeReview:
    """
    Code review system.
    """
    
    def __init__(self):
        self.comments: Dict[str, ReviewComment] = {}
        
    def add_comment(
        self,
        author: str,
        content: str,
        path: str,
        line: int,
    ) -> str:
        """Add comment"""
        import uuid
        comment_id = f"comment_{uuid.uuid4().hex[:8]}"
        self.comments[comment_id] = ReviewComment(
            comment_id=comment_id,
            author=author,
            content=content,
            path=path,
            line=line,
        )
        return comment_id
        
    def resolve(self, comment_id: str):
        """Resolve comment"""
        if comment_id in self.comments:
            self.comments[comment_id].resolved = True
            
    def get_comments(self, path: str = None) -> List[ReviewComment]:
        """Get comments"""
        if path:
            return [c for c in self.comments.values() if c.path == path]
        return list(self.comments.values())


# ============================================================================
# PAIR PROGRAMMING
# ============================================================================

class PairProgramming:
    """
    Pair programming session.
    """
    
    def __init__(self):
        self.driver: Optional[str] = None
        self.navigator: Optional[str] = None
        self.shared_editor = SharedEditor()
        
    async def start(self, driver_id: str, navigator_id: str):
        """Start pair session"""
        self.driver = driver_id
        self.navigator = navigator_id
        print(f"� pair programming: {driver_id} (driver) <-> {navigator_id} (navigator)")
        
    async def switch_roles(self):
        """Switch driver/navigator"""
        self.driver, self.navigator = self.navigator, self.driver
        print(f"🔄 Roles switched: {self.driver} (driver) <-> {self.navigator} (navigator)")


# Global
_collab = None

def get_collaboration() -> RealtimeCollab:
    """Get collaboration"""
    global _collab
    if _collab is None:
        _collab = RealtimeCollab()
    return _collab


__all__ = [
    "UserPresence",
    "RealtimeCollab",
    "SharedEditor",
    "ReviewComment",
    "CodeReview",
    "PairProgramming",
    "get_collaboration",
]