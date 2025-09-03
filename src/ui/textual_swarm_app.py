"""
Textual TUI Application for AI Swarm IDE
Provides a modern terminal-based user interface
"""

import asyncio
import threading
import time
from typing import Dict, Any, Optional
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Input, TextLog, Button, 
    Static, DataTable, Label, ProgressBar
)
from textual.reactive import reactive
from textual.worker import Worker, get_current_worker
from textual import work

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.multiprocessing_orchestrator import MultiprocessingOrchestrator
from agents.enhanced_multiprocessing_agents import (
    enhanced_code_gen_agent,
    enhanced_debug_agent,
    enhanced_analysis_agent,
    file_mgmt_agent,
    get_task_history,
    get_agent_stats,
    init_db
)

class SwarmStatusWidget(Static):
    """Widget to display swarm status"""
    
    def __init__(self):
        super().__init__("🤖 Swarm Status: Initializing...")
        self.status_data = {}
    
    def update_status(self, status_data: Dict[str, Any]):
        """Update the status display"""
        self.status_data = status_data
        self.update(f"🤖 Swarm Status: {status_data.get('active_agents', 0)} active agents, {status_data.get('pending_tasks', 0)} pending tasks")

class TaskHistoryWidget(DataTable):
    """Widget to display task history"""
    
    def __init__(self):
        super().__init__()
        self.add_columns("Time", "Agent", "Type", "Status", "Content")
        self.add_rows([])
    
    def update_history(self, history: list):
        """Update the task history table"""
        self.clear()
        for record in history[:20]:  # Show last 20 records
            timestamp = record['timestamp'][:19] if len(record['timestamp']) > 19 else record['timestamp']
            content = record['task_content'][:30] + "..." if len(record['task_content']) > 30 else record['task_content']
            status_icon = "✅" if record['status'] == "success" else "❌"
            
            self.add_row(
                timestamp,
                record['agent'],
                record['task_type'],
                f"{status_icon} {record['status']}",
                content
            )

class AgentStatsWidget(DataTable):
    """Widget to display agent statistics"""
    
    def __init__(self):
        super().__init__()
        self.add_columns("Agent", "Status", "Completed", "Failed", "Success Rate")
        self.add_rows([])
    
    def update_stats(self, stats: Dict[str, Any]):
        """Update the agent statistics table"""
        self.clear()
        for agent_name, agent_stats in stats.items():
            completed = agent_stats['tasks_completed']
            failed = agent_stats['tasks_failed']
            total = completed + failed
            success_rate = f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
            
            self.add_row(
                agent_name,
                agent_stats['current_status'],
                str(completed),
                str(failed),
                success_rate
            )

class SwarmApp(App):
    """Main Textual application for AI Swarm IDE"""
    
    CSS = """
    #main-container {
        height: 100%;
        layout: horizontal;
    }
    
    #left-panel {
        width: 30%;
        height: 100%;
        border-right: solid green;
        layout: vertical;
    }
    
    #right-panel {
        width: 70%;
        height: 100%;
        layout: vertical;
    }
    
    #status-widget {
        height: 10%;
        border-bottom: solid blue;
        padding: 1;
    }
    
    #input-section {
        height: 15%;
        border-bottom: solid blue;
        padding: 1;
    }
    
    #results-section {
        height: 75%;
        padding: 1;
    }
    
    #history-panel {
        height: 50%;
        border-bottom: solid green;
        padding: 1;
    }
    
    #stats-panel {
        height: 50%;
        padding: 1;
    }
    
    .title {
        text-align: center;
        color: yellow;
        text-style: bold;
    }
    
    Button {
        margin: 1;
    }
    
    Input {
        margin: 1;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.orchestrator = None
        self.background_thread = None
        self.running = False
        
        # Initialize database
        init_db()
    
    def compose(self) -> ComposeResult:
        """Compose the application layout"""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            with Container(id="left-panel"):
                yield Label("📊 Swarm Information", classes="title")
                
                with Container(id="history-panel"):
                    yield Label("📋 Task History", classes="title")
                    yield TaskHistoryWidget(id="task-history")
                
                with Container(id="stats-panel"):
                    yield Label("🤖 Agent Statistics", classes="title")
                    yield AgentStatsWidget(id="agent-stats")
            
            with Container(id="right-panel"):
                with Container(id="status-widget"):
                    yield SwarmStatusWidget(id="swarm-status")
                
                with Container(id="input-section"):
                    yield Label("💬 Command Input", classes="title")
                    yield Input(placeholder="Enter command (e.g., gen: create a function)", id="command-input")
                    
                    with Horizontal():
                        yield Button("Generate Code", id="gen-btn", variant="primary")
                        yield Button("Debug Code", id="debug-btn", variant="warning")
                        yield Button("Analyze Code", id="analyze-btn", variant="info")
                        yield Button("File Op", id="file-btn", variant="success")
                
                with Container(id="results-section"):
                    yield Label("📤 Results & Logs", classes="title")
                    yield TextLog(id="results-log")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.title = "AI Swarm IDE - Enhanced TUI"
        self.sub_title = "Multiprocessing Agent Coordination System"
        
        # Start the orchestrator in a background thread
        self.start_orchestrator()
        
        # Start background updates
        self.set_interval(2.0, self.update_ui)
    
    def start_orchestrator(self):
        """Start the orchestrator in a background thread"""
        def run_orchestrator():
            try:
                self.orchestrator = MultiprocessingOrchestrator(max_workers=4)
                
                # Register enhanced agents
                self.orchestrator.register_agent(
                    name="EnhancedCodeGenAgent",
                    agent_type="code_generation",
                    agent_function=enhanced_code_gen_agent,
                    capabilities=["code_generation", "function_creation", "class_creation", "llm_integration"],
                    model_name="mistral"
                )
                
                self.orchestrator.register_agent(
                    name="EnhancedDebugAgent",
                    agent_type="debugging",
                    agent_function=enhanced_debug_agent,
                    capabilities=["debugging", "error_analysis", "syntax_checking", "persistent_memory"]
                )
                
                self.orchestrator.register_agent(
                    name="EnhancedAnalysisAgent",
                    agent_type="analysis",
                    agent_function=enhanced_analysis_agent,
                    capabilities=["code_analysis", "quality_assessment", "metrics_calculation", "llm_integration"]
                )
                
                self.orchestrator.register_agent(
                    name="FileManagementAgent",
                    agent_type="file_management",
                    agent_function=file_mgmt_agent,
                    capabilities=["file_operations", "directory_listing", "file_reading", "file_writing"]
                )
                
                self.running = True
                
                # Log startup
                self.log_message("🚀 AI Swarm IDE TUI started successfully")
                self.log_message(f"✅ Registered {len(self.orchestrator.agents)} enhanced agents")
                
            except Exception as e:
                self.log_message(f"❌ Error starting orchestrator: {e}")
        
        self.background_thread = threading.Thread(target=run_orchestrator, daemon=True)
        self.background_thread.start()
        
        # Wait a moment for startup
        time.sleep(2)
    
    def log_message(self, message: str):
        """Log a message to the results section"""
        results_log = self.query_one("#results-log", TextLog)
        timestamp = time.strftime("%H:%M:%S")
        results_log.write(f"[{timestamp}] {message}")
    
    def update_ui(self):
        """Update the UI with current data"""
        if not self.orchestrator or not self.running:
            return
        
        try:
            # Update swarm status
            status = self.orchestrator.get_status()
            status_widget = self.query_one("#swarm-status", SwarmStatusWidget)
            status_widget.update_status(status['stats'])
            
            # Update task history
            history = get_task_history(limit=20)
            history_widget = self.query_one("#task-history", TaskHistoryWidget)
            history_widget.update_history(history)
            
            # Update agent statistics
            agent_stats = get_agent_stats()
            stats_widget = self.query_one("#agent-stats", AgentStatsWidget)
            stats_widget.update_stats(agent_stats)
            
            # Check for new results
            results = self.orchestrator.get_results()
            if results:
                for result in results:
                    agent_name = result['agent_name']
                    if 'error' in result:
                        self.log_message(f"❌ {agent_name}: {result['error']}")
                    else:
                        self.log_message(f"✅ {agent_name}: Task completed successfully")
            
            # Process pending tasks
            self.orchestrator.process_pending_tasks()
            
        except Exception as e:
            self.log_message(f"⚠️  Error updating UI: {e}")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input submission"""
        command = event.value.strip()
        if not command:
            return
        
        self.log_message(f"💬 Command: {command}")
        self.process_command(command)
        
        # Clear input
        event.input.value = ""
    
    def process_command(self, command: str):
        """Process a user command"""
        if not self.orchestrator or not self.running:
            self.log_message("❌ Orchestrator not ready")
            return
        
        try:
            if command.startswith('gen:'):
                task = command[4:].strip()
                self.orchestrator.route_task("code_generation", {
                    "title": f"Generate: {task}",
                    "requirements": task,
                    "language": "python",
                    "context": "TUI user request"
                })
                self.log_message(f"📝 Code generation task submitted: {task}")
                
            elif command.startswith('debug:'):
                code = command[6:].strip()
                self.orchestrator.route_task("debugging", {
                    "title": "Debug code",
                    "code": code,
                    "error_message": "User requested debugging",
                    "context": "TUI debugging session"
                })
                self.log_message(f"🐛 Debug task submitted for code: {code[:30]}...")
                
            elif command.startswith('analyze:'):
                code = command[8:].strip()
                self.orchestrator.route_task("analysis", {
                    "title": "Analyze code",
                    "code": code,
                    "analysis_type": "comprehensive"
                })
                self.log_message(f"📊 Analysis task submitted for code: {code[:30]}...")
                
            elif command.startswith('file:'):
                task = command[5:].strip()
                self.orchestrator.route_task("file_management", {
                    "title": f"File operation: {task}",
                    "operation": task
                })
                self.log_message(f"📁 File operation submitted: {task}")
                
            elif command.startswith('read:'):
                filename = command[5:].strip()
                self.orchestrator.route_task("file_management", {
                    "title": f"Read file: {filename}",
                    "operation": "read",
                    "filename": filename
                })
                self.log_message(f"📄 File read task submitted: {filename}")
                
            elif command.startswith('write:'):
                parts = command[6:].split(":", 1)
                if len(parts) == 2:
                    filename, content = parts
                    self.orchestrator.route_task("file_management", {
                        "title": f"Write file: {filename}",
                        "operation": "write",
                        "filename": filename.strip(),
                        "content": content.strip()
                    })
                    self.log_message(f"✍️  File write task submitted: {filename}")
                else:
                    self.log_message("❌ Invalid write format. Use: write:filename:content")
                    
            else:
                self.log_message(f"❓ Unknown command: {command}")
                self.log_message("💡 Try: gen:, debug:, analyze:, file:, read:, or write:")
                
        except Exception as e:
            self.log_message(f"❌ Error processing command: {e}")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        
        if button_id == "gen-btn":
            self.log_message("💡 Enter a code generation request in the input field")
            self.log_message("   Example: gen: create a function to calculate factorial")
            
        elif button_id == "debug-btn":
            self.log_message("💡 Enter code to debug in the input field")
            self.log_message("   Example: debug: def test(): x = 10; print(x + y)")
            
        elif button_id == "analyze-btn":
            self.log_message("💡 Enter code to analyze in the input field")
            self.log_message("   Example: analyze: def func(): return 42")
            
        elif button_id == "file-btn":
            self.log_message("💡 Enter a file operation in the input field")
            self.log_message("   Examples: file: list_files, read: filename, write: filename:content")
    
    def on_key(self, event):
        """Handle keyboard shortcuts"""
        if event.key == "ctrl+q":
            self.exit()
        elif event.key == "ctrl+r":
            self.log_message("🔄 Refreshing UI...")
            self.update_ui()
    
    def on_exit(self) -> None:
        """Called when the app is exiting"""
        if self.orchestrator and self.running:
            self.log_message("🛑 Shutting down orchestrator...")
            self.orchestrator.shutdown()
            self.running = False

def main():
    """Main entry point for the TUI application"""
    app = SwarmApp()
    app.run()

if __name__ == "__main__":
    main()
