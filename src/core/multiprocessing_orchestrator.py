"""
Multiprocessing Orchestrator for AI Swarm IDE
Provides process-based agent execution with queue-based communication
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class ProcessStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    STOPPED = "stopped"

@dataclass
class ProcessAgent:
    id: str
    name: str
    agent_type: str
    process: mp.Process
    input_queue: mp.Queue
    output_queue: mp.Queue
    status: ProcessStatus
    capabilities: List[str]
    current_task: Optional[str] = None
    performance_metrics: Dict[str, Any] = None

    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {
                "tasks_completed": 0,
                "tasks_failed": 0,
                "start_time": datetime.now(),
                "last_activity": datetime.now()
            }

class MultiprocessingOrchestrator:
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or mp.cpu_count()
        self.agents: Dict[str, ProcessAgent] = {}
        self.task_queue: List[Dict[str, Any]] = []
        self.results_queue: mp.Queue = mp.Queue()
        self.running = False
        
        # Performance tracking
        self.stats = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "total_agents": 0,
            "active_agents": 0,
            "start_time": datetime.now()
        }
        
        # Configure multiprocessing
        mp.set_start_method('spawn', force=True)
        
        self.console = Console()
        self.logger = logging.getLogger("multiprocessing_orchestrator")
    
    def register_agent(self, name: str, agent_type: str, agent_function: Callable, 
                      capabilities: List[str], **kwargs) -> str:
        """Register a new agent process"""
        agent_id = str(uuid.uuid4())
        
        # Create queues for this agent
        input_queue = mp.Queue()
        output_queue = mp.Queue()
        
        # Create and start the agent process
        process = mp.Process(
            target=agent_function,
            args=(input_queue, output_queue),
            kwargs=kwargs,
            name=f"{name}_{agent_id[:8]}"
        )
        
        process.start()
        
        # Create agent record
        agent = ProcessAgent(
            id=agent_id,
            name=name,
            agent_type=agent_type,
            process=process,
            input_queue=input_queue,
            output_queue=output_queue,
            status=ProcessStatus.IDLE,
            capabilities=capabilities
        )
        
        self.agents[agent_id] = agent
        self.stats["total_agents"] += 1
        self.stats["active_agents"] += 1
        
        self.console.print(f"[blue]🤖 Process agent registered: {name} ({agent_type})[/blue]")
        return agent_id
    
    def submit_task(self, task_data: Dict[str, Any], agent_type: str = None, 
                   priority: int = 1) -> str:
        """Submit a task to the orchestrator"""
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "data": task_data,
            "agent_type": agent_type,
            "priority": priority,
            "created_at": datetime.now(),
            "status": "pending"
        }
        
        self.task_queue.append(task)
        # Sort by priority (higher priority first)
        self.task_queue.sort(key=lambda x: x["priority"], reverse=True)
        
        self.console.print(f"[green]📋 Task submitted: {task_data.get('title', 'Unknown')} (Priority: {priority})[/green]")
        return task_id
    
    def route_task(self, agent_type: str, task_data: Dict[str, Any]):
        """Route a task to a specific agent type"""
        # Find available agent of the specified type
        available_agent = self._find_available_agent(agent_type)
        if available_agent:
            self._assign_task_to_agent(available_agent, task_data)
            return True
        else:
            # Queue the task for later
            self.submit_task(task_data, agent_type)
            return False
    
    def _find_available_agent(self, agent_type: str) -> Optional[ProcessAgent]:
        """Find an available agent of the specified type"""
        for agent in self.agents.values():
            if (agent.status == ProcessStatus.IDLE and 
                agent.agent_type == agent_type and 
                not agent.current_task):
                return agent
        return None
    
    def _assign_task_to_agent(self, agent: ProcessAgent, task_data: Dict[str, Any]):
        """Assign a task to a specific agent"""
        agent.current_task = task_data.get("id", str(uuid.uuid4()))
        agent.status = ProcessStatus.BUSY
        agent.performance_metrics["last_activity"] = datetime.now()
        
        # Send task to agent
        agent.input_queue.put(task_data)
        
        self.console.print(f"[cyan]⚡ Task assigned to {agent.name}[/cyan]")
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get all available results from agents"""
        results = []
        
        # Check each agent's output queue
        for agent in self.agents.values():
            try:
                while not agent.output_queue.empty():
                    result = agent.output_queue.get_nowait()
                    results.append({
                        "agent_id": agent.id,
                        "agent_name": agent.name,
                        "result": result,
                        "timestamp": datetime.now()
                    })
                    
                    # Update agent status
                    agent.status = ProcessStatus.IDLE
                    agent.current_task = None
                    agent.performance_metrics["tasks_completed"] += 1
                    agent.performance_metrics["last_activity"] = datetime.now()
                    
            except queue.Empty:
                continue
        
        return results
    
    def process_pending_tasks(self):
        """Process any pending tasks in the queue"""
        processed = 0
        
        for task in self.task_queue[:]:  # Copy to avoid modification during iteration
            if task["status"] == "pending":
                agent_type = task["agent_type"]
                available_agent = self._find_available_agent(agent_type)
                
                if available_agent:
                    self._assign_task_to_agent(available_agent, task["data"])
                    task["status"] = "assigned"
                    self.task_queue.remove(task)
                    processed += 1
        
        if processed > 0:
            self.console.print(f"[yellow]🔄 Processed {processed} pending tasks[/yellow]")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status"""
        return {
            "stats": self.stats.copy(),
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.agent_type,
                    "status": agent.status.value,
                    "capabilities": agent.capabilities,
                    "current_task": agent.current_task,
                    "performance": agent.performance_metrics
                }
                for agent in self.agents.values()
            ],
            "pending_tasks": len([t for t in self.task_queue if t["status"] == "pending"]),
            "assigned_tasks": len([t for t in self.task_queue if t["status"] == "assigned"])
        }
    
    def display_status(self):
        """Display current orchestrator status"""
        status = self.get_status()
        
        # Create status table
        table = Table(title="🤖 Multiprocessing Swarm Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Active Agents", str(status["stats"]["active_agents"]))
        table.add_row("Total Agents", str(status["stats"]["total_agents"]))
        table.add_row("Pending Tasks", str(status["pending_tasks"]))
        table.add_row("Assigned Tasks", str(status["assigned_tasks"]))
        table.add_row("Completed Tasks", str(status["stats"]["tasks_completed"]))
        table.add_row("Failed Tasks", str(status["stats"]["tasks_failed"]))
        
        self.console.print(table)
        
        # Display agent status
        if status["agents"]:
            agent_table = Table(title="🤖 Agent Status")
            agent_table.add_column("Name", style="cyan")
            agent_table.add_column("Type", style="green")
            agent_table.add_column("Status", style="yellow")
            agent_table.add_column("Current Task", style="blue")
            
            for agent in status["agents"]:
                current_task = agent["current_task"] or "None"
                agent_table.add_row(
                    agent["name"],
                    agent["type"],
                    agent["status"],
                    current_task
                )
            
            self.console.print(agent_table)
    
    def shutdown(self):
        """Shutdown all agent processes"""
        self.console.print("[yellow]🛑 Shutting down multiprocessing orchestrator...[/yellow]")
        
        # Send stop signal to all agents
        for agent in self.agents.values():
            try:
                agent.input_queue.put("STOP")
                agent.process.join(timeout=5)
                
                if agent.process.is_alive():
                    agent.process.terminate()
                    agent.process.join(timeout=2)
                    if agent.process.is_alive():
                        agent.process.kill()
                
                agent.status = ProcessStatus.STOPPED
                
            except Exception as e:
                self.logger.error(f"Error shutting down agent {agent.name}: {e}")
        
        self.running = False
        self.console.print("[red]🛑 All agent processes terminated[/red]")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents"""
        health_status = {}
        
        for agent_id, agent in self.agents.items():
            try:
                # Check if process is alive
                is_alive = agent.process.is_alive()
                
                if is_alive:
                    # Check if agent is responsive
                    try:
                        agent.input_queue.put({"type": "ping", "timestamp": time.time()})
                        health_status[agent_id] = {
                            "status": "healthy",
                            "process_alive": True,
                            "last_activity": agent.performance_metrics["last_activity"]
                        }
                    except Exception:
                        health_status[agent_id] = {
                            "status": "unresponsive",
                            "process_alive": True,
                            "last_activity": agent.performance_metrics["last_activity"]
                        }
                else:
                    health_status[agent_id] = {
                        "status": "dead",
                        "process_alive": False,
                        "last_activity": agent.performance_metrics["last_activity"]
                    }
                    
            except Exception as e:
                health_status[agent_id] = {
                    "status": "error",
                    "error": str(e),
                    "process_alive": False
                }
        
        return health_status
