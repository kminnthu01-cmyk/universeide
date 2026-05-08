"""
Universe IDE - Collaboration

Multi-user collaboration features.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


# ============================================================================
# USER ROLES
# ============================================================================

class UserRole(Enum):
    """User roles"""
    VIEWER = "viewer"
    CONTRIBUTOR = "contributor"
    REVIEWER = "reviewer"
    DEVELOPER = "developer"
    ADMIN = "admin"
    OWNER = "owner"


# ============================================================================
# USER
# ============================================================================

@dataclass
class User:
    """A user"""
    user_id: str
    username: str
    email: str
    role: UserRole = UserRole.VIEWER
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)


# ============================================================================
# COLLABORATION SESSION
# ============================================================================

@dataclass
class Session:
    """A collaboration session"""
    session_id: str
    name: str
    owner: str
    participants: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# PRESENCE
# ============================================================================

class Presence:
    """
    User presence tracking.
    """
    
    def __init__(self):
        self.online: dict[str, datetime] = {}
        self.away: set[str] = set()
        
    def set_online(self, user_id: str):
        """Mark user online"""
        self.online[user_id] = datetime.now()
        self.away.discard(user_id)
        
    def set_away(self, user_id: str):
        """Mark user away"""
        self.away.add(user_id)
        
    def set_offline(self, user_id: str):
        """Mark user offline"""
        self.online.pop(user_id, None)
        self.away.discard(user_id)
        
    def get_online(self) -> list[str]:
        """Get online users"""
        return list(self.online.keys())


# ============================================================================
# REAL-TIME COLLABORATION
# ============================================================================

class CollabSession:
    """
    Real-time collaboration.
    """
    
    def __init__(self, session_id: str, owner: str):
        self.session_id = session_id
        self.owner = owner
        self.participants: dict[str, User] = {}
        self.messages: list[dict] = []
        self.cursors: dict[str, int] = {}
        self.edits: list[dict] = field(default_factory=list)
        
    def join(self, user: User):
        """User joins session"""
        self.participants[user.user_id] = user
        
    def leave(self, user_id: str):
        """User leaves session"""
        self.participants.pop(user_id, None)
        self.cursors.pop(user_id, None)
        
    def send_message(self, user_id: str, message: str):
        """Send message"""
        self.messages.append({
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now(),
        })
        
    def update_cursor(self, user_id: str, position: int):
        """Update cursor position"""
        self.cursors[user_id] = position


# ============================================================================
# CODE REVIEW
# ============================================================================

@dataclass
class ReviewRequest:
    """Code review request"""
    request_id: str
    author: str
    title: str
    description: str
    status: str = "pending"
    reviewers: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    

@dataclass
class Comment:
    """Review comment"""
    comment_id: str
    author: str
    line: int
    content: str
    resolved: bool = False


# ============================================================================
# SHARED EDITOR
# ============================================================================

class SharedEditor:
    """
    Shared code editor.
    """
    
    def __init__(self, session_id: str, content: str = ""):
        self.session_id = session_id
        self.content = content
        self.version = 0
        self.locks: dict[str, tuple[int, int]] = {}  # user -> (start, end)
        
    def edit(self, user_id: str, start: int, end: int, text: str):
        """Apply edit"""
        # Apply edit to content
        self.content = self.content[:start] + text + self.content[end:]
        self.version += 1
        
        # Record edit
        self.edits.append({
            "user_id": user_id,
            "start": start,
            "end": end,
            "text": text,
            "version": self.version,
        })
        
    def lock(self, user_id: str, start: int, end: int):
        """Lock region"""
        self.locks[user_id] = (start, end)
        
    def unlock(self, user_id: str):
        """Unlock region"""
        self.locks.pop(user_id, None)


# ============================================================================
# COLLABORATION MANAGER
# ============================================================================

class CollaborationManager:
    """
    Manage collaboration.
    """
    
    def __init__(self):
        self.users: dict[str, User] = {}
        self.sessions: dict[str, CollabSession] = {}
        self.presence = Presence()
        self.review_requests: dict[str, ReviewRequest] = {}
        
    def register_user(self, username: str, email: str) -> str:
        """Register user"""
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        user = User(user_id=user_id, username=username, email=email)
        self.users[user_id] = user
        return user_id
        
    def create_session(self, name: str, owner: str) -> str:
        """Create session"""
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        session = CollabSession(session_id, owner)
        self.sessions[session_id] = session
        return session_id
        
    def create_review(
        self, 
        author: str, 
        title: str,
        description: str
    ) -> str:
        """Create review request"""
        request_id = f"review_{uuid.uuid4().hex[:8]}"
        request = ReviewRequest(
            request_id=request_id,
            author=author,
            title=title,
            description=description,
        )
        self.review_requests[request_id] = request
        return request_id


# Global
_collab = None

def get_collaboration() -> CollaborationManager:
    """Get collaboration manager"""
    global _collab
    if _collab is None:
        _collab = CollaborationManager()
    return _collab


__all__ = [
    "UserRole",
    "User",
    "Session",
    "Presence",
    "CollabSession",
    "ReviewRequest",
    "Comment",
    "SharedEditor",
    "CollaborationManager",
    "get_collaboration",
]