"""
Universe IDE - Self-Learning AI

AI that learns from interactions and improves over time.
"""

import asyncio
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# LEARNING TYPES
# ============================================================================

@dataclass
class Interaction:
    """Interaction record"""
    input: str
    output: Any
    quality: float = 0.0  # 0-1
    feedback: float = 0.0  # -1 to 1
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class LearnedPattern:
    """Learned pattern"""
    pattern: str
    response: str
    occurrences: int = 1
    success_rate: float = 0.5
    last_used: datetime = field(default_factory=datetime.now)


# ============================================================================
# PATTERN LEARNER
# ============================================================================

class PatternLearner:
    """Learn from interactions"""
    
    def __init__(self, min_occurrences: int = 3):
        self.min_occurrences = min_occurrences
        self.interactions: List[Interaction] = []
        self.patterns: Dict[str, LearnedPattern] = {}
        self.word_counts: Counter = Counter()
        
    def observe(self, input_text: str, output: Any, quality: float = 0.5):
        """Record interaction"""
        interaction = Interaction(
            input=input_text,
            output=output,
            quality=quality,
        )
        
        self.interactions.append(interaction)
        
        # Update word counts
        words = re.findall(r'\w+', input_text.lower())
        self.word_counts.update(words)
        
        # Keep only last 1000
        self.interactions = self.interactions[-1000:]
        
    def learn(self) -> List[LearnedPattern]:
        """Extract patterns from interactions"""
        patterns = []
        
        # Group similar inputs
        for i, interaction in enumerate(self.interactions):
            words = set(re.findall(r'\w+', interaction.input.lower()))
            
            # Find common words
            common = self.word_counts.most_common(20)
            keywords = {w for w, _ in common if _ >= self.min_occurrences}
            
            # Extract pattern
            relevant_words = words & keywords
            
            if relevant_words:
                pattern_key = " ".join(sorted(relevant_words))
                
                if pattern_key in self.patterns:
                    p = self.patterns[pattern_key]
                    p.occurrences += 1
                    p.success_rate = (
                        p.success_rate * (p.occurrences - 1) + interaction.quality
                    ) / p.occurrences
                else:
                    self.patterns[pattern_key] = LearnedPattern(
                        pattern=pattern_key,
                        response=str(interaction.output),
                    )
                    
        # Return high-success patterns
        learned = [
            p for p in self.patterns.values()
            if p.occurrences >= self.min_occurrences and p.success_rate > 0.7
        ]
        
        return learned
        
    def get_response(self, input_text: str) -> Optional[str]:
        """Get learned response"""
        words = set(re.findall(r'\w+', input_text.lower()))
        
        best_match = None
        best_score = 0
        
        for pattern in self.patterns.values():
            pattern_words = set(pattern.pattern.split())
            
            # Jaccard similarity
            intersection = len(words & pattern_words)
            union = len(words | pattern_words)
            score = intersection / union if union > 0 else 0
            
            if score > best_score:
                best_score = score
                best_match = pattern
                
        if best_match and best_score > 0.3:
            return best_match.response
            
        return None


# ============================================================================
# FEEDBACK LOOP
# ============================================================================

class FeedbackLoop:
    """Collect and process feedback"""
    
    def __init__(self):
        self.feedback: List[dict] = []
        
    def collect(self, interaction_id: str, rating: float, comment: str = ""):
        """Collect feedback"""
        self.feedback.append({
            "interaction_id": interaction_id,
            "rating": rating,  # -1 to 1
            "comment": comment,
            "timestamp": datetime.now(),
        })
        
    def analyze(self) -> dict:
        """Analyze feedback trends"""
        if not self.feedback:
            return {"count": 0, "avg_rating": 0}
            
        ratings = [f["rating"] for f in self.feedback]
        
        return {
            "count": len(self.feedback),
            "avg_rating": sum(ratings) / len(ratings),
            "positive": sum(1 for r in ratings if r > 0),
            "negative": sum(1 for r in ratings if r < 0),
            "neutral": sum(1 for r in ratings if r == 0),
        }


# ============================================================================
# ADAPTIVE MODEL
# ============================================================================

class AdaptiveModel:
    """Model that adapts to user"""
    
    def __init__(self):
        self.learner = PatternLearner()
        self.feedback = FeedbackLoop()
        self.user_preferences: Dict[str, Any] = {}
        self.conversation_history: List[dict] = []
        
    def process(self, input_text: str) -> str:
        """Process input with learning"""
        # Check for learned response
        learned = self.learner.get_response(input_text)
        
        if learned:
            return learned
            
        # Default response indicator
        return "[process with AI model]"
        
    def update(self, input_text: str, output: Any, quality: float, feedback: float = None):
        """Update model with interaction"""
        # Record for pattern learning
        self.learner.observe(input_text, output, quality)
        
        # Extract and learn patterns
        self.learner.learn()
        
        # Collect feedback if provided
        if feedback is not None:
            self.feedback.collect(input_text, feedback)
            
    def get_stats(self) -> dict:
        """Get learning stats"""
        patterns = self.learner.learn()
        
        return {
            "patterns_learned": len(patterns),
            "interactions": len(self.learner.interactions),
            "unique_words": len(self.learner.word_counts),
            "feedback": self.feedback.analyze(),
        }


# ============================================================================
# CONTINUOUS IMPROVER
# ============================================================================

class ContinuousImprover:
    """Continuously improve based on results"""
    
    def __init__(self):
        self.model = AdaptiveModel()
        self.successes = 0
        self.failures = 0
        
    def record_success(self, task: str, approach: str):
        """Record successful approach"""
        self.successes += 1
        self._save_approach(task, approach, True)
        
    def record_failure(self, task: str, approach: str):
        """Record failed approach"""
        self.failures += 1
        self._save_approach(task, approach, False)
        
    def _save_approach(self, task: str, approach: str, success: bool):
        """Save approach heuristic"""
        # In production, store to database
        pass
        
    def suggest_improvement(self, task: str) -> str:
        """Suggest improvement for task type"""
        success_rate = self.successes / (self.successes + self.failures) if (self.successes + self.failures) > 0 else 0
        
        if success_rate > 0.9:
            return "Current approach highly effective"
        elif success_rate > 0.7:
            return "Consider parallel processing"
        else:
            return "Need to revise approach"


# ============================================================================
# CONTEXT MANAGER
# ============================================================================

class ContextManager:
    """Manage conversation context"""
    
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.context: List[dict] = []
        
    def add(self, role: str, content: str, metadata: dict = None):
        """Add to context"""
        self.context.append({
            "role": role,  # "user" or "assistant"
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now(),
        })
        
        # Keep max
        if len(self.max_history) < self.max_history:
            self.context = self.context[-self.max_history:]
            
    def get_context(self, max_turns: int = 5) -> List[dict]:
        """Get recent context"""
        return self.context[-max_turns:]
        
    def get_summary(self) -> str:
        """Get context summary"""
        if not self.context:
            return ""
            
        recent = self.context[-5:]
        return " | ".join(f"{c['role']}: {c['content'][:50]}" for c in recent)


# ============================================================================
# INTELLIGENT CACHE
# ============================================================================

class IntelligentCache:
    """Cache with learning"""
    
    def __init__(self):
        self.cache: Dict[str, dict] = {}
        self.access_counts: Counter = Counter()
        self.temporal_patterns: Dict[str, str] = {}  # hourly patterns
        
    def get(self, key: str) -> Optional[Any]:
        """Get from cache"""
        if key in self.cache:
            entry = self.cache[key]
            entry["hits"] += 1
            self.access_counts[key] += 1
            return entry["value"]
            
        return None
        
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set cache"""
        self.cache[key] = {
            "value": value,
            "hits": 0,
            "created": datetime.now(),
            "ttl": ttl,
        }
        
    def get_popular(self, n: int = 5) -> List[tuple]:
        """Get most popular keys"""
        return self.access_counts.most_common(n)


# Global
_improver = None

def get_self_learning_ai() -> ContinuousImprover:
    """Get self-learning AI"""
    global _improver
    if _improver is None:
        _improver = ContinuousImprover()
    return _improver


__all__ = [
    "Interaction",
    "LearnedPattern",
    "PatternLearner",
    "FeedbackLoop",
    "AdaptiveModel",
    "ContinuousImprover",
    "ContextManager",
    "IntelligentCache",
    "get_self_learning_ai",
]