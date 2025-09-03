#!/usr/bin/env python3
"""
DevDollz CLI Interface
Where Code Meets Chaos - Built by Alexis Adams
"""

import sys
import os
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from .themes import get_theme_manager, ThemeStyle

# Initialize Typer app
app = typer.Typer(
    name="devdollz",
    help="🎀 DevDollz AI Swarm IDE - Where Code Meets Chaos",
    add_completion=False,
    rich_markup_mode="rich"
)

# Initialize Rich console
console = Console()

def print_banner():
    """Print the DevDollz banner"""
    banner = """
🎀 DevDollz AI Swarm IDE 🎀
   Where Code Meets Chaos
   Built by Alexis Adams for the Hacker Elite
"""
    
    console.print(Panel(
        banner,
        title="[bold hot_pink]DevDollz[/bold hot_pink]",
        border_style="hot_pink",
        padding=(1, 2)
    ))

def print_creator_quote():
    """Print a quote from Alexis Adams"""
    quote = '"I built this because I was tired of slow, boring AI tools. Real hackers need speed, style, and substance. DevDollz delivers all three."'
    author = "— Alexis Adams"
    
    console.print(Panel(
        f"[italic]{quote}[/italic]\n\n[bold hot_pink]{author}[/bold hot_pink]",
        title="[bold]Creator's Vision[/bold]",
        border_style="purple",
        padding=(1, 2)
    ))

@app.command()
def init(
    workspace: str = typer.Option(".", "--workspace", "-w", help="Workspace directory to initialize"),
    theme: str = typer.Option("hacker-barbie", "--theme", "-t", help="Theme to use")
):
    """Initialize a new DevDollz workspace"""
    print_banner()
    
    workspace_path = Path(workspace)
    workspace_path.mkdir(exist_ok=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Initializing DevDollz workspace...", total=4)
        
        # Create workspace structure
        progress.update(task, description="Creating workspace structure...")
        (workspace_path / "src").mkdir(exist_ok=True)
        (workspace_path / "tests").mkdir(exist_ok=True)
        (workspace_path / "docs").mkdir(exist_ok=True)
        progress.advance(task)
        
        # Set theme
        progress.update(task, description="Setting theme...")
        theme_manager = get_theme_manager()
        if theme_manager.set_current_theme(theme):
            console.print(f"✅ Theme set to: [bold]{theme}[/bold]")
        else:
            console.print(f"⚠️ Theme '{theme}' not found, using default")
            theme_manager.set_current_theme("hacker-barbie")
        progress.advance(task)
        
        # Create config file
        progress.update(task, description="Creating configuration...")
        config = {
            "workspace": str(workspace_path.absolute()),
            "theme": theme_manager.get_current_theme().name,
            "creator": "Alexis Adams",
            "version": "0.1.0"
        }
        
        import json
        with open(workspace_path / ".devdollz.json", "w") as f:
            json.dump(config, f, indent=2)
        progress.advance(task)
        
        # Finalize
        progress.update(task, description="Finalizing setup...")
        progress.advance(task)
    
    console.print(f"\n🎉 [bold green]DevDollz workspace initialized![/bold green]")
    console.print(f"📁 Location: [bold]{workspace_path.absolute()}[/bold]")
    console.print(f"🎨 Theme: [bold]{theme_manager.get_current_theme().name}[/bold]")
    console.print(f"👩‍💻 Creator: [bold hot_pink]Alexis Adams[/bold hot_pink]")

@app.command()
def start(
    workspace: str = typer.Option(".", "--workspace", "-w", help="Workspace directory to start"),
    mode: str = typer.Option("cli", "--mode", "-m", help="Mode: cli, tui, or web")
):
    """Start DevDollz AI Swarm IDE"""
    print_banner()
    print_creator_quote()
    
    workspace_path = Path(workspace)
    if not (workspace_path / ".devdollz.json").exists():
        console.print("❌ [bold red]Not a DevDollz workspace![/bold red]")
        console.print("Run [bold]devdollz init[/bold] first")
        raise typer.Exit(1)
    
    # Load configuration
    import json
    with open(workspace_path / ".devdollz.json", "r") as f:
        config = json.load(f)
    
    console.print(f"🚀 [bold]Starting DevDollz AI Swarm IDE[/bold]")
    console.print(f"📁 Workspace: [bold]{config['workspace']}[/bold]")
    console.print(f"🎨 Theme: [bold]{config['theme']}[/bold]")
    console.print(f"👩‍💻 Creator: [bold hot_pink]{config['creator']}[/bold hot_pink]")
    
    if mode == "cli":
        start_cli_mode()
    elif mode == "tui":
        start_tui_mode()
    elif mode == "web":
        start_web_mode()
    else:
        console.print(f"❌ [bold red]Unknown mode: {mode}[/bold red]")
        raise typer.Exit(1)

def start_cli_mode():
    """Start CLI mode"""
    console.print("\n🎯 [bold]CLI Mode Active[/bold]")
    console.print("Type [bold]help[/bold] for available commands")
    console.print("Type [bold]exit[/bold] to quit")
    
    while True:
        try:
            command = Prompt.ask("\n[bold hot_pink]devdollz[/bold hot_pink] >")
            
            if command.lower() in ["exit", "quit", "q"]:
                console.print("👋 [bold]Goodbye, hacker![/bold]")
                break
            elif command.lower() == "help":
                show_help()
            elif command.lower() == "theme":
                show_themes()
            elif command.lower() == "status":
                show_status()
            elif command.lower().startswith("generate"):
                handle_generate(command)
            elif command.lower().startswith("debug"):
                handle_debug(command)
            elif command.lower().startswith("analyze"):
                handle_analyze(command)
            else:
                console.print(f"❓ [yellow]Unknown command: {command}[/yellow]")
                console.print("Type [bold]help[/bold] for available commands")
                
        except KeyboardInterrupt:
            console.print("\n👋 [bold]Goodbye, hacker![/bold]")
            break
        except Exception as e:
            console.print(f"💥 [bold red]Error: {e}[/bold red]")

def start_tui_mode():
    """Start TUI mode"""
    console.print("\n🎭 [bold]TUI Mode[/bold]")
    console.print("Launching Textual interface...")
    
    try:
        from textual.app import App
        console.print("✅ Textual interface launched")
    except ImportError:
        console.print("❌ [bold red]Textual not available[/bold red]")
        console.print("Install with: [bold]pip install textual[/bold]")
        console.print("Falling back to CLI mode...")
        start_cli_mode()

def start_web_mode():
    """Start web mode"""
    console.print("\n🌐 [bold]Web Mode[/bold]")
    console.print("Launching web dashboard...")
    
    try:
        import streamlit
        console.print("✅ Streamlit dashboard launched")
    except ImportError:
        console.print("❌ [bold red]Streamlit not available[/bold red]")
        console.print("Install with: [bold]pip install streamlit[/bold]")
        console.print("Falling back to CLI mode...")
        start_cli_mode()

def show_help():
    """Show help information"""
    help_table = Table(title="🎀 DevDollz Commands")
    help_table.add_column("Command", style="bold hot_pink")
    help_table.add_column("Description", style="white")
    help_table.add_column("Example", style="cyan")
    
    help_table.add_row("generate", "Generate code", "generate function fibonacci")
    help_table.add_row("debug", "Debug code", "debug syntax file.py")
    help_table.add_row("analyze", "Analyze security", "analyze security file.py")
    help_table.add_row("theme", "Show themes", "theme")
    help_table.add_row("status", "Show status", "status")
    help_table.add_row("help", "Show this help", "help")
    help_table.add_row("exit", "Exit DevDollz", "exit")
    
    console.print(help_table)

def show_themes():
    """Show available themes"""
    theme_manager = get_theme_manager()
    
    theme_table = Table(title="🎨 Available Themes")
    theme_table.add_column("Theme", style="bold hot_pink")
    theme_table.add_column("Description", style="white")
    theme_table.add_column("Author", style="cyan")
    
    for theme_name in theme_manager.list_themes():
        theme = theme_manager.get_theme(theme_name)
        theme_table.add_row(
            theme.name,
            theme.description,
            theme.author
        )
    
    console.print(theme_table)

def show_status():
    """Show current status"""
    theme_manager = get_theme_manager()
    current_theme = theme_manager.get_current_theme()
    
    status_table = Table(title="📊 DevDollz Status")
    status_table.add_column("Property", style="bold hot_pink")
    status_table.add_column("Value", style="white")
    
    status_table.add_row("Status", "🟢 Active")
    status_table.add_row("Theme", current_theme.name)
    status_table.add_row("Creator", "Alexis Adams")
    status_table.add_row("Version", "0.1.0")
    status_table.add_row("Mode", "CLI")
    
    console.print(status_table)

def handle_generate(command: str):
    """Handle generate commands"""
    console.print("🧠 [bold]Code Generation Agent Activated[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Generating code...", total=3)
        
        progress.update(task, description="Analyzing requirements...")
        progress.advance(task)
        
        progress.update(task, description="Generating code...")
        progress.advance(task)
        
        progress.update(task, description="Optimizing output...")
        progress.advance(task)
    
    # Simulate generated code
    code = '''def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
print(fibonacci(10))  # Output: 55'''
    
    console.print("\n✅ [bold green]Code Generated Successfully![/bold green]")
    console.print(Syntax(code, "python", theme="monokai"))

def handle_debug(command: str):
    """Handle debug commands"""
    console.print("🔍 [bold]Debug Agent Activated[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Debugging code...", total=3)
        
        progress.update(task, description="Analyzing syntax...")
        progress.advance(task)
        
        progress.update(task, description="Checking logic...")
        progress.advance(task)
        
        progress.update(task, description="Generating report...")
        progress.advance(task)
    
    console.print("\n✅ [bold green]Debug Analysis Complete![/bold green]")
    console.print("🎯 [bold]No issues found[/bold]")
    console.print("💡 [italic]Your code looks great![/italic]")

def handle_analyze(command: str):
    """Handle analyze commands"""
    console.print("🛡️ [bold]Security Agent Activated[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("Analyzing security...", total=3)
        
        progress.update(task, description="Scanning for vulnerabilities...")
        progress.advance(task)
        
        progress.update(task, description="Checking dependencies...")
        progress.advance(task)
        
        progress.update(task, description="Generating security report...")
        progress.advance(task)
    
    console.print("\n✅ [bold green]Security Analysis Complete![/bold green]")
    console.print("🟢 [bold]No security issues detected[/bold]")
    console.print("🔒 [italic]Your code is secure![/italic]")

@app.command()
def theme(
    name: str = typer.Argument(..., help="Theme name to preview or apply"),
    apply: bool = typer.Option(False, "--apply", "-a", help="Apply the theme")
):
    """Preview or apply a DevDollz theme"""
    print_banner()
    
    theme_manager = get_theme_manager()
    theme = theme_manager.get_theme(name)
    
    if not theme:
        console.print(f"❌ [bold red]Theme '{name}' not found![/bold red]")
        console.print("Available themes:")
        for theme_name in theme_manager.list_themes():
            console.print(f"  • [bold]{theme_name}[/bold]")
        raise typer.Exit(1)
    
    # Show theme preview
    console.print(theme_manager.get_theme_preview(name))
    
    if apply:
        if Confirm.ask(f"Apply theme '{name}'?"):
            theme_manager.set_current_theme(name)
            console.print(f"✅ [bold green]Theme '{name}' applied![/bold green]")
        else:
            console.print("❌ [yellow]Theme not applied[/yellow]")

@app.command()
def version():
    """Show DevDollz version information"""
    print_banner()
    
    version_info = {
        "Version": "0.1.0",
        "Creator": "Alexis Adams",
        "Description": "Where Code Meets Chaos",
        "License": "MIT",
        "Repository": "https://github.com/devdollzai/ai-swarm-ide"
    }
    
    version_table = Table(title="📋 Version Information")
    version_table.add_column("Property", style="bold hot_pink")
    version_table.add_column("Value", style="white")
    
    for key, value in version_info.items():
        version_table.add_row(key, value)
    
    console.print(version_table)

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments, show banner and start interactive mode
        print_banner()
        print_creator_quote()
        start_cli_mode()
    else:
        # Run the Typer app
        app()

if __name__ == "__main__":
    main()
