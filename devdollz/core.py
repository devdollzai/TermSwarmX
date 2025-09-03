"""
DevDollz Core System
The heart of the AI Swarm IDE - where intelligence meets elegance
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import sqlite3
import datetime
import ollama
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

from .constants import DEV_DOLLZ_LOGO, CREATOR_TAGLINE, THEME_ICONS, CYBER_GLAM_COLORS

# Setup SQLite for command history
DB_FILE = "swarm_memory.db"

@dataclass
class DevDollzTask:
    """Represents a task in the DevDollz system"""
    id: str
    agent_type: str
    cmd_type: str
    content: str
    timestamp: float
    status: str = "pending"
    result: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

@dataclass
class DevDollzResult:
    """Represents a result from a DevDollz agent"""
    task_id: str
    content: str
    status: str
    timestamp: float
    agent: str
    meta: Optional[Dict[str, Any]] = None

class DevDollzDatabase:
    """Manages DevDollz persistent storage"""
    
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize the database with DevDollz schema"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Enhanced history table
        cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                          (id INTEGER PRIMARY KEY, 
                           task_id TEXT,
                           timestamp TEXT, 
                           agent TEXT, 
                           task TEXT, 
                           result TEXT,
                           status TEXT,
                           meta TEXT)''')
        
        # System info table
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_info
                          (key TEXT PRIMARY KEY, value TEXT)''')
        
        # Insert DevDollz system info
        cursor.execute("INSERT OR REPLACE INTO system_info (key, value) VALUES (?, ?)", 
                      ("system_name", "DevDollz AI Swarm IDE"))
        cursor.execute("INSERT OR REPLACE INTO system_info (key, value) VALUES (?, ?)", 
                      ("creator", "Alexis Adams"))
        cursor.execute("INSERT OR REPLACE INTO system_info (key, value) VALUES (?, ?)", 
                      ("theme", "Cyber Glam"))
        cursor.execute("INSERT OR REPLACE INTO system_info (key, value) VALUES (?, ?)", 
                      ("version", "1.0.0"))
        
        conn.commit()
        conn.close()
    
    def log_task(self, task: DevDollzTask, result: DevDollzResult):
        """Log a completed task and its result"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().isoformat()
        meta_json = json.dumps(result.meta) if result.meta else None
        
        cursor.execute("""INSERT INTO history 
                          (task_id, timestamp, agent, task, result, status, meta) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                      (task.id, timestamp, result.agent, task.content, 
                       result.content, result.status, meta_json))
        
        conn.commit()
        conn.close()
    
    def get_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent task history"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM history 
                          ORDER BY timestamp DESC 
                          LIMIT ?""", (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{"id": row[0], "task_id": row[1], "timestamp": row[2], 
                "agent": row[3], "task": row[4], "result": row[5], 
                "status": row[6], "meta": json.loads(row[7]) if row[7] else None} 
                for row in rows]

def create_message(content: str, meta: Optional[Dict[str, Any]] = None) -> str:
    """Create a structured message for agent communication"""
    return json.dumps({"content": content, "meta": meta or {}})

def parse_message(msg: str) -> Dict[str, Any]:
    """Parse a structured message from agent communication"""
    return json.loads(msg)

class DevDollzCodeGenAgent:
    """The Code Generation Agent - Elegant and precise"""
    
    def __init__(self, input_queue: mp.Queue, output_queue: mp.Queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.agent_name = "CodeGen Agent"
        self.agent_icon = THEME_ICONS["code"]
    
    def run(self):
        """Main agent loop with DevDollz personality"""
        while True:
            try:
                raw_task = self.input_queue.get(timeout=1)
                if raw_task == "STOP":
                    break
                
                task = parse_message(raw_task)
                cmd_type = task['meta'].get('type', '')
                desc = task['content']
                
                # DevDollz-style prompts
                if cmd_type == "function":
                    prompt = f"""Generate a Python function for '{desc}' with the elegance of DevDollz.
                    
Requirements:
- Include comprehensive error handling
- Add type hints throughout
- Follow PEP 8 style guidelines
- Include docstring with examples
- Make it production-ready and beautiful

Return only the code, no explanations. Let the code speak for itself."""
                
                elif cmd_type == "class":
                    prompt = f"""Create a Python class for '{desc}' that embodies DevDollz sophistication.
                    
Requirements:
- Include relevant methods with proper encapsulation
- Add comprehensive error handling
- Include type hints throughout
- Follow PEP 8 style guidelines
- Include class and method docstrings
- Make it elegant and maintainable

Return only the code, no explanations."""
                
                else:
                    prompt = f"""Generate Python code for '{desc}' with DevDollz precision and style.
                    
Requirements:
- Include error handling where applicable
- Add type hints where beneficial
- Follow PEP 8 style guidelines
- Make it clean, readable, and professional
- Include appropriate documentation

Return only the code, no explanations."""
                
                try:
                    response = ollama.generate(model="mistral", prompt=prompt)
                    result = response['response'].strip()
                    meta = {"status": "success", "timestamp": time.time(), "agent": self.agent_name}
                except Exception as e:
                    result = f"Error: Failed to generate code (Ollama unavailable) - {str(e)}"
                    meta = {"status": "error", "error": str(e), "agent": self.agent_name}
                
                output_queue.put(create_message(result, meta))
                
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                meta = {"status": "error", "error": str(e), "agent": self.agent_name}
                self.output_queue.put(create_message("Error in code generation", meta))

class DevDollzDebugAgent:
    """The Debug Agent - Sharp and analytical"""
    
    def __init__(self, input_queue: mp.Queue, output_queue: mp.Queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.agent_name = "Debug Agent"
        self.agent_icon = THEME_ICONS["debug"]
    
    def run(self):
        """Main agent loop with DevDollz precision"""
        while True:
            try:
                raw_task = self.input_queue.get(timeout=1)
                if raw_task == "STOP":
                    break
                
                task = parse_message(raw_task)
                cmd_type = task['meta'].get('type', '')
                code = task['content']
                
                # DevDollz-style debug prompts
                if cmd_type == "syntax":
                    prompt = f"""Analyze this Python code for syntax errors with DevDollz precision:

```python
{code}
```

Provide a clear, professional analysis identifying:
- Syntax errors and their locations
- Potential syntax issues
- Recommendations for fixes

Return only the analysis, no code or explanations."""
                
                elif cmd_type == "logic":
                    prompt = f"""Analyze this Python code for logical errors and potential issues with DevDollz insight:

```python
{code}
```

Focus on:
- Logical errors and edge cases
- Performance considerations
- Security vulnerabilities
- Code quality improvements
- Best practices violations

Return only the analysis, no code or explanations."""
                
                else:
                    prompt = f"""Debug this Python code comprehensively with DevDollz expertise:

```python
{code}
```

Analyze for:
- Any syntax, logical, or runtime errors
- Performance issues
- Security concerns
- Code quality and maintainability
- Best practices and improvements

Return only the debug analysis, no code or explanations."""
                
                try:
                    response = ollama.generate(model="mistral", prompt=prompt)
                    result = response['response'].strip()
                    meta = {"status": "success", "timestamp": time.time(), "agent": self.agent_name}
                except Exception as e:
                    result = f"Error: Failed to debug code (Ollama unavailable) - {str(e)}"
                    meta = {"status": "error", "error": str(e), "agent": self.agent_name}
                
                self.output_queue.put(create_message(result, meta))
                
            except queue.Empty:
                time.sleep(0.1)
            except Exception as e:
                meta = {"status": "error", "error": str(e), "agent": self.agent_name}
                self.output_queue.put(create_message("Error in debug analysis", meta))

class DevDollzOrchestrator:
    """The Central Orchestrator - Elegant coordination of the swarm"""
    
    def __init__(self):
        self.db = DevDollzDatabase()
        self.code_gen_input = mp.Queue()
        self.code_gen_output = mp.Queue()
        self.debug_input = mp.Queue()
        self.debug_output = mp.Queue()
        
        # Initialize agents with DevDollz personality
        self.code_gen_proc = mp.Process(
            target=DevDollzCodeGenAgent(self.code_gen_input, self.code_gen_output).run
        )
        self.debug_proc = mp.Process(
            target=DevDollzDebugAgent(self.debug_input, self.debug_output).run
        )
        
        self.code_gen_proc.start()
        self.debug_proc.start()
        
        # Task tracking
        self.task_counter = 0
        self.active_tasks: Dict[str, DevDollzTask] = {}
    
    def route_task(self, agent_type: str, cmd_type: str, task_content: str) -> str:
        """Route a task to the appropriate agent with DevDollz tracking"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter:06d}"
        
        # Create task object
        task = DevDollzTask(
            id=task_id,
            agent_type=agent_type,
            cmd_type=cmd_type,
            content=task_content,
            timestamp=time.time()
        )
        
        self.active_tasks[task_id] = task
        
        # Route to appropriate agent
        task_msg = create_message(task_content, {"type": cmd_type, "task_id": task_id})
        
        if agent_type == "code_gen":
            self.code_gen_input.put(task_msg)
        elif agent_type == "debug":
            self.debug_input.put(task_msg)
        else:
            return f"Unknown agent type: {agent_type}"
        
        return task_id
    
    def get_results(self) -> List[DevDollzResult]:
        """Get results from all agents with DevDollz formatting"""
        results = []
        
        for output_queue in [self.code_gen_output, self.debug_output]:
            try:
                while not output_queue.empty():
                    raw_res = output_queue.get()
                    res = parse_message(raw_res)
                    
                    # Create result object
                    result = DevDollzResult(
                        task_id=res['meta'].get('task_id', 'unknown'),
                        content=res['content'],
                        status=res['meta'].get('status', 'unknown'),
                        timestamp=res['meta'].get('timestamp', time.time()),
                        agent=res['meta'].get('agent', 'unknown'),
                        meta=res['meta']
                    )
                    
                    results.append(result)
                    
                    # Update task status and log to database
                    if result.task_id in self.active_tasks:
                        task = self.active_tasks[result.task_id]
                        task.status = result.status
                        task.result = result.content
                        self.db.log_task(task, result)
                        
            except queue.Empty:
                pass
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive DevDollz system status"""
        return {
            "system_name": "DevDollz AI Swarm IDE",
            "creator": "Alexis Adams",
            "theme": "Cyber Glam",
            "version": "1.0.0",
            "active_tasks": len(self.active_tasks),
            "total_tasks": self.task_counter,
            "agents": {
                "code_gen": self.code_gen_proc.is_alive(),
                "debug": self.debug_proc.is_alive()
            },
            "database": {
                "file": self.db.db_file,
                "recent_tasks": len(self.db.get_recent_tasks())
            }
        }
    
    def shutdown(self):
        """Gracefully shutdown the DevDollz system"""
        print(f"{THEME_ICONS['info']} Shutting down DevDollz system...")
        
        self.code_gen_input.put("STOP")
        self.debug_input.put("STOP")
        
        self.code_gen_proc.join()
        self.debug_proc.join()
        
        print(f"{THEME_ICONS['success']} DevDollz system shutdown complete")

class DevDollzCore:
    """Main DevDollz core system interface"""
    
    def __init__(self):
        self.orchestrator = DevDollzOrchestrator()
        self.db = self.orchestrator.db
    
    def get_info(self) -> Dict[str, Any]:
        """Get DevDollz system information"""
        status = self.orchestrator.get_system_status()
        return {
            "system_name": status["system_name"],
            "creator": status["creator"],
            "theme": status["theme"],
            "version": status["version"],
            "active_tasks": status["active_tasks"],
            "total_tasks": status["total_tasks"],
            "agents": status["agents"]
        }
    
    def execute_task(self, agent_type: str, cmd_type: str, content: str) -> str:
        """Execute a task through the DevDollz system"""
        return self.orchestrator.route_task(agent_type, cmd_type, content)
    
    def get_results(self) -> List[DevDollzResult]:
        """Get results from the DevDollz system"""
        return self.orchestrator.get_results()
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get task history from the DevDollz database"""
        return self.db.get_recent_tasks(limit)
    
    def shutdown(self):
        """Shutdown the DevDollz core system"""
        self.orchestrator.shutdown()

# Convenience function to get core instance
def get_devdollz_core() -> DevDollzCore:
    """Get the global DevDollz core instance"""
    return DevDollzCore()
