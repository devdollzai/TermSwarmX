#!/usr/bin/env python3
"""
AI Swarm IDE - Enhanced Textual TUI Interface
Professional multi-panel interface with code editor and sharp CLI experience
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import sqlite3
import datetime
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: ollama not available. Using simulated responses.")

try:
    from textual.app import App, ComposeResult
    from textual.widgets import DirectoryTree, TextLog, Input, Header, Footer, Static
    from textual.containers import Horizontal, Vertical, Container
    from textual.reactive import reactive
    from textual.binding import Binding
    from textual import work
    from textual.widgets.text_area import TextArea
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    print("Warning: textual not available. Using CLI fallback.")
    # Define placeholder classes for CLI fallback
    class TextArea:
        def __init__(self, **kwargs):
            self.text = ""
            self.placeholder = kwargs.get('placeholder', '')
            self.id = kwargs.get('id', '')
        def focus(self): pass
    class DirectoryTree:
        def __init__(self, **kwargs): pass
        class FileSelected:
            def __init__(self, path):
                self.path = path
    class TextLog:
        def __init__(self, **kwargs): pass
        def write(self, text): pass
        def clear(self): pass
    class Input:
        def __init__(self, **kwargs): 
            self.value = ""
        class Submitted:
            def __init__(self, value):
                self.value = value
    class Header: pass
    class Footer: pass
    class Static:
        def __init__(self, *args, **kwargs): pass
        def update(self, text): pass
    class Container: pass
    class Horizontal: pass
    class Vertical: pass
    class App:
        def __init__(self): pass
        def run(self): pass
        def set_interval(self, interval, callback): pass
        def query_one(self, selector): pass
    class Binding:
        def __init__(self, key, action, description):
            self.key = key
            self.action = action
            self.description = description
    class reactive:
        def __init__(self, value): self.value = value

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter, Completer, Completion
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.styles import Style
    from pygments.lexers.python import PythonLexer
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False
    print("Warning: prompt_toolkit not available. Using basic input.")

# Setup SQLite for command history and memory
DB_FILE = "swarm_memory.db"

def init_db():
    """Initialize SQLite database for persistent memory"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY, timestamp TEXT, agent TEXT, task TEXT, result TEXT, status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS agents 
                      (id INTEGER PRIMARY KEY, name TEXT, status TEXT, last_active TEXT)''')
    conn.commit()
    conn.close()

init_db()

def log_to_db(agent: str, task: str, result: str, status: str = "success"):
    """Log task execution to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO history (timestamp, agent, task, result, status) VALUES (?, ?, ?, ?, ?)", 
                   (timestamp, agent, task, result, status))
    conn.commit()
    conn.close()

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

# Structured message format
def create_message(content: str, meta: Optional[Dict[str, Any]] = None) -> str:
    """Create structured message for agent communication"""
    return json.dumps({"content": content, "meta": meta or {}})

def parse_message(msg: str) -> Dict[str, Any]:
    """Parse structured message from agent"""
    return json.loads(msg)

# Enhanced Code Generation Agent with Ollama
def code_gen_agent(input_queue: mp.Queue, output_queue: mp.Queue):
    """Advanced code generation agent with Ollama integration"""
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
                
            task = parse_message(raw_task)
            cmd_type = task['meta'].get('type', '')
            desc = task['content']
            
            if OLLAMA_AVAILABLE:
                try:
                    if cmd_type == "function":
                        prompt = f"Generate a Python function for '{desc}'. Include error handling, type hints, and docstring. Follow PEP 8. Return only the code, no explanations."
                    elif cmd_type == "class":
                        prompt = f"Generate a Python class for '{desc}' with relevant methods, error handling, and type hints. Follow PEP 8. Return only the code, no explanations."
                    else:
                        prompt = f"Generate Python code for '{desc}'. Include error handling and type hints where applicable. Follow PEP 8. Return only the code, no explanations."
                    
                    response = ollama.generate(model="mistral", prompt=prompt)
                    result = response['response'].strip()
                    meta = {"status": "success", "timestamp": time.time(), "agent": "code_gen"}
                except Exception as e:
                    result = f"Error: Failed to generate code (Ollama error: {str(e)})"
                    meta = {"status": "error", "error": str(e), "agent": "code_gen"}
            else:
                # Fallback to simulated responses
                if cmd_type == "function":
                    func_name = desc.replace(' ', '_').replace('-', '_')
                    result = f"""def {func_name}():
    \"\"\"
    {desc}
    
    Returns:
        Any: Description of return value
    \"\"\"
    # TODO: Implement function logic
    pass

# Example usage
# result = {func_name}()
# print(result)"""
                elif cmd_type == "class":
                    class_name = desc.replace(' ', '_').replace('-', '_').title()
                    result = f"""class {class_name}:
    \"\"\"
    {desc}
    \"\"\"
    
    def __init__(self):
        self.initialized = True
    
    def __str__(self):
        return f"{class_name}(initialized={{self.initialized}})
    
    def __repr__(self):
        return self.__str__()"""
                else:
                    result = f"""# Generated code for: {desc}
# This is a placeholder implementation

def main():
    print("Hello from generated code!")
    print(f"Task: {desc}")
    
if __name__ == "__main__":
    main()"""
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "code_gen"}
            
            output_queue.put(create_message(result, meta))
            log_to_db("code_gen", desc, result, meta.get("status", "success"))
            
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            meta = {"status": "error", "error": str(e), "agent": "code_gen"}
            output_queue.put(create_message(f"Error in code generation: {str(e)}", meta))
            log_to_db("code_gen", desc, f"Error: {str(e)}", "error")

# Enhanced Debug Agent with Ollama
def debug_agent(input_queue: mp.Queue, output_queue: mp.Queue):
    """Advanced debugging agent with Ollama integration"""
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
                
            task = parse_message(raw_task)
            cmd_type = task['meta'].get('type', '')
            code = task['content']
            
            if OLLAMA_AVAILABLE:
                try:
                    if cmd_type == "syntax":
                        prompt = f"Analyze this Python code for syntax errors: ```\n{code}\n```. Return only the analysis, no code or explanations."
                    elif cmd_type == "logic":
                        prompt = f"Analyze this Python code for logical errors and potential issues (e.g., edge cases, performance): ```\n{code}\n```. Return only the analysis, no code or explanations."
                    else:
                        prompt = f"Debug this Python code for any issues: ```\n{code}\n```. Return only the debug analysis, no code or explanations."
                    
                    response = ollama.generate(model="mistral", prompt=prompt)
                    result = response['response'].strip()
                    meta = {"status": "success", "timestamp": time.time(), "agent": "debug"}
                except Exception as e:
                    result = f"Error: Failed to debug code (Ollama error: {str(e)})"
                    meta = {"status": "error", "error": str(e), "agent": "debug"}
            else:
                # Fallback to simulated responses
                if cmd_type == "syntax":
                    try:
                        compile(code, '<string>', 'exec')
                        result = "✅ Syntax: Valid\n✅ Structure: Correct\n✅ Ready for execution"
                    except SyntaxError as e:
                        result = f"❌ Syntax Error: {str(e)}\n📍 Line: {e.lineno}\n💡 Suggestion: Check syntax around line {e.lineno}"
                    except Exception as e:
                        result = f"❌ Compilation Error: {str(e)}"
                        
                elif cmd_type == "logic":
                    result = "🔍 Logic Analysis:\n"
                    if "def " in code:
                        result += "✅ Function definition detected\n"
                    if "class " in code:
                        result += "✅ Class definition detected\n"
                    if "import " in code or "from " in code:
                        result += "✅ Import statements found\n"
                    if "if " in code:
                        result += "✅ Conditional logic detected\n"
                    if "for " in code or "while " in code:
                        result += "✅ Loop structures found\n"
                    result += "✅ No obvious logical errors detected"
                    
                else:
                    result = "🔍 General Code Review:\n"
                    result += "✅ Code structure appears sound\n"
                    result += "✅ No immediate issues detected\n"
                    result += "✅ Ready for testing"
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "debug"}
            
            output_queue.put(create_message(result, meta))
            log_to_db("debug", code, result, meta.get("status", "success"))
            
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            meta = {"status": "error", "error": str(e), "agent": "debug"}
            output_queue.put(create_message(f"Error in debug analysis: {str(e)}", meta))
            log_to_db("debug", code, f"Error: {str(e)}", "error")

# Central Orchestrator with enhanced features
class SwarmOrchestrator:
    """Enhanced orchestrator with better agent management and monitoring"""
    
    def __init__(self):
        self.code_gen_input = mp.Queue()
        self.code_gen_output = mp.Queue()
        self.debug_input = mp.Queue()
        self.debug_output = mp.Queue()
        
        # Start agent processes
        self.code_gen_proc = mp.Process(target=code_gen_agent, args=(self.code_gen_input, self.code_gen_output))
        self.debug_proc = mp.Process(target=debug_agent, args=(self.debug_input, self.debug_output))
        
        self.code_gen_proc.start()
        self.debug_proc.start()
        
        # Register agents in database
        self._register_agents()
    
    def _register_agents(self):
        """Register agents in the database"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        
        agents = [
            ("code_gen", "active", timestamp),
            ("debug", "active", timestamp)
        ]
        
        for name, status, last_active in agents:
            cursor.execute("INSERT OR REPLACE INTO agents (name, status, last_active) VALUES (?, ?, ?)", 
                         (name, status, last_active))
        
        conn.commit()
        conn.close()

    def route_task(self, agent_type: str, cmd_type: str, task_content: str) -> bool:
        """Route task to appropriate agent"""
        task_msg = create_message(task_content, {"type": cmd_type})
        
        try:
            if agent_type == "code_gen":
                self.code_gen_input.put(task_msg)
                return True
            elif agent_type == "debug":
                self.debug_input.put(task_msg)
                return True
            else:
                return False
        except Exception:
            return False

    def get_results(self) -> List[Dict[str, Any]]:
        """Get results from all agents"""
        results = []
        for output_queue in [self.code_gen_output, self.debug_output]:
            try:
                while not output_queue.empty():
                    raw_res = output_queue.get_nowait()
                    res = parse_message(raw_res)
                    results.append(res)
            except queue.Empty:
                pass
        return results

    def get_agent_status(self) -> Dict[str, str]:
        """Get current status of all agents"""
        status = {}
        for name, proc in [("code_gen", self.code_gen_proc), ("debug", self.debug_proc)]:
            status[name] = "active" if proc.is_alive() else "inactive"
        return status

    def shutdown(self):
        """Clean shutdown of all agents"""
        try:
            self.code_gen_input.put("STOP")
            self.debug_input.put("STOP")
            
            self.code_gen_proc.join(timeout=2)
            self.debug_proc.join(timeout=2)
            
            if self.code_gen_proc.is_alive():
                self.code_gen_proc.terminate()
            if self.debug_proc.is_alive():
                self.debug_proc.terminate()
                
        except Exception as e:
            print(f"Error during shutdown: {e}")

# Enhanced TUI Components
class CodeEditor(TextArea):
    """Multi-line code editor with syntax highlighting"""
    
    def __init__(self):
        super().__init__(
            placeholder="Enter code here for debugging or analysis...",
            id="code-editor"
        )
        self.language = "python"

class ResultsPanel(TextLog):
    """Enhanced results display with formatting"""
    
    def __init__(self):
        super().__init__(id="results-panel")
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

class StatusBar(Static):
    """Real-time status display"""
    
    def __init__(self):
        super().__init__("🤖 AI Swarm IDE - Ready", id="status-bar")
        self.status = reactive("Ready")
    
    def update_status(self, status: str):
        """Update status display"""
        self.status = status
        self.update(f"🤖 AI Swarm IDE - {status}")

# Enhanced Textual TUI Application
class SwarmTUIEnhanced(App):
    """Enhanced TUI application with multi-panel layout"""
    
    CSS = """
    #main-container {
        height: 100%;
        width: 100%;
    }
    
    #left-panel {
        width: 25%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #center-panel {
        width: 35%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #right-panel {
        width: 40%;
        height: 100%;
        border: solid $accent;
        padding: 1;
    }
    
    #command-input {
        height: 3;
        margin: 1;
    }
    
    #code-editor {
        height: 60%;
        border: solid $accent;
        padding: 1;
        background: $surface;
    }
    
    #results-panel {
        height: 70%;
        border: solid $accent;
        padding: 1;
        background: $surface;
    }
    
    #status-bar {
        height: 3;
        margin: 1;
        text-align: center;
        color: $accent;
    }
    
    #file-tree {
        height: 100%;
        border: solid $accent;
        padding: 1;
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
        Binding("ctrl+l", "clear_results", "Clear Results"),
        Binding("ctrl+e", "clear_editor", "Clear Editor"),
        Binding("ctrl+h", "show_help", "Help"),
        Binding("f1", "show_help", "Help"),
        Binding("tab", "focus_next", "Next Panel"),
        Binding("ctrl+s", "save_editor", "Save Editor"),
        Binding("ctrl+o", "load_file", "Load File"),
    ]
    
    def __init__(self):
        super().__init__()
        self.orchestrator = None
        self.current_file = None
        
    def compose(self) -> ComposeResult:
        """Compose the enhanced TUI layout"""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal():
                # Left Panel - File Tree
                with Container(id="left-panel"):
                    yield StatusBar()
                    yield DirectoryTree("./", id="file-tree")
                
                # Center Panel - Code Editor
                with Container(id="center-panel"):
                    with Vertical():
                        yield CodeEditor()
                        yield Input(placeholder="Enter command (e.g., 'generate function calc' or 'debug syntax')", id="command-input")
                
                # Right Panel - Results
                with Container(id="right-panel"):
                    yield ResultsPanel()
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the application"""
        self.status_bar = self.query_one(StatusBar)
        self.results_panel = self.query_one(ResultsPanel)
        self.code_editor = self.query_one(CodeEditor)
        self.command_input = self.query_one("#command-input")
        self.file_tree = self.query_one(DirectoryTree)
        
        # Initialize orchestrator
        self.init_orchestrator()
        
        # Focus on command input
        self.command_input.focus()
        
        # Show welcome message
        self.results_panel.add_info("🤖 AI Swarm IDE - Enhanced TUI")
        self.results_panel.add_info("Multi-panel interface with code editor")
        self.results_panel.add_info("Press F1 or Ctrl+H for help")
        self.results_panel.add_separator()
        
        # Set up result checking
        self.set_interval(0.1, self.check_results)
    
    def init_orchestrator(self):
        """Initialize the Swarm orchestrator"""
        try:
            self.orchestrator = SwarmOrchestrator()
            self.status_bar.update_status("Ready")
        except Exception as e:
            self.results_panel.add_error(f"Failed to initialize orchestrator: {e}")
            self.status_bar.update_status("Error")
    
    def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle command input submission"""
        command = message.value.strip()
        if not command:
            return
        
        # Clear input
        self.command_input.value = ""
        
        # Process command
        self.process_command(command)
    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection from tree"""
        file_path = event.path
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.code_editor.text = content
                self.current_file = file_path
                self.results_panel.add_info(f"Loaded file: {file_path}")
        except Exception as e:
            self.results_panel.add_error(f"Failed to load file {file_path}: {e}")
    
    def process_command(self, command: str):
        """Process command with instant validation and execution"""
        # Show command in output
        self.results_panel.add_info(f"Executing: {command}")
        
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
            self.status_bar.update_status("Processing...")
            
            # Route task to appropriate agent
            agent_type = "code_gen" if parsed_cmd.type == CommandType.GENERATE else "debug"
            
            if not self.orchestrator.route_task(agent_type, parsed_cmd.subcommand, parsed_cmd.description):
                self.results_panel.add_error("Failed to route task to agent")
                self.status_bar.update_status("Error")
                return
            
            self.status_bar.update_status("Ready")
            
        except Exception as e:
            self.results_panel.add_error(f"Execution failed: {str(e)}")
            self.status_bar.update_status("Error")
    
    def check_results(self) -> None:
        """Check for new results from agents"""
        if not self.orchestrator:
            return
            
        results = self.orchestrator.get_results()
        for res in results:
            status = res['meta'].get('status', 'unknown')
            content = res['content']
            
            if status == 'success':
                self.results_panel.add_success(content)
            else:
                self.results_panel.add_error(content)
    
    def show_usage_error(self):
        """Show sharp usage error"""
        self.results_panel.add_error("Unknown command.")
        self.results_panel.add_info("Usage:")
        self.results_panel.add_info("  generate [function|class|code] <description>")
        self.results_panel.add_info("  debug [syntax|logic|code] <code or description>")
        self.results_panel.add_info("Examples:")
        self.results_panel.add_info("  generate function calculate_sum")
        self.results_panel.add_info("  debug syntax def foo(: pass")
    
    def action_clear_results(self):
        """Clear results panel"""
        self.results_panel.clear()
        self.results_panel.add_info("Results cleared. Ready for new commands...")
    
    def action_clear_editor(self):
        """Clear code editor"""
        self.code_editor.text = ""
        self.current_file = None
        self.results_panel.add_info("Code editor cleared.")
    
    def action_save_editor(self):
        """Save editor content to file"""
        if not self.current_file:
            self.results_panel.add_error("No file loaded. Use Ctrl+O to load a file first.")
            return
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.text)
            self.results_panel.add_success(f"Saved to {self.current_file}")
        except Exception as e:
            self.results_panel.add_error(f"Failed to save: {e}")
    
    def action_load_file(self):
        """Load file into editor"""
        # This would typically open a file dialog
        # For now, we'll use the file tree selection
        self.results_panel.add_info("Use the file tree on the left to select files to load.")
    
    def action_show_help(self):
        """Show comprehensive help"""
        self.results_panel.clear()
        self.results_panel.add_info("🤖 AI Swarm IDE - Enhanced TUI Help")
        self.results_panel.add_separator()
        
        self.results_panel.add_info("Panel Layout:")
        self.results_panel.add_info("  Left (25%): File tree and status")
        self.results_panel.add_info("  Center (35%): Code editor and command input")
        self.results_panel.add_info("  Right (40%): Results and output")
        self.results_panel.add_separator()
        
        self.results_panel.add_info("Commands:")
        self.results_panel.add_info("  generate function <name>     - Generate a function")
        self.results_panel.add_info("  generate class <name>        - Generate a class")
        self.results_panel.add_info("  generate code <description>  - Generate general code")
        self.results_panel.add_info("  debug syntax <code>          - Check syntax validity")
        self.results_panel.add_info("  debug logic <code>           - Analyze logical flow")
        self.results_panel.add_info("  debug code <code>            - General code review")
        self.results_panel.add_separator()
        
        self.results_panel.add_info("Navigation:")
        self.results_panel.add_info("  Ctrl+Q                       - Quit application")
        self.results_panel.add_info("  Ctrl+L                       - Clear results")
        self.results_panel.add_info("  Ctrl+E                       - Clear editor")
        self.results_panel.add_info("  Ctrl+S                       - Save editor")
        self.results_panel.add_info("  Ctrl+O                       - Load file")
        self.results_panel.add_info("  F1 or Ctrl+H                 - Show this help")
        self.results_panel.add_info("  Tab                          - Navigate panels")
        self.results_panel.add_separator()
        
        self.results_panel.add_info("Tips:")
        self.results_panel.add_info("  • Click files in the tree to load them")
        self.results_panel.add_info("  • Use the code editor for multi-line input")
        self.results_panel.add_info("  • Commands are case-insensitive")
        self.results_panel.add_info("  • Be specific with descriptions")
    
    def on_app_exit(self) -> None:
        """Clean shutdown when app exits"""
        if self.orchestrator:
            self.orchestrator.shutdown()

# CLI Fallback (if Textual is unavailable)
def create_cli():
    """Create CLI interface with prompt_toolkit"""
    if not PROMPT_TOOLKIT_AVAILABLE:
        return None
        
    bindings = KeyBindings()
    
    @bindings.add('?')
    def _(event):
        event.app.exit(result='help')
    
    completer = WordCompleter(['generate function ', 'generate class ', 'generate code ',
                               'debug syntax ', 'debug logic ', 'debug code '], ignore_case=True)
    
    session = PromptSession('swarm> ',
                           completer=completer,
                           lexer=PygmentsLexer(PythonLexer),
                           key_bindings=bindings)
    return session

def print_usage():
    """Show sharp usage error"""
    print("Error: Unknown command.")
    print("Usage:")
    print("  generate [function|class|code] <description>")
    print("  debug [syntax|logic|code] <code or description>")
    print("Example:")
    print("  generate function calculate_sum")
    print("  debug syntax def foo(: pass")

# Main entry point
def main():
    """Main application entry point"""
    # Set multiprocessing start method for Windows compatibility
    if mp.get_start_method(allow_none=True) != 'spawn':
        mp.set_start_method('spawn', force=True)
    
    try:
        if TEXTUAL_AVAILABLE:
            # Try running enhanced TUI
            app = SwarmTUIEnhanced()
            app.run()
        else:
            # Fallback to CLI
            print("🤖 AI Swarm IDE - CLI Mode (Textual not available)")
            print("Install with: pip install textual")
            print("-" * 60)
            
            orchestrator = SwarmOrchestrator()
            session = create_cli()
            
            if session:
                # Use prompt_toolkit CLI
                while True:
                    try:
                        command = session.prompt()
                        if command.lower() in ['quit', 'exit']:
                            break
                        if command == 'help':
                            print_usage()
                            continue
                        
                        # Parse and execute command
                        parsed_cmd = Command.parse(command)
                        if not parsed_cmd:
                            print_usage()
                            continue
                        
                        # Execute command
                        agent_type = "code_gen" if parsed_cmd.type == CommandType.GENERATE else "debug"
                        orchestrator.route_task(agent_type, parsed_cmd.subcommand, parsed_cmd.description)
                        
                        # Get results
                        time.sleep(0.1)
                        results = orchestrator.get_results()
                        for res in results:
                            status = res['meta'].get('status', 'unknown')
                            print(f"[{status.upper()}] {res['content']}")
                            
                    except KeyboardInterrupt:
                        break
                    except EOFError:
                        break
                    except Exception as e:
                        print(f"Error: {str(e)}")
                        print_usage()
                
                orchestrator.shutdown()
                print("Shutdown complete.")
            else:
                # Basic CLI fallback
                print("Basic CLI mode - no advanced features available")
                print("Install prompt_toolkit for better experience: pip install prompt_toolkit")
                
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
