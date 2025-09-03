#!/usr/bin/env python3
"""
Test script for LLM output quality evaluation
Runs the specific test commands mentioned in the summary
"""

import asyncio
import multiprocessing as mp
import queue
import time
import json
from swarm_ide_llm import (
    SwarmOrchestrator, 
    code_gen_agent, 
    debug_agent,
    create_message,
    parse_message
)

async def test_llm_output():
    """Test the LLM agents with specific commands"""
    
    print("🧪 Testing LLM Output Quality")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = SwarmOrchestrator()
    
    # Start agents
    code_gen_proc = mp.Process(target=code_gen_agent, args=(orchestrator.code_gen_queue, orchestrator.result_queue))
    debug_proc = mp.Process(target=debug_agent, args=(orchestrator.debug_queue, orchestrator.result_queue))
    
    code_gen_proc.start()
    debug_proc.start()
    
    orchestrator.register_agent("code_gen", code_gen_proc)
    orchestrator.register_agent("debug", debug_proc)
    
    # Wait for agents to start
    time.sleep(2)
    
    # Test commands from the summary
    test_commands = [
        ("generate function", "read_csv_to_dataframe"),
        ("generate class", "SimpleLogger"),
        ("generate code", "a REST API endpoint for user authentication"),
        ("debug syntax", "def my_func(x: pass"),
        ("debug logic", "def factorial(n): if n == 0: return 1 else: return n * factorial(n-1)")
    ]
    
    results = []
    
    for cmd_type, description in test_commands:
        print(f"\n🔍 Testing: {cmd_type} {description}")
        print("-" * 40)
        
        try:
            if cmd_type.startswith("generate"):
                agent_type = "code_gen"
                task_content = f"{cmd_type.split()[1]}: {description}"
                task_meta = {"type": cmd_type.split()[1], "task_id": f"test_{len(results)}"}
            else:  # debug
                agent_type = "debug"
                task_content = description
                task_meta = {"error_type": cmd_type.split()[1], "task_id": f"test_{len(results)}"}
            
            # Submit task using orchestrator
            result = await orchestrator.dispatch_task(agent_type, task_content, task_meta["task_id"])
            
            if result:
                print("✅ Result:")
                print(result)
                results.append({
                    "command": f"{cmd_type} {description}",
                    "result": result,
                    "status": "success"
                })
            else:
                print("❌ No result received")
                results.append({
                    "command": f"{cmd_type} {description}",
                    "result": "No result",
                    "status": "failed"
                })
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                "command": f"{cmd_type} {description}",
                "result": f"Error: {str(e)}",
                "status": "error"
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    total_count = len(results)
    
    print(f"Total tests: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    print(f"Success rate: {(success_count/total_count)*100:.1f}%")
    
    print("\nDetailed Results:")
    for i, result in enumerate(results, 1):
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"{i}. {status_icon} {result['command']}")
        print(f"   Status: {result['status']}")
        if result["status"] == "success":
            # Show first few lines of result
            lines = result["result"].split('\n')[:3]
            preview = '\n'.join(lines)
            if len(result["result"].split('\n')) > 3:
                preview += "\n   ..."
            print(f"   Preview: {preview}")
        print()
    
    # Cleanup
    orchestrator.shutdown()
    
    return results

if __name__ == "__main__":
    try:
        # Set multiprocessing start method
        mp.set_start_method('spawn', force=True)
        
        # Run tests
        results = asyncio.run(test_llm_output())
        
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
