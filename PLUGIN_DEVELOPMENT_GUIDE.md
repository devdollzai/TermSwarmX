# DevDollz: Atelier Edition - Plugin Development Guide

## 🚀 Plugin System Overview

The DevDollz: Atelier Edition IDE features a powerful plugin architecture that allows developers to extend the IDE's capabilities with custom AI agents. Built for power users who demand excellence in their development environment, plugins run in isolated processes and communicate with the main IDE through a standardized interface, making them safe, efficient, and easy to develop.

## 🏗️ Plugin Architecture

### Core Components
- **Plugin Interface**: All plugins must implement a `plugin_agent(input_queue, output_queue)` function
- **Process Isolation**: Each plugin runs in its own multiprocessing process
- **Queue Communication**: Plugins communicate via input/output queues using JSON messages
- **Dynamic Loading**: Plugins can be loaded and unloaded at runtime without restarting the IDE

### Security Features
- **Sandboxed Execution**: Plugins run in separate processes from the main IDE
- **Path Validation**: Plugins can only be loaded from within the project directory
- **Error Isolation**: Plugin crashes don't affect the main IDE
- **Resource Management**: Automatic cleanup of plugin processes

## 📝 Plugin Interface Specification

### Required Function Signature
```python
def plugin_agent(input_queue, output_queue):
    """
    Plugin agent function - required interface for DevDollz: Atelier Edition plugins
    
    Args:
        input_queue: multiprocessing.Queue to receive tasks from the orchestrator
        output_queue: multiprocessing.Queue to send results back to the orchestrator
    """
    pass
```

### Message Format
Plugins communicate using JSON messages with this structure:
```python
{
    "content": "task or result content",
    "meta": {
        "type": "command_type",
        "status": "success|error",
        "timestamp": 1234567890.123,
        "error": "error_message_if_applicable"
    }
}
```

### Lifecycle Management
1. **Initialization**: Plugin starts and enters the main loop
2. **Task Processing**: Plugin waits for tasks from `input_queue`
3. **Result Sending**: Plugin sends results to `output_queue`
4. **Shutdown**: Plugin receives "STOP" signal and exits cleanly

## 🛠️ Creating Your First Plugin

### Step 1: Create the Plugin File
Create a Python file (e.g., `my_plugin.py`) with this basic structure:

```python
import time
import json

def create_message(content, meta=None):
    """Helper function to create properly formatted messages - DevDollz: Atelier Edition"""
    return json.dumps({"content": content, "meta": meta or {}})

def plugin_agent(input_queue, output_queue):
    """Your plugin agent implementation - DevDollz: Atelier Edition"""
    print(f"[Plugin] DevDollz: Atelier Edition - My plugin started")
    
    while True:
        try:
            # Wait for a task
            raw_task = input_queue.get(timeout=1)
            
            if raw_task == "STOP":
                print(f"[Plugin] DevDollz: Atelier Edition - My plugin stopping")
                break
            
            # Parse the task
            try:
                task = json.loads(raw_task)
                task_content = task.get('content', '')
                cmd_type = task.get('meta', {}).get('type', 'custom')
            except:
                task_content = str(raw_task)
                cmd_type = 'custom'
            
            # Process the task
            result = process_task(task_content, cmd_type)
            
            # Send the result back
            meta = {"status": "success", "timestamp": time.time()}
            output_queue.put(create_message(result, meta))
            
        except Exception as e:
            error_msg = f"DevDollz: Atelier Edition - Plugin error: {str(e)}"
            meta = {"status": "error", "error": str(e)}
            output_queue.put(create_message(error_msg, meta))

def process_task(content, cmd_type):
    """Process the actual task - DevDollz: Atelier Edition"""
    if cmd_type == "custom":
        return f"DevDollz: Atelier Edition - Processed: {content}"
    else:
        return f"DevDollz: Atelier Edition - Unknown command type: {cmd_type}"

if __name__ == "__main__":
    print("DevDollz: Atelier Edition - Sample Plugin")
    print("Built for power users - DevDolls")
    print("To use it, load it into the IDE with: plugin load my_plugin.py")
    print("Then use it with: my_plugin <task_description>")
```

### Step 2: Load the Plugin
In the DevDollz: Atelier Edition IDE:
```bash
plugin load my_plugin.py
```

### Step 3: Use the Plugin
```bash
my_plugin analyze this text
```

## 🎯 Advanced Plugin Examples

### Example 1: Code Quality Analyzer
```python
import ast
import time
import json

def plugin_agent(input_queue, output_queue):
    """Code quality analysis plugin - DevDollz: Atelier Edition"""
    print(f"[Plugin] DevDollz: Atelier Edition - Code Quality Analyzer started")
    
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
            
            task = json.loads(raw_task)
            code = task.get('content', '')
            
            # Analyze code quality
            result = analyze_code_quality(code)
            
            meta = {"status": "success", "timestamp": time.time()}
            output_queue.put(create_message(result, meta))
            
        except Exception as e:
            error_msg = f"DevDollz: Atelier Edition - Code quality plugin error: {str(e)}"
            meta = {"status": "error", "error": str(e)}
            output_queue.put(create_message(error_msg, meta))

def analyze_code_quality(code):
    """Analyze Python code for quality issues - DevDollz: Atelier Edition"""
    try:
        tree = ast.parse(code)
        
        # Count various code elements
        functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        imports = len([node for node in ast.walk(tree) if isinstance(node, ast.Import)])
        
        # Check for common issues
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id == 'l':
                issues.append("Single letter variable 'l' detected (confusing with '1')")
            if isinstance(node, ast.FunctionDef) and len(node.args.args) > 5:
                issues.append(f"Function '{node.name}' has too many parameters ({len(node.args.args)})")
        
        return f"""DevDollz: Atelier Edition - Code Quality Analysis:
        
📊 Structure:
• Functions: {functions}
• Classes: {classes}
• Imports: {imports}

⚠️ Issues Found:
{chr(10).join(f"• {issue}" for issue in issues) if issues else "• No major issues detected"}"""
        
    except SyntaxError as e:
        return f"DevDollz: Atelier Edition - Syntax Error: {e}"
    except Exception as e:
        return f"DevDollz: Atelier Edition - Analysis Error: {e}"
```

### Example 2: Documentation Generator
```python
import time
import json
import re

def plugin_agent(input_queue, output_queue):
    """Documentation generation plugin - DevDollz: Atelier Edition"""
    print(f"[Plugin] DevDollz: Atelier Edition - Documentation Generator started")
    
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
            
            task = json.loads(raw_task)
            code = task.get('content', '')
            
            # Generate documentation
            result = generate_documentation(code)
            
            meta = {"status": "success", "timestamp": time.time()}
            output_queue.put(create_message(result, meta))
            
        except Exception as e:
            error_msg = f"DevDollz: Atelier Edition - Documentation plugin error: {str(e)}"
            meta = {"status": "error", "error": str(e)}
            output_queue.put(create_message(error_msg, meta))

def generate_documentation(code):
    """Generate documentation for Python code - DevDollz: Atelier Edition"""
    lines = code.split('\n')
    doc_lines = []
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Function definition
        if line.startswith('def '):
            func_name = line.split('(')[0][4:]
            doc_lines.append(f"\n## Function: {func_name}")
            doc_lines.append(f"**Line {i}:** `{line}`")
            
            # Extract parameters
            params = re.findall(r'\(([^)]*)\)', line)
            if params and params[0]:
                param_list = params[0].split(',')
                doc_lines.append("**Parameters:**")
                for param in param_list:
                    param = param.strip()
                    if '=' in param:
                        name, default = param.split('=', 1)
                        doc_lines.append(f"- `{name.strip()}` (default: {default.strip()})")
                    else:
                        doc_lines.append(f"- `{param}`")
        
        # Class definition
        elif line.startswith('class '):
            class_name = line.split('(')[0][6:]
            doc_lines.append(f"\n## Class: {class_name}")
            doc_lines.append(f"**Line {i}:** `{line}`")
    
    if doc_lines:
        return "DevDollz: Atelier Edition - Generated Documentation:\n" + "\n".join(doc_lines)
    else:
        return "DevDollz: Atelier Edition - No functions or classes found to document."
```

## 🔒 Security Best Practices

### 1. Input Validation
```python
def safe_process_input(content):
    """Safely process user input - DevDollz: Atelier Edition"""
    # Limit input size
    if len(content) > 10000:
        return "DevDollz: Atelier Edition - Input too large (max 10KB)"
    
    # Sanitize content
    dangerous_chars = ['<', '>', '"', "'", '&']
    if any(char in content for char in dangerous_chars):
        return "DevDollz: Atelier Edition - Input contains potentially dangerous characters"
    
    return content
```

### 2. Resource Limits
```python
import signal
import time

def plugin_agent(input_queue, output_queue):
    """Plugin with resource limits - DevDollz: Atelier Edition"""
    # Set timeout for operations
    def timeout_handler(signum, frame):
        raise TimeoutError("Operation timed out")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
            
            # Set 30-second timeout for processing
            signal.alarm(30)
            try:
                result = process_task(raw_task)
                signal.alarm(0)  # Cancel alarm
            except TimeoutError:
                result = "DevDollz: Atelier Edition - Operation timed out"
            
            output_queue.put(create_message(result, {"status": "success"}))
            
        except Exception as e:
            output_queue.put(create_message(f"DevDollz: Atelier Edition - Error: {e}", {"status": "error"}))
```

### 3. Error Handling
```python
def robust_plugin_agent(input_queue, output_queue):
    """Plugin with robust error handling - DevDollz: Atelier Edition"""
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
            
            # Wrap processing in try-catch
            try:
                result = process_task(raw_task)
                meta = {"status": "success", "timestamp": time.time()}
            except Exception as e:
                result = f"DevDollz: Atelier Edition - Processing failed: {str(e)}"
                meta = {"status": "error", "error": str(e), "timestamp": time.time()}
            
            output_queue.put(create_message(result, meta))
            
        except Exception as e:
            # Even the main loop has error handling
            error_msg = f"DevDollz: Atelier Edition - Critical plugin error: {str(e)}"
            meta = {"status": "error", "error": str(e), "timestamp": time.time()}
            output_queue.put(create_message(error_msg, meta))
```

## 📚 Plugin Development Workflow

### 1. Planning
- Define the plugin's purpose and functionality
- Identify input/output requirements
- Plan error handling and edge cases
- Consider performance implications

### 2. Development
- Start with the basic plugin structure
- Implement core functionality incrementally
- Add comprehensive error handling
- Test with various input types

### 3. Testing
- Test with the sample plugin interface
- Verify error handling works correctly
- Check resource usage and cleanup
- Test edge cases and invalid inputs

### 4. Deployment
- Document the plugin's usage
- Provide examples and use cases
- Include any dependencies or requirements
- Test in the actual DevDollz: Atelier Edition IDE

## 🚨 Common Pitfalls and Solutions

### 1. Infinite Loops
**Problem**: Plugin gets stuck in processing loop
**Solution**: Always include timeout handling and the STOP signal check

### 2. Memory Leaks
**Problem**: Plugin consumes increasing memory
**Solution**: Clear large objects and use proper cleanup in the main loop

### 3. Queue Blocking
**Problem**: Plugin blocks waiting for input
**Solution**: Use timeout in `input_queue.get(timeout=1)`

### 4. Error Propagation
**Problem**: Plugin errors crash the main IDE
**Solution**: Wrap all operations in try-catch blocks

## 🔧 Debugging Plugins

### 1. Console Output
```python
def plugin_agent(input_queue, output_queue):
    """Plugin with debug output - DevDollz: Atelier Edition"""
    print(f"[Plugin] DevDollz: Atelier Edition - Starting plugin with PID: {os.getpid()}")
    
    while True:
        try:
            print(f"[Plugin] DevDollz: Atelier Edition - Waiting for task...")
            raw_task = input_queue.get(timeout=1)
            print(f"[Plugin] DevDollz: Atelier Edition - Received: {raw_task}")
            
            if raw_task == "STOP":
                print(f"[Plugin] DevDollz: Atelier Edition - Stopping...")
                break
            
            # Process task...
            
        except Exception as e:
            print(f"[Plugin] DevDollz: Atelier Edition - Error: {e}")
            import traceback
            traceback.print_exc()
```

### 2. Logging
```python
import logging

def setup_plugin_logging():
    """Setup logging for the plugin - DevDollz: Atelier Edition"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='[Plugin] DevDollz: Atelier Edition - %(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('plugin.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def plugin_agent(input_queue, output_queue):
    """Plugin with logging - DevDollz: Atelier Edition"""
    logger = setup_plugin_logging()
    logger.info("DevDollz: Atelier Edition - Plugin started")
    
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            logger.info(f"DevDollz: Atelier Edition - Received task: {raw_task}")
            
            if raw_task == "STOP":
                logger.info("DevDollz: Atelier Edition - Stopping plugin")
                break
            
            # Process task...
            logger.info("DevDollz: Atelier Edition - Task processed successfully")
            
        except Exception as e:
            logger.error(f"DevDollz: Atelier Edition - Plugin error: {e}", exc_info=True)
```

## 🎉 Getting Started Checklist

- [ ] Create plugin file with `plugin_agent` function
- [ ] Implement basic task processing
- [ ] Add error handling and logging
- [ ] Test with simple inputs
- [ ] Load plugin in DevDollz: Atelier Edition IDE
- [ ] Test plugin functionality
- [ ] Add documentation and examples
- [ ] Share your plugin with the community!

## 📖 Additional Resources

- **Sample Plugin**: `sample_plugin.py` - Basic text analysis plugin
- **Plugin Interface**: See the Orchestrator class in `swarm_ide.py`
- **Message Format**: JSON-based communication protocol
- **Security Guidelines**: Sandboxed execution and input validation

---

*Plugins transform the DevDollz: Atelier Edition IDE from a static tool into a dynamic, extensible platform. Built for power users who demand excellence in their development environment, with the right plugin, you can add any AI capability you can imagine!*

**Brand**: DevDollz: Atelier Edition  
**Author**: Alexis Adams  
**Built for power users - DevDolls**
