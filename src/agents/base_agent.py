"""
Base Agent Class for AI Swarm IDE
Provides common functionality for all agent types
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import uuid
from datetime import datetime

from rich.console import Console
from rich.panel import Panel

console = Console()

@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    agent_type: str
    capabilities: List[str]
    max_concurrent_tasks: int = 1
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000

class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.id = str(uuid.uuid4())
        self.status = "idle"
        self.current_task: Optional[str] = None
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "average_response_time": 0.0,
            "total_response_time": 0.0
        }
        self.console = Console()
        
        # Task processing
        self.task_queue: List[str] = []
        self.processing = False
        
        # Logging
        self.logger = logging.getLogger(f"agent.{config.name}")
        self.logger.setLevel(logging.INFO)
    
    @abstractmethod
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Check if this agent can handle a specific task"""
        pass
    
    async def start(self):
        """Start the agent"""
        self.status = "idle"
        self.processing = True
        self.console.print(f"[blue]🤖 Agent {self.config.name} started[/blue]")
        
        # Start task processing loop
        asyncio.create_task(self._task_processor())
    
    async def stop(self):
        """Stop the agent"""
        self.processing = False
        self.status = "stopped"
        self.console.print(f"[yellow]🛑 Agent {self.config.name} stopped[/yellow]")
    
    async def _task_processor(self):
        """Main task processing loop"""
        while self.processing:
            if self.task_queue and self.status == "idle":
                task_id = self.task_queue.pop(0)
                await self._execute_task(task_id)
            
            await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
    
    async def _execute_task(self, task_id: str):
        """Execute a specific task"""
        try:
            self.status = "busy"
            self.current_task = task_id
            
            # Get task data (in real implementation, this would come from orchestrator)
            task_data = {"task_id": task_id, "status": "processing"}
            
            start_time = datetime.now()
            
            # Process the task
            result = await self.process_task(task_data)
            
            # Calculate response time
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            # Update performance metrics
            self._update_metrics(response_time, success=True)
            
            self.console.print(f"[green]✅ Task {task_id} completed by {self.config.name}[/green]")
            
        except Exception as e:
            self.logger.error(f"Error processing task {task_id}: {e}")
            self._update_metrics(0.0, success=False)
            self.console.print(f"[red]❌ Task {task_id} failed: {e}[/red]")
        
        finally:
            self.status = "idle"
            self.current_task = None
    
    def _update_metrics(self, response_time: float, success: bool):
        """Update agent performance metrics"""
        if success:
            self.performance_metrics["tasks_completed"] += 1
        else:
            self.performance_metrics["tasks_failed"] += 1
        
        # Update average response time
        total_time = self.performance_metrics["total_response_time"] + response_time
        total_tasks = self.performance_metrics["tasks_completed"] + self.performance_metrics["tasks_failed"]
        
        if total_tasks > 0:
            self.performance_metrics["average_response_time"] = total_time / total_tasks
            self.performance_metrics["total_response_time"] = total_time
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "id": self.id,
            "name": self.config.name,
            "agent_type": self.config.agent_type,
            "capabilities": self.config.capabilities,
            "status": self.status,
            "current_task": self.current_task,
            "performance_metrics": self.performance_metrics.copy(),
            "queue_length": len(self.task_queue)
        }
    
    def add_task(self, task_id: str):
        """Add a task to the agent's queue"""
        if len(self.task_queue) < self.config.max_concurrent_tasks:
            self.task_queue.append(task_id)
            self.console.print(f"[cyan]📥 Task {task_id} added to {self.config.name}[/cyan]")
            return True
        return False
    
    def is_available(self) -> bool:
        """Check if the agent is available for new tasks"""
        return (self.status == "idle" and 
                len(self.task_queue) < self.config.max_concurrent_tasks and
                not self.current_task)
    
    async def health_check(self) -> bool:
        """Perform a health check on the agent"""
        try:
            # Basic health check - could be extended with model availability checks
            return self.status in ["idle", "busy"] and self.processing
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False
    
    def get_capabilities_summary(self) -> str:
        """Get a human-readable summary of agent capabilities"""
        return f"{self.config.name} ({self.config.agent_type}): {', '.join(self.config.capabilities)}"
