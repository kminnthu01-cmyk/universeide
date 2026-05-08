"""
Universe IDE - Neural Code Understanding

Deep learning for code comprehension.
"""

import re
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ============================================================================
# CODE TOKENIZER
# ============================================================================

class CodeTokenizer:
    """Neural tokenization of code"""
    
    RESERVED = {
        'python': {'def', 'class', 'if', 'else', 'for', 'while', 'return', 'import', 'from', 'as', 'try', 'except', 'with', 'lambda', 'yield', 'raise', 'pass', 'break', 'continue'},
        'javascript': {'function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'import', 'export', 'class', 'async', 'await', 'try', 'catch'},
    }
    
    def tokenize(self, code: str, language: str = 'python') -> List[str]:
        """Tokenize code into neural tokens"""
        tokens = []
        
        # Split by whitespace and operators
        pattern = r'[\w_]+|[+\-*/=<>(){}[\],.:;@#]+'
        matches = re.findall(pattern, code)
        
        reserved = self.RESERVED.get(language, set())
        
        for match in matches:
            # Check if reserved word
            if match.lower() in reserved:
                tokens.append(f'KEYWORD:{match}')
            # Check if number
            elif match.isdigit():
                tokens.append(f'NUMBER:{match}')
            # Check if string
            elif match.startswith('"') or match.startswith("'"):
                tokens.append('STRING')
            # Check if comment
            elif match.startswith('#') or match.startswith('//'):
                tokens.append('COMMENT')
            else:
                tokens.append(f'IDENTIFIER:{match}')
                
        return tokens
    
    def encode(self, code: str) -> List[int]:
        """Encode to integer IDs"""
        tokens = self.tokenize(code)
        
        # Build vocabulary
        vocab = {}
        for token in tokens:
            if token not in vocab:
                vocab[token] = len(vocab)
                
        return [vocab[t] for t in tokens]


# ============================================================================
# CODE EMBEDDING
# ============================================================================

class CodeEmbedding:
    """Neural embeddings for code"""
    
    def __init__(self, dimensions: int = 128):
        self.dimensions = dimensions
        self.embeddings = {}
        
    def embed_token(self, token: str) -> List[float]:
        """Generate embedding for token"""
        # Simple hash-based embedding
        h = hashlib.md5(token.encode()).digest()
        
        embedding = []
        for i in range(self.dimensions):
            byte_idx = i % len(h)
            value = (h[byte_idx] - 128) / 128.0
            embedding.append(value)
            
        return embedding
    
    def embed_code(self, code: str) -> List[float]:
        """Embed entire code"""
        tokens = CodeTokenizer().tokenize(code)
        
        # Average embeddings
        if not tokens:
            return [0.0] * self.dimensions
            
        embeddings = [self.embed_token(t) for t in tokens]
        
        # Mean pooling
        return [
            sum(e[i] for e in embeddings) / len(embeddings)
            for i in range(self.dimensions)
        ]
    
    def similar(self, code1: str, code2: str) -> float:
        """Calculate code similarity"""
        e1 = self.embed_code(code1)
        e2 = self.embed_code(code2)
        
        # Cosine similarity
        dot = sum(a * b for a, b in zip(e1, e2))
        mag1 = sum(a * a for a in e1) ** 0.5
        mag2 = sum(b * b for b in e2) ** 0.5
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
            
        return dot / (mag1 * mag2)


# ============================================================================
# CODE UNDERSTANDING
# ============================================================================

class CodeUnderstanding:
    """Neural code comprehension"""
    
    def __init__(self):
        self.tokenizer = CodeTokenizer()
        self.embedding = CodeEmbedding()
        
    def analyze(self, code: str) -> dict:
        """Deep code analysis"""
        tokens = self.tokenizer.tokenize(code)
        
        # Count patterns
        keywords = [t for t in tokens if t.startswith('KEYWORD:')]
        identifiers = [t for t in tokens if t.startswith('IDENTIFIER:')]
        strings = [t for t in tokens if t.startswith('STRING:')]
        
        return {
            'tokens': len(tokens),
            'keywords': len(keywords),
            'identifiers': len(identifiers),
            'strings': len(strings),
            'unique_tokens': len(set(tokens)),
            'complexity': self._calculate_complexity(code),
        }
    
    def _calculate_complexity(self, code: str) -> float:
        """Calculate neural complexity"""
        # Factors
        lines = len(code.split('\n'))
        nesting = max(code.count('{'), code.count('('), code.count('['))
        loops = code.lower().count('for ') + code.lower().count('while ')
        conditionals = code.lower().count('if ')
        
        # Neural score
        complexity = (lines * 0.1) + (nesting * 0.2) + (loops * 0.3) + (conditionals * 0.4)
        
        return min(1.0, complexity / 10.0)
    
    def predict_intent(self, code: str) -> str:
        """Predict code intent"""
        code_lower = code.lower()
        
        if 'def ' in code_lower and 'return' in code_lower:
            return 'function_definition'
        elif 'for ' in code_lower or 'while ' in code_lower:
            return 'iteration'
        elif 'if ' in code_lower:
            return 'conditional'
        elif 'class ' in code_lower:
            return 'class_definition'
        elif 'import ' in code_lower:
            return 'import_module'
        else:
            return 'general_code'
    
    def find_patterns(self, code: str) -> List[str]:
        """Find common patterns"""
        patterns = []
        
        # Check for common patterns
        if re.search(r'def \w+\([^)]*\):', code):
            patterns.append('function')
        if re.search(r'class \w+:', code):
            patterns.append('class')
        if re.search(r'for \w+ in \w+:', code):
            patterns.append('for_loop')
        if re.search(r'if \w+ ==', code):
            patterns.append('comparison')
        if re.search(r'try:', code):
            patterns.append('error_handling')
        if re.search(r'async def', code):
            patterns.append('async')
            
        return patterns


# ============================================================================
# SEMANTIC ANALYSIS
# ============================================================================

class SemanticAnalyzer:
    """Semantic code analysis"""
    
    def __init__(self):
        self.understanding = CodeUnderstanding()
        
    def analyze(self, code: str) -> dict:
        """Full semantic analysis"""
        understanding = self.understanding.analyze(code)
        intent = self.understanding.predict_intent(code)
        patterns = self.understanding.find_patterns(code)
        
        return {
            'understanding': understanding,
            'intent': intent,
            'patterns': patterns,
            'suggestions': self._get_suggestions(intent, patterns),
        }
    
    def _get_suggestions(self, intent: str, patterns: List[str]) -> List[str]:
        """Get AI suggestions"""
        suggestions = []
        
        if intent == 'function_definition':
            suggestions.append('Consider adding type hints')
            suggestions.append('Add docstring')
        elif intent == 'iteration':
            suggestions.append('Consider list comprehension for brevity')
        elif intent == 'conditional':
            suggestions.append('Consider match statement (Python 3.10+)')
            
        return suggestions


# Global
_neural = None

def get_neural_ai() -> SemanticAnalyzer:
    """Get neural ai"""
    global _neural
    if _neural is None:
        _neural = SemanticAnalyzer()
    return _neural


__all__ = [
    "CodeTokenizer",
    "CodeEmbedding", 
    "CodeUnderstanding",
    "SemanticAnalyzer",
    "get_neural_ai",
]