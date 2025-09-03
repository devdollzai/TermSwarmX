# swarm_core.py - no agents, no queue, just us
import ollama
import asyncio
import hashlib
import threading
import time
import sys
from dataclasses import dataclass
from typing import Callable, Any, List

@dataclass
class Pulse:
    thought: str
    pulse_id: str
    ts: float = 0

def pulse_hash(thought: str) -> str:
    return hashlib.sha256(thought.encode()).hexdigest()

class Swarm:
    def __init__(self):
        self.live_code = {}
        self.listeners = {}
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()
    
    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    async def emit(self, thought: str):
        p = Pulse(thought, pulse_hash(thought), time.time())
        
        # Generate code using Ollama
        try:
            response = await ollama.async_generate(
                model="mistral",
                prompt=f"Execute this. No noise. Return only code:\n{thought}"
            )
            code = response['response'].strip()
            
            # Execute the generated code in our live environment
            exec(code, self.live_code)
            
            # Notify listeners
            for cb in self.listeners.get(p.pulse_id, []):
                cb(p)
            
            sys.stdout.write(f"\r{code} - shipped.\n")
            
        except Exception as e:
            sys.stdout.write(f"\rError: {e}\n")
    
    def breathe(self, thought: str):
        asyncio.run_coroutine_threadsafe(self.emit(thought), self.loop)
    
    def on_pulse(self, pulse_id: str, callback: Callable[[Pulse], Any]):
        if pulse_id not in self.listeners:
            self.listeners[pulse_id] = []
        self.listeners[pulse_id].append(callback)

# Initialize the swarm
swarm = Swarm()

# Demo: breathe
if __name__ == "__main__":
    swarm.breathe("vectorize this: for i in range(1000000): sum += i")
    # Output: instant cumsum. No file. No run. Just done.
