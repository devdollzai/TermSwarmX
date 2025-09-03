"""
Central Orchestrator for AI Swarm IDE
Manages agent lifecycle, task distribution, and swarm coordination
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

console = Console()

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Task:
    id: str
    title: str
    description: str
    agent_type: str
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None

@dataclass
class Agent:
    id: str
    name: str
    agent_type: str
    capabilities: List[str]
    status: str
    performance_metrics: Dict[str, float]
    current_task: Optional[str] = None

class SwarmOrchestrator:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
        self.running = False
        self.console = Console()
        
        # Performance tracking
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_agents": 0,
            "active_agents": 0
        }
    
    async def start(self):
        """Start the swarm orchestrator"""
        self.running = True
        self.console.print("[bold green]🚀 AI Swarm IDE Orchestrator Started[/bold green]")
        
        # Start background tasks
        asyncio.create_task(self._task_scheduler())
        asyncio.create_task(self._health_monitor())
        asyncio.create_task(self._performance_tracker())
    
    async def stop(self):
        """Stop the swarm orchestrator"""
        self.running = False
        self.console.print("[bold red]🛑 AI Swarm IDE Orchestrator Stopped[/bold red]")
    
    def register_agent(self, agent: Agent) -> bool:
        """Register a new agent with the swarm"""
        if agent.id in self.agents:
            return False
        
        self.agents[agent.id] = agent
        self.stats["total_agents"] += 1
        self.stats["active_agents"] += 1
        
        self.console.print(f"[blue]🤖 Agent registered: {agent.config.name} ({agent.config.agent_type})[/blue]")
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the swarm"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        if agent.current_task:
            self._reassign_task(agent.current_task)
        
        del self.agents[agent_id]
        self.stats["active_agents"] -= 1
        
        self.console.print(f"[yellow]👋 Agent unregistered: {agent.config.name}[/yellow]")
        return True
    
    def submit_task(self, title: str, description: str, agent_type: str, 
                   priority: TaskPriority = TaskPriority.NORMAL) -> str:
        """Submit a new task to the swarm"""
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title,
            description=description,
            agent_type=agent_type,
            priority=priority,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        self.task_queue.append(task_id)
        
        # Sort queue by priority
        self.task_queue.sort(key=lambda tid: self.tasks[tid].priority.value, reverse=True)
        
        self.console.print(f"[green]📋 Task submitted: {title} (Priority: {priority.name})[/green]")
        return task_id
    
    async def _task_scheduler(self):
        """Background task scheduler that assigns tasks to available agents"""
        while self.running:
            if self.task_queue and self.stats["active_agents"] > 0:
                task_id = self.task_queue[0]
                task = self.tasks[task_id]
                
                # Find available agent
                available_agent = self._find_available_agent(task.agent_type)
                if available_agent:
                    self._assign_task(task_id, available_agent.id)
                    self.task_queue.pop(0)
            
            await asyncio.sleep(1)  # Check every second
    
    def _find_available_agent(self, agent_type: str) -> Optional[Agent]:
        """Find an available agent of the specified type"""
        for agent in self.agents.values():
            if (agent.status == "idle" and 
                agent.config.agent_type == agent_type and 
                not agent.current_task):
                return agent
        return None
    
    def _assign_task(self, task_id: str, agent_id: str):
        """Assign a task to an agent"""
        task = self.tasks[task_id]
        agent = self.agents[agent_id]
        
        task.assigned_agent = agent_id
        task.status = TaskStatus.IN_PROGRESS
        agent.current_task = task_id
        agent.status = "busy"
        
        self.console.print(f"[cyan]⚡ Task '{task.title}' assigned to {agent.config.name}[/cyan]")
    
    def _reassign_task(self, task_id: str):
        """Reassign a task when an agent becomes unavailable"""
        task = self.tasks[task_id]
        task.assigned_agent = None
        task.status = TaskStatus.PENDING
        
        # Add back to front of queue for immediate reassignment
        if task_id not in self.task_queue:
            self.task_queue.insert(0, task_id)
    
    async def _health_monitor(self):
        """Monitor agent health and performance"""
        while self.running:
            for agent_id, agent in list(self.agents.items()):
                # Simple health check - could be extended with actual agent communication
                if agent.status == "error":
                    self.console.print(f"[red]⚠️  Agent {agent.config.name} has errors[/red]")
                    # Could implement agent recovery logic here
            
            await asyncio.sleep(5)  # Check every 5 seconds
    
    async def _performance_tracker(self):
        """Track and display swarm performance metrics"""
        while self.running:
            await asyncio.sleep(10)  # Update every 10 seconds
            self._display_status()
    
    def _display_status(self):
        """Display current swarm status"""
        # Create status table
        table = Table(title="🤖 AI Swarm Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Active Agents", str(self.stats["active_agents"]))
        table.add_row("Total Agents", str(self.stats["total_agents"]))
        table.add_row("Pending Tasks", str(len(self.task_queue)))
        table.add_row("Active Tasks", str(len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])))
        table.add_row("Completed Tasks", str(self.stats["tasks_completed"]))
        table.add_row("Failed Tasks", str(self.stats["tasks_failed"]))
        
        # Clear console and display status
        self.console.clear()
        self.console.print(table)
        
        # Display active tasks
        if any(t.status == TaskStatus.IN_PROGRESS for t in self.tasks.values()):
            task_table = Table(title="📋 Active Tasks")
            task_table.add_column("Task", style="cyan")
            task_table.add_column("Agent", style="green")
            task_table.add_column("Status", style="yellow")
            
            for task in self.tasks.values():
                if task.status == TaskStatus.IN_PROGRESS:
                    agent_name = self.agents[task.assigned_agent].config.name if task.assigned_agent else "Unassigned"
                    task_table.add_row(task.title, agent_name, task.status.value)
            
            self.console.print(task_table)
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get the current status of a task"""
        return self.tasks.get(task_id)
    
    def complete_task(self, task_id: str, result: Any = None, error: str = None):
        """Mark a task as completed"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        if error:
            task.status = TaskStatus.FAILED
            task.error = error
            self.stats["tasks_failed"] += 1
        else:
            task.status = TaskStatus.COMPLETED
            task.result = result
            self.stats["tasks_completed"] += 1
        
        # Free up the agent
        if task.assigned_agent:
            agent = self.agents[task.assigned_agent]
            agent.current_task = None
            agent.status = "idle"
        
        self.console.print(f"[green]✅ Task completed: {task.title}[/green]")
    
    def get_swarm_summary(self) -> Dict[str, Any]:
        """Get a summary of the current swarm state"""
        return {
            "stats": self.stats.copy(),
            "agents": [agent.get_status() for agent in self.agents.values()],
            "pending_tasks": len(self.task_queue),
            "active_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS])
        }
