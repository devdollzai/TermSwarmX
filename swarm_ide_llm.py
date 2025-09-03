#!/usr/bin/env python3
"""
AI Swarm IDE - LLM-Integrated Sharp CLI Interface
Professional, frictionless AI development terminal with real Ollama integration
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
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter, Completer, Completion
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.styles import Style
    from pygments.lexers.python import PythonLexer
    from pygments.styles import get_style_by_name
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False
    print("Warning: prompt_toolkit not available. Using basic input.")

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: ollama not available. Install with: pip install ollama")

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
        print(f"✅ Ollama response received: {result[:100]}...")
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
    print("🚀 Code gen agent started")
    message_count = 0
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                print("🛑 Code gen agent stopping")
                break
            message_count += 1
            print(f"📨 Code gen agent received message #{message_count}")
                
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
                # Extract task_id from metadata
                task_id = task['meta'].get('task_id', 'unknown')
                print(f"🤖 Code gen agent processing task: {task_id}")
                
                # Craft specific prompts for different task types
                if task_type == "function":
                    prompt = f"Generate a Python function for '{task_content}' that reads a CSV file into a pandas DataFrame. Include error handling and type hints. Follow PEP 8. Return only the code, no explanations, no conversational text, no markdown formatting outside of the code block itself."
                elif task_type == "class":
                    prompt = f"Generate a Python class for '{task_content}' with methods for logging messages to a file. Include error handling and type hints. Follow PEP 8. Return only the code, no explanations, no conversational text, no markdown formatting outside of the code block itself."
                elif task_type == "code":
                    prompt = f"Generate Python code for '{task_content}' using Flask and JWT. Include input validation, secure password checking, and error handling. Follow PEP 8. Return only the code, no explanations, no conversational text, no markdown formatting outside of the code block itself."
                else:
                    prompt = f"Generate a Python {task_type} for '{task_content}'. Return only the code, no explanations, no conversational text, no markdown formatting outside of the code block itself."
                
                print(f"📝 Calling Ollama with prompt: {prompt[:100]}...")
                
                # Use the helper function for Ollama calls
                result = call_ollama_with_timeout(prompt)
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "code_gen", "task_id": task_id}
                output_queue.put(create_message(result, meta))
                print(f"📤 Result sent to output queue with task_id: {task_id}")
                log_to_db("code_gen", task_content, result, "success")
                
            except Exception as e:
                print(f"❌ Error in code generation: {str(e)}")
                import traceback
                traceback.print_exc()
                result = f"Error in code generation: {str(e)}"
                task_id = task['meta'].get('task_id', 'unknown')
                meta = {"status": "error", "error": str(e), "agent": "code_gen", "task_id": task_id}
                output_queue.put(create_message(result, meta))
                log_to_db("code_gen", task_content, result, "error")
            
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            result = f"Error in code generation: {str(e)}"
            meta = {"status": "error", "error": str(e), "agent": "code_gen", "task_id": "unknown"}
            output_queue.put(create_message(result, meta))
            log_to_db("code_gen", "unknown", result, "error")

# LLM-Integrated Debug Agent
def debug_agent(input_queue: mp.Queue, output_queue: mp.Queue):
    """Debugging agent with real Ollama LLM integration"""
    print("🚀 Debug agent started")
    message_count = 0
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                print("🛑 Debug agent stopping")
                break
            message_count += 1
            print(f"📨 Debug agent received message #{message_count}")
                
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
                # Extract task_id from metadata
                task_id = task['meta'].get('task_id', 'unknown')
                print(f"🤖 Debug agent processing task: {task_id}")
                
                # Craft specific prompts for different debug types
                if error_type == "logic":
                    prompt = f"Analyze this Python code for logical errors and potential issues (e.g., edge cases, performance): ```python\n{code_to_debug}\n```. Return only the analysis, no code or explanations, no conversational text."
                else:  # Default for syntax or other debug types
                    prompt = f"Analyze this Python code for {error_type} errors: ```python\n{code_to_debug}\n```. Return only the analysis, no code or explanations, no conversational text."
                
                print(f"📝 Calling Ollama with prompt: {prompt[:100]}...")
                
                # Call Ollama with timeout using threading
                import threading
                import queue
                
                result_queue = queue.Queue()
                error_queue = queue.Queue()
                
                def ollama_worker():
                    try:
                        response = ollama.generate(model='mistral', prompt=prompt)
                        result_queue.put(response)
                    except Exception as e:
                        error_queue.put(e)
                
                # Start Ollama call in a separate thread
                thread = threading.Thread(target=ollama_worker)
                thread.daemon = True
                thread.start()
                
                # Wait for result with timeout
                try:
                    response = result_queue.get(timeout=10)
                    result = response['response']
                    print(f"✅ Ollama response received: {result[:100]}...")
                except queue.Empty:
                    raise TimeoutError("Ollama call timed out after 10 seconds")
                except Exception as e:
                    if not error_queue.empty():
                        raise error_queue.get()
                    raise e
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "debug", "task_id": task_id}
                output_queue.put(create_message(result, meta))
                print(f"📤 Result sent to output queue with task_id: {task_id}")
                log_to_db("debug", code_to_debug, result, "success")
                
            except Exception as e:
                print(f"❌ Error in debugging: {str(e)}")
                import traceback
                traceback.print_exc()
                result = f"Error in debugging: {str(e)}"
                task_id = task['meta'].get('task_id', 'unknown')
                meta = {"status": "error", "error": str(e), "agent": "debug", "task_id": task_id}
                output_queue.put(create_message(result, meta))
                log_to_db("debug", code_to_debug, result, "error")
            
        except queue.Empty:
            time.sleep(0.1)
        except Exception as e:
            result = f"Error in debugging: {str(e)}"
            meta = {"status": "error", "error": str(e), "agent": "debug", "task_id": "unknown"}
            output_queue.put(create_message(result, meta))
            log_to_db("debug", "unknown", result, "error")

# Central Orchestrator
class SwarmOrchestrator:
    def __init__(self):
        self.code_gen_queue = mp.Queue()
        self.debug_queue = mp.Queue()
        self.result_queue = mp.Queue()
        self.task_queue = mp.Queue()  # Add missing task_queue
        self.agents: Dict[str, mp.Process] = {}
        self.task_counter = 0

    def register_agent(self, role: str, process: mp.Process):
        self.agents[role] = process

    async def dispatch_task(self, role: str, content: str, task_id: str):
        if role == "code_gen":
            message = create_message(content, {"type": "code", "task_id": task_id})
            self.code_gen_queue.put(message)
        elif role == "debug":
            message = create_message(content, {"type": "syntax", "task_id": task_id})
            self.debug_queue.put(message)
        else:
            message = create_message(content, {"type": role, "task_id": task_id})
            self.code_gen_queue.put(message)
        
        return await self._wait_for_result(task_id)

    async def _wait_for_result(self, task_id: str) -> Optional[str]:
        timeout = 30.0  # 30 second timeout for LLM calls
        start_time = asyncio.get_event_loop().time()
        print(f"🔍 Waiting for result with task_id: {task_id}")
        
        while True:
            if asyncio.get_event_loop().time() - start_time > timeout:
                print(f"⏰ Timeout waiting for task_id: {task_id}")
                return "Task timed out"
                
            try:
                if not self.result_queue.empty():
                    raw_result = self.result_queue.get_nowait()
                    result = parse_message(raw_result)
                    result_task_id = result["meta"].get("task_id", "unknown")
                    print(f"📥 Received result with task_id: {result_task_id}, looking for: {task_id}")
                    if result_task_id == task_id:
                        print(f"✅ Task ID match! Returning result for: {task_id}")
                        return result["content"]
                    else:
                        print(f"❌ Task ID mismatch. Expected: {task_id}, got: {result_task_id}")
                        # Put the result back in the queue for the correct task
                        self.result_queue.put(raw_result)
            except Exception as e:
                print(f"⚠️ Error processing result: {e}")
                pass
                
            await asyncio.sleep(0.1)

    def submit_task(self, role: str, content: str) -> str:
        """Submit a task and return task ID"""
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1
        
        if role == "code_gen":
            message = create_message(content, {"type": "code", "task_id": task_id})
            self.code_gen_queue.put(message)  # Use correct queue
        elif role == "debug":
            message = create_message(content, {"type": "syntax", "task_id": task_id})
            self.debug_queue.put(message)  # Use correct queue
        else:
            return "Unknown role"
            
        return task_id

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all available results"""
        results = []
        try:
            while not self.result_queue.empty():
                raw_result = self.result_queue.get_nowait()
                result = parse_message(raw_result)
                results.append(result)
        except queue.Empty:
            pass
        return results

    def shutdown(self):
        """Clean shutdown of all agent processes"""
        for process in self.agents.values():
            if process.is_alive():
                process.terminate()
                process.join(timeout=2)
                if process.is_alive():
                    process.kill()

# Enhanced Sharp CLI Interface
class EnhancedSharpCLI:
    def __init__(self, orchestrator: SwarmOrchestrator):
        self.orchestrator = orchestrator
        self.running = True
        self.setup_interface()
        
    def setup_interface(self):
        """Setup the CLI interface"""
        if PROMPT_TOOLKIT_AVAILABLE:
            self.completer = WordCompleter(['generate', 'debug', 'help', 'quit', 'exit'])
            self.key_bindings = KeyBindings()
            
            @self.key_bindings.add('?')
            def show_help(event):
                self.show_help()
                
            self.session = PromptSession(
                completer=self.completer,
                key_bindings=self.key_bindings,
                lexer=PygmentsLexer(PythonLexer),
                style=Style.from_dict({
                    'prompt': 'ansicyan',
                    'input': 'ansiwhite',
                })
            )
        else:
            self.session = None
            
    def show_usage(self):
        """Display sharp, concise usage information"""
        print("Usage:")
        print("  generate [function|class|code] <description>")
        print("  debug [syntax|logic|code] <code or description>")
        print("  help")
        print("  quit")
        print("")
        print("Examples:")
        print("  generate function calculate_sum")
        print("  debug syntax def foo(: pass")
        
    def show_help(self):
        """Display detailed help"""
        print("AI Swarm IDE - Command Reference")
        print("=" * 40)
        print("")
        print("Code Generation:")
        print("  generate function <name>     - Generate a function")
        print("  generate class <name>        - Generate a class")
        print("  generate code <description>  - Generate general code")
        print("")
        print("Code Analysis:")
        print("  debug syntax <code>          - Check syntax validity")
        print("  debug logic <code>           - Analyze logical flow")
        print("  debug code <code>            - General code review")
        print("")
        print("Navigation:")
        print("  help                         - Show this help")
        print("  quit, exit, q               - Exit the application")
        print("")
        print("Tips:")
        print("  • Use TAB for command completion")
        print("  • Press ? for help")
        print("  • Commands are case-insensitive")
        print("  • Be specific with descriptions")
        
    def show_error(self, message: str):
        """Display sharp error message"""
        print(f"Error: {message}")
        
    def show_unknown_command(self):
        """Display unknown command error with usage hint"""
        self.show_error("Unknown command.")
        print("")
        self.show_usage()
        
    def format_output(self, content: str) -> str:
        """Format output for clean display"""
        # Remove markdown code blocks for cleaner output
        if content.startswith("```python"):
            content = content.replace("```python", "").replace("```", "")
        return content.strip()
        
    async def process_command(self, input_text: str):
        """Process command with instant validation"""
        if not input_text.strip():
            return
            
        if input_text.lower() in ['quit', 'exit', 'q']:
            self.running = False
            return
            
        if input_text.lower() == 'help':
            self.show_help()
            return
            
        # Parse command with strict validation
        command = Command.parse(input_text)
        if not command:
            self.show_unknown_command()
            return
            
        # Route to appropriate agent
        try:
            if command.type == CommandType.GENERATE:
                agent_type = "code_gen"
                task_content = f"{command.subcommand}: {command.description}"
            else:  # DEBUG
                agent_type = "debug"
                task_content = command.description
                
            print(f"🤖 Routing to {agent_type} agent...")
            result = await self.orchestrator.dispatch_task(agent_type, task_content, f"task_{int(time.time())}")
            
            if result:
                print("✅ Result:")
                print(self.format_output(result))
            else:
                print("❌ No result received")
                
        except Exception as e:
            print(f"Error: Execution failed - {str(e)}")
        
    async def run(self):
        """Main CLI loop with enhanced UX"""
        print("🤖 AI Swarm IDE - LLM-Integrated Sharp CLI")
        print("=" * 50)
        
        if not OLLAMA_AVAILABLE:
            print("⚠️  Warning: Ollama not available. Install with: pip install ollama")
            print("   The system will show errors for LLM operations.")
        else:
            print("✅ Ollama integration available")
            
        print("")
        self.show_usage()
        print("")
        
        while self.running:
            try:
                if self.session:
                    user_input = await self.session.prompt_async("🤖> ")
                else:
                    user_input = input("🤖> ")
                    
                await self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"Unexpected error: {e}")

# Tab completion for prompt_toolkit
class SwarmCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        
        if len(words) == 0:
            yield Completion('generate', start_position=0, display='generate [function|class|code]')
            yield Completion('debug', start_position=0, display='debug [syntax|logic|code]')
            yield Completion('help', start_position=0, display='help')
            yield Completion('quit', start_position=0, display='quit')
            
        elif len(words) == 1:
            first_word = words[0].lower()
            if first_word.startswith('g'):
                yield Completion('generate', start_position=-len(first_word), display='generate [function|class|code]')
            elif first_word.startswith('d'):
                yield Completion('debug', start_position=-len(first_word), display='debug [syntax|logic|code]')
            elif first_word.startswith('h'):
                yield Completion('help', start_position=-len(first_word), display='help')
            elif first_word.startswith('q'):
                yield Completion('quit', start_position=-len(first_word), display='quit')
                
        elif len(words) == 2:
            first_word = words[0].lower()
            second_word = words[1].lower()
            
            if first_word == 'generate':
                if second_word.startswith('f'):
                    yield Completion('function', start_position=-len(second_word), display='function <name>')
                elif second_word.startswith('c'):
                    if second_word.startswith('cl'):
                        yield Completion('class', start_position=-len(second_word), display='class <name>')
                    else:
                        yield Completion('code', start_position=-len(second_word), display='code <description>')
                        
            elif first_word == 'debug':
                if second_word.startswith('s'):
                    yield Completion('syntax', start_position=-len(second_word), display='syntax <code>')
                elif second_word.startswith('l'):
                    yield Completion('logic', start_position=-len(second_word), display='logic <code>')
                elif second_word.startswith('c'):
                    yield Completion('code', start_position=-len(second_word), display='code <code>')

# Main entry point
def main():
    """Main application entry point"""
    try:
        # Set multiprocessing start method
        mp.set_start_method('spawn', force=True)
        
        # Initialize orchestrator
        orchestrator = SwarmOrchestrator()
        
        # Start agents
        code_gen_proc = mp.Process(target=code_gen_agent, args=(orchestrator.code_gen_queue, orchestrator.result_queue))
        debug_proc = mp.Process(target=debug_agent, args=(orchestrator.debug_queue, orchestrator.result_queue))
        
        code_gen_proc.start()
        debug_proc.start()
        
        orchestrator.register_agent("code_gen", code_gen_proc)
        orchestrator.register_agent("debug", debug_proc)
        
        # Start CLI
        cli = EnhancedSharpCLI(orchestrator)
        
        # Run CLI
        asyncio.run(cli.run())
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if 'orchestrator' in locals():
            orchestrator.shutdown()

if __name__ == "__main__":
    main()
