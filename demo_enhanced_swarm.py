#!/usr/bin/env python3
"""
Enhanced Demo Script for AI Swarm IDE
Features: LLM integration, persistent memory, structured messaging, database queries
"""

import time
import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.multiprocessing_orchestrator import MultiprocessingOrchestrator
from agents.enhanced_multiprocessing_agents import (
    enhanced_code_gen_agent,
    enhanced_debug_agent,
    enhanced_analysis_agent,
    file_mgmt_agent,
    get_task_history,
    get_agent_stats,
    init_db
)

def print_banner():
    """Print a nice banner for the demo"""
    print("🚀 AI Swarm IDE - Enhanced Multiprocessing Demo")
    print("=" * 60)
    print("✨ Features: LLM Integration, Persistent Memory, Structured Messaging")
    print("📊 Database: SQLite with task history and agent statistics")
    print("🤖 Agents: Enhanced code generation, debugging, analysis, file management")
    print("=" * 60)

def main():
    """Main enhanced demo function"""
    print_banner()
    
    # Initialize database
    print("\n🗄️  Initializing persistent memory database...")
    init_db()
    print("✅ Database initialized successfully")
    
    # Initialize the orchestrator
    orchestrator = MultiprocessingOrchestrator(max_workers=4)
    
    try:
        # Register enhanced agents
        print("\n📋 Registering enhanced agents...")
        
        # Enhanced Code Generation Agent
        code_agent_id = orchestrator.register_agent(
            name="EnhancedCodeGenAgent",
            agent_type="code_generation",
            agent_function=enhanced_code_gen_agent,
            capabilities=["code_generation", "function_creation", "class_creation", "llm_integration"],
            model_name="mistral"
        )
        
        # Enhanced Debug Agent
        debug_agent_id = orchestrator.register_agent(
            name="EnhancedDebugAgent",
            agent_type="debugging",
            agent_function=enhanced_debug_agent,
            capabilities=["debugging", "error_analysis", "syntax_checking", "persistent_memory"]
        )
        
        # Enhanced Analysis Agent
        analysis_agent_id = orchestrator.register_agent(
            name="EnhancedAnalysisAgent",
            agent_type="analysis",
            agent_function=enhanced_analysis_agent,
            capabilities=["code_analysis", "quality_assessment", "metrics_calculation", "llm_integration"]
        )
        
        # File Management Agent
        file_agent_id = orchestrator.register_agent(
            name="FileManagementAgent",
            agent_type="file_management",
            agent_function=file_mgmt_agent,
            capabilities=["file_operations", "directory_listing", "file_reading", "file_writing"]
        )
        
        print(f"✅ Registered {len(orchestrator.agents)} enhanced agents")
        
        # Wait for agents to start up
        print("\n⏳ Waiting for agents to initialize...")
        time.sleep(3)
        
        # Display initial status
        print("\n📊 Initial Status:")
        orchestrator.display_status()
        
        # Submit enhanced sample tasks
        print("\n📝 Submitting enhanced sample tasks...")
        
        # Task 1: Generate a function with enhanced metadata
        task1_id = orchestrator.submit_task(
            task_data={
                "title": "Generate a function",
                "requirements": "Create a function to calculate fibonacci numbers",
                "language": "python",
                "context": "Mathematical utility function for educational purposes"
            },
            agent_type="code_generation",
            priority=3
        )
        
        # Task 2: Debug code with error context
        task2_id = orchestrator.submit_task(
            task_data={
                "title": "Debug code",
                "code": "def test():\n    x = 10\n    print(x + y)",  # y is undefined
                "error_message": "NameError: name 'y' is not defined",
                "context": "User debugging session"
            },
            agent_type="debugging",
            priority=2
        )
        
        # Task 3: Analyze code quality with enhanced metrics
        task3_id = orchestrator.submit_task(
            task_data={
                "title": "Analyze code quality",
                "code": """def calculate_sum(a, b):
    return a + b

def main():
    result = calculate_sum(5, 10)
    print(result)

if __name__ == "__main__":
    main()""",
                "analysis_type": "comprehensive",
                "focus_areas": ["readability", "maintainability", "performance"]
            },
            agent_type="analysis",
            priority=1
        )
        
        # Task 4: File management operations
        task4_id = orchestrator.submit_task(
            task_data={
                "title": "File operations",
                "operation": "list_files",
                "context": "Current directory listing"
            },
            agent_type="file_management",
            priority=2
        )
        
        # Task 5: Write a sample file
        task5_id = orchestrator.submit_task(
            task_data={
                "title": "Create sample file",
                "operation": "write",
                "filename": "sample_output.py",
                "content": "# Sample file created by AI Swarm IDE\nprint('Hello from generated file!')"
            },
            agent_type="file_management",
            priority=1
        )
        
        print(f"✅ Submitted {len(orchestrator.task_queue)} enhanced tasks")
        
        # Process pending tasks
        print("\n🔄 Processing pending tasks...")
        orchestrator.process_pending_tasks()
        
        # Main processing loop with enhanced result handling
        print("\n⏳ Processing tasks (this may take a few seconds)...")
        max_wait_time = 45  # Increased wait time for enhanced processing
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # Check for results
            results = orchestrator.get_results()
            
            if results:
                print(f"\n📤 Received {len(results)} enhanced results:")
                for result in results:
                    print(f"\n🤖 {result['agent_name']}:")
                    
                    # Parse the structured result
                    try:
                        parsed_result = json.loads(result['result']) if isinstance(result['result'], str) else result['result']
                        
                        if 'error' in result:
                            print(f"❌ Error: {result['error']}")
                        else:
                            print(f"✅ Task completed successfully")
                            
                            # Display enhanced result information
                            if 'generated_code' in parsed_result:
                                print(f"📝 Generated {parsed_result.get('metadata', {}).get('lines_of_code', 0)} lines of code")
                                print(f"🔧 Language: {parsed_result.get('metadata', {}).get('language', 'Unknown')}")
                                print(f"🤖 Model: {parsed_result.get('metadata', {}).get('model', 'Unknown')}")
                                
                            elif 'debug_result' in parsed_result:
                                debug_data = parsed_result['debug_result']
                                print(f"🐛 Found {len(debug_data.get('issues', []))} issues")
                                print(f"🔍 Compilation: {debug_data.get('compilation_status', 'Unknown')}")
                                
                            elif 'analysis' in parsed_result:
                                analysis_data = parsed_result['analysis']
                                print(f"📊 Code quality score: {analysis_data.get('overall_score', 0)}/100")
                                print(f"📋 Recommendations: {len(analysis_data.get('recommendations', []))}")
                                
                            elif 'refactored_code' in parsed_result:
                                print(f"🔄 Applied {parsed_result.get('refactoring_type', 'general')} refactoring")
                                
                            elif isinstance(parsed_result, str) and "Files in current directory" in parsed_result:
                                print(f"📁 {parsed_result}")
                                
                            elif isinstance(parsed_result, str) and "Successfully wrote to" in parsed_result:
                                print(f"✍️  {parsed_result}")
                                
                            elif isinstance(parsed_result, str) and "File" in parsed_result:
                                print(f"📄 {parsed_result}")
                    
                    except Exception as e:
                        print(f"📄 Raw result: {result['result'][:100]}...")
                    
                    # Display metadata if available
                    if 'timestamp' in result:
                        print(f"⏰ Timestamp: {result['timestamp']}")
            
            # Process any new pending tasks
            orchestrator.process_pending_tasks()
            
            # Check if all tasks are completed
            if not orchestrator.task_queue:
                print("\n✅ All tasks completed!")
                break
            
            # Wait before checking again
            time.sleep(1)
        
        # Final status display
        print("\n📊 Final Status:")
        orchestrator.display_status()
        
        # Health check
        print("\n🏥 Health Check:")
        health_status = orchestrator.health_check()
        for agent_id, status in health_status.items():
            agent_name = orchestrator.agents[agent_id].name
            print(f"🤖 {agent_name}: {status['status']}")
        
        # Database queries demonstration
        print("\n🗄️  Database Queries Demonstration:")
        
        # Get task history
        print("\n📋 Recent Task History:")
        history = get_task_history(limit=10)
        for i, record in enumerate(history[:5], 1):  # Show first 5
            print(f"  {i}. [{record['timestamp'][:19]}] {record['agent']}: {record['task_type']} - {record['status']}")
        
        # Get agent statistics
        print("\n📊 Agent Performance Statistics:")
        agent_stats = get_agent_stats()
        for agent_name, stats in agent_stats.items():
            print(f"  🤖 {agent_name}:")
            print(f"    📈 Tasks completed: {stats['tasks_completed']}")
            print(f"    ❌ Tasks failed: {stats['tasks_failed']}")
            print(f"    🕒 Last active: {stats['last_active'][:19]}")
            print(f"    📊 Current status: {stats['current_status']}")
        
        print("\n🎉 Enhanced demo completed successfully!")
        print("💾 All data has been persisted to swarm_memory.db")
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean shutdown
        print("\n🛑 Shutting down orchestrator...")
        orchestrator.shutdown()
        print("✅ Shutdown complete")

def interactive_mode():
    """Interactive command-line interface with enhanced features"""
    print_banner()
    print("\n🎮 Interactive Mode - Enhanced Features Available")
    print("=" * 60)
    
    # Initialize database
    print("\n🗄️  Initializing persistent memory database...")
    init_db()
    print("✅ Database initialized successfully")
    
    # Initialize the orchestrator
    orchestrator = MultiprocessingOrchestrator(max_workers=4)
    
    try:
        # Register enhanced agents
        print("\n📋 Registering enhanced agents...")
        
        orchestrator.register_agent(
            name="EnhancedCodeGenAgent",
            agent_type="code_generation",
            agent_function=enhanced_code_gen_agent,
            capabilities=["code_generation", "function_creation", "class_creation", "llm_integration"],
            model_name="mistral"
        )
        
        orchestrator.register_agent(
            name="EnhancedDebugAgent",
            agent_type="debugging",
            agent_function=enhanced_debug_agent,
            capabilities=["debugging", "error_analysis", "syntax_checking", "persistent_memory"]
        )
        
        orchestrator.register_agent(
            name="EnhancedAnalysisAgent",
            agent_type="analysis",
            agent_function=enhanced_analysis_agent,
            capabilities=["code_analysis", "quality_assessment", "metrics_calculation", "llm_integration"]
        )
        
        orchestrator.register_agent(
            name="FileManagementAgent",
            agent_type="file_management",
            agent_function=file_mgmt_agent,
            capabilities=["file_operations", "directory_listing", "file_reading", "file_writing"]
        )
        
        print("✅ Enhanced agents registered. Type 'help' for available commands.")
        
        # Wait for agents to start
        time.sleep(3)
        
        # Command loop
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                elif command.lower() == 'help':
                    print_enhanced_help()
                elif command.lower() == 'status':
                    orchestrator.display_status()
                elif command.lower() == 'health':
                    health_status = orchestrator.health_check()
                    for agent_id, status in health_status.items():
                        agent_name = orchestrator.agents[agent_id].name
                        print(f"🤖 {agent_name}: {status['status']}")
                elif command.lower() == 'results':
                    results = orchestrator.get_results()
                    if results:
                        for result in results:
                            print(f"\n🤖 {result['agent_name']}: {result.get('result', {}).get('title', 'Unknown')}")
                    else:
                        print("No results available")
                elif command.lower() == 'history':
                    show_task_history()
                elif command.lower() == 'stats':
                    show_agent_stats()
                elif command.startswith('gen:'):
                    task = command[4:].strip()
                    orchestrator.route_task("code_generation", {
                        "title": f"Generate: {task}",
                        "requirements": task,
                        "language": "python",
                        "context": "Interactive user request"
                    })
                    print(f"✅ Task submitted to enhanced code generation agent")
                elif command.startswith('debug:'):
                    code = command[6:].strip()
                    orchestrator.route_task("debugging", {
                        "title": "Debug code",
                        "code": code,
                        "error_message": "User requested debugging",
                        "context": "Interactive debugging session"
                    })
                    print(f"✅ Task submitted to enhanced debug agent")
                elif command.startswith('analyze:'):
                    code = command[8:].strip()
                    orchestrator.route_task("analysis", {
                        "title": "Analyze code",
                        "code": code,
                        "analysis_type": "comprehensive"
                    })
                    print(f"✅ Task submitted to enhanced analysis agent")
                elif command.startswith('file:'):
                    task = command[5:].strip()
                    orchestrator.route_task("file_management", {
                        "title": f"File operation: {task}",
                        "operation": task
                    })
                    print(f"✅ Task submitted to file management agent")
                elif command.startswith('read:'):
                    filename = command[5:].strip()
                    orchestrator.route_task("file_management", {
                        "title": f"Read file: {filename}",
                        "operation": "read",
                        "filename": filename
                    })
                    print(f"✅ File read task submitted")
                elif command.startswith('write:'):
                    parts = command[6:].split(":", 1)
                    if len(parts) == 2:
                        filename, content = parts
                        orchestrator.route_task("file_management", {
                            "title": f"Write file: {filename}",
                            "operation": "write",
                            "filename": filename.strip(),
                            "content": content.strip()
                        })
                        print(f"✅ File write task submitted")
                    else:
                        print("❌ Invalid write format. Use: write:filename:content")
                else:
                    print("Unknown command. Type 'help' for available commands.")
                
                # Process pending tasks and check for results
                orchestrator.process_pending_tasks()
                time.sleep(0.5)  # Small delay for processing
                
            except EOFError:
                break
            except KeyboardInterrupt:
                break
    
    finally:
        print("\n🛑 Shutting down...")
        orchestrator.shutdown()

def print_enhanced_help():
    """Print enhanced help information"""
    print("\n📚 Enhanced Commands Available:")
    print("  help                    - Show this help message")
    print("  status                  - Show orchestrator status")
    print("  health                  - Show agent health status")
    print("  results                 - Show available results")
    print("  history                 - Show recent task history from database")
    print("  stats                   - Show agent performance statistics")
    print("  gen: <description>      - Generate code using LLM")
    print("  debug: <code>           - Debug code with enhanced analysis")
    print("  analyze: <code>         - Analyze code quality using LLM")
    print("  file: <operation>       - File management operations")
    print("  read: <filename>        - Read file contents")
    print("  write: <filename>:<content> - Write content to file")
    print("  quit/exit/q             - Exit the program")
    print("\n📝 Enhanced Examples:")
    print("  gen: create a function to calculate factorial")
    print("  debug: def test(): x = 10; print(x + y)")
    print("  analyze: def func(): return 42")
    print("  file: list_files")
    print("  read: sample_output.py")
    print("  write: test.py:print('Hello World')")
    print("\n✨ Enhanced Features:")
    print("  • LLM Integration (placeholder - replace with actual LLM)")
    print("  • Persistent Memory (SQLite database)")
    print("  • Structured Messaging (JSON with metadata)")
    print("  • Enhanced Error Handling")
    print("  • Task History Tracking")
    print("  • Agent Performance Metrics")

def show_task_history():
    """Display recent task history from database"""
    print("\n📋 Recent Task History:")
    history = get_task_history(limit=15)
    
    if not history:
        print("  No task history available")
        return
    
    for i, record in enumerate(history, 1):
        timestamp = record['timestamp'][:19] if len(record['timestamp']) > 19 else record['timestamp']
        status_icon = "✅" if record['status'] == "success" else "❌"
        print(f"  {i:2d}. [{timestamp}] {status_icon} {record['agent']}: {record['task_type']}")
        print(f"       📝 {record['task_content'][:60]}{'...' if len(record['task_content']) > 60 else ''}")

def show_agent_stats():
    """Display agent performance statistics"""
    print("\n📊 Agent Performance Statistics:")
    agent_stats = get_agent_stats()
    
    if not agent_stats:
        print("  No agent statistics available")
        return
    
    for agent_name, stats in agent_stats.items():
        print(f"  🤖 {agent_name}:")
        print(f"    📈 Tasks completed: {stats['tasks_completed']}")
        print(f"    ❌ Tasks failed: {stats['tasks_failed']}")
        print(f"    🕒 Last active: {stats['last_active'][:19]}")
        print(f"    📊 Current status: {stats['current_status']}")
        
        # Calculate success rate
        total = stats['tasks_completed'] + stats['tasks_failed']
        if total > 0:
            success_rate = (stats['tasks_completed'] / total) * 100
            print(f"    🎯 Success rate: {success_rate:.1f}%")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()
