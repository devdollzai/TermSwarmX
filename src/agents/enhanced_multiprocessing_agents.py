"""
Enhanced Multiprocessing Agent Functions for AI Swarm IDE
Features: LLM integration, persistent memory, structured messaging, error handling
"""

import multiprocessing as mp
import queue
import time
import sys
import json
import sqlite3
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Configure logging for multiprocessing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Database setup
DB_FILE = "swarm_memory.db"

def init_db():
    """Initialize the SQLite database for persistent memory"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables for different types of data
    cursor.execute('''CREATE TABLE IF NOT EXISTS task_history 
                      (id INTEGER PRIMARY KEY, timestamp TEXT, agent TEXT, task_type TEXT, 
                       task_content TEXT, result TEXT, status TEXT, metadata TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS agent_states 
                      (id INTEGER PRIMARY KEY, agent_name TEXT, last_active TEXT, 
                       tasks_completed INTEGER, tasks_failed INTEGER, current_status TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS code_snippets 
                      (id INTEGER PRIMARY KEY, timestamp TEXT, agent TEXT, code_type TEXT, 
                       code_content TEXT, language TEXT, metadata TEXT)''')
    
    conn.commit()
    conn.close()

def log_to_db(agent: str, task_type: str, task_content: str, result: str, 
              status: str = "success", metadata: Optional[Dict] = None):
    """Log task execution to database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        metadata_str = json.dumps(metadata) if metadata else "{}"
        
        cursor.execute("""
            INSERT INTO task_history (timestamp, agent, task_type, task_content, result, status, metadata) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, agent, task_type, task_content, result, status, metadata_str))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to log to database: {e}")

def update_agent_state(agent_name: str, status: str, tasks_completed: int = 0, tasks_failed: int = 0):
    """Update agent state in database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        # Check if agent exists
        cursor.execute("SELECT id FROM agent_states WHERE agent_name = ?", (agent_name,))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE agent_states 
                SET last_active = ?, tasks_completed = ?, tasks_failed = ?, current_status = ?
                WHERE agent_name = ?
            """, (timestamp, tasks_completed, tasks_failed, status, agent_name))
        else:
            cursor.execute("""
                INSERT INTO agent_states (agent_name, last_active, tasks_completed, tasks_failed, current_status)
                VALUES (?, ?, ?, ?, ?)
            """, (agent_name, timestamp, tasks_completed, tasks_failed, status))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to update agent state: {e}")

# Structured message format (JSON)
def create_message(content: Any, meta: Optional[Dict] = None) -> str:
    """Create a structured message with metadata"""
    message = {
        "content": content,
        "meta": meta or {},
        "timestamp": datetime.now().isoformat(),
        "message_id": f"msg_{int(time.time() * 1000)}"
    }
    return json.dumps(message)

def parse_message(msg: str) -> Dict[str, Any]:
    """Parse a structured message"""
    try:
        return json.loads(msg)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse message: {e}")
        return {"content": msg, "meta": {"error": "parse_error"}, "timestamp": datetime.now().isoformat()}

# LLM Integration (placeholder - replace with actual LLM calls)
class LLMInterface:
    """Interface for LLM calls - replace with actual implementation"""
    
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.logger = logging.getLogger(f"llm_{model_name}")
    
    def generate_code(self, prompt: str, language: str = "python", context: str = "") -> str:
        """Generate code using LLM - replace with actual LLM call"""
        # Placeholder implementation - replace with:
        # import ollama
        # response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
        # return response['message']['content']
        
        self.logger.info(f"Generating {language} code for: {prompt}")
        
        # Simulate LLM processing time
        time.sleep(2)
        
        # Generate sample code based on prompt
        if "function" in prompt.lower():
            return f'''def {prompt.lower().replace(" ", "_")}(param1, param2):
    """
    {prompt}
    
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
    result = {prompt.lower().replace(" ", "_")}(10, 20)
    print(f"Result: {{result}}")'''
        
        elif "class" in prompt.lower():
            return f'''class {prompt.replace(" ", "")}:
    """
    {prompt}
    """
    
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name

# Example usage
obj = {prompt.replace(" ", "")}("Example")
print(obj.get_name())'''
        
        else:
            return f'''# {prompt}
# This is a sample implementation generated by AI

def main():
    print("Hello, World!")
    print("This code was generated by the AI Swarm IDE Code Agent")

if __name__ == "__main__":
    main()'''
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code using LLM - replace with actual LLM call"""
        self.logger.info("Analyzing code quality")
        
        # Simulate LLM analysis
        time.sleep(1.5)
        
        # Basic code analysis
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        metrics = {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_ratio": len([line for line in lines if line.strip().startswith('#')]) / max(len(lines), 1),
            "function_count": len([line for line in lines if line.strip().startswith('def ')]),
            "class_count": len([line for line in lines if line.strip().startswith('class ')])
        }
        
        recommendations = []
        if metrics["comment_ratio"] < 0.1:
            recommendations.append("Consider adding more comments for better readability")
        if metrics["function_count"] == 0:
            recommendations.append("Consider breaking down code into smaller functions")
        
        return {
            "metrics": metrics,
            "recommendations": recommendations,
            "overall_score": min(100, max(0, 100 - len(recommendations) * 20))
        }

# Enhanced Code Generation Agent
def enhanced_code_gen_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """Enhanced code generation agent with LLM integration and persistent memory"""
    logger = logging.getLogger("enhanced_code_gen_agent")
    agent_name = kwargs.get("name", "EnhancedCodeGenAgent")
    model_name = kwargs.get("model_name", "mistral")
    
    # Initialize LLM interface
    llm = LLMInterface(model_name)
    
    # Initialize database
    init_db()
    
    # Update agent state
    update_agent_state(agent_name, "started")
    
    logger.info(f"Enhanced code generation agent started with model: {model_name}")
    
    tasks_completed = 0
    tasks_failed = 0
    
    try:
        while True:
            try:
                # Get task with timeout
                raw_task = input_queue.get(timeout=1)
                
                if raw_task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                # Parse structured message
                task = parse_message(raw_task)
                task_content = task.get('content', '')
                task_type = task.get('meta', {}).get('task_type', 'code_generation')
                
                logger.info(f"Processing task: {task_content[:50]}...")
                
                # Generate code using LLM
                try:
                    language = task.get('meta', {}).get('language', 'python')
                    context = task.get('meta', {}).get('context', '')
                    
                    generated_code = llm.generate_code(task_content, language, context)
                    
                    # Create result with metadata
                    result_meta = {
                        "status": "success",
                        "agent": agent_name,
                        "model": model_name,
                        "language": language,
                        "lines_of_code": len(generated_code.split('\n')),
                        "generation_time": datetime.now().isoformat()
                    }
                    
                    # Log to database
                    log_to_db(agent_name, task_type, task_content, generated_code, "success", result_meta)
                    
                    # Send structured result
                    output_queue.put(create_message(generated_code, result_meta))
                    
                    tasks_completed += 1
                    update_agent_state(agent_name, "idle", tasks_completed, tasks_failed)
                    
                    logger.info(f"Task completed successfully. Generated {result_meta['lines_of_code']} lines of code.")
                    
                except Exception as e:
                    error_msg = f"Error generating code: {str(e)}"
                    error_meta = {
                        "status": "error",
                        "agent": agent_name,
                        "error": str(e),
                        "error_time": datetime.now().isoformat()
                    }
                    
                    # Log error to database
                    log_to_db(agent_name, task_type, task_content, error_msg, "error", error_meta)
                    
                    # Send error result
                    output_queue.put(create_message(error_msg, error_meta))
                    
                    tasks_failed += 1
                    update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
                    
                    logger.error(f"Task failed: {e}")
                
            except queue.Empty:
                # No tasks available, continue loop
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Unexpected error in code generation agent: {e}")
                tasks_failed += 1
                update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
    
    except Exception as e:
        logger.error(f"Fatal error in enhanced code generation agent: {e}")
    finally:
        # Final state update
        update_agent_state(agent_name, "stopped", tasks_completed, tasks_failed)
        logger.info(f"Enhanced code generation agent stopped. Tasks: {tasks_completed} completed, {tasks_failed} failed")

# Enhanced Debug Agent
def enhanced_debug_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """Enhanced debug agent with better error analysis and persistent memory"""
    logger = logging.getLogger("enhanced_debug_agent")
    agent_name = kwargs.get("name", "EnhancedDebugAgent")
    
    # Initialize database
    init_db()
    update_agent_state(agent_name, "started")
    
    logger.info("Enhanced debug agent started")
    
    tasks_completed = 0
    tasks_failed = 0
    
    try:
        while True:
            try:
                raw_task = input_queue.get(timeout=1)
                
                if raw_task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                task = parse_message(raw_task)
                code_to_debug = task.get('content', '')
                error_message = task.get('meta', {}).get('error_message', '')
                task_type = task.get('meta', {}).get('task_type', 'debugging')
                
                logger.info(f"Processing debug task: {code_to_debug[:50]}...")
                
                try:
                    # Enhanced debugging logic
                    issues = []
                    suggested_fixes = []
                    
                    # Check for common issues
                    if "NameError" in error_message:
                        issues.append("Undefined variable or function")
                        suggested_fixes.append("Check variable names and ensure all functions are defined")
                    
                    if "IndentationError" in error_message:
                        issues.append("Incorrect indentation")
                        suggested_fixes.append("Check indentation levels and ensure consistency")
                    
                    if "SyntaxError" in error_message:
                        issues.append("Syntax error in code")
                        suggested_fixes.append("Review code syntax and check for missing brackets, quotes, etc.")
                    
                    # Try to compile the code
                    try:
                        compile(code_to_debug, '<string>', 'exec')
                        compilation_status = "No syntax errors found"
                    except SyntaxError as e:
                        compilation_status = f"Syntax error: {str(e)}"
                        issues.append(f"Compilation error: {str(e)}")
                    
                    # Create debug result
                    debug_result = {
                        "issues": issues,
                        "suggested_fixes": suggested_fixes,
                        "compilation_status": compilation_status,
                        "error_type": error_message.split(":")[0] if ":" in error_message else "Unknown"
                    }
                    
                    result_meta = {
                        "status": "success",
                        "agent": agent_name,
                        "issues_found": len(issues),
                        "compilation_status": compilation_status,
                        "debug_time": datetime.now().isoformat()
                    }
                    
                    # Log to database
                    log_to_db(agent_name, task_type, code_to_debug, json.dumps(debug_result), "success", result_meta)
                    
                    # Send result
                    output_queue.put(create_message(debug_result, result_meta))
                    
                    tasks_completed += 1
                    update_agent_state(agent_name, "idle", tasks_completed, tasks_failed)
                    
                    logger.info(f"Debug task completed. Found {len(issues)} issues.")
                    
                except Exception as e:
                    error_msg = f"Error during debugging: {str(e)}"
                    error_meta = {
                        "status": "error",
                        "agent": agent_name,
                        "error": str(e),
                        "error_time": datetime.now().isoformat()
                    }
                    
                    log_to_db(agent_name, task_type, code_to_debug, error_msg, "error", error_meta)
                    output_queue.put(create_message(error_msg, error_meta))
                    
                    tasks_failed += 1
                    update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
                    
                    logger.error(f"Debug task failed: {e}")
                
            except queue.Empty:
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Unexpected error in debug agent: {e}")
                tasks_failed += 1
                update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
    
    except Exception as e:
        logger.error(f"Fatal error in enhanced debug agent: {e}")
    finally:
        update_agent_state(agent_name, "stopped", tasks_completed, tasks_failed)
        logger.info(f"Enhanced debug agent stopped. Tasks: {tasks_completed} completed, {tasks_failed} failed")

# Enhanced Analysis Agent
def enhanced_analysis_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """Enhanced code analysis agent with LLM integration"""
    logger = logging.getLogger("enhanced_analysis_agent")
    agent_name = kwargs.get("name", "EnhancedAnalysisAgent")
    
    # Initialize LLM interface and database
    llm = LLMInterface("analysis_model")
    init_db()
    update_agent_state(agent_name, "started")
    
    logger.info("Enhanced analysis agent started")
    
    tasks_completed = 0
    tasks_failed = 0
    
    try:
        while True:
            try:
                raw_task = input_queue.get(timeout=1)
                
                if raw_task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                task = parse_message(raw_task)
                code_to_analyze = task.get('content', '')
                task_type = task.get('meta', {}).get('task_type', 'code_analysis')
                
                logger.info(f"Processing analysis task: {code_to_analyze[:50]}...")
                
                try:
                    # Use LLM for enhanced analysis
                    analysis_result = llm.analyze_code(code_to_analyze)
                    
                    result_meta = {
                        "status": "success",
                        "agent": agent_name,
                        "overall_score": analysis_result.get('overall_score', 0),
                        "recommendations_count": len(analysis_result.get('recommendations', [])),
                        "analysis_time": datetime.now().isoformat()
                    }
                    
                    # Log to database
                    log_to_db(agent_name, task_type, code_to_analyze, json.dumps(analysis_result), "success", result_meta)
                    
                    # Send result
                    output_queue.put(create_message(analysis_result, result_meta))
                    
                    tasks_completed += 1
                    update_agent_state(agent_name, "idle", tasks_completed, tasks_failed)
                    
                    logger.info(f"Analysis completed. Score: {analysis_result.get('overall_score', 0)}/100")
                    
                except Exception as e:
                    error_msg = f"Error during analysis: {str(e)}"
                    error_meta = {
                        "status": "error",
                        "agent": agent_name,
                        "error": str(e),
                        "error_time": datetime.now().isoformat()
                    }
                    
                    log_to_db(agent_name, task_type, code_to_analyze, error_msg, "error", error_meta)
                    output_queue.put(create_message(error_msg, error_meta))
                    
                    tasks_failed += 1
                    update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
                    
                    logger.error(f"Analysis task failed: {e}")
                
            except queue.Empty:
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Unexpected error in analysis agent: {e}")
                tasks_failed += 1
                update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
    
    except Exception as e:
        logger.error(f"Fatal error in enhanced analysis agent: {e}")
    finally:
        update_agent_state(agent_name, "stopped", tasks_completed, tasks_failed)
        logger.info(f"Enhanced analysis agent stopped. Tasks: {tasks_completed} completed, {tasks_failed} failed")

# File Management Agent
def file_mgmt_agent(input_queue: mp.Queue, output_queue: mp.Queue, **kwargs):
    """File management agent for basic file operations"""
    logger = logging.getLogger("file_mgmt_agent")
    agent_name = kwargs.get("name", "FileManagementAgent")
    
    # Initialize database
    init_db()
    update_agent_state(agent_name, "started")
    
    logger.info("File management agent started")
    
    tasks_completed = 0
    tasks_failed = 0
    
    try:
        while True:
            try:
                raw_task = input_queue.get(timeout=1)
                
                if raw_task == "STOP":
                    logger.info("Received STOP signal, shutting down")
                    break
                
                task = parse_message(raw_task)
                task_content = task.get('content', '')
                task_type = task.get('meta', {}).get('task_type', 'file_management')
                
                logger.info(f"Processing file task: {task_content}")
                
                try:
                    result = ""
                    
                    if task_content == "list_files":
                        # List files in current directory
                        files = os.listdir(".")
                        result = f"Files in current directory: {', '.join(files)}"
                    
                    elif task_content.startswith("read:"):
                        # Read a file
                        filename = task_content[5:].strip()
                        if os.path.exists(filename):
                            with open(filename, 'r') as f:
                                content = f.read()
                            result = f"File '{filename}' contents:\n{content}"
                        else:
                            result = f"File '{filename}' not found"
                    
                    elif task_content.startswith("write:"):
                        # Write to a file (basic implementation)
                        parts = task_content[6:].split(":", 1)
                        if len(parts) == 2:
                            filename, content = parts
                            filename = filename.strip()
                            content = content.strip()
                            
                            # Basic safety check
                            if not filename.startswith("/") and not filename.startswith(".."):
                                with open(filename, 'w') as f:
                                    f.write(content)
                                result = f"Successfully wrote to '{filename}'"
                            else:
                                result = "Invalid filename (security restriction)"
                        else:
                            result = "Invalid write format. Use: write:filename:content"
                    
                    else:
                        result = f"Unknown file task: {task_content}"
                    
                    result_meta = {
                        "status": "success",
                        "agent": agent_name,
                        "task": task_content,
                        "execution_time": datetime.now().isoformat()
                    }
                    
                    # Log to database
                    log_to_db(agent_name, task_type, task_content, result, "success", result_meta)
                    
                    # Send result
                    output_queue.put(create_message(result, result_meta))
                    
                    tasks_completed += 1
                    update_agent_state(agent_name, "idle", tasks_completed, tasks_failed)
                    
                    logger.info(f"File task completed: {task_content}")
                    
                except Exception as e:
                    error_msg = f"Error during file operation: {str(e)}"
                    error_meta = {
                        "status": "error",
                        "agent": agent_name,
                        "error": str(e),
                        "error_time": datetime.now().isoformat()
                    }
                    
                    log_to_db(agent_name, task_type, task_content, error_msg, "error", error_meta)
                    output_queue.put(create_message(error_msg, error_meta))
                    
                    tasks_failed += 1
                    update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
                    
                    logger.error(f"File task failed: {e}")
                
            except queue.Empty:
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Unexpected error in file management agent: {e}")
                tasks_failed += 1
                update_agent_state(agent_name, "error", tasks_completed, tasks_failed)
    
    except Exception as e:
        logger.error(f"Fatal error in file management agent: {e}")
    finally:
        update_agent_state(agent_name, "stopped", tasks_completed, tasks_failed)
        logger.info(f"File management agent stopped. Tasks: {tasks_completed} completed, {tasks_failed} failed")

# Database query functions for external use
def get_task_history(limit: int = 100, agent: Optional[str] = None) -> list:
    """Get task execution history from database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        if agent:
            cursor.execute("""
                SELECT timestamp, agent, task_type, task_content, result, status 
                FROM task_history 
                WHERE agent = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (agent, limit))
        else:
            cursor.execute("""
                SELECT timestamp, agent, task_type, task_content, result, status 
                FROM task_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "timestamp": row[0],
                "agent": row[1],
                "task_type": row[2],
                "task_content": row[3],
                "result": row[4],
                "status": row[5]
            }
            for row in results
        ]
    except Exception as e:
        logging.error(f"Failed to get task history: {e}")
        return []

def get_agent_stats() -> Dict[str, Any]:
    """Get agent performance statistics"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM agent_states")
        results = cursor.fetchall()
        conn.close()
        
        stats = {}
        for row in results:
            agent_name = row[1]
            stats[agent_name] = {
                "last_active": row[2],
                "tasks_completed": row[3],
                "tasks_failed": row[4],
                "current_status": row[5]
            }
        
        return stats
    except Exception as e:
        logging.error(f"Failed to get agent stats: {e}")
        return {}
