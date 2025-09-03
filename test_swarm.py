#!/usr/bin/env python3
"""
Test script for the Live Swarm Brain system
Run this to verify everything is working correctly
"""

import sys
import time

def test_basic_swarm():
    """Test basic swarm functionality"""
    print("🧪 Testing basic swarm functionality...")
    
    try:
        from swarm_core import swarm
        print("✅ Basic swarm import successful")
        
        # Test a simple thought
        print("🔄 Testing simple execution...")
        swarm.breathe("print('Hello from the swarm!')")
        
        time.sleep(2)  # Give time for async execution
        print("✅ Basic execution test completed")
        
    except Exception as e:
        print(f"❌ Basic swarm test failed: {e}")
        return False
    
    return True

def test_enhanced_features():
    """Test enhanced swarm features"""
    print("\n🧪 Testing enhanced features...")
    
    try:
        from swarm_extensions import enhanced_swarm
        print("✅ Enhanced swarm import successful")
        
        # Test memory system
        print("🧠 Testing memory system...")
        enhanced_swarm.memory.store("test_key", "test_value")
        retrieved = enhanced_swarm.memory.retrieve("test_key")
        if retrieved == "test_value":
            print("✅ Memory system working")
        else:
            print("❌ Memory system failed")
        
        # Test collaborator system
        print("🤝 Testing collaborator system...")
        enhanced_swarm.collaborator.add_collaborator("test_user", {"test": "context"})
        if "test_user" in enhanced_swarm.collaborator.collaborators:
            print("✅ Collaborator system working")
        else:
            print("❌ Collaborator system failed")
        
        # Test code validation
        print("🛡️ Testing code validation...")
        is_valid, message = enhanced_swarm.validator.validate("print('Hello')")
        if is_valid:
            print("✅ Code validation working")
        else:
            print("❌ Code validation failed")
        
    except Exception as e:
        print(f"❌ Enhanced features test failed: {e}")
        return False
    
    return True

def test_examples():
    """Test example usage patterns"""
    print("\n🧪 Testing example patterns...")
    
    try:
        from swarm_examples import demo_vectorization
        print("✅ Examples import successful")
        
        # Test a simple example
        print("🔄 Running vectorization demo...")
        demo_vectorization()
        
        time.sleep(2)  # Give time for execution
        print("✅ Examples test completed")
        
    except Exception as e:
        print(f"❌ Examples test failed: {e}")
        return False
    
    return False

def main():
    """Run all tests"""
    print("🚀 Live Swarm Brain - System Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Swarm", test_basic_swarm),
        ("Enhanced Features", test_enhanced_features),
        ("Examples", test_examples)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your swarm brain is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
