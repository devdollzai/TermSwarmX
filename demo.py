#!/usr/bin/env python3
"""
AI Swarm IDE Demo Script
Demonstrates the capabilities of the AI swarm development environment
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.orchestrator import SwarmOrchestrator, TaskPriority
from agents.base_agent import AgentConfig
from agents.code_agent import CodeAgent
from agents.testing_agent import TestingAgent
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

async def demo_swarm_workflow():
    """Demonstrate a complete swarm workflow"""
    
    console.print(Panel.fit(
        "[bold blue]🚀 AI Swarm IDE Demo[/bold blue]\n\n"
        "This demo will showcase:\n"
        "• Agent registration and management\n"
        "• Task submission and distribution\n"
        "• Parallel task execution\n"
        "• Real-time status monitoring\n"
        "• Collaborative development workflow",
        title="🤖 AI Swarm IDE Demo"
    ))
    
    # Initialize orchestrator
    console.print("\n[cyan]1. Initializing Swarm Orchestrator...[/cyan]")
    orchestrator = SwarmOrchestrator()
    await orchestrator.start()
    
    # Register agents
    console.print("\n[cyan]2. Registering AI Agents...[/cyan]")
    
    # Code Agent
    code_config = AgentConfig(
        name="CodeMaster",
        agent_type="code",
        capabilities=["code_generation", "refactoring", "analysis", "debugging"],
        max_concurrent_tasks=3
    )
    code_agent = CodeAgent(code_config)
    await code_agent.start()
    
    # Testing Agent
    test_config = AgentConfig(
        name="TestRunner",
        agent_type="testing",
        capabilities=["test_execution", "coverage_analysis", "test_generation"],
        max_concurrent_tasks=2
    )
    test_agent = TestingAgent(test_config)
    await test_agent.start()
    
    # Register with orchestrator
    orchestrator.register_agent(code_agent)
    orchestrator.register_agent(test_agent)
    
    console.print("[green]✅ Agents registered successfully![/green]")
    
    # Submit tasks
    console.print("\n[cyan]3. Submitting Development Tasks...[/cyan]")
    
    # Task 1: Generate a REST API
    task1_id = orchestrator.submit_task(
        title="Generate REST API",
        description="Create a Python Flask REST API with CRUD operations for a user management system",
        agent_type="code",
        priority=TaskPriority.HIGH
    )
    
    # Task 2: Generate tests for the API
    task2_id = orchestrator.submit_task(
        title="Generate API Tests",
        description="Create comprehensive pytest tests for the user management API",
        agent_type="testing",
        priority=TaskPriority.NORMAL
    )
    
    # Task 3: Code analysis
    task3_id = orchestrator.submit_task(
        title="Analyze Code Quality",
        description="Analyze the generated API code for quality, security, and best practices",
        agent_type="code",
        priority=TaskPriority.NORMAL
    )
    
    # Task 4: Performance testing
    task4_id = orchestrator.submit_task(
        title="Performance Testing",
        description="Run performance tests on the API endpoints to identify bottlenecks",
        agent_type="testing",
        priority=TaskPriority.LOW
    )
    
    console.print("[green]✅ Tasks submitted successfully![/green]")
    
    # Monitor task execution
    console.print("\n[cyan]4. Monitoring Task Execution...[/cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Monitor for 30 seconds to show task execution
        for i in range(30):
            # Show current status
            summary = orchestrator.get_swarm_summary()
            
            # Update progress description
            progress.update(
                progress.add_task("Monitoring swarm...", total=None),
                description=f"Active: {summary['active_tasks']}, Pending: {summary['pending_tasks']}, Completed: {summary['stats']['tasks_completed']}"
            )
            
            await asyncio.sleep(1)
    
    # Show final results
    console.print("\n[cyan]5. Final Results...[/cyan]")
    
    final_summary = orchestrator.get_swarm_summary()
    
    # Results table
    table = Table(title="📊 Demo Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Agents", str(final_summary["stats"]["total_agents"]))
    table.add_row("Active Agents", str(final_summary["stats"]["active_agents"]))
    table.add_row("Tasks Submitted", str(len(orchestrator.tasks)))
    table.add_row("Tasks Completed", str(final_summary["stats"]["tasks_completed"]))
    table.add_row("Tasks Failed", str(final_summary["stats"]["tasks_failed"]))
    table.add_row("Pending Tasks", str(final_summary["pending_tasks"]))
    
    console.print(table)
    
    # Show completed tasks
    if final_summary["stats"]["tasks_completed"] > 0:
        console.print("\n[green]✅ Completed Tasks:[/green]")
        for task in orchestrator.tasks.values():
            if task.status.value == "completed":
                console.print(f"  • {task.title} (by {orchestrator.agents[task.assigned_agent].config.name if task.assigned_agent else 'Unknown'})")
    
    # Show active tasks
    if final_summary["active_tasks"] > 0:
        console.print("\n[cyan]🔄 Active Tasks:[/cyan]")
        for task in orchestrator.tasks.values():
            if task.status.value == "in_progress":
                console.print(f"  • {task.title} (assigned to {orchestrator.agents[task.assigned_agent].config.name if task.assigned_agent else 'Unknown'})")
    
    # Show pending tasks
    if final_summary["pending_tasks"] > 0:
        console.print("\n[yellow]⏳ Pending Tasks:[/yellow]")
        for task in orchestrator.tasks.values():
            if task.status.value == "pending":
                console.print(f"  • {task.title} (waiting for {task.agent_type} agent)")
    
    # Demonstrate collaborative workflow
    console.print("\n[cyan]6. Collaborative Workflow Benefits...[/cyan]")
    
    workflow_table = Table(title="🤝 Collaborative Development Workflow")
    workflow_table.add_column("Phase", style="cyan")
    workflow_table.add_column("Agents Involved", style="green")
    workflow_table.add_column("Benefits", style="yellow")
    
    workflow_table.add_row(
        "Code Generation",
        "CodeMaster",
        "• Rapid prototyping\n• Consistent code style\n• Best practices"
    )
    
    workflow_table.add_row(
        "Testing",
        "TestRunner",
        "• Immediate validation\n• Coverage analysis\n• Quality assurance"
    )
    
    workflow_table.add_row(
        "Code Analysis",
        "CodeMaster",
        "• Security review\n• Performance optimization\n• Maintainability"
    )
    
    workflow_table.add_row(
        "Performance Testing",
        "TestRunner",
        "• Load testing\n• Bottleneck identification\n• Scalability validation"
    )
    
    console.print(workflow_table)
    
    # Cleanup
    console.print("\n[cyan]7. Cleaning up...[/cyan]")
    await orchestrator.stop()
    
    console.print(Panel.fit(
        "[bold green]🎉 Demo Completed Successfully![/bold green]\n\n"
        "The AI Swarm IDE demonstrated:\n"
        "• Autonomous task distribution\n"
        "• Parallel agent execution\n"
        "• Real-time status monitoring\n"
        "• Collaborative development workflow\n"
        "• Scalable architecture\n\n"
        "Ready for production use! 🚀",
        title="✅ Demo Complete"
    ))

def run_demo():
    """Run the demo"""
    try:
        asyncio.run(demo_swarm_workflow())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo failed with error: {e}[/red]")
        raise

if __name__ == "__main__":
    run_demo()
