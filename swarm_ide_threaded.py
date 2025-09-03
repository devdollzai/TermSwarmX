#!/usr/bin/env python3
"""
AI Swarm IDE - Threaded LLM-Integrated Sharp CLI Interface
Testing if threading resolves the Ollama hanging issue
"""

import threading
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

# Setup SQLite for command history and memory
DB_FILE = "swarm_memory.db"

def init_db():
    """Initialize SQLite database for persistent memory"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY, timestamp TEXT, agent TEXT, task TEXT, result TEXT, status TEXT)''')
    conn.commit()
    conn.close()

init_db()

def log_to_db(agent: str, task: str, result: str, status: str = "success"):
    """Log task execution to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO history (timestamp, agent, task, result, status) VALUES (?, ?, ?, ?)", 
                   (timestamp, agent, task, result, status))
    conn.commit()
    conn.close()

# Simplified Code Generation Agent (Threaded)
def code_gen_agent(input_queue: queue.Queue, output_queue: queue.Queue):
    """Code generation agent with real Ollama LLM integration"""
    print("🚀 Code gen agent started")
    message_count = 0
    
    while True:
        try:
            try:
                raw_task = input_queue.get(timeout=1)
            except queue.Empty:
                continue
                
            if raw_task == "STOP":
                print("🛑 Code gen agent stopping")
                break
            message_count += 1
            print(f"📨 Code gen agent received message #{message_count}")
                
            task = json.loads(raw_task)
            task_type = task['meta'].get('type', 'code')
            task_content = task['content']
            
            if not OLLAMA_AVAILABLE:
                result = "Error: Ollama not available. Install with: pip install ollama"
                meta = {"status": "error", "error": "Ollama not available", "agent": "code_gen", "task_id": task['meta'].get('task_id', 'unknown')}
                output_queue.put(json.dumps({"content": result, "meta": meta}))
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
                
                # Simple Ollama call
                response = ollama.generate(model='mistral', prompt=prompt)
                result = response['response']
                print(f"✅ Ollama response received: {result[:100]}...")
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "code_gen", "task_id": task_id}
                output_queue.put(json.dumps({"content": result, "meta": meta}))
                print(f"📤 Result sent to output queue with task_id: {task_id}")
                log_to_db("code_gen", task_content, result, "success")
                
            except Exception as e:
                print(f"❌ Error in code generation: {str(e)}")
                import traceback
                traceback.print_exc()
                result = f"Error in code generation: {str(e)}"
                task_id = task['meta'].get('task_id', 'unknown')
                meta = {"status": "error", "error": str(e), "agent": "code_gen", "task_id": task_id}
                output_queue.put(json.dumps({"content": result, "meta": meta}))
                log_to_db("code_gen", task_content, result, "error")
            
        except Exception as e:
            print(f"❌ Fatal error in code gen agent: {e}")
            import traceback
            traceback.print_exc()

# Simplified Debug Agent (Threaded)
def debug_agent(input_queue: queue.Queue, output_queue: queue.Queue):
    """Debugging agent with real Ollama LLM integration"""
    print("🚀 Debug agent started")
    message_count = 0
    
    while True:
        try:
            try:
                raw_task = input_queue.get(timeout=1)
            except queue.Empty:
                continue
                
            if raw_task == "STOP":
                print("🛑 Debug agent stopping")
                break
            message_count += 1
            print(f"📨 Debug agent received message #{message_count}")
                
            task = json.loads(raw_task)
            error_type = task['meta'].get('error_type', 'syntax')
            code_to_debug = task['content']
            
            if not OLLAMA_AVAILABLE:
                result = "Error: Ollama not available. Install with: pip install ollama"
                meta = {"status": "error", "error": "Ollama not available", "agent": "debug", "task_id": task['meta'].get('task_id', 'unknown')}
                output_queue.put(json.dumps({"content": result, "meta": meta}))
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
                
                # Simple Ollama call
                response = ollama.generate(model='mistral', prompt=prompt)
                result = response['response']
                print(f"✅ Ollama response received: {result[:100]}...")
                
                meta = {"status": "success", "timestamp": time.time(), "agent": "debug", "task_id": task_id}
                output_queue.put(json.dumps({"content": result, "meta": meta}))
                print(f"📤 Result sent to output queue with task_id: {task_id}")
                log_to_db("debug", code_to_debug, result, "success")
                
            except Exception as e:
                print(f"❌ Error in debugging: {str(e)}")
                import traceback
                traceback.print_exc()
                result = f"Error in debugging: {str(e)}"
                task_id = task['meta'].get('task_id', 'unknown')
                meta = {"status": "error", "error": str(e), "agent": "debug", "task_id": task_id}
                output_queue.put(json.dumps({"content": result, "meta": meta}))
                log_to_db("debug", code_to_debug, result, "error")
            
        except Exception as e:
            print(f"❌ Fatal error in debug agent: {e}")
            import traceback
            traceback.print_exc()

# Central Orchestrator (Threaded)
class SwarmOrchestrator:
    def __init__(self):
        self.code_gen_queue = queue.Queue()
        self.debug_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.agents: Dict[str, threading.Thread] = {}
        self.task_counter = 0

    def register_agent(self, role: str, thread: threading.Thread):
        self.agents[role] = thread

    def dispatch_task(self, role: str, content: str, task_id: str):
        if role == "code_gen":
            message = json.dumps({"content": content, "meta": {"type": "code", "task_id": task_id}})
            self.code_gen_queue.put(message)
        elif role == "debug":
            message = json.dumps({"content": content, "meta": {"type": "syntax", "task_id": task_id}})
            self.debug_queue.put(message)
        else:
            message = json.dumps({"content": content, "meta": {"type": role, "task_id": task_id}})
            self.code_gen_queue.put(message)
        
        return self._wait_for_result(task_id)

    def _wait_for_result(self, task_id: str) -> Optional[str]:
        timeout = 60.0  # 60 second timeout for LLM calls
        start_time = time.time()
        print(f"🔍 Waiting for result with task_id: {task_id}")
        
        while True:
            if time.time() - start_time > timeout:
                print(f"⏰ Timeout waiting for task_id: {task_id}")
                return "Task timed out"
                
            try:
                if not self.result_queue.empty():
                    raw_result = self.result_queue.get_nowait()
                    result = json.loads(raw_result)
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
                
            time.sleep(0.1)

    def shutdown(self):
        """Clean shutdown of all agent threads"""
        for role, thread in self.agents.items():
            if thread.is_alive():
                if role == "code_gen":
                    self.code_gen_queue.put("STOP")
                elif role == "debug":
                    self.debug_queue.put("STOP")
                thread.join(timeout=2)

# Main entry point
def main():
    """Main application entry point"""
    try:
        # Initialize orchestrator
        orchestrator = SwarmOrchestrator()
        
        # Start agents as threads
        code_gen_thread = threading.Thread(target=code_gen_agent, args=(orchestrator.code_gen_queue, orchestrator.result_queue))
        debug_thread = threading.Thread(target=debug_agent, args=(orchestrator.debug_queue, orchestrator.result_queue))
        
        code_gen_thread.daemon = True
        debug_thread.daemon = True
        
        code_gen_thread.start()
        debug_thread.start()
        
        orchestrator.register_agent("code_gen", code_gen_thread)
        orchestrator.register_agent("debug", debug_thread)
        
        # Wait for agents to start
        time.sleep(2)
        
        print("🤖 AI Swarm IDE - Threaded LLM Integration")
        print("=" * 50)
        
        if not OLLAMA_AVAILABLE:
            print("⚠️  Warning: Ollama not available. Install with: pip install ollama")
        else:
            print("✅ Ollama integration available")
            
        print("")
        print("Testing LLM integration...")
        
        # Test a simple command
        result = orchestrator.dispatch_task("code_gen", "function: test_function", "test_1")
        print(f"Test result: {result[:200]}...")
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'orchestrator' in locals():
            orchestrator.shutdown()

if __name__ == "__main__":
    main()
