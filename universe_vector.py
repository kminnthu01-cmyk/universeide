"""
Universe IDE - Vector Database

Vector embeddings for semantic search.
"""

import asyncio
import hashlib
import math
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, List, Optional


# ============================================================================
# VECTOR TYPES
# ============================================================================

@dataclass
class VectorEntry:
    """Vector entry"""
    id: str
    vector: List[float]
    text: str
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SearchResult:
    """Search result"""
    id: str
    score: float
    text: str
    metadata: dict = field(default_factory=dict)


# ============================================================================
# EMBEDDINGS
# ============================================================================

class Embeddings:
    """Generate embeddings"""
    
    # Simple hash-based embeddings (for demo)
    # In production, use actual embeddings from OpenAI, etc.
    
    @staticmethod
    def simple_embed(text: str, dimensions: int = 128) -> List[float]:
        """Generate simple embedding from text"""
        # Use hash to generate deterministic pseudo-random
        h = hashlib.md5(text.encode()).digest()
        
        # Convert to float vector
        vector = []
        for i in range(dimensions):
            byte_idx = i % len(h)
            value = (h[byte_idx] - 128) / 128.0
            vector.append(value)
            
        return vector
        
    @staticmethod
    def random_embed(dimensions: int = 128) -> List[float]:
        """Generate random embedding"""
        return [random.random() * 2 - 1 for _ in range(dimensions)]


# ============================================================================
# VECTOR STORE
# ============================================================================

class VectorStore:
    """Vector database"""
    
    def __init__(self, dimensions: int = 128):
        self.dimensions = dimensions
        self.entries: dict[str, VectorEntry] = {}
        self.index: dict[str, List[str]] = {}  # inverted index
        
    def add(
        self, 
        text: str, 
        embedding: List[float] = None,
        metadata: dict = None,
        id: str = None
    ) -> str:
        """Add vector entry"""
        # Generate ID
        if id is None:
            id = hashlib.md5(text.encode()).hexdigest()[:16]
            
        # Generate embedding
        if embedding is None:
            embedding = Embeddings.simple_embed(text, self.dimensions)
            
        # Create entry
        entry = VectorEntry(
            id=id,
            vector=embedding,
            text=text,
            metadata=metadata or {},
        )
        
        self.entries[id] = entry
        
        # Update index
        words = text.lower().split()
        for word in words[:10]:  # Index first 10 words
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(id)
            
        return id
        
    def get(self, id: str) -> Optional[VectorEntry]:
        """Get entry by ID"""
        return self.entries.get(id)
        
    def search(
        self, 
        query: str, 
        k: int = 5,
        threshold: float = 0.0
    ) -> List[SearchResult]:
        """Semantic search"""
        # Generate query embedding
        query_embedding = Embeddings.simple_embed(query, self.dimensions)
        
        # Calculate similarities
        results = []
        
        for id, entry in self.entries.items():
            similarity = self._cosine_similarity(query_embedding, entry.vector)
            
            if similarity >= threshold:
                results.append(SearchResult(
                    id=id,
                    score=similarity,
                    text=entry.text,
                    metadata=entry.metadata,
                ))
                
        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)
        
        return results[:k]
        
    def search_by_vector(
        self, 
        embedding: List[float], 
        k: int = 5,
        threshold: float = 0.0
    ) -> List[SearchResult]:
        """Search by embedding vector"""
        results = []
        
        for id, entry in self.entries.items():
            similarity = self._cosine_similarity(embedding, entry.vector)
            
            if similarity >= threshold:
                results.append(SearchResult(
                    id=id,
                    score=similarity,
                    text=entry.text,
                    metadata=entry.metadata,
                ))
                
        results.sort(key=lambda r: r.score, reverse=True)
        
        return results[:k]
        
    def _cosine_similarity(
        self, 
        a: List[float], 
        b: List[float]
    ) -> float:
        """Calculate cosine similarity"""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return dot / (norm_a * norm_b)
        
    def delete(self, id: str) -> bool:
        """Delete entry"""
        if id in self.entries:
            del self.entries[id]
            return True
        return False
        
    def count(self) -> int:
        """Count entries"""
        return len(self.entries)


# ============================================================================
# SEMANTIC SEARCH
# ============================================================================

class SemanticSearch:
    """Semantic search over code"""
    
    def __init__(self):
        self.store = VectorStore()
        
    def index_code(self, code: str, file: str = ""):
        """Index code"""
        # Split into chunks
        lines = code.split("\n")
        
        for i, line in enumerate(lines):
            if line.strip() and len(line.strip()) > 10:
                self.store.add(
                    text=line.strip(),
                    metadata={"file": file, "line": i, "type": "code"},
                )
                
    def search_code(self, query: str, k: int = 5) -> List[SearchResult]:
        """Search code"""
        return self.store.search(query, k=k, threshold=0.1)
        
    def similar_code(self, code: str, k: int = 5) -> List[SearchResult]:
        """Find similar code"""
        embedding = Embeddings.simple_embed(code)
        return self.store.search_by_vector(embedding, k=k)


# ============================================================================
# DOCUMENT STORE
# ============================================================================

class DocumentStore:
    """Store and search documents"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.documents: dict[str, str] = {}
        
    def add_document(self, id: str, content: str, metadata: dict = None):
        """Add document"""
        self.documents[id] = content
        self.vector_store.add(content, metadata={"doc_id": id, **(metadata or {})}, id=id)
        
    def get_document(self, id: str) -> Optional[str]:
        """Get document"""
        return self.documents.get(id)
        
    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """Search documents"""
        return self.vector_store.search(query, k=k)
        
    def delete(self, id: str) -> bool:
        """Delete document"""
        if id in self.documents:
            del self.documents[id]
            self.vector_store.delete(id)
            return True
        return False


# ============================================================================
# CODE KNOWLEDGE BASE
# ============================================================================

class CodeKnowledgeBase:
    """Knowledge base with semantic search"""
    
    # Pre-indexed code patterns
    PATTERNS = {
        "api": "async def api_call(url): return await fetch(url)",
        "database": "import sqlite3\nconn = sqlite3.connect('db.sqlite')",
        "logging": "import logging\nlogging.basicConfig(level=logging.INFO)",
        "testing": "import pytest\ndef test_example(): assert True",
        "async": "async def main():\n    await asyncio.gather(*tasks)",
    }
    
    def __init__(self):
        self.doc_store = DocumentStore()
        self._bootstrap()
        
    def _bootstrap(self):
        """Bootstrap with patterns"""
        for name, code in self.PATTERNS.items():
            self.doc_store.add_document(name, code, {"type": "pattern"})
            
    def search(self, query: str) -> List[SearchResult]:
        """Search knowledge base"""
        return self.doc_store.search(query)
        
    def suggest(self, query: str) -> List[str]:
        """Suggest code"""
        results = self.search(query)
        return [r.text for r in results[:3]]


# Global
_kb = None
_vs = None
_ss = None

def get_vector_store() -> VectorStore:
    """Get vector store"""
    global _vs
    if _vs is None:
        _vs = VectorStore()
    return _vs


def get_semantic_search() -> SemanticSearch:
    """Get semantic search"""
    global _ss
    if _ss is None:
        _ss = SemanticSearch()
    return _ss


def get_code_kb() -> CodeKnowledgeBase:
    """Get code knowledge base"""
    global _kb
    if _kb is None:
        _kb = CodeKnowledgeBase()
    return _kb


__all__ = [
    "VectorEntry",
    "SearchResult",
    "Embeddings",
    "VectorStore",
    "SemanticSearch",
    "DocumentStore",
    "CodeKnowledgeBase",
    "get_vector_store",
    "get_semantic_search",
    "get_code_kb",
]