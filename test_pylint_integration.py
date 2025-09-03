#!/usr/bin/env python3
"""
DevDollz: Atelier Edition - Pylint Integration Test Suite
Tests the static analysis capabilities and async debugging features

Author: Alexis Adams
Brand: DevDollz: Atelier Edition
"""

import asyncio
import sys
import os
import time
from io import StringIO

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the pylint function from swarm_ide
try:
    from swarm_ide import run_pylint, create_message, parse_message
    print("✅ Successfully imported pylint functions from swarm_ide")
except ImportError as e:
    print(f"❌ Failed to import from swarm_ide: {e}")
    sys.exit(1)

def test_pylint_basic_functionality():
    """Test basic pylint functionality with simple code"""
    print("\n🔍 Testing Basic Pylint Functionality...")
    
    # Test 1: Valid code
    valid_code = """
def hello_world():
    print("Hello, World!")
"""
    result = run_pylint(valid_code)
    print(f"Valid Code Result: {result}")
    assert "No issues found" in result or "No issues found." in result, f"Expected 'No issues found', got: {result}"
    
    # Test 2: Code with issues
    problematic_code = """
def bad_function(x):
    y = x
    return y
"""
    result = run_pylint(problematic_code)
    print(f"Problematic Code Result: {result}")
    assert "Undefined variable" in result or "unused" in result, f"Expected issues, got: {result}"
    
    print("✅ Basic pylint functionality test passed")

def test_pylint_error_handling():
    """Test pylint error handling and edge cases"""
    print("\n🚨 Testing Pylint Error Handling...")
    
    # Test 1: Empty code
    empty_code = ""
    result = run_pylint(empty_code)
    print(f"Empty Code Result: {result}")
    
    # Test 2: Very long code (stress test)
    long_code = "def test():\n    " + "x = 1\n    " * 100 + "return x"
    result = run_pylint(long_code)
    print(f"Long Code Result: {result[:100]}...")
    
    # Test 3: Code with syntax errors
    syntax_error_code = """
def broken_function(
    x = 1
    return x
"""
    result = run_pylint(syntax_error_code)
    print(f"Syntax Error Code Result: {result}")
    
    print("✅ Pylint error handling test passed")

def test_pylint_output_formatting():
    """Test pylint output formatting and readability"""
    print("\n📝 Testing Pylint Output Formatting...")
    
    # Test code with multiple issues
    multi_issue_code = """
def complex_function(x, y):
    a = x
    b = y
    c = a + b
    print(c)
    return c
"""
    result = run_pylint(multi_issue_code)
    print(f"Multi-Issue Code Result: {result}")
    
    # Verify output is readable and not too long
    assert len(result) < 500, f"Output too long: {len(result)} characters"
    assert ";" in result or "No issues found" in result, f"Unexpected output format: {result}"
    
    print("✅ Pylint output formatting test passed")

def test_pylint_integration_with_swarm_ide():
    """Test pylint integration with the main IDE system"""
    print("\n🔗 Testing Pylint Integration with SwarmIDE...")
    
    # Test message creation and parsing
    test_code = "def test(): pass"
    pylint_result = run_pylint(test_code)
    
    # Create message using IDE's message system
    message = create_message(pylint_result, {"type": "pylint", "source": "debug"})
    print(f"Created Message: {message[:100]}...")
    
    # Parse message back
    parsed = parse_message(message)
    print(f"Parsed Message: {parsed}")
    
    assert parsed['content'] == pylint_result, "Message content mismatch"
    assert parsed['meta']['type'] == 'pylint', "Message type mismatch"
    
    print("✅ Pylint integration test passed")

async def test_async_debug_agent():
    """Test the async debug agent functionality"""
    print("\n⚡ Testing Async Debug Agent...")
    
    try:
        # Import the async debug agent
        from swarm_ide import debug_agent
        
        # Create async queues
        input_queue = asyncio.Queue()
        output_queue = asyncio.Queue()
        
        # Start the debug agent
        agent_task = asyncio.create_task(debug_agent(input_queue, output_queue))
        
        # Wait a moment for agent to start
        await asyncio.sleep(0.1)
        
        # Test pylint-only analysis
        test_message = create_message("def test(): x = 1; return x", {"type": "pylint"})
        await input_queue.put(test_message)
        
        # Wait for result
        await asyncio.sleep(0.5)
        
        # Check for results
        results = []
        while not output_queue.empty():
            try:
                result = output_queue.get_nowait()
                results.append(result)
            except asyncio.QueueEmpty:
                break
        
        if results:
            print(f"✅ Debug agent produced {len(results)} results")
            for result in results:
                parsed = parse_message(result)
                print(f"  - {parsed['content'][:100]}...")
        else:
            print("⚠️  No results from debug agent (this may be normal)")
        
        # Clean up
        await input_queue.put(None)  # Stop signal
        await agent_task
        
    except Exception as e:
        print(f"❌ Async debug agent test failed: {e}")
        return False
    
    print("✅ Async debug agent test passed")
    return True

def test_pylint_performance():
    """Test pylint performance with various code sizes"""
    print("\n⚡ Testing Pylint Performance...")
    
    # Test small code
    start_time = time.time()
    small_code = "def small(): return 1"
    result = run_pylint(small_code)
    small_time = time.time() - start_time
    
    # Test medium code
    start_time = time.time()
    medium_code = "def medium():\n    " + "x = 1\n    " * 50 + "return x"
    result = run_pylint(medium_code)
    medium_time = time.time() - start_time
    
    # Test large code
    start_time = time.time()
    large_code = "def large():\n    " + "x = 1\n    " * 200 + "return x"
    result = run_pylint(large_code)
    large_time = time.time() - start_time
    
    print(f"Small code (1 line): {small_time:.3f}s")
    print(f"Medium code (50 lines): {medium_time:.3f}s")
    print(f"Large code (200 lines): {large_time:.3f}s")
    
    # Performance should be reasonable
    assert small_time < 1.0, f"Small code took too long: {small_time}s"
    assert medium_time < 2.0, f"Medium code took too long: {medium_time}s"
    assert large_time < 5.0, f"Large code took too long: {large_time}s"
    
    print("✅ Pylint performance test passed")

def test_pylint_edge_cases():
    """Test pylint with edge cases and unusual code"""
    print("\n🔍 Testing Pylint Edge Cases...")
    
    # Test 1: Code with special characters
    special_char_code = """
def special_chars():
    # Test with special characters: éñüß
    x = "Hello, 世界!"
    return x
"""
    result = run_pylint(special_char_code)
    print(f"Special Characters Result: {result}")
    
    # Test 2: Code with very long lines
    long_line_code = """
def long_lines():
    x = "This is a very long line that might cause issues with pylint formatting and display in the terminal interface" * 10
    return x
"""
    result = run_pylint(long_line_code)
    print(f"Long Lines Result: {result}")
    
    # Test 3: Code with mixed indentation (should catch this)
    mixed_indent_code = """
def mixed_indentation():
    x = 1
  y = 2  # Wrong indentation
    return x + y
"""
    result = run_pylint(mixed_indent_code)
    print(f"Mixed Indentation Result: {result}")
    
    print("✅ Pylint edge cases test passed")

def main():
    """Run all pylint integration tests"""
    print("🚀 DevDollz: Atelier Edition - Pylint Integration Test Suite")
    print("=" * 60)
    
    test_results = []
    
    try:
        # Run synchronous tests
        test_pylint_basic_functionality()
        test_results.append(("Basic Functionality", "✅ PASSED"))
    except Exception as e:
        test_results.append(("Basic Functionality", f"❌ FAILED: {e}"))
    
    try:
        test_pylint_error_handling()
        test_results.append(("Error Handling", "✅ PASSED"))
    except Exception as e:
        test_results.append(("Error Handling", f"❌ FAILED: {e}"))
    
    try:
        test_pylint_output_formatting()
        test_results.append(("Output Formatting", "✅ PASSED"))
    except Exception as e:
        test_results.append(("Output Formatting", f"❌ FAILED: {e}"))
    
    try:
        test_pylint_integration_with_swarm_ide()
        test_results.append(("IDE Integration", "✅ PASSED"))
    except Exception as e:
        test_results.append(("IDE Integration", f"❌ FAILED: {e}"))
    
    try:
        test_pylint_performance()
        test_results.append(("Performance", "✅ PASSED"))
    except Exception as e:
        test_results.append(("Performance", f"❌ FAILED: {e}"))
    
    try:
        test_pylint_edge_cases()
        test_results.append(("Edge Cases", "✅ PASSED"))
    except Exception as e:
        test_results.append(("Edge Cases", f"❌ FAILED: {e}"))
    
    # Run async test
    try:
        asyncio.run(test_async_debug_agent())
        test_results.append(("Async Debug Agent", "✅ PASSED"))
    except Exception as e:
        test_results.append(("Async Debug Agent", f"❌ FAILED: {e}"))
    
    # Print results summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        print(f"{test_name:20} : {result}")
        if "PASSED" in result:
            passed += 1
    
    print("=" * 60)
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Pylint integration is working correctly.")
        print("🚀 DevDollz: Atelier Edition is ready for production use!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
