"""
CLI Interface for AI Swarm IDE
Provides command-line access to the AI swarm development environment
"""

import asyncio
import typer
from typing import Optional, List
from pathlib import Path
import json
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from core.orchestrator import SwarmOrchestrator, TaskPriority
from agents.base_agent import AgentConfig
from agents.code_agent import CodeAgent
from agents.testing_agent import TestingAgent

app = typer.Typer(help="AI Swarm IDE - Autonomous AI Development Environment")
console = Console()

# Global orchestrator instance
orchestrator: Optional[SwarmOrchestrator] = None
current_project: Optional[Path] = None

def _get_project_config_path() -> Optional[Path]:
    """Get the project configuration path from current directory"""
    current_dir = Path.cwd()
    
    # Look for .ai-swarm-ide file in current or parent directories
    while current_dir != current_dir.parent:
        config_file = current_dir / ".ai-swarm-ide"
        if config_file.exists():
            return current_dir
        current_dir = current_dir.parent
    
    # Also check subdirectories for projects
    for item in Path.cwd().iterdir():
        if item.is_dir():
            config_file = item / ".ai-swarm-ide"
            if config_file.exists():
                return item
    
    return None

def _load_orchestrator() -> Optional[SwarmOrchestrator]:
    """Load orchestrator from project configuration"""
    global orchestrator, current_project
    
    if orchestrator is not None:
        return orchestrator
    
    project_path = _get_project_config_path()
    if project_path is None:
        return None
    
    current_project = project_path
    orchestrator = SwarmOrchestrator()
    console.print(f"[blue]📁 Loaded project from: {project_path}[/blue]")
    return orchestrator

@app.command()
def init(
    project_path: str = typer.Argument(".", help="Path to initialize the AI swarm IDE")
):
    """Initialize AI Swarm IDE in a project directory"""
    global orchestrator, current_project
    
    project_path = Path(project_path).resolve()
    
    if not project_path.exists():
        project_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✅ Created project directory: {project_path}[/green]")
    
    # Initialize orchestrator
    orchestrator = SwarmOrchestrator()
    current_project = project_path
    
    # Create basic project structure
    _create_project_structure(project_path)
    
    # Create project marker file
    marker_file = project_path / ".ai-swarm-ide"
    marker_file.write_text(f"AI Swarm IDE Project\nInitialized: {project_path}")
    
    console.print(f"[bold green]🚀 AI Swarm IDE initialized in {project_path}[/bold green]")
    console.print("[yellow]Use 'swarm start' to launch the swarm[/yellow]")

@app.command()
def start():
    """Start the AI swarm IDE"""
    global orchestrator
    
    # Try to load orchestrator if not already loaded
    if orchestrator is None:
        orchestrator = _load_orchestrator()
    
    if orchestrator is None:
        console.print("[red]❌ AI Swarm IDE not initialized. Run 'swarm init' first.[/red]")
        raise typer.Exit(1)
    
    console.print("[bold blue]🚀 Starting AI Swarm IDE...[/bold blue]")
    
    async def start_swarm():
        await orchestrator.start()
        
        # Register default agents
        await _register_default_agents()
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await orchestrator.stop()
    
    asyncio.run(start_swarm())

@app.command()
def agent(
    action: str = typer.Argument(..., help="Action: add, list, remove"),
    agent_type: Optional[str] = typer.Option(None, help="Type of agent to add"),
    name: Optional[str] = typer.Option(None, help="Name for the agent")
):
    """Manage AI agents in the swarm"""
    global orchestrator
    
    # Try to load orchestrator if not already loaded
    if orchestrator is None:
        orchestrator = _load_orchestrator()
    
    if orchestrator is None:
        console.print("[red]❌ AI Swarm IDE not initialized. Run 'swarm init' first.[/red]")
        raise typer.Exit(1)
    
    if action == "add":
        if not agent_type or not name:
            console.print("[red]❌ Both --agent-type and --name are required for adding agents[/red]")
            raise typer.Exit(1)
        
        _add_agent(agent_type, name)
    
    elif action == "list":
        _list_agents()
    
    elif action == "remove":
        if not name:
            console.print("[red]❌ --name is required for removing agents[/red]")
            raise typer.Exit(1)
        _remove_agent(name)
    
    else:
        console.print(f"[red]❌ Unknown action: {action}[/red]")
        raise typer.Exit(1)

@app.command()
def task(
    action: str = typer.Argument(..., help="Action: submit, list, status"),
    title: Optional[str] = typer.Option(None, help="Task title"),
    description: Optional[str] = typer.Option(None, help="Task description"),
    agent_type: Optional[str] = typer.Option(None, help="Type of agent to handle the task"),
    priority: Optional[str] = typer.Option("NORMAL", help="Task priority: LOW, NORMAL, HIGH, CRITICAL")
):
    """Manage tasks in the swarm"""
    global orchestrator
    
    # Try to load orchestrator if not already loaded
    if orchestrator is None:
        orchestrator = _load_orchestrator()
    
    if orchestrator is None:
        console.print("[red]❌ AI Swarm IDE not initialized. Run 'swarm init' first.[/red]")
        raise typer.Exit(1)
    
    if action == "submit":
        if not title or not description or not agent_type:
            console.print("[red]❌ --title, --description, and --agent-type are required for submitting tasks[/red]")
            raise typer.Exit(1)
        
        _submit_task(title, description, agent_type, priority)
    
    elif action == "list":
        _list_tasks()
    
    elif action == "status":
        if not title:
            console.print("[red]❌ --title is required for checking task status[/red]")
            raise typer.Exit(1)
        _get_task_status(title)
    
    else:
        console.print(f"[red]❌ Unknown action: {action}[/red]")
        raise typer.Exit(1)

@app.command()
def code(
    action: str = typer.Argument(..., help="Action: generate, refactor, analyze, debug"),
    requirements: Optional[str] = typer.Option(None, help="Code requirements or description"),
    language: Optional[str] = typer.Option("python", help="Programming language"),
    file_path: Optional[str] = typer.Option(None, help="Path to existing code file")
):
    """Code-related operations using the code agent"""
    global orchestrator
    
    # Try to load orchestrator if not already loaded
    if orchestrator is None:
        orchestrator = _load_orchestrator()
    
    if orchestrator is None:
        console.print("[red]❌ AI Swarm IDE not initialized. Run 'swarm init' first.[/red]")
        raise typer.Exit(1)
    
    if action == "generate":
        if not requirements:
            console.print("[red]❌ --requirements is required for code generation[/red]")
            raise typer.Exit(1)
        _generate_code(requirements, language)
    
    elif action == "refactor":
        if not file_path:
            console.print("[red]❌ --file-path is required for code refactoring[/red]")
            raise typer.Exit(1)
        _refactor_code(file_path)
    
    elif action == "analyze":
        if not file_path:
            console.print("[red]❌ --file-path is required for code analysis[/red]")
            raise typer.Exit(1)
        _analyze_code(file_path)
    
    elif action == "debug":
        if not file_path:
            console.print("[red]❌ --file-path is required for debugging[/red]")
            raise typer.Exit(1)
        _debug_code(file_path)
    
    else:
        console.print(f"[red]❌ Unknown action: {action}[/red]")
        raise typer.Exit(1)

@app.command()
def test(
    action: str = typer.Argument(..., help="Action: run, coverage, generate, report"),
    project_path: Optional[str] = typer.Option(".", help="Project path"),
    test_type: Optional[str] = typer.Option("unit", help="Type of tests to run"),
    language: Optional[str] = typer.Option("python", help="Programming language")
):
    """Testing operations using the testing agent"""
    global orchestrator
    
    # Try to load orchestrator if not already loaded
    if orchestrator is None:
        orchestrator = _load_orchestrator()
    
    if orchestrator is None:
        console.print("[red]❌ AI Swarm IDE not initialized. Run 'swarm init' first.[/red]")
        raise typer.Exit(1)
    
    if action == "run":
        _run_tests(project_path, test_type, language)
    
    elif action == "coverage":
        _analyze_coverage(project_path, language)
    
    elif action == "generate":
        _generate_tests(project_path, language)
    
    elif action == "report":
        _generate_test_report(project_path)
    
    else:
        console.print(f"[red]❌ Unknown action: {action}[/red]")
        raise typer.Exit(1)

@app.command()
def status():
    """Show current swarm status"""
    global orchestrator
    
    # Try to load orchestrator if not already loaded
    if orchestrator is None:
        orchestrator = _load_orchestrator()
    
    if orchestrator is None:
        console.print("[red]❌ AI Swarm IDE not initialized. Run 'swarm init' first.[/red]")
        raise typer.Exit(1)
    
    _show_swarm_status()

@app.command()
def config():
    """Show configuration and help"""
    _show_config()

def _create_project_structure(project_path: Path):
    """Create basic project structure"""
    # Create directories
    (project_path / "src").mkdir(exist_ok=True)
    (project_path / "tests").mkdir(exist_ok=True)
    (project_path / "docs").mkdir(exist_ok=True)
    (project_path / "config").mkdir(exist_ok=True)
    
    # Create basic files
    (project_path / "README.md").write_text("# AI Swarm IDE Project\n\nThis project is managed by AI Swarm IDE.")
    (project_path / "requirements.txt").write_text("# Project dependencies\n")
    (project_path / ".gitignore").write_text("# Python\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.Python\nenv/\nvenv/\n.env\n")

async def _register_default_agents():
    """Register default agents with the swarm"""
    global orchestrator
    
    # Code Agent
    code_config = AgentConfig(
        name="CodeMaster",
        agent_type="code",
        capabilities=["code_generation", "refactoring", "analysis"],
        max_concurrent_tasks=3
    )
    code_agent = CodeAgent(code_config)
    await code_agent.start()
    
    # Testing Agent
    test_config = AgentConfig(
        name="TestRunner",
        agent_type="testing",
        capabilities=["test_execution", "coverage_analysis"],
        max_concurrent_tasks=2
    )
    test_agent = TestingAgent(test_config)
    await test_agent.start()
    
    # Register with orchestrator
    orchestrator.register_agent(code_agent)
    orchestrator.register_agent(test_agent)
    
    console.print("[green]✅ Default agents registered: CodeMaster, TestRunner[/green]")

def _add_agent(agent_type: str, name: str):
    """Add a new agent to the swarm"""
    # This would create and register a new agent
    console.print(f"[blue]🤖 Adding {agent_type} agent: {name}[/blue]")
    console.print("[yellow]Note: Agent creation not fully implemented in this prototype[/yellow]")

def _list_agents():
    """List all agents in the swarm"""
    global orchestrator
    
    if not orchestrator.agents:
        console.print("[yellow]No agents registered[/yellow]")
        return
    
    table = Table(title="🤖 Registered Agents")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Capabilities", style="magenta")
    
    for agent in orchestrator.agents.values():
        table.add_row(
            agent.config.name,
            agent.config.agent_type,
            agent.status,
            ", ".join(agent.config.capabilities[:3]) + ("..." if len(agent.config.capabilities) > 3 else "")
        )
    
    console.print(table)

def _remove_agent(name: str):
    """Remove an agent from the swarm"""
    global orchestrator
    
    # Find agent by name
    agent_to_remove = None
    for agent in orchestrator.agents.values():
        if agent.config.name == name:
            agent_to_remove = agent
            break
    
    if agent_to_remove:
        orchestrator.unregister_agent(agent_to_remove.id)
        console.print(f"[green]✅ Agent {name} removed[/green]")
    else:
        console.print(f"[red]❌ Agent {name} not found[/red]")

def _submit_task(title: str, description: str, agent_type: str, priority: str):
    """Submit a new task to the swarm"""
    global orchestrator
    
    try:
        priority_enum = TaskPriority[priority.upper()]
    except KeyError:
        console.print(f"[red]❌ Invalid priority: {priority}. Use LOW, NORMAL, HIGH, or CRITICAL[/red]")
        raise typer.Exit(1)
    
    task_id = orchestrator.submit_task(title, description, agent_type, priority_enum)
    console.print(f"[green]✅ Task submitted with ID: {task_id}[/green]")

def _list_tasks():
    """List all tasks in the swarm"""
    global orchestrator
    
    if not orchestrator.tasks:
        console.print("[yellow]No tasks found[/yellow]")
        return
    
    table = Table(title="📋 Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Agent Type", style="magenta")
    table.add_column("Priority", style="blue")
    
    for task in orchestrator.tasks.values():
        table.add_row(
            task.id[:8],
            task.title,
            task.status.value,
            task.agent_type,
            task.priority.name
        )
    
    console.print(table)

def _get_task_status(title: str):
    """Get status of a specific task"""
    global orchestrator
    
    # Find task by title
    task = None
    for t in orchestrator.tasks.values():
        if t.title == title:
            task = t
            break
    
    if not task:
        console.print(f"[red]❌ Task '{title}' not found[/red]")
        return
    
    console.print(f"[cyan]Task: {task.title}[/cyan]")
    console.print(f"[green]Status: {task.status.value}[/green]")
    console.print(f"[blue]Agent Type: {task.agent_type}[/blue]")
    console.print(f"[yellow]Priority: {task.priority.name}[/yellow]")
    
    if task.assigned_agent:
        agent = orchestrator.agents.get(task.assigned_agent)
        if agent:
            console.print(f"[magenta]Assigned to: {agent.config.name}[/magenta]")

def _generate_code(requirements: str, language: str):
    """Generate code using the code agent"""
    console.print(f"[cyan]🔧 Generating {language} code for: {requirements}[/cyan]")
    console.print("[yellow]Note: Code generation not fully implemented in this prototype[/yellow]")

def _refactor_code(file_path: str):
    """Refactor code using the code agent"""
    console.print(f"[cyan]🔄 Refactoring code in: {file_path}[/cyan]")
    console.print("[yellow]Note: Code refactoring not fully implemented in this prototype[/yellow]")

def _analyze_code(file_path: str):
    """Analyze code using the code agent"""
    console.print(f"[cyan]🔍 Analyzing code in: {file_path}[/cyan]")
    console.print("[yellow]Note: Code analysis not fully implemented in this prototype[/yellow]")

def _debug_code(file_path: str):
    """Debug code using the code agent"""
    console.print(f"[cyan]🐛 Debugging code in: {file_path}[/cyan]")
    console.print("[yellow]Note: Code debugging not fully implemented in this prototype[/yellow]")

def _run_tests(project_path: str, test_type: str, language: str):
    """Run tests using the testing agent"""
    console.print(f"[cyan]🧪 Running {test_type} tests for {language} project in {project_path}[/cyan]")
    console.print("[yellow]Note: Test execution not fully implemented in this prototype[/yellow]")

def _analyze_coverage(project_path: str, language: str):
    """Analyze test coverage using the testing agent"""
    console.print(f"[cyan]📊 Analyzing test coverage for {language} project in {project_path}[/cyan]")
    console.print("[yellow]Note: Coverage analysis not fully implemented in this prototype[/yellow]")

def _generate_tests(project_path: str, language: str):
    """Generate tests using the testing agent"""
    console.print(f"[cyan]🔧 Generating tests for {language} project in {project_path}[/cyan]")
    console.print("[yellow]Note: Test generation not fully implemented in this prototype[/yellow]")

def _generate_test_report(project_path: str):
    """Generate test report using the testing agent"""
    console.print(f"[cyan]📋 Generating test report for project in {project_path}[/cyan]")
    console.print("[yellow]Note: Test reporting not fully implemented in this prototype[/yellow]")

def _show_swarm_status():
    """Show current swarm status"""
    global orchestrator
    
    summary = orchestrator.get_swarm_summary()
    
    # Status table
    table = Table(title="🤖 AI Swarm Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    for key, value in summary["stats"].items():
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)
    
    # Active tasks
    if summary["active_tasks"] > 0:
        console.print(f"\n[cyan]Active Tasks: {summary['active_tasks']}[/cyan]")
    
    # Pending tasks
    if summary["pending_tasks"] > 0:
        console.print(f"[yellow]Pending Tasks: {summary['pending_tasks']}[/yellow]")

def _show_config():
    """Show configuration and help"""
    console.print(Panel.fit(
        "[bold blue]AI Swarm IDE - Configuration[/bold blue]\n\n"
        "[cyan]Available Commands:[/cyan]\n"
        "• swarm init [path]     - Initialize AI Swarm IDE\n"
        "• swarm start          - Start the swarm\n"
        "• swarm agent [action] - Manage agents\n"
        "• swarm task [action]  - Manage tasks\n"
        "• swarm code [action]  - Code operations\n"
        "• swarm test [action]  - Testing operations\n"
        "• swarm status         - Show swarm status\n"
        "• swarm config         - Show this help\n\n"
        "[yellow]Example Usage:[/yellow]\n"
        "swarm init myproject\n"
        "swarm start\n"
        "swarm code generate --requirements 'Create a REST API' --language python\n"
        "swarm test run --test-type unit --language python",
        title="🚀 AI Swarm IDE Help"
    ))

if __name__ == "__main__":
    app()
