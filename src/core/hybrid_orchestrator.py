"""
Hybrid Orchestrator for AI Swarm IDE
Coordinates between async and multiprocessing orchestrators
"""

import asyncio
import threading
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from .orchestrator import SwarmOrchestrator
from .multiprocessing_orchestrator import MultiprocessingOrchestrator

class OrchestratorType(Enum):
    ASYNC = "async"
    MULTIPROCESSING = "multiprocessing"
    HYBRID = "hybrid"

@dataclass
class TaskRouting:
    """Configuration for routing tasks to different orchestrators"""
    task_type: str
    orchestrator_type: OrchestratorType
    priority: int = 1
    agent_type: Optional[str] = None

class HybridOrchestrator:
    """
    Hybrid orchestrator that coordinates between async and multiprocessing systems
    """
    
    def __init__(self, max_workers: int = None):
        self.async_orchestrator = SwarmOrchestrator()
        self.multiprocessing_orchestrator = MultiprocessingOrchestrator(max_workers)
        
        # Task routing configuration
        self.task_routing: List[TaskRouting] = [
            # Code generation tasks go to multiprocessing (CPU-intensive)
            TaskRouting("code_generation", OrchestratorType.MULTIPROCESSING, 3),
            TaskRouting("code_refactoring", OrchestratorType.MULTIPROCESSING, 2),
            
            # Analysis and debugging tasks go to multiprocessing
            TaskRouting("code_analysis", OrchestratorType.MULTIPROCESSING, 2),
            TaskRouting("debugging", OrchestratorType.MULTIPROCESSING, 2),
            
            # File management and coordination tasks go to async
            TaskRouting("file_management", OrchestratorType.ASYNC, 1),
            TaskRouting("coordination", OrchestratorType.ASYNC, 1),
            TaskRouting("monitoring", OrchestratorType.ASYNC, 1),
        ]
        
        # Performance tracking
        self.stats = {
            "async_tasks": 0,
            "multiprocessing_tasks": 0,
            "hybrid_tasks": 0,
            "total_tasks": 0
        }
        
        # Threading for async operations
        self.async_thread = None
        self.running = False
    
    async def start(self):
        """Start both orchestrators"""
        self.running = True
        
        # Start async orchestrator
        await self.async_orchestrator.start()
        
        # Start multiprocessing orchestrator in a separate thread
        self.async_thread = threading.Thread(target=self._run_async_loop)
        self.async_thread.start()
        
        print("🚀 Hybrid orchestrator started successfully")
    
    async def stop(self):
        """Stop both orchestrators"""
        self.running = False
        
        # Stop async orchestrator
        await self.async_orchestrator.stop()
        
        # Stop multiprocessing orchestrator
        self.multiprocessing_orchestrator.shutdown()
        
        # Wait for async thread to finish
        if self.async_thread and self.async_thread.is_alive():
            self.async_thread.join(timeout=5)
        
        print("🛑 Hybrid orchestrator stopped")
    
    def _run_async_loop(self):
        """Run async event loop in a separate thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_forever()
        finally:
            loop.close()
    
    def submit_task(self, task_data: Dict[str, Any], task_type: str = None, 
                   priority: int = 1, agent_type: str = None) -> str:
        """Submit a task to the appropriate orchestrator"""
        # Determine which orchestrator to use
        orchestrator_type = self._determine_orchestrator(task_type, agent_type)
        
        if orchestrator_type == OrchestratorType.ASYNC:
            # For async tasks, we need to handle them differently
            # since we can't directly call async methods from sync context
            task_id = self._submit_async_task(task_data, priority)
            self.stats["async_tasks"] += 1
        elif orchestrator_type == OrchestratorType.MULTIPROCESSING:
            task_id = self.multiprocessing_orchestrator.submit_task(
                task_data, agent_type, priority
            )
            self.stats["multiprocessing_tasks"] += 1
        else:
            # Hybrid task - submit to both
            task_id = self._submit_hybrid_task(task_data, priority, agent_type)
            self.stats["hybrid_tasks"] += 1
        
        self.stats["total_tasks"] += 1
        return task_id
    
    def _determine_orchestrator(self, task_type: str, agent_type: str) -> OrchestratorType:
        """Determine which orchestrator should handle a task"""
        if task_type:
            # Check explicit routing rules
            for routing in self.task_routing:
                if routing.task_type == task_type:
                    return routing.orchestrator_type
        
        if agent_type:
            # Check agent type patterns
            if agent_type in ["code_generation", "code_refactoring", "code_analysis", "debugging"]:
                return OrchestratorType.MULTIPROCESSING
            elif agent_type in ["file_management", "coordination", "monitoring"]:
                return OrchestratorType.ASYNC
        
        # Default to multiprocessing for code-related tasks
        return OrchestratorType.MULTIPROCESSING
    
    def _submit_async_task(self, task_data: Dict[str, Any], priority: int) -> str:
        """Submit a task to the async orchestrator"""
        # Since we can't directly call async methods from sync context,
        # we'll queue it for later processing
        task_id = f"async_{int(time.time() * 1000)}"
        
        # Store the task for later async processing
        if not hasattr(self, '_async_task_queue'):
            self._async_task_queue = []
        
        self._async_task_queue.append({
            "id": task_id,
            "data": task_data,
            "priority": priority,
            "timestamp": time.time()
        })
        
        return task_id
    
    def _submit_hybrid_task(self, task_data: Dict[str, Any], priority: int, 
                           agent_type: str) -> str:
        """Submit a task to both orchestrators for coordinated processing"""
        task_id = f"hybrid_{int(time.time() * 1000)}"
        
        # Submit to multiprocessing orchestrator
        mp_task_id = self.multiprocessing_orchestrator.submit_task(
            task_data, agent_type, priority
        )
        
        # Submit to async orchestrator for coordination
        async_task_id = self._submit_async_task({
            **task_data,
            "hybrid_coordination": True,
            "mp_task_id": mp_task_id
        }, priority)
        
        return task_id
    
    def route_task(self, agent_type: str, task_data: Dict[str, Any]) -> bool:
        """Route a task to a specific agent type"""
        orchestrator_type = self._determine_orchestrator(None, agent_type)
        
        if orchestrator_type == OrchestratorType.MULTIPROCESSING:
            return self.multiprocessing_orchestrator.route_task(agent_type, task_data)
        else:
            # For async tasks, queue them
            self._submit_async_task(task_data, 1)
            return True
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get results from both orchestrators"""
        results = []
        
        # Get results from multiprocessing orchestrator
        mp_results = self.multiprocessing_orchestrator.get_results()
        results.extend(mp_results)
        
        # Get results from async orchestrator (if any)
        if hasattr(self, '_async_results') and self._async_results:
            results.extend(self._async_results)
            self._async_results = []
        
        return results
    
    def process_pending_tasks(self):
        """Process pending tasks in both orchestrators"""
        # Process multiprocessing tasks
        self.multiprocessing_orchestrator.process_pending_tasks()
        
        # Process async tasks (if any)
        if hasattr(self, '_async_task_queue') and self._async_task_queue:
            # This would need to be handled in the async thread
            pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get combined status from both orchestrators"""
        async_status = self.async_orchestrator.get_swarm_summary()
        mp_status = self.multiprocessing_orchestrator.get_status()
        
        return {
            "hybrid_stats": self.stats.copy(),
            "async_orchestrator": async_status,
            "multiprocessing_orchestrator": mp_status,
            "task_routing": [
                {
                    "task_type": routing.task_type,
                    "orchestrator": routing.orchestrator_type.value,
                    "priority": routing.priority
                }
                for routing in self.task_routing
            ]
        }
    
    def display_status(self):
        """Display combined status from both orchestrators"""
        status = self.get_status()
        
        print("🤖 Hybrid Orchestrator Status")
        print("=" * 40)
        
        # Display hybrid stats
        print(f"📊 Total Tasks: {status['hybrid_stats']['total_tasks']}")
        print(f"🔄 Async Tasks: {status['hybrid_stats']['async_tasks']}")
        print(f"⚡ Multiprocessing Tasks: {status['hybrid_stats']['multiprocessing_tasks']}")
        print(f"🔗 Hybrid Tasks: {status['hybrid_stats']['hybrid_tasks']}")
        
        print("\n📋 Task Routing Configuration:")
        for routing in status['task_routing']:
            print(f"  {routing['task_type']} → {routing['orchestrator']} (Priority: {routing['priority']})")
        
        print("\n🤖 Async Orchestrator:")
        async_stats = status['async_orchestrator']['stats']
        print(f"  Active Agents: {async_stats['active_agents']}")
        print(f"  Total Agents: {async_stats['total_agents']}")
        
        print("\n⚡ Multiprocessing Orchestrator:")
        mp_stats = status['multiprocessing_orchestrator']['stats']
        print(f"  Active Agents: {mp_stats['active_agents']}")
        print(f"  Total Agents: {mp_stats['total_agents']}")
        print(f"  Pending Tasks: {status['multiprocessing_orchestrator']['pending_tasks']}")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on both orchestrators"""
        mp_health = self.multiprocessing_orchestrator.health_check()
        
        # For async orchestrator, we'd need to check in the async thread
        async_health = {"status": "async_thread_running", "thread_alive": self.async_thread.is_alive() if self.async_thread else False}
        
        return {
            "multiprocessing": mp_health,
            "async": async_health,
            "hybrid": {
                "status": "healthy" if self.running else "stopped",
                "running": self.running
            }
        }
