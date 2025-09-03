#!/usr/bin/env python3
"""
Test script for Warp Killer Swarm
Verifies the system works before running the full demo
"""

import asyncio
import time
from warp_killer_swarm import InfiniteSwarmOrchestrator

async def test_basic_functionality():
    """Test basic swarm functionality"""
    print("🧪 Testing Warp Killer Swarm...")
    
    # Create orchestrator with limited agents for testing
    swarm = InfiniteSwarmOrchestrator(max_agents=10, max_processes=4)
    
    try:
        # Start the swarm
        await swarm.start()
        print("✅ Swarm started successfully")
        
        # Submit a few test tasks
        task_ids = []
        for i in range(5):
            task_id = swarm.submit_task(
                "code_gen", 
                f"Create a simple Python function for task {i}",
                priority=1
            )
            task_ids.append(task_id)
            print(f"📝 Submitted task {i+1}: {task_id}")
        
        # Wait for some results
        print("⏳ Waiting for results...")
        await asyncio.sleep(5)
        
        # Get results
        results = swarm.get_results()
        print(f"📊 Got {len(results)} results")
        
        # Show stats
        stats = swarm.get_stats()
        print(f"📈 Stats: {stats['active_agents']} agents, {stats['tasks_completed']} completed")
        
        print("✅ Basic functionality test passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        await swarm.stop()
        print("🛑 Swarm stopped")
    
    return True

async def test_performance():
    """Test performance characteristics"""
    print("\n🚀 Testing performance...")
    
    swarm = InfiniteSwarmOrchestrator(max_agents=50, max_processes=8)
    
    try:
        await swarm.start()
        
        # Submit tasks rapidly
        start_time = time.time()
        task_count = 100
        
        for i in range(task_count):
            swarm.submit_task(
                "code_gen",
                f"Generate code for performance test {i}",
                priority=1
            )
        
        submit_time = time.time() - start_time
        print(f"📝 Submitted {task_count} tasks in {submit_time:.2f}s")
        
        # Wait for processing
        await asyncio.sleep(10)
        
        # Check results
        results = swarm.get_results()
        stats = swarm.get_stats()
        
        print(f"📊 Performance Results:")
        print(f"   Tasks submitted: {task_count}")
        print(f"   Tasks completed: {stats['tasks_completed']}")
        print(f"   Requests per second: {stats['requests_per_second']:.2f}")
        print(f"   Active agents: {stats['active_agents']}")
        
        if stats['tasks_completed'] > 0:
            print("✅ Performance test passed!")
            return True
        else:
            print("❌ No tasks completed")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False
    
    finally:
        await swarm.stop()

async def main():
    """Run all tests"""
    print("🔥 WARP KILLER SWARM - TEST SUITE")
    print("=" * 50)
    
    # Test 1: Basic functionality
    basic_ok = await test_basic_functionality()
    
    if basic_ok:
        # Test 2: Performance
        perf_ok = await test_performance()
        
        if perf_ok:
            print("\n🎯 All tests passed! Warp Killer Swarm is ready.")
            print("💡 Run 'python warp_killer_swarm.py' for the full demo.")
        else:
            print("\n⚠️  Performance test failed, but basic functionality works.")
    else:
        print("\n❌ Basic functionality test failed. Check your setup.")
        print("🔧 Ensure Ollama is running and models are available.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        print("🔧 Check your Python environment and dependencies")
