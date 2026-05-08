"""
Universe IDE - Kafka Module

Message streaming with Kafka-like API.
"""

from typing import Any, Callable, Dict, List
from collections import deque
import time


# ============================================================================
# TOPIC
# ============================================================================

class Topic:
    """Message topic"""
    
    def __init__(self, name: str):
        self.name = name
        self.messages = deque(maxlen=1000)
        self.subscribers = []
        
    def publish(self, message: Any):
        self.messages.append({
            "data": message,
            "timestamp": time.time(),
        })
        
    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)
        
    def consume(self) -> List:
        messages = list(self.messages)
        self.messages.clear()
        return [m["data"] for m in messages]


# ============================================================================
# PRODUCER
# ============================================================================

class Producer:
    """Message producer"""
    
    def __init__(self):
        self.topics = {}
        
    def create_topic(self, name: str) -> Topic:
        topic = Topic(name)
        self.topics[name] = topic
        return topic
        
    def send(self, topic: str, message: Any):
        if topic in self.topics:
            self.topics[topic].publish(message)
            return True
        return False


# ============================================================================
# CONSUMER
# ============================================================================

class Consumer:
    """Message consumer"""
    
    def __init__(self):
        self.subscriptions = {}
        
    def subscribe(self, topic: str, callback: Callable):
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(callback)
        
    def consume(self, topic: str) -> List:
        return []


# ============================================================================
# STREAMS
# ============================================================================

class StreamProcessor:
    """Process message streams"""
    
    def __init__(self):
        self.pipeline = []
        
    def add_processor(self, func: Callable):
        self.pipeline.append(func)
        
    def process(self, message: Any) -> Any:
        for processor in self.pipeline:
            message = processor(message)
        return message


# Global producer
_producer = None

def get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer()
    return _producer


__all__ = [
    "Topic",
    "Producer", 
    "Consumer",
    "StreamProcessor",
    "get_producer",
]