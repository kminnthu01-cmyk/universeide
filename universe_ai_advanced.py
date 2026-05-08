"""
Universe IDE - Advanced AI Engine

State-of-the-art AI with reasoning and planning.
"""

import asyncio
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


# ============================================================================
# REASONING TYPES
# ============================================================================

class ReasoningType(Enum):
    """Reasoning strategies"""
    CHAIN_OF_THOUGHT = "cot"
    TREE_OF_THOUGHT = "tot"
    REFLECTION = "reflection"
    REACT = "react"
    PROMPT_CHAINING = "prompt_chaining"


@dataclass
class ThoughtStep:
    """Single thought step"""
    step: int
    thought: str
    action: str = ""
    observation: str = ""
    result: Any = None


@dataclass
class ReasoningResult:
    """Reasoning result"""
    steps: List[ThoughtStep] = field(default_factory=list)
    final_answer: str = ""
    confidence: float = 0.0
    duration_ms: int = 0


# ============================================================================
# CHAIN OF THOUGHT
# ============================================================================

class ChainOfThought:
    """Chain of Thought reasoning"""
    
    def think(
        self, 
        problem: str, 
        max_steps: int = 10,
        execute_fn: Callable = None
    ) -> ReasoningResult:
        """Perform chain of thought"""
        steps = []
        
        # Parse problem into steps
        sub_problems = self._decompose(problem)
        
        for i, sub in enumerate(sub_problems[:max_steps]):
            step = ThoughtStep(
                step=i + 1,
                thought=f"Analyze: {sub}",
            )
            
            # Execute if function provided
            if execute_fn:
                result = execute_fn(sub)
                step.observation = f"Result: {result}"
                step.result = result
                
            steps.append(step)
            
        # Generate answer
        answer = " | ".join(s.observation for s in steps)
        
        return ReasoningResult(
            steps=steps,
            final_answer=answer,
            confidence=0.8 if steps else 0.0,
        )
        
    def _decompose(self, problem: str) -> List[str]:
        """Decompose problem into sub-problems"""
        # Simple decomposition by sentences
        sentences = re.split(r'[.!?]+', problem)
        return [s.strip() for s in sentences if s.strip()]


# ============================================================================
# TREE OF THOUGHT
# ============================================================================

class TreeOfThought:
    """Tree of Thought exploration"""
    
    def explore(
        self,
        problem: str,
        branches: int = 3,
        depth: int = 3,
        evaluate_fn: Callable = None
    ) -> ReasoningResult:
        """Explore multiple solution paths"""
        steps = []
        
        # Generate branches
        for b in range(branches):
            branch_step = ThoughtStep(
                step=1,
                thought=f"Branch {b+1}: {problem}",
                action=f"explore_branch_{b}",
            )
            
            steps.append(branch_step)
            
        # Evaluate and select best
        if evaluate_fn:
            evaluations = [evaluate_fn(s.thought) for s in steps]
            best = max(range(len(evaluations)), key=lambda i: evaluations[i])
        else:
            best = 0
            
        return ReasoningResult(
            steps=steps,
            final_answer=f"Selected branch {best + 1}",
            confidence=0.7,
        )


# ============================================================================
# REACT ENGINE
# ============================================================================

class ReActEngine:
    """Reasoning + Acting engine"""
    
    def __init__(self):
        self.thought_steps: List[ThoughtStep] = []
        
    async def reasoning_act(
        self,
        user_goal: str,
        available_actions: Dict[str, Callable],
        max_iterations: int = 10
    ) -> ReasoningResult:
        """Execute ReAct loop"""
        goal = user_goal
        self.thought_steps = []
        
        for i in range(max_iterations):
            # Think
            step = ThoughtStep(
                step=i + 1,
                thought=f"Analyze: {goal}",
            )
            
            # Select action
            action_name, action_fn = self._select_action(goal, available_actions)
            
            if not action_name:
                break
                
            step.action = action_name
            
            # Act
            try:
                result = await action_fn(goal)
                step.observation = f"Result: {result}"
                step.result = result
            except Exception as e:
                step.observation = f"Error: {e}"
                
            self.thought_steps.append(step)
            
            # Check if done
            if self._is_complete(result):
                break
                
            # Update goal
            goal = str(result) if result else goal
            
        return ReasoningResult(
            steps=self.thought_steps,
            final_answer=str(self.thought_steps[-1].result) if self.thought_steps else "",
            confidence=0.7,
        )
        
    def _select_action(self, goal: str, actions: Dict[str, Callable]) -> tuple:
        """Select best action"""
        # Simple selection - in production use more sophisticated logic
        for name in actions:
            if name.lower() in goal.lower() or name.lower() in goal.lower():
                return name, actions[name]
        return None, None
        
    def _is_complete(self, result: Any) -> bool:
        """Check if complete"""
        if not result:
            return False
        result_str = str(result).lower()
        complete_markers = ["complete", "done", "finished", "success"]
        return any(m in result_str for m in complete_markers)


# ============================================================================
# PROMPT ENGINEERING
# ============================================================================

class PromptEngine:
    """Advanced prompt engineering"""
    
    TEMPLATES = {
        "analysis": """Analyze the following:
{input}

Think step by step:""",
        
        "code_review": """Review this code:
```{language}
{code}
```

Provide: 1) Issues found, 2) Severity, 3) Suggested fixes""",
        
        "debug": """Debug this error:
{error}

Provide: 1) Root cause, 2) Fix, 3) Prevention""",
        
        "create": """Create a {target} that:
{requirements}

Include best practices and error handling.""",
    }
    
    def build_prompt(
        self,
        template: str,
        **kwargs
    ) -> str:
        """Build prompt from template"""
        if template not in self.TEMPLATES:
            template = "analysis"
            
        prompt = self.TEMPLATES[template]
        
        for key, value in kwargs.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
            
        return prompt
        
    def add_template(self, name: str, template: str):
        """Add custom template"""
        self.TEMPLATES[name] = template
        
    def chain_prompts(self, prompts: List[str]) -> str:
        """Chain multiple prompts"""
        return "\n\n".join(f"Step {i+1}:\n{p}" for i, p in enumerate(prompts))


# ============================================================================
# AI ORCHESTRATOR
# ============================================================================

class AIOrchestrator:
    """Main AI orchestrator with all reasoning strategies"""
    
    def __init__(self):
        self.cot = ChainOfThought()
        self.tot = TreeOfThought()
        self.react = ReActEngine()
        self.prompts = PromptEngine()
        
    async def solve(
        self,
        problem: str,
        strategy: ReasoningType = ReasoningType.CHAIN_OF_THOUGHT,
        **kwargs
    ) -> ReasoningResult:
        """Solve problem with selected strategy"""
        
        if strategy == ReasoningType.CHAIN_OF_THOUGHT:
            return self.cot.think(
                problem,
                max_steps=kwargs.get("max_steps", 10),
                execute_fn=kwargs.get("execute_fn"),
            )
            
        elif strategy == ReasoningType.TREE_OF_THOUGHT:
            return self.tot.explore(
                problem,
                branches=kwargs.get("branches", 3),
                depth=kwargs.get("depth", 3),
                evaluate_fn=kwargs.get("evaluate_fn"),
            )
            
        elif strategy == ReasoningType.REACT:
            return await self.react.reasoning_act(
                problem,
                available_actions=kwargs.get("actions", {}),
                max_iterations=kwargs.get("max_iterations", 10),
            )
            
        else:
            # Default to CoT
            return self.cot.think(problem)
            
    def build_prompt(
        self,
        template: str,
        **kwargs
    ) -> str:
        """Build prompt using template"""
        return self.prompts.build_prompt(template, **kwargs)
        
    def add_prompt_template(self, name: str, template: str):
        """Add custom prompt template"""
        self.prompts.add_template(name, template)


# Global
_ai_orchestrator = None

def get_ai_orchestrator() -> AIOrchestrator:
    """Get AI orchestrator"""
    global _ai_orchestrator
    if _ai_orchestrator is None:
        _ai_orchestrator = AIOrchestrator()
    return _ai_orchestrator


__all__ = [
    "ReasoningType",
    "ThoughtStep",
    "ReasoningResult",
    "ChainOfThought",
    "TreeOfThought",
    "ReActEngine",
    "PromptEngine",
    "AIOrchestrator",
    "get_ai_orchestrator",
]