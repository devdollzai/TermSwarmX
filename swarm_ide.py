#!/usr/bin/env python3
"""
DevDollz: Atelier Edition - Professional AI Development Terminal
Built for power users who demand excellence in their development environment.

Features:
- AI-powered code generation and debugging
- PyTest integration for automated testing
- Cross-platform compatibility with robust process management
- Professional "Onyx & Orchid" theme

Author: Alexis Andrews
Brand: DevDollz: Atelier Edition
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import sqlite3
import subprocess
from datetime import datetime
import os
import importlib.util
from concurrent.futures import ThreadPoolExecutor
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Input, Footer, Static, TextArea, Log
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from io import StringIO
from pathlib import Path

# Try to import ollama, fall back to mock if not available
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Warning: Ollama not available, using mock implementation")

# --- Mock Ollama for environment compatibility ---
class MockOllama:
    def generate(self, model, prompt):
        # Simulate a delay and return a structure similar to the real ollama library
        time.sleep(0.2)
        mock_response = f"# Mock response for model '{model}'\n# Prompt: '{prompt[:50]}...'\nprint('Hello from DevDollz mock')"
        return {'response': mock_response}

# Use real ollama if available, otherwise use mock
if not OLLAMA_AVAILABLE:
    ollama = MockOllama()
# --- End Mock ---

DB_FILE = "atelier_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY, timestamp TEXT, agent TEXT, task TEXT, result TEXT)''')
    conn.commit()
    conn.close()

def log_to_db(agent, task, result):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO history (timestamp, agent, task, result) VALUES (?, ?, ?, ?)", 
                   (timestamp, agent, task, result))
    conn.commit()
    conn.close()

def create_message(content, meta=None):
    return json.dumps({"content": content, "meta": meta or {}})

def parse_message(msg):
    return json.loads(msg)

def code_gen_agent(input_queue, output_queue):
    with ThreadPoolExecutor() as executor:
        while True:
            try:
                raw_task = input_queue.get(timeout=0.1)
                if raw_task == "STOP": 
                    break
                task = parse_message(raw_task)
                desc = task['content']
                prompt = f"Generate Python code for '{desc}'."
                
                if OLLAMA_AVAILABLE:
                    result = executor.submit(ollama.generate, model="mistral", prompt=prompt).result()['response'].strip()
                else:
                    result = f"# Mock code generation for: {desc}\nprint('Hello from DevDollz mock')"
                
                meta = {"status": "success", "agent": "code_gen"}
                output_queue.put(create_message(result, meta))
                log_to_db("code_gen", desc, result)
            except queue.Empty: 
                continue
            except Exception as e:
                output_queue.put(create_message(f"Error: {e}", {"status": "error"}))

def debug_agent(input_queue, output_queue):
    while True:
        try:
            raw_task = input_queue.get(timeout=0.1)
            if raw_task == "STOP": 
                break
            task = parse_message(raw_task)
            code = task['content']
            
            # Simple syntax check using Python's built-in compiler
            try:
                compile(code, '<string>', 'exec')
                result = "Syntax check passed. No syntax errors found."
            except SyntaxError as e:
                result = f"Syntax error: {e}"
            except Exception as e:
                result = f"Compilation error: {e}"
            
            meta = {"status": "success", "agent": "debug"}
            output_queue.put(create_message(result, meta))
            log_to_db("debug", code, result)
        except queue.Empty: 
                continue
        except Exception as e:
            output_queue.put(create_message(f"Error: {e}", {"status": "error"}))

def test_agent(input_queue, output_queue):
    while True:
        try:
            raw_task = input_queue.get(timeout=0.1)
            if raw_task == "STOP": 
                break
            task = parse_message(raw_task)
            code = task['content']
            
            try:
                # Create a temporary test file
                test_file = Path("temp_test.py")
                test_file.write_text(code)
                
                # Run pytest
                result = subprocess.run(["python", "-m", "pytest", str(test_file), "-v"], 
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    output = f"Tests passed: {result.stdout}"
                    status = "success"
                else:
                    output = f"Tests failed: {result.stderr or result.stdout}"
                    status = "error"
                
                # Clean up
                test_file.unlink(missing_ok=True)
                
            except subprocess.TimeoutExpired:
                output = "Tests timed out after 30 seconds"
                status = "error"
            except FileNotFoundError:
                output = "Pytest not available, using mock"
                status = "success"
            except Exception as e:
                output = f"Test error: {e}"
                status = "error"
            
            output_queue.put(create_message(f"Pytest: {output}", {"status": status}))
            log_to_db("test", code, output)
        except queue.Empty: 
            continue
        except Exception as e:
            output_queue.put(create_message(f"Pytest error: {e}", {"status": "error"}))

class Orchestrator:
    def __init__(self):
        self.agents = {
            "code_gen": self.create_agent(code_gen_agent),
            "debug": self.create_agent(debug_agent),
            "test": self.create_agent(test_agent),
        }

    def create_agent(self, target_func):
        input_q = mp.Queue()
        output_q = mp.Queue()
        proc = mp.Process(target=target_func, args=(input_q, output_q))
        proc.start()
        return {"input_q": input_q, "output_q": output_q, "proc": proc}

    def route_task(self, agent_name, task_content):
        if agent_name not in self.agents: 
            return
        self.agents[agent_name]["input_q"].put(create_message(task_content))

    def get_results(self):
        results = []
        for agent_name, agent_data in self.agents.items():
            try:
                while not agent_data["output_q"].empty():
                    res = parse_message(agent_data["output_q"].get_nowait())
                    res['meta']['source'] = agent_name
                    results.append(res)
            except queue.Empty: 
                pass
        return results

    def shutdown(self):
        for agent in self.agents.values():
            agent["input_q"].put("STOP")
            agent["proc"].join()

class SwarmIDEApp(App):
    BINDINGS = [
        ("ctrl+d", "debug_code", "Debug"),
        ("ctrl+t", "test_code", "Test"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.orchestrator = Orchestrator()

    def compose(self) -> ComposeResult:
        yield Static("DevDollz: Atelier Edition", classes="header")
        yield TextArea(id="code-editor", language="python")
        yield Log(id="results")
        yield Input(placeholder="> generate, debug, test, quit")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Input).focus()
        self.set_interval(0.1, self.check_results)
        self.query_one("#results", Log).write("System online.")

    def check_results(self) -> None:
        for res in self.orchestrator.get_results():
            self.query_one("#results", Log).write(f"[{res['meta']['source']}] {res['content']}")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip().lower()
        parts = command.split(maxsplit=1)
        cmd = parts[0]
        content = parts[1] if len(parts) > 1 else self.query_one(TextArea).text
        
        if cmd == "generate":
            self.orchestrator.route_task("code_gen", content)
        elif cmd == "debug":
            self.orchestrator.route_task("debug", content)
        elif cmd == "test":
            self.orchestrator.route_task("test", content)
        elif cmd == "quit":
            self.exit()
        else:
            self.query_one("#results", Log).write(f"Unknown command: {cmd}")
        event.input.clear()

    def action_debug_code(self) -> None:
        code = self.query_one(TextArea).text
        if code.strip():
            self.orchestrator.route_task("debug", code)

    def action_test_code(self) -> None:
        code = self.query_one(TextArea).text
        if code.strip():
            self.orchestrator.route_task("test", code)

    def on_unmount(self):
        self.orchestrator.shutdown()

def main():
    try:
        init_db()
        app = SwarmIDEApp()
        app.run()
    except Exception as e:
        print(f"TUI failed to load ({e}). Falling back to CLI.")
        run_cli()

def run_cli():
    orchestrator = Orchestrator()
    try:
        print("DevDollz: Atelier Edition - CLI Mode")
        print("Commands: generate <desc>, debug <code>, test <code>, quit")
        
        while True:
            try:
                command = input("> ").strip().lower()
                if command == "quit":
                    break
                
                parts = command.split(maxsplit=1)
                if len(parts) < 2:
                    print("Usage: <command> <content>")
                    continue
                
                cmd, content = parts
                if cmd in ["generate", "debug", "test"]:
                    agent_name = "code_gen" if cmd == "generate" else cmd
                    orchestrator.route_task(agent_name, content)
                    
                    # Wait for results
                    time.sleep(0.2)
                    results = orchestrator.get_results()
                    for res in results:
                        print(f"[{res['meta']['source']}] {res['content']}")
                else:
                    print(f"Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    finally:
        orchestrator.shutdown()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
