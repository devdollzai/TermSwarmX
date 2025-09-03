#!/usr/bin/env python3
"""
Demo script for AI Swarm IDE Multiprocessing Orchestrator
Demonstrates the multiprocessing-based agent coordination system
"""

import time
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.multiprocessing_orchestrator import MultiprocessingOrchestrator
from agents.multiprocessing_agents import (
    code_gen_agent, 
    debug_agent, 
    analysis_agent, 
    refactor_agent
)

def main():
    """Main demo function"""
    print("🚀 AI Swarm IDE - Multiprocessing Demo")
    print("=" * 50)
    
    # Initialize the orchestrator
    orchestrator = MultiprocessingOrchestrator(max_workers=4)
    
    try:
        # Register different types of agents
        print("\n📋 Registering agents...")
        
        # Code generation agent
        code_agent_id = orchestrator.register_agent(
            name="CodeGenAgent",
            agent_type="code_generation",
            agent_function=code_gen_agent,
            capabilities=["code_generation", "function_creation", "class_creation"],
            model_name="gpt-4"
        )
        
        # Debug agent
        debug_agent_id = orchestrator.register_agent(
            name="DebugAgent",
            agent_type="debugging",
            agent_function=debug_agent,
            capabilities=["debugging", "error_analysis", "syntax_checking"]
        )
        
        # Analysis agent
        analysis_agent_id = orchestrator.register_agent(
            name="AnalysisAgent",
            agent_type="analysis",
            agent_function=analysis_agent,
            capabilities=["code_analysis", "quality_assessment", "metrics_calculation"]
        )
        
        # Refactor agent
        refactor_agent_id = orchestrator.register_agent(
            name="RefactorAgent",
            agent_type="refactoring",
            agent_function=refactor_agent,
            capabilities=["code_refactoring", "optimization", "cleanup"]
        )
        
        print(f"✅ Registered {len(orchestrator.agents)} agents")
        
        # Wait a moment for agents to start up
        time.sleep(2)
        
        # Display initial status
        print("\n📊 Initial Status:")
        orchestrator.display_status()
        
        # Submit some sample tasks
        print("\n📝 Submitting sample tasks...")
        
        # Task 1: Generate a function
        task1_id = orchestrator.submit_task(
            task_data={
                "title": "Generate a function",
                "requirements": "Create a function to calculate fibonacci numbers",
                "language": "python",
                "context": "Mathematical utility function"
            },
            agent_type="code_generation",
            priority=3
        )
        
        # Task 2: Debug some code
        task2_id = orchestrator.submit_task(
            task_data={
                "title": "Debug code",
                "code": "def test():\n    x = 10\n    print(x + y)",  # y is undefined
                "error_message": "NameError: name 'y' is not defined"
            },
            agent_type="debugging",
            priority=2
        )
        
        # Task 3: Analyze code quality
        task3_id = orchestrator.submit_task(
            task_data={
                "title": "Analyze code quality",
                "code": """def calculate_sum(a, b):
    return a + b

def main():
    result = calculate_sum(5, 10)
    print(result)

if __name__ == "__main__":
    main()"""
            },
            agent_type="analysis",
            priority=1
        )
        
        # Task 4: Refactor code
        task4_id = orchestrator.submit_task(
            task_data={
                "title": "Refactor code",
                "code": "def main():\n    x = 10\n    y = 20\n    z = x + y\n    print(z)",
                "refactoring_type": "extract_method"
            },
            agent_type="refactoring",
            priority=2
        )
        
        print(f"✅ Submitted {len(orchestrator.task_queue)} tasks")
        
        # Process pending tasks
        print("\n🔄 Processing pending tasks...")
        orchestrator.process_pending_tasks()
        
        # Main processing loop
        print("\n⏳ Processing tasks (this may take a few seconds)...")
        max_wait_time = 30  # Maximum time to wait for results
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # Check for results
            results = orchestrator.get_results()
            
            if results:
                print(f"\n📤 Received {len(results)} results:")
                for result in results:
                    print(f"\n🤖 {result['agent_name']}:")
                    if 'error' in result:
                        print(f"❌ Error: {result['error']}")
                    else:
                        print(f"✅ Task completed successfully")
                        # Display result summary
                        if 'result' in result:
                            res = result['result']
                            if 'generated_code' in res:
                                print(f"📝 Generated {res.get('metadata', {}).get('lines_of_code', 0)} lines of code")
                            elif 'debug_result' in res:
                                print(f"🐛 Found {res.get('issues_found', 0)} issues")
                            elif 'analysis' in res:
                                print(f"📊 Code quality score: {res['analysis'].get('overall_score', 0)}/100")
                            elif 'refactored_code' in res:
                                print(f"🔄 Applied {res.get('refactoring_type', 'general')} refactoring")
            
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
        
        print("\n🎉 Demo completed successfully!")
        
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
    """Interactive command-line interface"""
    print("🚀 AI Swarm IDE - Interactive Multiprocessing Mode")
    print("=" * 50)
    
    # Initialize the orchestrator
    orchestrator = MultiprocessingOrchestrator(max_workers=4)
    
    try:
        # Register agents
        print("\n📋 Registering agents...")
        
        orchestrator.register_agent(
            name="CodeGenAgent",
            agent_type="code_generation",
            agent_function=code_gen_agent,
            capabilities=["code_generation", "function_creation", "class_creation"]
        )
        
        orchestrator.register_agent(
            name="DebugAgent",
            agent_type="debugging",
            agent_function=debug_agent,
            capabilities=["debugging", "error_analysis", "syntax_checking"]
        )
        
        orchestrator.register_agent(
            name="AnalysisAgent",
            agent_type="analysis",
            agent_function=analysis_agent,
            capabilities=["code_analysis", "quality_assessment", "metrics_calculation"]
        )
        
        orchestrator.register_agent(
            name="RefactorAgent",
            agent_type="refactoring",
            agent_function=refactor_agent,
            capabilities=["code_refactoring", "optimization", "cleanup"]
        )
        
        print("✅ Agents registered. Type 'help' for available commands.")
        
        # Wait for agents to start
        time.sleep(2)
        
        # Command loop
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                elif command.lower() == 'help':
                    print_help()
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
                elif command.startswith('gen:'):
                    task = command[4:].strip()
                    orchestrator.route_task("code_generation", {
                        "title": f"Generate: {task}",
                        "requirements": task,
                        "language": "python"
                    })
                    print(f"✅ Task submitted to code generation agent")
                elif command.startswith('debug:'):
                    code = command[6:].strip()
                    orchestrator.route_task("debugging", {
                        "title": "Debug code",
                        "code": code,
                        "error_message": "User requested debugging"
                    })
                    print(f"✅ Task submitted to debug agent")
                elif command.startswith('analyze:'):
                    code = command[8:].strip()
                    orchestrator.route_task("analysis", {
                        "title": "Analyze code",
                        "code": code
                    })
                    print(f"✅ Task submitted to analysis agent")
                elif command.startswith('refactor:'):
                    code = command[9:].strip()
                    orchestrator.route_task("refactoring", {
                        "title": "Refactor code",
                        "code": code,
                        "refactoring_type": "general"
                    })
                    print(f"✅ Task submitted to refactor agent")
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

def print_help():
    """Print help information"""
    print("\n📚 Available Commands:")
    print("  help                    - Show this help message")
    print("  status                  - Show orchestrator status")
    print("  health                  - Show agent health status")
    print("  results                 - Show available results")
    print("  gen: <description>      - Generate code")
    print("  debug: <code>           - Debug code")
    print("  analyze: <code>         - Analyze code quality")
    print("  refactor: <code>        - Refactor code")
    print("  quit/exit/q             - Exit the program")
    print("\n📝 Examples:")
    print("  gen: create a function to calculate factorial")
    print("  debug: def test(): x = 10; print(x + y)")
    print("  analyze: def func(): return 42")
    print("  refactor: def main(): x = 10; print(x)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()
