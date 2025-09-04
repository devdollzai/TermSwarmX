#!/usr/bin/env python3
"""
Example Plugin for DevDollz: Atelier Edition
Demonstrates the working plugin system
"""

import time
import json
from typing import Dict, Any

def create_message(content, meta=None):
    """Create a message in the format expected by DevDollz"""
    return json.dumps({"content": content, "meta": meta or {}})

def parse_message(msg):
    """Parse a message from DevDollz"""
    return json.loads(msg)

def plugin_agent(input_queue, output_queue):
    """
    Example plugin agent that processes tasks
    
    This function will be called by DevDollz's plugin system.
    It runs in a separate thread to avoid blocking the main application.
    """
    print("🔌 Example plugin agent started")
    
    while True:
        try:
            # Get task from input queue
            raw_task = input_queue.get(timeout=1)
            
            # Check for stop signal
            if raw_task == "STOP":
                print("🔌 Example plugin agent stopping")
                break
            
            # Parse the task
            task = parse_message(raw_task)
            task_content = task.get('content', '')
            task_type = task.get('meta', {}).get('type', 'custom')
            
            print(f"🔌 Processing task: {task_type} - {task_content}")
            
            # Process different task types
            if task_type == "hello":
                result = f"Hello from the example plugin! You said: {task_content}"
                meta = {"status": "success", "source": "example_plugin"}
                
            elif task_type == "math":
                try:
                    # Simple math evaluation (safe)
                    if task_content.isdigit():
                        number = int(task_content)
                        result = f"Square of {number} is {number ** 2}"
                        meta = {"status": "success", "source": "example_plugin"}
                    else:
                        result = f"Please provide a number for math operations"
                        meta = {"status": "error", "source": "example_plugin"}
                except Exception as e:
                    result = f"Math error: {str(e)}"
                    meta = {"status": "error", "source": "example_plugin"}
                    
            elif task_type == "echo":
                result = f"Echo: {task_content}"
                meta = {"status": "success", "source": "example_plugin"}
                
            else:
                result = f"Unknown task type '{task_type}'. Available: hello, math, echo"
                meta = {"status": "error", "source": "example_plugin"}
            
            # Send result back
            output_queue.put(create_message(result, meta))
            
            # Add timestamp for tracking
            print(f"🔌 Task completed: {result[:50]}...")
            
        except Exception as e:
            # Handle any errors gracefully
            error_msg = f"Plugin error: {str(e)}"
            error_meta = {"status": "error", "source": "example_plugin", "error": str(e)}
            output_queue.put(create_message(error_msg, error_meta))
            print(f"🔌 Error in plugin: {e}")
            
        # Small delay to prevent excessive CPU usage
        time.sleep(0.1)
    
    print("🔌 Example plugin agent stopped")

# Example usage functions for testing
def test_plugin():
    """Test the plugin functionality"""
    print("🧪 Testing example plugin...")
    
    # Simulate the plugin system
    import queue
    import threading
    
    input_q = queue.Queue()
    output_q = queue.Queue()
    
    # Start plugin in a thread
    plugin_thread = threading.Thread(
        target=plugin_agent, 
        args=(input_q, output_q),
        daemon=True
    )
    plugin_thread.start()
    
    # Test different task types
    test_tasks = [
        ("hello", "world"),
        ("math", "5"),
        ("echo", "test message"),
        ("unknown", "invalid task")
    ]
    
    for task_type, content in test_tasks:
        print(f"\n📤 Sending task: {task_type} - {content}")
        
        # Create and send task
        task_msg = create_message(content, {"type": task_type})
        input_q.put(task_msg)
        
        # Wait for response
        time.sleep(0.5)
        
        # Get response
        try:
            while not output_q.empty():
                response = output_q.get_nowait()
                parsed = parse_message(response)
                print(f"📥 Response: {parsed['content']}")
                print(f"   Status: {parsed['meta'].get('status', 'unknown')}")
        except queue.Empty:
            print("   No response received")
    
    # Stop plugin
    input_q.put("STOP")
    plugin_thread.join(timeout=2)
    
    print("\n✅ Plugin test completed")

if __name__ == "__main__":
    # Run test if executed directly
    test_plugin()
