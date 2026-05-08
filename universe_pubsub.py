"""
Universe IDE - Pub/Sub Module

Publish-subscribe messaging.
"""

from typing import Any, Callable, Dict, List
from collections import defaultdict


# ============================================================================
# TOPIC
# ============================================================================

class PubSubTopic:
    """Pub/Sub topic"""
    
    def __init__(self, name: str):
        self.name = name
        self.subscribers = []
        
    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)
        
    def publish(self, message: Any):
        for sub in self.subscribers:
            sub(message)


# ============================================================================
# PUBSUB
# ============================================================================

class PubSub:
    """Pub/Sub broker"""
    
    def __init__(self):
        self.topics = defaultdict(PubSubTopic)
        
    def create_topic(self, name: str) -> PubSubTopic:
        topic = PubSubTopic(name)
        self.topics[name] = topic
        return topic
        
    def publish(self, topic: str, message: Any):
        if topic in self.topics:
            self.topics[topic].publish(message)
            
    def subscribe(self, topic: str, callback: Callable):
        if topic not in self.topics:
            self.create_topic(topic)
        self.topics[topic].subscribe(callback)


# Global
_ps = None

def get_pubsub() -> PubSub:
    global _ps
    if _ps is None:
        _ps = PubSub()
    return _ps


__all__ = ["PubSubTopic", "PubSub", "get_pubsub"]