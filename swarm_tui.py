#!/usr/bin/env python3
"""
AI Swarm IDE - Textual TUI Interface
Professional split-panel interface with sharp CLI experience
"""

import asyncio
import json
import sqlite3
import datetime
import multiprocessing as mp
import queue
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static, Button, TextLog, Tree
from textual.reactive import reactive
from textual import work
from textual.binding import Binding

# Import our enhanced Swarm IDE components
from swarm_ide_enhanced import (
    SwarmOrchestrator, Command, CommandType, 
    create_message, parse_message, log_to_db
)

# Command structure and validation
class CommandType(Enum):
    GENERATE = "generate"
    DEBUG = "debug"

@dataclass
class Command:
    type: CommandType
    subcommand: str
    description: str
    
    @classmethod
    def parse(cls, input_text: str) -> Optional['Command']:
        """Parse command with strict validation"""
        parts = input_text.strip().split(maxsplit=2)
        if len(parts) < 2:
            return None
            
        try:
            cmd_type = CommandType(parts[0].lower())
            subcommand = parts[1].lower()
            
            if cmd_type == CommandType.GENERATE and subcommand not in ['function', 'class', 'code']:
                return None
            if cmd_type == CommandType.DEBUG and subcommand not in ['syntax', 'logic', 'code']:
                return None
                
            description = parts[2] if len(parts) > 2 else ""
            return cls(type=cmd_type, subcommand=subcommand, description=description)
        except ValueError:
            return None

# TUI Components
class CommandInput(Input):
    """Enhanced command input with validation"""
    
    def __init__(self):
        super().__init__(
            placeholder="Enter command (e.g., 'generate function calc' or 'debug syntax def x:')",
            id="command-input"
        )
        self.validation_error = False

class OutputPanel(TextLog):
    """Output display panel with formatting"""
    
    def __init__(self):
        super().__init__(id="output-panel")
        self.markup = True
    
    def add_success(self, content: str):
        """Add success message with formatting"""
        self.write(f"[bold green]✓ SUCCESS[/bold green]\n{content}\n")
    
    def add_error(self, content: str):
        """Add error message with formatting"""
        self.write(f"[bold red]✗ ERROR[/bold red]\n{content}\n")
    
    def add_info(self, content: str):
        """Add info message with formatting"""
        self.write(f"[bold blue]ℹ INFO[/bold blue]\n{content}\n")
    
    def add_separator(self):
        """Add visual separator"""
        self.write("─" * 80 + "\n")

class StatusPanel(Static):
    """Real-time status display"""
    
    def __init__(self):
        super().__init__("🤖 AI Swarm IDE - Ready", id="status-panel")
        self.status = reactive("Ready")
    
    def update_status(self, status: str):
        """Update status display"""
        self.status = status
        self.update(f"🤖 AI Swarm IDE - {status}")

class HistoryPanel(Tree):
    """Command history tree"""
    
    def __init__(self):
        super().__init__("Command History", id="history-panel")
        self.root.expand()
    
    def add_command(self, command: str, result: str, status: str):
        """Add command to history"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        status_icon = "✓" if status == "success" else "✗"
        
        # Create command node
        cmd_node = self.root.add(f"{status_icon} {timestamp}: {command}")
        
        # Add result as child node
        result_preview = result[:50] + "..." if len(result) > 50 else result
        cmd_node.add(f"Result: {result_preview}")

# Main TUI Application
class SwarmTUI(App):
    """Main TUI application with split panels"""
    
    CSS = """
    #main-container {
        height: 100%;
        width: 100%;
    }
    
    #left-panel {
        width: 30%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #right-panel {
        width: 70%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #command-input {
        height: 3;
        margin: 1;
    }
    
    #output-panel {
        height: 60%;
        border: solid $accent;
        padding: 1;
        background: $surface;
    }
    
    #status-panel {
        height: 3;
        margin: 1;
        text-align: center;
        color: $accent;
    }
    
    #history-panel {
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #button-container {
        height: 4;
        margin: 1;
    }
    
    .error {
        color: $error;
    }
    
    .success {
        color: $success;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+l", "clear_output", "Clear Output"),
        Binding("ctrl+h", "show_help", "Help"),
        Binding("f1", "show_help", "Help"),
        Binding("tab", "focus_next", "Next Panel"),
    ]
    
    def __init__(self):
        super().__init__()
        self.orchestrator = None
        self.command_history = []
        
    def compose(self) -> ComposeResult:
        """Compose the TUI layout"""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal():
                # Left Panel - History and Status
                with Container(id="left-panel"):
                    yield StatusPanel()
                    yield HistoryPanel()
                
                # Right Panel - Command Input and Output
                with Container(id="right-panel"):
                    with Vertical():
                        yield CommandInput()
                        
                        with Container(id="button-container"):
                            with Horizontal():
                                yield Button("Generate Code", id="generate-btn", variant="primary")
                                yield Button("Debug Code", id="debug-btn", variant="warning")
                                yield Button("Clear Output", id="clear-btn", variant="default")
                                yield Button("Help", id="help-btn", variant="default")
                        
                        yield OutputPanel()
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application"""
        self.status_panel = self.query_one(StatusPanel)
        self.output_panel = self.query_one(OutputPanel)
        self.history_panel = self.query_one(HistoryPanel)
        self.command_input = self.query_one(CommandInput)
        
        # Initialize orchestrator
        self.init_orchestrator()
        
        # Focus on command input
        self.command_input.focus()
        
        # Show welcome message
        self.output_panel.add_info("🤖 AI Swarm IDE - Enhanced TUI")
        self.output_panel.add_info("Type commands or use the buttons above")
        self.output_panel.add_info("Press F1 or Ctrl+H for help")
        self.output_panel.add_separator()
    
    def init_orchestrator(self):
        """Initialize the Swarm orchestrator"""
        try:
            self.orchestrator = SwarmOrchestrator()
            self.status_panel.update_status("Ready")
        except Exception as e:
            self.output_panel.add_error(f"Failed to initialize orchestrator: {e}")
            self.status_panel.update_status("Error")
    
    def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle command input submission"""
        command = message.value.strip()
        if not command:
            return
        
        # Clear input
        self.command_input.value = ""
        
        # Process command
        self.process_command(command)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        
        if button_id == "generate-btn":
            self.command_input.value = "generate function "
            self.command_input.focus()
        elif button_id == "debug-btn":
            self.command_input.value = "debug syntax "
            self.command_input.focus()
        elif button_id == "clear-btn":
            self.action_clear_output()
        elif button_id == "help-btn":
            self.action_show_help()
    
    def process_command(self, command: str):
        """Process command with instant validation and execution"""
        # Add to history
        self.command_history.append(command)
        
        # Show command in output
        self.output_panel.add_info(f"Executing: {command}")
        
        # Parse command with strict validation
        parsed_cmd = Command.parse(command)
        if not parsed_cmd:
            self.show_usage_error()
            return
        
        # Execute command
        self.execute_command(parsed_cmd)
    
    def execute_command(self, parsed_cmd: Command):
        """Execute parsed command"""
        try:
            self.status_panel.update_status("Processing...")
            
            # Route task to appropriate agent
            agent_type = "code_gen" if parsed_cmd.type == CommandType.GENERATE else "debug"
            
            if not self.orchestrator.route_task(agent_type, parsed_cmd.subcommand, parsed_cmd.description):
                self.output_panel.add_error("Failed to route task to agent")
                self.status_panel.update_status("Error")
                return
            
            # Get results with minimal delay
            time.sleep(0.1)
            results = self.orchestrator.get_results()
            
            if not results:
                self.output_panel.add_error("No results received from agent")
                self.status_panel.update_status("Error")
                return
            
            # Process results
            for res in results:
                status = res['meta'].get('status', 'unknown')
                content = res['content']
                
                if status == 'success':
                    self.output_panel.add_success(content)
                    # Add to history panel
                    self.history_panel.add_command(
                        f"{parsed_cmd.type.value} {parsed_cmd.subcommand}",
                        content,
                        "success"
                    )
                else:
                    self.output_panel.add_error(content)
                    # Add to history panel
                    self.history_panel.add_command(
                        f"{parsed_cmd.type.value} {parsed_cmd.subcommand}",
                        content,
                        "error"
                    )
            
            self.status_panel.update_status("Ready")
            
        except Exception as e:
            self.output_panel.add_error(f"Execution failed: {str(e)}")
            self.status_panel.update_status("Error")
    
    def show_usage_error(self):
        """Show sharp usage error"""
        self.output_panel.add_error("Unknown command.")
        self.output_panel.add_info("Usage:")
        self.output_panel.add_info("  generate [function|class|code] <description>")
        self.output_panel.add_info("  debug [syntax|logic|code] <code or description>")
        self.output_panel.add_info("Examples:")
        self.output_panel.add_info("  generate function calculate_sum")
        self.output_panel.add_info("  debug syntax def foo(: pass")
    
    def action_clear_output(self):
        """Clear output panel"""
        self.output_panel.clear()
        self.output_panel.add_info("Output cleared. Ready for new commands...")
    
    def action_show_help(self):
        """Show comprehensive help"""
        self.output_panel.clear()
        self.output_panel.add_info("🤖 AI Swarm IDE - Command Reference")
        self.output_panel.add_separator()
        
        self.output_panel.add_info("Code Generation:")
        self.output_panel.add_info("  generate function <name>     - Generate a function")
        self.output_panel.add_info("  generate class <name>        - Generate a class")
        self.output_panel.add_info("  generate code <description>  - Generate general code")
        self.output_panel.add_separator()
        
        self.output_panel.add_info("Code Analysis:")
        self.output_panel.add_info("  debug syntax <code>          - Check syntax validity")
        self.output_panel.add_info("  debug logic <code>           - Analyze logical flow")
        self.output_panel.add_info("  debug code <code>            - General code review")
        self.output_panel.add_separator()
        
        self.output_panel.add_info("Navigation:")
        self.output_panel.add_info("  Ctrl+Q                       - Quit application")
        self.output_panel.add_info("  Ctrl+L                       - Clear output")
        self.output_panel.add_info("  F1 or Ctrl+H                 - Show this help")
        self.output_panel.add_info("  Tab                          - Navigate panels")
        self.output_panel.add_separator()
        
        self.output_panel.add_info("Tips:")
        self.output_panel.add_info("  • Use buttons for quick access")
        self.output_panel.add_info("  • Commands are case-insensitive")
        self.output_panel.add_info("  • Be specific with descriptions")
    
    def on_app_exit(self) -> None:
        """Clean shutdown when app exits"""
        if self.orchestrator:
            self.orchestrator.shutdown()

# Main entry point
def main():
    """Main application entry point"""
    # Set multiprocessing start method for Windows compatibility
    if mp.get_start_method(allow_none=True) != 'spawn':
        mp.set_start_method('spawn', force=True)
    
    try:
        # Start TUI
        app = SwarmTUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
