# swarm_extensions.py - Advanced extensions for the live swarm brain
import json
import pickle
import hashlib
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from swarm_core import Swarm, Pulse, pulse_hash

class SwarmMemory:
    """Persistent memory for the swarm brain"""
    
    def __init__(self, filename: str = "swarm_memory.pkl"):
        self.filename = filename
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict[str, Any]:
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_memory(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.memory, f)
    
    def store(self, key: str, value: Any):
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat(),
            'hash': hashlib.sha256(str(value).encode()).hexdigest()
        }
        self._save_memory()
    
    def retrieve(self, key: str) -> Optional[Any]:
        if key in self.memory:
            return self.memory[key]['value']
        return None
    
    def list_keys(self) -> List[str]:
        return list(self.memory.keys())

class CodeValidator:
    """Validates generated code before execution"""
    
    @staticmethod
    def validate_syntax(code: str) -> bool:
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    
    @staticmethod
    def check_security(code: str) -> bool:
        dangerous_patterns = [
            'import os',
            'import subprocess',
            'eval(',
            'exec(',
            '__import__',
            'open(',
            'file('
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                return False
        return True
    
    @staticmethod
    def validate(code: str) -> tuple[bool, str]:
        if not CodeValidator.validate_syntax(code):
            return False, "Syntax error in generated code"
        
        if not CodeValidator.check_security(code):
            return False, "Code contains potentially dangerous operations"
        
        return True, "Code validation passed"

class SwarmCollaborator:
    """Enables collaborative swarm development"""
    
    def __init__(self, swarm: Swarm):
        self.swarm = swarm
        self.collaborators = {}
        self.shared_context = {}
    
    def add_collaborator(self, name: str, context: Dict[str, Any]):
        self.collaborators[name] = context
        self.shared_context.update(context)
        print(f"🤝 Added collaborator: {name}")
    
    def merge_contexts(self):
        """Merge all collaborator contexts"""
        merged = {}
        for name, context in self.collaborators.items():
            merged.update(context)
        self.shared_context = merged
        return merged
    
    def collaborative_breathe(self, thought: str, collaborator: str):
        """Execute thought with collaborator context"""
        if collaborator in self.collaborators:
            context = self.collaborators[collaborator]
            thought_with_context = f"Context: {context}\nThought: {thought}"
            self.swarm.breathe(thought_with_context)
        else:
            print(f"❌ Collaborator {collaborator} not found")

class EnhancedSwarm(Swarm):
    """Enhanced swarm with memory, validation, and collaboration"""
    
    def __init__(self):
        super().__init__()
        self.memory = SwarmMemory()
        self.validator = CodeValidator()
        self.collaborator = SwarmCollaborator(self)
        self.execution_history = []
    
    async def emit(self, thought: str):
        p = Pulse(thought, pulse_hash(thought), time.time())
        
        try:
            # Generate code using Ollama
            response = await ollama.async_generate(
                model="mistral",
                prompt=f"Execute this. No noise. Return only code:\n{thought}"
            )
            code = response['response'].strip()
            
            # Validate code before execution
            is_valid, message = self.validator.validate(code)
            if not is_valid:
                sys.stdout.write(f"\r❌ Validation failed: {message}\n")
                return
            
            # Store in execution history
            self.execution_history.append({
                'thought': thought,
                'code': code,
                'timestamp': datetime.now().isoformat(),
                'pulse_id': p.pulse_id
            })
            
            # Execute with enhanced context
            exec_context = self.live_code.copy()
            exec_context.update(self.collaborator.shared_context)
            exec(code, exec_context)
            
            # Store successful execution in memory
            self.memory.store(f"exec_{p.pulse_id}", {
                'thought': thought,
                'code': code,
                'result': 'executed_successfully'
            })
            
            # Notify listeners
            for cb in self.listeners.get(p.pulse_id, []):
                cb(p)
            
            sys.stdout.write(f"\r✅ {code} - shipped and validated.\n")
            
        except Exception as e:
            error_msg = f"Error: {e}"
            sys.stdout.write(f"\r❌ {error_msg}\n")
            self.memory.store(f"error_{p.pulse_id}", {
                'thought': thought,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            })
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get statistics about swarm execution"""
        return {
            'total_executions': len(self.execution_history),
            'memory_entries': len(self.memory.list_keys()),
            'collaborators': len(self.collaborator.collaborators),
            'last_execution': self.execution_history[-1] if self.execution_history else None
        }
    
    def replay_execution(self, pulse_id: str):
        """Replay a specific execution from history"""
        for entry in self.execution_history:
            if entry['pulse_id'] == pulse_id:
                print(f"🔄 Replaying execution: {entry['thought']}")
                self.breathe(entry['thought'])
                return
        print(f"❌ Execution {pulse_id} not found in history")

# Create enhanced swarm instance
enhanced_swarm = EnhancedSwarm()

# Example usage
if __name__ == "__main__":
    print("🚀 Enhanced Swarm Brain with Extensions")
    print("=" * 50)
    
    # Add a collaborator
    enhanced_swarm.collaborator.add_collaborator("numpy_expert", {
        'numpy': 'import numpy as np',
        'optimization_tips': 'Use vectorized operations for speed'
    })
    
    # Execute with enhanced features
    enhanced_swarm.breathe("Create a fast matrix multiplication function")
    
    # Show stats
    stats = enhanced_swarm.get_execution_stats()
    print(f"\n📊 Swarm Stats: {stats}")
