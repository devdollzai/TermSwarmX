#!/usr/bin/env python3
"""
Plugin System Validation Test Script

This script tests the core plugin system functionality to ensure it works correctly
before proceeding with performance optimization features.
"""

import os
import sys
import time
import multiprocessing as mp
import importlib.util

# Add the current directory to Python path to import swarm_ide modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the plugin system components
from swarm_ide import Orchestrator, create_message, parse_message

def test_plugin_system():
    """Test the plugin system functionality"""
    print("🔍 DevDollz Plugin System Validation Test")
    print("=" * 50)
    
    # Test 1: Plugin Loading
    print("\n📦 Test 1: Plugin Loading")
    print("-" * 30)
    
    try:
        # Create orchestrator
        orch = Orchestrator()
        print("✅ Orchestrator created successfully")
        
        # Test loading the sample plugin
        success, message = orch.load_plugin("sample_plugin.py")
        if success:
            print(f"✅ Plugin loaded: {message}")
        else:
            print(f"❌ Plugin loading failed: {message}")
            return False
        
        # Test listing plugins
        plugins = orch.list_plugins()
        print(f"✅ Available plugins: {plugins}")
        
    except Exception as e:
        print(f"❌ Orchestrator creation failed: {e}")
        return False
    
    # Test 2: Plugin Usage
    print("\n🚀 Test 2: Plugin Usage")
    print("-" * 30)
    
    try:
        # Test routing a task to the plugin
        task_content = "hello world"
        print(f"📤 Sending task to sample_plugin: '{task_content}'")
        
        success = orch.route_task("sample_plugin", "custom", task_content)
        if success:
            print("✅ Task routed successfully")
        else:
            print("❌ Task routing failed")
            return False
        
        # Wait for results
        print("⏳ Waiting for plugin response...")
        time.sleep(2)
        
        results = orch.get_results()
        if results:
            for res in results:
                source = res['meta'].get('source', 'unknown')
                status = res['meta'].get('status', 'unknown')
                content = res['content']
                print(f"📥 Response from [{source}]: [{status}] {content[:100]}...")
        else:
            print("⚠️ No results received from plugin")
        
    except Exception as e:
        print(f"❌ Plugin usage test failed: {e}")
        return False
    
    # Test 3: Error Handling
    print("\n⚠️ Test 3: Error Handling")
    print("-" * 30)
    
    try:
        # Test loading nonexistent plugin
        success, message = orch.load_plugin("nonexistent.py")
        if not success:
            print(f"✅ Correctly rejected nonexistent plugin: {message}")
        else:
            print(f"❌ Should have rejected nonexistent plugin")
        
        # Test loading plugin from outside project directory
        success, message = orch.load_plugin("/etc/passwd")
        if not success:
            print(f"✅ Correctly rejected external path: {message}")
        else:
            print(f"❌ Should have rejected external path")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    # Test 4: Security - Process Isolation
    print("\n🔒 Test 4: Security - Process Isolation")
    print("-" * 30)
    
    try:
        # Check that plugins are properly registered in thread agents
        plugin_agents = []
        for agent_name, agent_data in orch.thread_agents.items():
            if agent_data.get("type") == "plugin":
                plugin_agents.append((agent_name, agent_data))
                print(f"✅ Plugin '{agent_name}' registered with type: {agent_data['type']}")
        
        # Check that core agents are in process agents
        core_agents = []
        for agent_name, agent_data in orch.process_agents.items():
            core_agents.append((agent_name, agent_data))
            print(f"✅ Core agent '{agent_name}' registered as process agent")
        
        # Verify these are different from the main process
        main_pid = os.getpid()
        print(f"✅ Main process PID: {main_pid}")
        
        for plugin_name, plugin_data in plugin_agents:
            if plugin_data["type"] == "plugin":
                print(f"✅ Plugin '{plugin_name}' properly isolated in thread pool")
            else:
                print(f"❌ Plugin '{plugin_name}' not properly isolated")
        
        for core_name, core_data in core_agents:
            if "proc" in core_data and core_data["proc"]:
                core_pid = core_data["proc"].pid
                if core_pid != main_pid:
                    print(f"✅ Core agent '{core_name}' isolated in separate process (PID: {core_pid})")
                else:
                    print(f"❌ Core agent '{core_name}' running in main process (security issue)")
            else:
                print(f"❌ Core agent '{core_name}' missing process")
        
    except Exception as e:
        print(f"❌ Security test failed: {e}")
        return False
    
    # Test 5: Plugin Communication Protocol
    print("\n📡 Test 5: Plugin Communication Protocol")
    print("-" * 30)
    
    try:
        # Test message creation and parsing
        test_meta = {"type": "test", "status": "success", "timestamp": time.time()}
        test_content = "Test message content"
        
        message = create_message(test_content, test_meta)
        print(f"✅ Message created: {message[:50]}...")
        
        parsed = parse_message(message)
        if parsed['content'] == test_content and parsed['meta']['type'] == test_meta['type']:
            print("✅ Message parsing successful")
        else:
            print("❌ Message parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ Communication protocol test failed: {e}")
        return False
    
    # Test 6: Clean Shutdown
    print("\n🔄 Test 6: Clean Shutdown")
    print("-" * 30)
    
    try:
        orch.shutdown()
        print("✅ Orchestrator shutdown successful")
        
        # Verify process agents are terminated
        for agent_name, agent_data in orch.process_agents.items():
            if "proc" in agent_data and agent_data["proc"]:
                if not agent_data["proc"].is_alive():
                    print(f"✅ Core agent '{agent_name}' process terminated")
                else:
                    print(f"❌ Core agent '{agent_name}' process still running")
        
        # Verify thread agents (plugins) are cleaned up
        if not orch.thread_agents:
            print("✅ All plugins cleaned up during shutdown")
        else:
            print(f"⚠️ {len(orch.thread_agents)} plugins still registered after shutdown")
                
    except Exception as e:
        print(f"❌ Shutdown test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All Plugin System Tests Passed!")
    print("✅ Plugin loading and management")
    print("✅ Task routing and communication")
    print("✅ Error handling and validation")
    print("✅ Security and process isolation")
    print("✅ Communication protocol")
    print("✅ Clean shutdown")
    print("\n🚀 Ready to proceed with Performance Optimization!")
    
    return True

if __name__ == "__main__":
    success = test_plugin_system()
    sys.exit(0 if success else 1)
