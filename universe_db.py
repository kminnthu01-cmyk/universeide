"""
Universe IDE - Database Layer v2

Database layer with SQL + cache.
"""

import asyncio
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ============================================================================
# DATABASE TYPES
# ============================================================================

class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    REDIS = "redis"


# ============================================================================
# SQLITE MANAGER
# ============================================================================

class SQLiteDB:
    """SQLite database"""
    
    def __init__(self, db_path: str = "universe.db"):
        self.db_path = db_path
        self._init()
        
    def _init(self):
        """Initialize schema"""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Agents
        cur.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                config TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Messages
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                sender_id TEXT,
                recipient_id TEXT,
                content TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # Knowledge
        cur.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                key TEXT PRIMARY KEY,
                value TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    @contextmanager
    def transaction(self):
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def insert(self, table: str, data: dict) -> bool:
        cols = ", ".join(data.keys())
        ph = ", ".join(["?"] * len(data))
        sql = f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})"
        with self.transaction() as conn:
            conn.execute(sql, list(data.values()))
        return True
    
    def select(self, table: str, where: str = "", params: tuple = ()) -> list:
        sql = f"SELECT * FROM {table}"
        if where:
            sql += f" WHERE {where}"
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        cols = [c[0] for c in cur.description] if cur.description else []
        results = [dict(zip(cols, row)) for row in cur.fetchall()]
        conn.close()
        return results


# ============================================================================
# CACHE
# ============================================================================

class Cache:
    """In-memory cache"""
    
    def __init__(self):
        self._store = {}
    
    def get(self, key: str):
        return self._store.get(key)
    
    def set(self, key: str, value, ttl: int = 0):
        self._store[key] = value
    
    def delete(self, key: str):
        if key in self._store:
            del self._store[key]
    
    def keys(self):
        return list(self._store.keys())


# ============================================================================
# REPOSITORIES
# ============================================================================

class AgentRepo:
    """Agent repository"""
    
    def __init__(self, db: SQLiteDB):
        self.db = db
    
    def save(self, agent: dict):
        agent["created_at"] = datetime.now().isoformat()
        self.db.insert("agents", agent)
        return agent
    
    def get(self, agent_id: str):
        results = self.db.select("agents", "id = ?", (agent_id,))
        return results[0] if results else None
    
    def all(self):
        return self.db.select("agents")


class MessageRepo:
    """Message repository"""
    
    def __init__(self, db: SQLiteDB):
        self.db = db
    
    def send(self, sender: str, recipient: str, content: str):
        import uuid
        self.db.insert("messages", {
            "id": uuid.uuid4().hex[:16],
            "sender_id": sender,
            "recipient_id": recipient,
            "content": content,
            "created_at": datetime.now().isoformat(),
        })
    
    def inbox(self, recipient_id: str):
        return self.db.select("messages", "recipient_id = ?", (recipient_id,))


class KnowledgeRepo:
    """Knowledge repository"""
    
    def __init__(self, db: SQLiteDB):
        self.db = db
    
    def store(self, key: str, value):
        if not isinstance(value, str):
            value = json.dumps(value)
        self.db.insert("knowledge", {
            "key": key,
            "value": value,
            "created_at": datetime.now().isoformat(),
        })
    
    def retrieve(self, key: str):
        results = self.db.select("knowledge", "key = ?", (key,))
        if results:
            try:
                return json.loads(results[0]["value"])
            except:
                return results[0]["value"]
        return None
    
    def search(self, query: str):
        return self.db.select("knowledge", f"key LIKE '%{query}%'")


# Global instances
_db = None
_cache = None

def get_database() -> SQLiteDB:
    global _db
    if _db is None:
        _db = SQLiteDB()
    return _db

def get_cache() -> Cache:
    global _cache
    if _cache is None:
        _cache = Cache()
    return _cache


__all__ = [
    "DatabaseType",
    "SQLiteDB",
    "Cache",
    "AgentRepo",
    "MessageRepo",
    "KnowledgeRepo",
    "get_database",
    "get_cache",
]