"""
Universe IDE - Vector Store Module

Vector database for embeddings.
"""

from typing import Any, Dict, List, Tuple
import math
import random


# ============================================================================
# VECTOR
# ============================================================================

class Vector:
    """Embedding vector"""
    
    def __init__(self, values: List[float]):
        self.values = values
        self.dim = len(values)
        
    def cosine_similarity(self, other: "Vector") -> float:
        """Cosine similarity"""
        dot = sum(a * b for a, b in zip(self.values, other.values))
        mag1 = math.sqrt(sum(a * a for a in self.values))
        mag2 = math.sqrt(sum(a * a for a in other.values))
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot / (mag1 * mag2)
        
    def euclidean(self, other: "Vector") -> float:
        """Euclidean distance"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.values, other.values)))


# ============================================================================
# DOCUMENT
# ============================================================================

class Document:
    """Text document with embedding"""
    
    def __init__(self, doc_id: str, text: str, embedding: Vector = None):
        self.doc_id = doc_id
        self.text = text
        self.embedding = embedding or Vector([random.random() for _ in range(128)])
        self.metadata = {}
        
    def get_embedding(self) -> Vector:
        return self.embedding


# ============================================================================
# VECTOR STORE
# ============================================================================

class VectorStore:
    """Vector database"""
    
    def __init__(self, dimension: int = 128):
        self.dimension = dimension
        self.documents = {}
        
    def add(self, doc: Document):
        self.documents[doc.doc_id] = doc
        
    def search(self, query: Vector, top_k: int = 5) -> List[Tuple[Document, float]]:
        results = []
        for doc in self.documents.values():
            sim = query.cosine_similarity(doc.embedding)
            results.append((doc, sim))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
        
    def delete(self, doc_id: str):
        if doc_id in self.documents:
            del self.documents[doc_id]
            
    def count(self) -> int:
        return len(self.documents)


# ============================================================================
# RETRIEVER
# ============================================================================

class Retriever:
    """Retriever for RAG"""
    
    def __init__(self):
        self.store = VectorStore()
        
    def index(self, documents: List[Document]):
        for doc in documents:
            self.store.add(doc)
            
    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        query_vec = Vector([random.random() for _ in range(128)])
        results = self.store.search(query_vec, top_k)
        return [doc for doc, _ in results]


# Global instance
_store = None

def get_vector_store() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore()
    return _store


def get_retriever() -> Retriever:
    return Retriever()


__all__ = ["Vector", "Document", "VectorStore", "Retriever", "get_vector_store", "get_retriever"]