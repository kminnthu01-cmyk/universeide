"""
Universe IDE - GraphQL API

GraphQL schema and resolvers for Universe IDE.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, List, Optional


# ============================================================================
# GRAPHQL TYPES
# ============================================================================

@dataclass
class GraphQLAgent:
    """GraphQL Agent type"""
    id: str
    name: str
    status: str = "idle"
    config: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GraphQLMessage:
    """GraphQL Message type"""
    id: str
    content: str
    sender_id: str
    recipient_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False


@dataclass
class GraphQLKnowledge:
    """GraphQL Knowledge type"""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class GraphQLTask:
    """GraphQL Task type"""
    id: str
    name: str
    status: str = "pending"
    result: Any = None
    created_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# GRAPHQL SCHEMA
# ============================================================================

class GraphQLSchema:
    """GraphQL schema definition"""
    
    # Type definitions
    TYPES = """
    type Agent {
        id: ID!
        name: String!
        status: String!
        config: JSON
        createdAt: String!
    }
    
    type Message {
        id: ID!
        content: String!
        senderId: String!
        recipientId: String!
        timestamp: String!
        read: Boolean!
    }
    
    type Knowledge {
        key: String!
        value: JSON!
        createdAt: String!
        updatedAt: String!
    }
    
    type Task {
        id: ID!
        name: String!
        status: String!
        result: JSON
        createdAt: String!
    }
    
    type Query {
        # Agent queries
        agents(status: String): [Agent!]!
        agent(id: ID!): Agent
        
        # Message queries
        messages(agentId: ID!): [Message!]!
        message(id: ID!): Message
        
        # Knowledge queries
        knowledge(key: String!): Knowledge
        allKnowledge: [Knowledge!]!
        
        # Task queries
        tasks(status: String): [Task!]!
        task(id: ID!): Task
    }
    
    type Mutation {
        # Agent mutations
        createAgent(name: String!, config: JSON): Agent!
        updateAgent(id: ID!, config: JSON): Agent!
        deleteAgent(id: ID!): Boolean!
        
        # Message mutations  
        sendMessage(content: String!, recipientId: ID!): Message!
        markMessageRead(id: ID!): Message!
        
        # Knowledge mutations
        storeKnowledge(key: String!, value: JSON!): Knowledge!
        deleteKnowledge(key: String!): Boolean!
        
        # Task mutations
        createTask(name: String!): Task!
        executeTask(id: ID!): Task!
        cancelTask(id: ID!): Task!
    }
    
    type Subscription {
        agentStatusUpdated(id: ID!): Agent!
        messageReceived(agentId: ID!): Message!
        taskCompleted(id: ID!): Task!
    }
    """
    
    # Resolvers
    def resolve_agents(self, info, status: str = None) -> List[GraphQLAgent]:
        """Query: Get all agents"""
        from universe_ide import cosmos
        universe = cosmos(10)
        
        return [
            GraphQLAgent(
                id=f"agent-{i}",
                name=f"Agent {i}",
                status=status or "idle",
            )
            for i in range(universe.num_agents)
        ]
        
    def resolve_agent(self, info, id: str) -> Optional[GraphQLAgent]:
        """Query: Get single agent"""
        return GraphQLAgent(id=id, name=f"Agent {id}")
        
    def resolve_messages(self, info, agent_id: str) -> List[GraphQLMessage]:
        """Query: Get messages for agent"""
        from universe_messaging import get_message_bus
        bus = get_message_bus()
        return bus.get_inbox(agent_id)
        
    def resolve_knowledge(self, info, key: str) -> Optional[GraphQLKnowledge]:
        """Query: Get knowledge by key"""
        from universe_memory import get_knowledge_base
        kb = get_knowledge_base()
        value = kb.retrieve(key)
        
        if value:
            return GraphQLKnowledge(key=key, value=value)
        return None
        
    def resolve_tasks(self, info, status: str = None) -> List[GraphQLTask]:
        """Query: Get all tasks"""
        from universe_queue import get_task_queue
        queue = get_task_queue()
        # Return some sample tasks
        return [
            GraphQLTask(id=f"task-{i}", name=f"Task {i}", status=status or "pending")
            for i in range(5)
        ]
        
    # Mutation resolvers
    def resolve_create_agent(self, info, name: str, config: dict = None) -> GraphQLAgent:
        """Mutation: Create agent"""
        return GraphQLAgent(
            id=f"agent-{datetime.now().timestamp()}",
            name=name,
            config=config or {},
        )
        
    def resolve_send_message(
        self, 
        info, 
        content: str, 
        recipient_id: str
    ) -> GraphQLMessage:
        """Mutation: Send message"""
        from universe_messaging import get_message_bus
        bus = get_message_bus()
        
        msg = bus.create_message(content, recipient_id)
        bus.send(msg)
        
        return msg
        
    def resolve_store_knowledge(
        self, 
        info, 
        key: str, 
        value: Any
    ) -> GraphQLKnowledge:
        """Mutation: Store knowledge"""
        from universe_memory import get_knowledge_base
        kb = get_knowledge_base()
        kb.store(key, value)
        
        return GraphQLKnowledge(key=key, value=value)
        
    def resolve_create_task(self, info, name: str) -> GraphQLTask:
        """Mutation: Create task"""
        return GraphQLTask(
            id=f"task-{datetime.now().timestamp()}",
            name=name,
        )


# ============================================================================
# GRAPHQL EXECUTOR
# ============================================================================

class GraphQLExecutor:
    """Execute GraphQL queries"""
    
    def __init__(self):
        self.schema = GraphQLSchema()
        self.resolvers = self._build_resolvers()
        
    def _build_resolvers(self) -> dict:
        """Build resolver map"""
        return {
            "Query": {
                "agents": self.schema.resolve_agents,
                "agent": self.schema.resolve_agent,
                "messages": self.schema.resolve_messages,
                "knowledge": self.schema.resolve_knowledge,
                "tasks": self.schema.resolve_tasks,
            },
            "Mutation": {
                "createAgent": self.schema.resolve_create_agent,
                "sendMessage": self.schema.resolve_send_message,
                "storeKnowledge": self.schema.resolve_store_knowledge,
                "createTask": self.schema.resolve_create_task,
            },
        }
        
    def execute(self, query: str, variables: dict = None) -> dict:
        """Execute GraphQL query"""
        # Simple query parsing (for demo)
        # In production, use graphql-core
        
        if "query {" in query and "agents" in query:
            return {"data": {"agents": self.schema.resolve_agents(None)}}
            
        if "query {" in query and "knowledge" in query:
            key = variables.get("key", "default") if variables else "default"
            return {"data": {"knowledge": self.schema.resolve_knowledge(None, key)}}
            
        if "mutation {" in query and "createAgent" in query:
            name = variables.get("name", "NewAgent") if variables else "NewAgent"
            return {"data": {"createAgent": self.schema.resolve_create_agent(None, name)}}
            
        return {"data": {}}
        
    def introspect(self) -> dict:
        """Introspect schema"""
        return {
            "data": {
                "__schema": {
                    "types": [
                        {"name": "Agent"},
                        {"name": "Message"},
                        {"name": "Knowledge"},
                        {"name": "Task"},
                    ]
                }
            }
        }


# ============================================================================
# GRAPHQL SERVER
# ============================================================================

class GraphQLServer:
    """GraphQL HTTP server"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 4000):
        self.host = host
        self.port = port
        self.executor = GraphQLExecutor()
        
    async def handle(self, query: str, variables: dict = None) -> dict:
        """Handle GraphQL request"""
        return self.executor.execute(query, variables)
        
    async def start(self):
        """Start server"""
        print(f"🔵 GraphQL Server: http://{self.host}:{self.port}/graphql")
        print(f"   Playground: http://{self.host}:{self.port}/")


# Global
_graphql = None

def get_graphql() -> GraphQLExecutor:
    """Get GraphQL executor"""
    global _graphql
    if _graphql is None:
        _graphql = GraphQLExecutor()
    return _graphql


__all__ = [
    "GraphQLAgent",
    "GraphQLMessage", 
    "GraphQLKnowledge",
    "GraphQLTask",
    "GraphQLSchema",
    "GraphQLExecutor",
    "GraphQLServer",
    "get_graphql",
]