"""
Multiprocessing Agent Functions for AI Swarm IDE
These functions run in separate processes and communicate via queues
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import logging
from typing import Dict, Any
from datetime import datetime

# Configure logging for multiprocessing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def code_gen_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """
    Code generation agent that runs in a separate process
    
    Args:
        input_queue: Queue for receiving tasks
        output_queue: Queue for sending results
        **kwargs: Additional configuration parameters
    """
    logger = logging.getLogger("code_gen_agent")
    logger.info("Code generation agent started")
    
    # Agent configuration
    agent_name = kwargs.get("name", "CodeGenAgent")
    model_name = kwargs.get("model_name", "default")
    
    try:
        while True:
            try:
                # Get task with timeout to allow graceful shutdown
                task = input_queue.get(timeout=1)
                
                # Check for shutdown signal
                if task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                # Process the task
                logger.info(f"Processing task: {task.get('title', 'Unknown')}")
                result = _generate_code(task)
                
                # Send result back
                output_queue.put({
                    "task_id": task.get("id"),
                    "result": result,
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                })
                
                logger.info(f"Task completed successfully")
                
            except queue.Empty:
                # No tasks available, continue loop
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing task: {e}")
                # Send error result
                if 'task' in locals():
                    output_queue.put({
                        "task_id": task.get("id"),
                        "error": str(e),
                        "agent": agent_name,
                        "timestamp": datetime.now().isoformat()
                    })
    
    except Exception as e:
        logger.error(f"Fatal error in code generation agent: {e}")
    finally:
        logger.info("Code generation agent stopped")

def debug_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """
    Debug agent that runs in a separate process
    
    Args:
        input_queue: Queue for receiving tasks
        output_queue: Queue for sending results
        **kwargs: Additional configuration parameters
    """
    logger = logging.getLogger("debug_agent")
    logger.info("Debug agent started")
    
    # Agent configuration
    agent_name = kwargs.get("name", "DebugAgent")
    
    try:
        while True:
            try:
                # Get task with timeout to allow graceful shutdown
                task = input_queue.get(timeout=1)
                
                # Check for shutdown signal
                if task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                # Process the task
                logger.info(f"Processing debug task: {task.get('title', 'Unknown')}")
                result = _debug_code(task)
                
                # Send result back
                output_queue.put({
                    "task_id": task.get("id"),
                    "result": result,
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                })
                
                logger.info(f"Debug task completed successfully")
                
            except queue.Empty:
                # No tasks available, continue loop
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing debug task: {e}")
                # Send error result
                if 'task' in locals():
                    output_queue.put({
                        "task_id": task.get("id"),
                        "error": str(e),
                        "agent": agent_name,
                        "timestamp": datetime.now().isoformat()
                    })
    
    except Exception as e:
        logger.error(f"Fatal error in debug agent: {e}")
    finally:
        logger.info("Debug agent stopped")

def analysis_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """
    Code analysis agent that runs in a separate process
    
    Args:
        input_queue: Queue for receiving tasks
        output_queue: Queue for sending results
        **kwargs: Additional configuration parameters
    """
    logger = logging.getLogger("analysis_agent")
    logger.info("Analysis agent started")
    
    # Agent configuration
    agent_name = kwargs.get("name", "AnalysisAgent")
    
    try:
        while True:
            try:
                # Get task with timeout to allow graceful shutdown
                task = input_queue.get(timeout=1)
                
                # Check for shutdown signal
                if task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                # Process the task
                logger.info(f"Processing analysis task: {task.get('title', 'Unknown')}")
                result = _analyze_code(task)
                
                # Send result back
                output_queue.put({
                    "task_id": task.get("id"),
                    "result": result,
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                })
                
                logger.info(f"Analysis task completed successfully")
                
            except queue.Empty:
                # No tasks available, continue loop
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing analysis task: {e}")
                # Send error result
                if 'task' in locals():
                    output_queue.put({
                        "task_id": task.get("id"),
                        "error": str(e),
                        "agent": agent_name,
                        "timestamp": datetime.now().isoformat()
                    })
    
    except Exception as e:
        logger.error(f"Fatal error in analysis agent: {e}")
    finally:
        logger.info("Analysis agent stopped")

def refactor_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """
    Code refactoring agent that runs in a separate process
    
    Args:
        input_queue: Queue for receiving tasks
        output_queue: Queue for sending results
        **kwargs: Additional configuration parameters
    """
    logger = logging.getLogger("refactor_agent")
    logger.info("Refactor agent started")
    
    # Agent configuration
    agent_name = kwargs.get("name", "RefactorAgent")
    
    try:
        while True:
            try:
                # Get task with timeout to allow graceful shutdown
                task = input_queue.get(timeout=1)
                
                # Check for shutdown signal
                if task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                # Process the task
                logger.info(f"Processing refactor task: {task.get('title', 'Unknown')}")
                result = _refactor_code(task)
                
                # Send result back
                output_queue.put({
                    "task_id": task.get("id"),
                    "result": result,
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                })
                
                logger.info(f"Refactor task completed successfully")
                
            except queue.Empty:
                # No tasks available, continue loop
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing refactor task: {e}")
                # Send error result
                if 'task' in locals():
                    output_queue.put({
                        "task_id": task.get("id"),
                        "error": str(e),
                        "agent": agent_name,
                        "timestamp": datetime.now().isoformat()
                    })
    
    except Exception as e:
        logger.error(f"Fatal error in refactor agent: {e}")
    finally:
        logger.info("Refactor agent stopped")

# Helper functions for task processing

def _generate_code(task: Dict[str, Any]) -> Dict[str, Any]:
    """Generate code based on task requirements"""
    requirements = task.get("data", {}).get("requirements", "")
    language = task.get("data", {}).get("language", "python")
    context = task.get("data", {}).get("context", "")
    
    # Simulate processing time
    time.sleep(2)
    
    # Generate sample code based on requirements
    if "function" in requirements.lower():
        generated_code = f'''def {requirements.lower().replace(" ", "_")}(param1, param2):
    """
    {requirements}
    
    Args:
        param1: First parameter
        param2: Second parameter
    
    Returns:
        Result of the operation
    """
    result = param1 + param2
    return result

# Example usage
if __name__ == "__main__":
    result = {requirements.lower().replace(" ", "_")}(10, 20)
    print(f"Result: {{result}}")'''
    
    elif "class" in requirements.lower():
        generated_code = f'''class {requirements.replace(" ", "")}:
    """
    {requirements}
    """
    
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

# Example usage
obj = {requirements.replace(" ", "")}("Example")
print(obj.get_name())'''
    
    else:
        generated_code = f'''# {requirements}
# This is a sample implementation

def main():
    print("Hello, World!")
    print("This code was generated by the AI Swarm IDE Code Agent")

if __name__ == "__main__":
    main()'''
    
    return {
        "generated_code": generated_code,
        "language": language,
        "requirements": requirements,
        "metadata": {
            "lines_of_code": len(generated_code.split('\n')),
            "complexity": "medium",
            "generation_time": datetime.now().isoformat()
        }
    }

def _debug_code(task: Dict[str, Any]) -> Dict[str, Any]:
    """Debug code and identify issues"""
    code = task.get("data", {}).get("code", "")
    error_message = task.get("data", {}).get("error_message", "")
    
    # Simulate processing time
    time.sleep(1.5)
    
    # Simple pattern matching for common issues
    issues = []
    suggested_fixes = []
    
    if "NameError" in error_message:
        issues.append("Undefined variable or function")
        suggested_fixes.append("Check variable names and ensure all functions are defined")
    
    if "IndentationError" in error_message:
        issues.append("Incorrect indentation")
        suggested_fixes.append("Check indentation levels and ensure consistency")
    
    if "SyntaxError" in error_message:
        issues.append("Syntax error in code")
        suggested_fixes.append("Review code syntax and check for missing brackets, quotes, etc.")
    
    # Try to compile the code to check for syntax errors
    try:
        compile(code, '<string>', 'exec')
        compilation_status = "No syntax errors found"
    except SyntaxError as e:
        compilation_status = f"Syntax error: {str(e)}"
        issues.append(f"Compilation error: {str(e)}")
    
    return {
        "debug_result": {
            "issues": issues,
            "suggested_fixes": suggested_fixes,
            "compilation_status": compilation_status,
            "error_type": error_message.split(":")[0] if ":" in error_message else "Unknown"
        },
        "issues_found": len(issues),
        "suggested_fixes": suggested_fixes,
        "debug_time": datetime.now().isoformat()
    }

def _analyze_code(task: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze code quality and provide insights"""
    code = task.get("data", {}).get("code", "")
    
    # Simulate processing time
    time.sleep(1)
    
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    metrics = {
        "total_lines": len(lines),
        "non_empty_lines": len(non_empty_lines),
        "comment_ratio": len([line for line in lines if line.strip().startswith('#')]) / max(len(lines), 1),
        "function_count": len([line for line in lines if line.strip().startswith('def ')]),
        "class_count": len([line for line in lines if line.strip().startswith('class ')]),
        "average_line_length": sum(len(line) for line in non_empty_lines) / max(len(non_empty_lines), 1)
    }
    
    recommendations = []
    if metrics["comment_ratio"] < 0.1:
        recommendations.append("Consider adding more comments for better readability")
    if metrics["function_count"] == 0:
        recommendations.append("Consider breaking down code into smaller functions")
    if metrics["average_line_length"] > 80:
        recommendations.append("Consider breaking long lines for better readability")
    
    return {
        "analysis": {
            "metrics": metrics,
            "recommendations": recommendations,
            "overall_score": min(100, max(0, 100 - len(recommendations) * 20))
        },
        "recommendations": recommendations,
        "metrics": metrics,
        "analysis_time": datetime.now().isoformat()
    }

def _refactor_code(task: Dict[str, Any]) -> Dict[str, Any]:
    """Refactor existing code"""
    code = task.get("data", {}).get("code", "")
    refactoring_type = task.get("data", {}).get("refactoring_type", "general")
    
    # Simulate processing time
    time.sleep(1.5)
    
    # Apply refactoring (simplified)
    if refactoring_type == "extract_method":
        refactored_code = code.replace("def main():", "def main():\n    process_data()\n\ndef process_data():")
        improvements = ["Extracted process_data method", "Improved readability", "Better separation of concerns"]
    elif refactoring_type == "rename_variable":
        refactored_code = code.replace("x = 10", "counter = 10")
        improvements = ["Renamed variable for clarity", "Improved code readability", "Better naming conventions"]
    else:
        # General refactoring
        refactored_code = code.replace("print(", "logger.info(")
        improvements = ["Replaced print with logger", "Improved logging", "Better error handling"]
    
    return {
        "original_code": code,
        "refactored_code": refactored_code,
        "refactoring_type": refactoring_type,
        "improvements": improvements,
        "refactor_time": datetime.now().isoformat()
    }
