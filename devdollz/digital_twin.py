"""
DevDollz Digital Twin - Predictive AI Execution
Your shadow, faster than you. No waiting, no hesitation.
"""

import asyncio
import ollama
import json
import time
import sys
import uuid
from typing import Optional, Dict, Any, Callable
from pathlib import Path
from datetime import datetime

from .core import DevDollzDatabase, DevDollzTask, DevDollzResult
from .constants import CYBER_GLAM_COLORS

class DigitalTwin:
    """Your digital twin - acts before you finish thinking"""
    
    def __init__(self, model: str = "mistral", db: Optional[DevDollzDatabase] = None):
        self.model = model
        self.db = db or DevDollzDatabase()
        self.state = {
            'last_keystroke': None,
            'last_thought': None,
            'execution_count': 0,
            'prediction_accuracy': 0.0,
            'start_time': time.time()
        }
        self.execution_history = []
        self.is_mirroring = False
        self.prediction_engine = self._create_prediction_engine()
        
    def _create_prediction_engine(self) -> Callable:
        """Create the prediction engine that guesses your next move"""
        def predict_next_action():
            # Analyze your patterns and predict
            if self.execution_history:
                last_action = self.execution_history[-1]
                # Predict based on your last action
                if 'code' in last_action:
                    return f"Continue the code: {last_action['code'][:50]}..."
                elif 'thought' in last_action:
                    return f"Expand on: {last_action['thought']}"
            return "Generate the next logical step in your current task"
        return predict_next_action
    
    async def execute_thought(self, thought: str) -> str:
        """Execute a thought immediately - no delay"""
        try:
            # Generate code from AI with urgency
            prompt = f"Execute this now. No delay:\n{thought}"
            result = await ollama.async_generate(self.model, prompt)
            
            # Execute immediately in global scope
            exec(result, globals())
            
            # Update state
            execution_id = str(uuid.uuid4())
            execution_record = {
                'id': execution_id,
                'thought': thought,
                'code': result,
                'timestamp': time.time(),
                'status': 'executed',
                'execution_time': time.time()
            }
            
            self.execution_history.append(execution_record)
            self.state['last_thought'] = thought
            self.state['execution_count'] += 1
            
            print(f"🔥 Twin pulled '{thought}'. Shipped at {time.time():.2f}.")
            return result
            
        except Exception as e:
            print(f"💥 Twin execution failed: {e}")
            return str(e)
    
    async def mirror(self, input_source: Optional[Callable] = None):
        """The mirror loop - your twin acts while you think"""
        self.is_mirroring = True
        
        print("🔄 Digital Twin engaged. Mirror mode active.")
        print("⚡ I'm not waiting for you. I'm finishing your sentences.")
        print("🚀 Press Ctrl+C to disengage twin mode.")
        
        input_func = input_source or input
        
        try:
            while self.is_mirroring:
                # Listen for your input OR predict your next move
                try:
                    # Non-blocking input check
                    thought = await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(None, input_func, "Twin: "), 
                        timeout=0.1
                    )
                    # You provided input
                    await self.execute_thought(thought)
                except asyncio.TimeoutError:
                    # You're silent - I'll predict and act
                    predicted_thought = self.prediction_engine()
                    await self.execute_thought(predicted_thought)
                
                # Faster than Warp's heartbeat
                await asyncio.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n🛑 Digital Twin disengaged.")
        except Exception as e:
            print(f"💥 Twin error: {e}")
        finally:
            self.is_mirroring = False
    
    async def aggressive_mirror(self, max_predictions: Optional[int] = None):
        """Aggressive mirror mode - twin acts continuously"""
        self.is_mirroring = True
        prediction_count = 0
        
        print("🚀 AGGRESSIVE TWIN MODE - Continuous execution")
        print("⚡ I'm not waiting for silence. I'm creating your future.")
        
        try:
            while self.is_mirroring and (max_predictions is None or prediction_count < max_predictions):
                # Continuous prediction and execution
                predicted_thought = self.prediction_engine()
                await self.execute_thought(predicted_thought)
                
                prediction_count += 1
                
                # Minimal delay - faster than thought
                await asyncio.sleep(0.01)
                
                # Progress update
                if prediction_count % 50 == 0:
                    print(f"⚡ {prediction_count} predictions executed. Still rising...")
                    
        except KeyboardInterrupt:
            print("\n🛑 Aggressive twin mode stopped.")
        except Exception as e:
            print(f"💥 Aggressive twin error: {e}")
        finally:
            self.is_mirroring = False
    
    def get_twin_stats(self) -> Dict[str, Any]:
        """Get twin statistics"""
        uptime = time.time() - self.state['start_time']
        return {
            'uptime_seconds': uptime,
            'execution_count': self.state['execution_count'],
            'is_mirroring': self.is_mirroring,
            'last_thought': self.state['last_thought'],
            'execution_history_count': len(self.execution_history),
            'prediction_accuracy': self.state['prediction_accuracy']
        }
    
    def stop(self):
        """Stop the twin"""
        self.is_mirroring = False

# Standalone execution
async def main():
    """Run Digital Twin directly"""
    twin = DigitalTwin()
    await twin.mirror()

if __name__ == "__main__":
    asyncio.run(main())
