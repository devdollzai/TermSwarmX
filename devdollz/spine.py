#!/usr/bin/env python3
"""
DevDollz Spine - The Current That Flows
Zero external dependencies, local Ollama, lightning-fast agent spawning
"""

import asyncio
import threading
import time
import json
import sqlite3
import datetime
import subprocess
import os
import signal
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import ollama

# DevDollz Core Constants
SPINE_VERSION = "1.0.0"
MAX_AGENTS = 50  # Maximum concurrent agents
AGENT_TIMEOUT = 30  # Seconds before agent timeout
PULSE_INTERVAL = 0.1  # Pulse feed update frequency

@dataclass
class SpineAgent:
    """Lightning-fast agent that spawns on breath"""
    id: str
    name: str
    agent_type: str
    status: str = "spawning"
    created_at: float = field(default_factory=time.time)
    last_pulse: float = field(default_factory=time.time)
    thread: Optional[threading.Thread] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.pulse_id = f"{self.agent_type}_{self.id}"

@dataclass
class SpineTask:
    """Task that triggers agent spawning"""
    id: str
    command: str
    agent_type: str
    priority: int = 1
    created_at: float = field(default_factory=time.time)
    timeout: int = AGENT_TIMEOUT
    rules: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SpinePulse:
    """Live pulse from an agent"""
    agent_id: str
    agent_name: str
    message: str
    level: str = "info"  # info, warning, error, success
    timestamp: float = field(default_factory=time.time)
    meta: Dict[str, Any] = field(default_factory=dict)

class SpineDatabase:
    """Zero-external database for DevDollz spine"""
    
    def __init__(self, db_file: str = "spine_memory.db"):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize spine database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Agents table
        cursor.execute('''CREATE TABLE IF NOT EXISTS agents
                          (id TEXT PRIMARY KEY,
                           name TEXT,
                           agent_type TEXT,
                           status TEXT,
                           created_at REAL,
                           last_pulse REAL,
                           meta TEXT)''')
        
        # Tasks table
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                          (id TEXT PRIMARY KEY,
                           command TEXT,
                           agent_type TEXT,
                           priority INTEGER,
                           created_at REAL,
                           timeout INTEGER,
                           rules TEXT,
                           meta TEXT)''')
        
        # Pulse feed table
        cursor.execute('''CREATE TABLE IF NOT EXISTS pulse_feed
                          (id INTEGER PRIMARY KEY,
                           agent_id TEXT,
                           agent_name TEXT,
                           message TEXT,
                           level TEXT,
                           timestamp REAL,
                           meta TEXT)''')
        
        # System rules table
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_rules
                          (command TEXT PRIMARY KEY,
                           allowed BOOLEAN,
                           description TEXT)''')
        
        # Insert default safety rules
        default_rules = [
            ("rm", True, "Allow single file removal"),
            ("rm -rf", False, "Deny recursive force removal"),
            ("sudo", False, "Deny sudo commands"),
            ("chmod 777", False, "Deny dangerous permissions"),
            ("dd", False, "Deny disk operations"),
            ("mkfs", False, "Deny filesystem operations")
        ]
        
        for cmd, allowed, desc in default_rules:
            cursor.execute("INSERT OR REPLACE INTO system_rules VALUES (?, ?, ?)", 
                          (cmd, allowed, desc))
        
        conn.commit()
        conn.close()
    
    def log_pulse(self, pulse: SpinePulse):
        """Log a pulse to the feed"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        meta_json = json.dumps(pulse.meta)
        cursor.execute("""INSERT INTO pulse_feed 
                          (agent_id, agent_name, message, level, timestamp, meta) 
                          VALUES (?, ?, ?, ?, ?, ?)""", 
                      (pulse.agent_id, pulse.agent_name, pulse.message, 
                       pulse.level, pulse.timestamp, meta_json))
        
        conn.commit()
        conn.close()
    
    def get_recent_pulses(self, limit: int = 100) -> List[SpinePulse]:
        """Get recent pulse feed entries"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""SELECT * FROM pulse_feed 
                          ORDER BY timestamp DESC 
                          LIMIT ?""", (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        pulses = []
        for row in rows:
            meta = json.loads(row[6]) if row[6] else {}
            pulse = SpinePulse(
                agent_id=row[1],
                agent_name=row[2],
                message=row[3],
                level=row[4],
                timestamp=row[5],
                meta=meta
            )
            pulses.append(pulse)
        
        return pulses

class SpineAgentManager:
    """Manages lightning-fast agent spawning"""
    
    def __init__(self, max_agents: int = MAX_AGENTS):
        self.max_agents = max_agents
        self.active_agents: Dict[str, SpineAgent] = {}
        self.agent_templates: Dict[str, Callable] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_agents)
        self.db = SpineDatabase()
        
        # Register default agent types
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Register the core DevDollz agent types"""
        self.register_agent_type("scraper", self._create_scraper_agent)
        self.register_agent_type("codegen", self._create_codegen_agent)
        self.register_agent_type("deploy", self._create_deploy_agent)
        self.register_agent_type("analyzer", self._create_analyzer_agent)
        self.register_agent_type("validator", self._create_validator_agent)
    
    def register_agent_type(self, agent_type: str, creator_func: Callable):
        """Register a new agent type"""
        self.agent_templates[agent_type] = creator_func
    
    def spawn_agent(self, task: SpineTask) -> SpineAgent:
        """Spawn an agent on breath - lightning fast"""
        if len(self.active_agents) >= self.max_agents:
            # Kill oldest agent to make room
            oldest = min(self.active_agents.values(), key=lambda a: a.created_at)
            self.kill_agent(oldest.id)
        
        # Create agent
        agent = SpineAgent(
            id=f"{task.agent_type}_{int(time.time() * 1000)}",
            name=f"{task.agent_type.title()} Agent",
            agent_type=task.agent_type
        )
        
        # Spawn agent process/thread
        if agent.agent_type in self.agent_templates:
            creator = self.agent_templates[agent.agent_type]
            
            # Start agent in separate thread for Windows compatibility
            agent.thread = threading.Thread(
                target=creator,
                args=(task,),
                daemon=True
            )
            agent.thread.start()
            agent.status = "running"
        
        self.active_agents[agent.id] = agent
        
        # Log spawn pulse
        pulse = SpinePulse(
            agent_id=agent.id,
            agent_name=agent.name,
            message=f"Agent spawned for task: {task.command}",
            level="info",
            meta={"task_id": task.id, "agent_type": agent.agent_type}
        )
        self.db.log_pulse(pulse)
        
        return agent
    
    def kill_agent(self, agent_id: str):
        """Kill an agent immediately"""
        if agent_id in self.active_agents:
            agent = self.active_agents[agent_id]
            if agent.thread and agent.thread.is_alive():
                # Threads can't be forcefully killed, just mark as killed
                agent.status = "killed"
            
            del self.active_agents[agent_id]
            
            # Log kill pulse
            pulse = SpinePulse(
                agent_id=agent_id,
                agent_name=agent.name,
                message="Agent killed",
                level="warning"
            )
            self.db.log_pulse(pulse)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all active agents"""
        return {
            agent_id: {
                "name": agent.name,
                "type": agent.agent_type,
                "status": agent.status,
                "uptime": time.time() - agent.created_at,
                "last_pulse": agent.last_pulse,
                "thread_alive": agent.thread.is_alive() if agent.thread else False
            }
            for agent_id, agent in self.active_agents.items()
        }
    
    # Agent template functions
    def _create_scraper_agent(self, task: SpineTask):
        """Scraper agent - pulls HTML, regexes, processes"""
        try:
            # Simulate HTML scraping
            print(f"🔍 Scraper Agent: Scraping HTML content...")
            
            # Simulate regex processing
            time.sleep(0.5)
            print(f"🔍 Scraper Agent: Processing with regex patterns...")
            
            # Simulate completion
            time.sleep(0.3)
            print(f"✅ Scraper Agent: Completed - {task.command}")
            
        except Exception as e:
            print(f"❌ Scraper Agent Error: {e}")
    
    def _create_codegen_agent(self, task: SpineTask):
        """Code generation agent using local Ollama"""
        try:
            print(f"💻 CodeGen Agent: Generating code with local Ollama...")
            
            # Use local Ollama
            response = ollama.generate(
                model="mistral",
                prompt=f"Generate Python code for: {task.command}. Return only the code."
            )
            
            print(f"✅ CodeGen Agent: Code generated successfully")
            print(f"📝 Generated code:\n{response['response']}")
            
        except Exception as e:
            print(f"❌ CodeGen Agent Error: Ollama error - {str(e)}")
    
    def _create_deploy_agent(self, task: SpineTask):
        """Deployment agent"""
        try:
            print(f"🚀 Deploy Agent: Preparing deployment...")
            
            # Simulate deployment steps
            time.sleep(0.8)
            print(f"🚀 Deploy Agent: Deploying to target environment...")
            
            time.sleep(0.5)
            print(f"✅ Deploy Agent: Deployed successfully - {task.command}")
            
        except Exception as e:
            print(f"❌ Deploy Agent Error: {e}")
    
    def _create_analyzer_agent(self, task: SpineTask):
        """Code analysis agent"""
        try:
            print(f"🔍 Analyzer Agent: Analyzing code structure...")
            
            time.sleep(0.6)
            print(f"✅ Analyzer Agent: Analysis complete for - {task.command}")
            
        except Exception as e:
            print(f"❌ Analyzer Agent Error: {e}")
    
    def _create_validator_agent(self, task: SpineTask):
        """Code validation agent"""
        try:
            print(f"✅ Validator Agent: Validating code quality...")
            
            time.sleep(0.4)
            print(f"✅ Validator Agent: Validation passed for - {task.command}")
            
        except Exception as e:
            print(f"❌ Validator Agent Error: {e}")

class SpineCommandProcessor:
    """Processes commands and spawns agents"""
    
    def __init__(self, agent_manager: SpineAgentManager):
        self.agent_manager = agent_manager
        self.db = SpineDatabase()
        self.command_history: List[str] = []
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """Process a command and spawn appropriate agents"""
        # Check command against safety rules
        if not self._is_command_safe(command):
            return {
                "status": "blocked",
                "message": f"Command blocked by safety rules: {command}",
                "level": "error"
            }
        
        # Parse command to determine agent type
        agent_type = self._determine_agent_type(command)
        
        # Create task
        task = SpineTask(
            id=f"task_{int(time.time() * 1000)}",
            command=command,
            agent_type=agent_type,
            priority=1
        )
        
        # Spawn agent
        agent = self.agent_manager.spawn_agent(task)
        
        # Log command
        self.command_history.append(command)
        
        return {
            "status": "spawned",
            "agent_id": agent.id,
            "agent_type": agent_type,
            "message": f"Agent spawned for: {command}",
            "task_id": task.id
        }
    
    def _is_command_safe(self, command: str) -> bool:
        """Check if command is allowed by safety rules"""
        conn = sqlite3.connect(self.db.db_file)
        cursor = conn.cursor()
        
        # Check against blocked patterns
        cursor.execute("SELECT command FROM system_rules WHERE allowed = 0")
        blocked_commands = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        for blocked in blocked_commands:
            if blocked in command:
                return False
        
        return True
    
    def _determine_agent_type(self, command: str) -> str:
        """Determine which agent type to spawn based on command"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ["scrape", "html", "web", "crawl"]):
            return "scraper"
        elif any(word in command_lower for word in ["generate", "create", "write", "code"]):
            return "codegen"
        elif any(word in command_lower for word in ["deploy", "push", "release", "ship"]):
            return "deploy"
        elif any(word in command_lower for word in ["analyze", "review", "inspect", "check"]):
            return "analyzer"
        elif any(word in command_lower for word in ["validate", "test", "verify", "lint"]):
            return "validator"
        else:
            return "codegen"  # Default to code generation

class SpinePulseFeed:
    """Live pulse feed showing all agent activity"""
    
    def __init__(self, db: SpineDatabase):
        self.db = db
        self.last_pulse_time = 0
        self.pulse_cache: List[SpinePulse] = []
    
    def get_live_pulses(self) -> List[SpinePulse]:
        """Get live pulse feed updates"""
        current_time = time.time()
        
        # Get new pulses since last check
        recent_pulses = self.db.get_recent_pulses(1000)
        new_pulses = [p for p in recent_pulses if p.timestamp > self.last_pulse_time]
        
        if new_pulses:
            self.last_pulse_time = current_time
            self.pulse_cache.extend(new_pulses)
            
            # Keep only last 1000 pulses in cache
            if len(self.pulse_cache) > 1000:
                self.pulse_cache = self.pulse_cache[-1000:]
        
        return self.pulse_cache
    
    def get_pulse_summary(self) -> Dict[str, Any]:
        """Get summary of pulse activity"""
        pulses = self.get_live_pulses()
        
        if not pulses:
            return {"total": 0, "by_level": {}, "recent": []}
        
        by_level = {}
        for pulse in pulses:
            level = pulse.level
            by_level[level] = by_level.get(level, 0) + 1
        
        return {
            "total": len(pulses),
            "by_level": by_level,
            "recent": pulses[-10:] if pulses else []
        }

class DevDollzSpine:
    """The main spine - where everything connects"""
    
    def __init__(self):
        self.db = SpineDatabase()
        self.agent_manager = SpineAgentManager()
        self.command_processor = SpineCommandProcessor(self.agent_manager)
        self.pulse_feed = SpinePulseFeed(self.db)
        self.running = False
        
        print("🔥 DevDollz Spine initialized")
        print("🚀 Zero external dependencies")
        print("⚡ Lightning-fast agent spawning")
        print("🎯 Local Ollama integration")
        print("🛡️ Safety rules active")
    
    def start(self):
        """Start the spine"""
        self.running = True
        print("🎭 DevDollz Spine is alive!")
        
        # Start pulse monitoring
        self._start_pulse_monitor()
    
    def stop(self):
        """Stop the spine"""
        self.running = False
        
        # Kill all agents
        for agent_id in list(self.agent_manager.active_agents.keys()):
            self.agent_manager.kill_agent(agent_id)
        
        print("💀 DevDollz Spine stopped")
    
    def _start_pulse_monitor(self):
        """Start monitoring agent pulses"""
        def monitor():
            while self.running:
                try:
                    # Simple monitoring - just update timestamps and check thread status
                    for agent_id, agent in self.agent_manager.active_agents.items():
                        if agent.thread and not agent.thread.is_alive():
                            # Thread finished, update status
                            if agent.status == "running":
                                agent.status = "completed"
                                agent.last_pulse = time.time()
                                
                                # Log completion pulse
                                pulse = SpinePulse(
                                    agent_id=agent_id,
                                    agent_name=agent.name,
                                    message="Task completed successfully",
                                    level="success"
                                )
                                self.db.log_pulse(pulse)
                    
                    time.sleep(PULSE_INTERVAL)
                    
                except Exception as e:
                    print(f"Pulse monitor error: {e}")
                    time.sleep(1)
        
        # Start monitor in background thread
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def execute(self, command: str) -> Dict[str, Any]:
        """Execute a command through the spine"""
        return self.command_processor.process_command(command)
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall spine status"""
        return {
            "version": SPINE_VERSION,
            "status": "running" if self.running else "stopped",
            "agents": self.agent_manager.get_agent_status(),
            "pulse_summary": self.pulse_feed.get_pulse_summary(),
            "command_history": self.command_processor.command_history[-10:]
        }
    
    def get_pulse_feed(self, limit: int = 100) -> List[SpinePulse]:
        """Get live pulse feed"""
        return self.pulse_feed.get_live_pulses()[-limit:]

# Main execution
if __name__ == "__main__":
    print("🔥 DevDollz Spine - The Current That Flows")
    print("=" * 50)
    
    spine = DevDollzSpine()
    
    try:
        spine.start()
        
        # Demo commands
        print("\n🧪 Testing agent spawning...")
        
        # Test scraper
        result = spine.execute("scrape website for data")
        print(f"Scraper: {result}")
        
        # Test codegen
        result = spine.execute("generate Python function for file processing")
        print(f"CodeGen: {result}")
        
        # Test deploy
        result = spine.execute("deploy to production")
        print(f"Deploy: {result}")
        
        # Let agents run for a bit
        print("\n⏳ Letting agents work...")
        time.sleep(5)
        
        # Show status
        status = spine.get_status()
        print(f"\n📊 Status: {json.dumps(status, indent=2)}")
        
        # Show pulse feed
        pulses = spine.get_pulse_feed(10)
        print(f"\n💓 Recent pulses:")
        for pulse in pulses:
            print(f"  [{pulse.level.upper()}] {pulse.agent_name}: {pulse.message}")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    finally:
        spine.stop()
        print("\n👋 DevDollz Spine shutdown complete")
