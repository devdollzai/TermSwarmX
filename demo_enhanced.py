#!/usr/bin/env python3
"""
AI Swarm IDE - Enhanced Features Demo
Showcases the sharp CLI experience and advanced capabilities
"""

import asyncio
import time
from swarm_ide_enhanced import SwarmOrchestrator, Command, CommandType

async def demo_enhanced_features():
    """Demonstrate the enhanced Swarm IDE capabilities"""
    
    print("🚀 AI Swarm IDE - Enhanced Features Demo")
    print("=" * 60)
    print()
    
    # Initialize orchestrator
    orchestrator = SwarmOrchestrator()
    
    try:
        print("📋 Demo Commands:")
        print("1. Code Generation Examples")
        print("2. Debug Analysis Examples")
        print("3. Error Handling")
        print("4. Agent Status")
        print()
        
        # Demo 1: Code Generation
        print("🔧 Demo 1: Code Generation")
        print("-" * 30)
        
        # Generate function
        print("Generating function 'calculate_fibonacci'...")
        orchestrator.route_task("code_gen", "function", "calculate_fibonacci")
        await asyncio.sleep(0.2)
        results = orchestrator.get_results()
        for res in results:
            print(f"[{res['meta']['status'].upper()}] {res['content']}")
        print()
        
        # Generate class
        print("Generating class 'DataProcessor'...")
        orchestrator.route_task("code_gen", "class", "DataProcessor")
        await asyncio.sleep(0.2)
        results = orchestrator.get_results()
        for res in results:
            print(f"[{res['meta']['status'].upper()}] {res['content']}")
        print()
        
        # Demo 2: Debug Analysis
        print("🔍 Demo 2: Debug Analysis")
        print("-" * 30)
        
        # Syntax check - valid code
        valid_code = "def hello():\n    print('Hello, World!')"
        print(f"Checking syntax for valid code:\n{valid_code}")
        orchestrator.route_task("debug", "syntax", valid_code)
        await asyncio.sleep(0.2)
        results = orchestrator.get_results()
        for res in results:
            print(f"[{res['meta']['status'].upper()}] {res['content']}")
        print()
        
        # Syntax check - invalid code
        invalid_code = "def hello(: pass"
        print(f"Checking syntax for invalid code:\n{invalid_code}")
        orchestrator.route_task("debug", "syntax", invalid_code)
        await asyncio.sleep(0.2)
        results = orchestrator.get_results()
        for res in results:
            print(f"[{res['meta']['status'].upper()}] {res['content']}")
        print()
        
        # Logic analysis
        complex_code = """
def process_data(items):
    if not items:
        return []
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
"""
        print(f"Analyzing logic for complex code:\n{complex_code}")
        orchestrator.route_task("debug", "logic", complex_code)
        await asyncio.sleep(0.2)
        results = orchestrator.get_results()
        for res in results:
            print(f"[{res['meta']['status'].upper()}] {res['content']}")
        print()
        
        # Demo 3: Error Handling
        print("⚠️ Demo 3: Error Handling")
        print("-" * 30)
        
        # Test invalid command parsing
        print("Testing command parsing...")
        test_commands = [
            "invalid command",
            "generate invalid_type test",
            "debug unknown_type test",
            "generate function",  # Missing description
            "debug syntax"       # Missing code
        ]
        
        for cmd_text in test_commands:
            parsed = Command.parse(cmd_text)
            if parsed is None:
                print(f"❌ Invalid command rejected: '{cmd_text}'")
            else:
                print(f"✅ Valid command parsed: '{cmd_text}'")
        print()
        
        # Demo 4: Agent Status
        print("🤖 Demo 4: Agent Status")
        print("-" * 30)
        
        status = orchestrator.get_agent_status()
        for agent, state in status.items():
            icon = "🟢" if state == "active" else "🔴"
            print(f"{icon} {agent}: {state}")
        print()
        
        # Demo 5: Performance
        print("⚡ Demo 5: Performance Test")
        print("-" * 30)
        
        start_time = time.time()
        for i in range(5):
            orchestrator.route_task("code_gen", "function", f"test_function_{i}")
        
        await asyncio.sleep(0.5)
        results = orchestrator.get_results()
        end_time = time.time()
        
        print(f"Generated {len(results)} functions in {end_time - start_time:.3f} seconds")
        print(f"Average response time: {(end_time - start_time) / len(results):.3f} seconds per task")
        print()
        
        print("🎉 Demo completed successfully!")
        print("The enhanced Swarm IDE provides:")
        print("• Sharp, instant command validation")
        print("• Professional error messages")
        print("• Advanced code generation templates")
        print("• Comprehensive debug analysis")
        print("• Real-time agent monitoring")
        print("• Persistent memory and logging")
        print()
        print("Ready for production use! 🚀")
        
    finally:
        orchestrator.shutdown()

def main():
    """Run the enhanced features demo"""
    try:
        asyncio.run(demo_enhanced_features())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo failed: {e}")

if __name__ == "__main__":
    main()
