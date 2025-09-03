#!/usr/bin/env python3
"""
AI Swarm IDE - Enhanced Textual TUI with Code Editor Integration
Professional, frictionless AI development environment with real Ollama integration
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import sqlite3
import datetime
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: ollama not available. Install with: pip install ollama")

try:
    from textual.app import App, ComposeResult
    from textual.widgets import DirectoryTree, TextLog, Input, Header, Footer, Static, TextArea
    from textual.containers import Horizontal, Vertical
    from textual.reactive import reactive
    from textual.binding import Binding
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    print("Warning: textual not available. Install with: pip install textual")

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

# Helper function for Ollama calls with timeout
def call_ollama_with_timeout(prompt: str, model: str = 'mistral', timeout: int = 10) -> str:
    """Call Ollama with timeout using threading"""
    import threading
    import queue
    
    result_queue = queue.Queue()
    error_queue = queue.Queue()
    
    def ollama_worker():
        try:
            response = ollama.generate(model=model, prompt=prompt)
            result_queue.put(response)
        except Exception as e:
            error_queue.put(e)
    
    # Start Ollama call in a separate thread
    thread = threading.Thread(target=ollama_worker)
    thread.daemon = True
    thread.start()
    
    # Wait for result with timeout
    try:
        response = result_queue.get(timeout=timeout)
        result = response['response']
        return result
    except queue.Empty:
        raise TimeoutError(f"Ollama call timed out after {timeout} seconds")
    except Exception as e:
        if not error_queue.empty():
            raise error_queue.get()
        raise e

# LLM-Integrated Code Generation Agent
def code_gen_agent(input_queue: mp.Queue, output_queue: mp.Queue):
    """Code generation agent with real Ollama LLM integration"""
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
                
            task = parse_message(raw_task)
            task_type = task['meta'].get('type', 'code')
            task_content = task['content']
            
            if not OLLAMA_AVAILABLE:
                result = "Error: Ollama not available. Install with: pip install ollama"
                meta = {"status": "error", "error": "Ollama not available", "agent": "code_gen"}
                output_queue.put(create_message(result, meta))
                log_to_db("code_gen", task_content, result, "error")
                continue
            
            try:
                # Craft specific prompts for different task types
                if task_type == "function":
                    prompt = f"Generate a Python function for '{task_content}'. Include error handling and type hints. Follow PEP 8. Return only the code, no explanations."
                elif task_type == "class":
                    prompt = f"Generate a Python class for '{task_content}' with relevant methods. Include error handling and type hints. Follow PEP 8. Return only the code, no explanations."
                else:
                    prompt = f"Generate Python code for '{task_content}'. Include error handling and type hints where applicable. Follow PEP 8. Return only the code, no explanations."
                
                # Use the helper function for Ollama calls
                result = call_ollama_with_timeout(prompt)
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "code_gen"}
                output_queue.put(create_message(result, meta))
                log_to_db("code_gen", task_content, result, "success")
                
            except Exception as e:
                result = f"Error in code generation: {str(e)}"
                meta = {"status": "error", "error": str(e), "agent": "code_gen"}
                output_queue.put(create_message(result, meta))
                log_to_db("code_gen", task_content, result, "error")
            
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            result = f"Error in code generation: {str(e)}"
            meta = {"status": "error", "error": str(e), "agent": "code_gen"}
            output_queue.put(create_message(result, meta))
            log_to_db("code_gen", "unknown", result, "error")

# LLM-Integrated Debug Agent
def debug_agent(input_queue: mp.Queue, output_queue: mp.Queue):
    """Debugging agent with real Ollama LLM integration"""
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
                
            task = parse_message(raw_task)
            error_type = task['meta'].get('error_type', 'syntax')
            code_to_debug = task['content']
            
            if not OLLAMA_AVAILABLE:
                result = "Error: Ollama not available. Install with: pip install ollama"
                meta = {"status": "error", "error": "Ollama not available", "agent": "debug"}
                output_queue.put(create_message(result, meta))
                log_to_db("debug", code_to_debug, result, "error")
                continue
            
            try:
                # Craft specific prompts for different debug types
                if error_type == "logic":
                    prompt = f"Analyze this Python code for logical errors and potential issues (e.g., edge cases, performance): ```python\n{code_to_debug}\n```. Return only the analysis, no code or explanations."
                else:  # Default for syntax or other debug types
                    prompt = f"Analyze this Python code for {error_type} errors: ```python\n{code_to_debug}\n```. Return only the analysis, no code or explanations."
                
                # Use the helper function for Ollama calls
                result = call_ollama_with_timeout(prompt)
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "debug"}
                output_queue.put(create_message(result, meta))
                log_to_db("debug", code_to_debug, result, "success")
                
            except Exception as e:
                result = f"Error in debugging: {str(e)}"
                meta = {"status": "error", "error": str(e), "agent": "debug"}
                output_queue.put(create_message(result, meta))
                log_to_db("debug", code_to_debug, result, "error")
            
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            result = f"Error in debugging: {str(e)}"
            meta = {"status": "error", "error": str(e), "agent": "debug"}
            output_queue.put(create_message(result, meta))
            log_to_db("debug", "unknown", result, "error")

# Central Orchestrator
class Orchestrator:
    def __init__(self):
        self.code_gen_input = mp.Queue()
        self.code_gen_output = mp.Queue()
        self.debug_input = mp.Queue()
        self.debug_output = mp.Queue()

        self.code_gen_proc = mp.Process(target=code_gen_agent, args=(self.code_gen_input, self.code_gen_output))
        self.debug_proc = mp.Process(target=debug_agent, args=(self.debug_input, self.debug_output))

        self.code_gen_proc.start()
        self.debug_proc.start()

    def route_task(self, agent_type: str, cmd_type: str, task_content: str):
        """Route task to appropriate agent"""
        task_msg = create_message(task_content, {"type": cmd_type})
        if agent_type == "code_gen":
            self.code_gen_input.put(task_msg)
        elif agent_type == "debug":
            self.debug_input.put(task_msg)
        else:
            return {"content": "Unknown agent type", "meta": {"status": "error"}}

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all available results from agents"""
        results = []
        for output_queue in [self.code_gen_output, self.debug_output]:
            try:
                while not output_queue.empty():
                    raw_res = output_queue.get()
                    res = parse_message(raw_res)
                    results.append(res)
            except queue.Empty:
                pass
        return results

    def shutdown(self):
        """Clean shutdown of all agent processes"""
        self.code_gen_input.put("STOP")
        self.debug_input.put("STOP")
        self.code_gen_proc.join()
        self.debug_proc.join()

# DevDollz ASCII Logo
DEV_DOLLZ_LOGO = """
██████╗ ██╗██╗██╗██╗ ██╗ ██████╗ ██╗ ██╗ ███████╗
██╔══██╗██║██║ ██║██║ ██║██╔═══██╗██║ ██║ ╚══███╔╝
██║ ██║██║██║ ██║██║ ██║██║ ██║██║ ██║ ███╔╝
██║ ██║██║██║ ██║██║ ██║██║ ██║██║ ██║ ███╔╝
██████╔╝██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗███████╗
╚═════╝ ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
"""

# Enhanced Textual TUI App with Code Editor Integration
class SwarmIDEEnhancedApp(App):
    CSS = """
    $background: #1A1A1B;
    $primary: #D944D4;
    $panel: #2C2C2E;
    $success: #D944D4;
    $error: #E06C75;
    $text: #EAEAEB;
    $muted: #8A8A8E;

    Screen {
        background: $background;
        color: $text;
    }

    /* === HEADER & FOOTER === */
    Header {
        display: none; /* Hide default header */
    }
    #logo {
        color: $muted;
        height: auto;
        padding: 1 0;
    }
    Footer {
        background: $background;
        color: $muted;
    }

    /* === PANELS & CONTAINERS === */
    Horizontal, Vertical {
        background: $background;
    }

    DirectoryTree, TextLog, TextArea {
        background: $panel;
        border: sharp $panel;
        padding: 1 2;
    }

    /* === COMMAND INPUT === */
    Input {
        background: $background;
        border: sharp $muted;
        padding: 0 1;
        color: $text;
        height: 1;
    }

    Input:focus {
        border: sharp $primary;
    }

    Input > .input--placeholder {
        color: $muted;
        text-style: normal;
    }

    /* === CODE EDITOR === */
    TextArea {
        background: $panel;
        border: sharp $muted;
        color: $text;
    }

    TextArea:focus {
        border: sharp $primary;
    }

    /* === FILE & DIRECTORY TREE === */
    DirectoryTree > .directory-tree--file {
        color: $text;
    }
    DirectoryTree > .directory-tree--folder {
        color: $text;
    }
    DirectoryTree > .directory-tree--selected {
        background: $primary;
        color: $background;
        text-style: bold;
    }

    /* === RESULTS LOG === */
    TextLog {
        color: $text;
    }

    /* === SCROLLBARS === */
    ::-webkit-scrollbar {
        background: $panel;
        width: 1;
    }
    ::-webkit-scrollbar-thumb {
        background: $muted;
    }
    """

    BINDINGS = [
        Binding("ctrl+d", "debug_editor", "Debug Code in Editor"),
        Binding("ctrl+g", "generate_from_editor", "Generate from Editor"),
        Binding("?", "show_help", "Show Help"),
        Binding("tab", "focus_next", "Next Focus"),
    ]

    def __init__(self):
        super().__init__()
        self.orchestrator = Orchestrator()

    def compose(self) -> ComposeResult:
        yield Static(DEV_DOLLZ_LOGO, id="logo")
        yield Horizontal(
            DirectoryTree("./", id="file-tree"),
            Vertical(
                TextArea(id="code-editor", language="python", placeholder="Write or paste your code here..."),
                TextLog(id="results"),
                Input(placeholder="> Enter command...", id="command-input"),
                id="main-panel"
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Footer).update("DevDollz | Enhanced TUI Edition by Alexis Adams | Ctrl+D: Debug | Ctrl+G: Generate")
        self.query_one("#command-input").focus()
        self.set_interval(0.1, self.check_results)
        text_log = self.query_one("#results", TextLog)
        text_log.write("Welcome to the Enhanced Atelier. | DevDollz by Alexis Adams")
        text_log.write("Hotkeys: Ctrl+D (Debug Editor) | Ctrl+G (Generate from Editor)")

    def check_results(self) -> None:
        """Check for results from AI agents"""
        results = self.orchestrator.get_results()
        text_log = self.query_one("#results", TextLog)
        for res in results:
            status = res['meta'].get('status', 'unknown')
            if status == "success":
                text_log.write(f"[◆] {res['content']}")
            else:
                text_log.write(f"[x] {res['content']}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input submission"""
        text_log = self.query_one("#results", TextLog)
        command = event.value.strip()
        
        protocol_text = "Atelier Protocol:\n  generate [function|class|code] <description>\n  debug [syntax|logic|code] <code or description>"

        if command.lower() in ['quit', 'exit']:
            self.exit()
            return
        if command == 'help':
            text_log.write(protocol_text)
            return

        parts = command.split(maxsplit=2)
        if len(parts) < 2:
            text_log.write(f"Access Denied. Please verify command syntax.\n{protocol_text}")
            return

        action, cmd_type = parts[0], parts[1]
        task_content = parts[2] if len(parts) > 2 else ""

        if action not in ["generate", "debug"] or cmd_type not in ["function", "class", "code", "syntax", "logic"]:
            text_log.write(f"Access Denied. Please verify command syntax.\n{protocol_text}")
            return

        agent_type = "code_gen" if action == "generate" else "debug"
        text_log.write("[»] Crafting response...")
        self.orchestrator.route_task(agent_type, cmd_type, task_content)
        event.input.value = ""  # Clear input field

    def action_debug_editor(self) -> None:
        """Debug the code currently in the editor (Ctrl+D)"""
        text_log = self.query_one("#results", TextLog)
        code_editor = self.query_one("#code-editor", TextArea)
        
        if not code_editor.text.strip():
            text_log.write("[!] No code in editor to debug")
            return
            
        code_content = code_editor.text.strip()
        text_log.write(f"[»] Debugging code from editor ({len(code_content)} chars)...")
        
        # Route to debug agent with syntax analysis
        self.orchestrator.route_task("debug", "syntax", code_content)

    def action_generate_from_editor(self) -> None:
        """Generate code based on editor content (Ctrl+G)"""
        text_log = self.query_one("#results", TextLog)
        code_editor = self.query_one("#code-editor", TextArea)
        
        if not code_editor.text.strip():
            text_log.write("[!] No description in editor to generate from")
            return
            
        description = code_editor.text.strip()
        text_log.write(f"[»] Generating code from description ({len(description)} chars)...")
        
        # Route to code generation agent
        self.orchestrator.route_task("code_gen", "code", description)

    def action_show_help(self) -> None:
        """Show help information (?)"""
        text_log = self.query_one("#results", TextLog)
        text_log.write("Enhanced Atelier Protocol:")
        text_log.write("  generate [function|class|code] <description>")
        text_log.write("  debug [syntax|logic|code] <code or description>")
        text_log.write("  Ctrl+D: Debug code in editor")
        text_log.write("  Ctrl+G: Generate from editor content")
        text_log.write("  ?: Show this help")

    def on_unmount(self):
        """Cleanup on app exit"""
        self.orchestrator.shutdown()

# CLI Fallback (if Textual is unavailable)
def create_cli():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.key_binding import KeyBindings
    
    bindings = KeyBindings()
    @bindings.add('?')
    def _(event):
        event.app.exit(result='help')

    completer = WordCompleter(['generate function ', 'generate class ', 'generate code ', 
                               'debug syntax ', 'debug logic ', 'debug code '], ignore_case=True)
    session = PromptSession('> ')
    return session

def print_usage():
    print("Access Denied. Please verify command syntax.")
    print("Atelier Protocol:")
    print("  generate [function|class|code] <description>")
    print("  debug [syntax|logic|code] <code or description>")

# Main entry point
if __name__ == "__main__":
    try:
        if TEXTUAL_AVAILABLE:
            SwarmIDEEnhancedApp().run()
        else:
            # Fallback to CLI if Textual is not available
            print("Textual TUI not available. Falling back to CLI.")
            orch = Orchestrator()
            try:
                while True:
                    try:
                        command = input("> ")
                        if command.lower() in ['quit', 'exit']:
                            break
                        if command == 'help':
                            print_usage()
                            continue

                        parts = command.strip().split(maxsplit=2)
                        if len(parts) < 2:
                            print_usage()
                            continue

                        action, cmd_type = parts[0], parts[1]
                        task_content = parts[2] if len(parts) > 2 else ""

                        if action not in ["generate", "debug"] or cmd_type not in ["function", "class", "code", "syntax", "logic"]:
                            print_usage()
                            continue

                        agent_type = "code_gen" if action == "generate" else "debug"
                        print("[»] Crafting response...")
                        orch.route_task(agent_type, cmd_type, task_content)

                        time.sleep(0.1)  # Give agents a moment to process
                        results = orch.get_results()
                        for res in results:
                            status = res['meta'].get('status', 'unknown')
                            if status == "success":
                                print(f"[◆] {res['content']}")
                            else:
                                print(f"[x] {res['content']}")

                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        print(f"[x] Error: {str(e)}")
                        print_usage()
            finally:
                orch.shutdown()
                print("Shutdown complete.")
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install textual ollama")
