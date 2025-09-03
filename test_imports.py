#!/usr/bin/env python3
"""
Test script to verify all imports are working correctly
"""

def test_basic_imports():
    """Test basic Python imports"""
    print("🧪 Testing basic imports...")
    
    try:
        import asyncio
        import json
        import time
        import sys
        print("✅ Basic imports successful")
    except ImportError as e:
        print(f"❌ Basic import failed: {e}")
        return False
    
    return True

def test_swarm_core_imports():
    """Test swarm core imports"""
    print("🧪 Testing swarm core imports...")
    
    try:
        from swarm_core import Swarm, Pulse, pulse_hash
        print("✅ Swarm core imports successful")
    except ImportError as e:
        print(f"❌ Swarm core import failed: {e}")
        return False
    
    return True

def test_swarm_extensions_imports():
    """Test swarm extensions imports"""
    print("🧪 Testing swarm extensions imports...")
    
    try:
        from swarm_extensions import SwarmMemory, CodeValidator, SwarmCollaborator
        print("✅ Swarm extensions imports successful")
    except ImportError as e:
        print(f"❌ Swarm extensions import failed: {e}")
        return False
    
    return True

def test_config_imports():
    """Test configuration imports"""
    print("🧪 Testing configuration imports...")
    
    try:
        from config import PRECOGNITION_CONFIG, AI_CONFIG, SYSTEM_CONFIG
        print("✅ Configuration imports successful")
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False
    
    return True

def test_precognitive_ai_imports():
    """Test precognitive AI imports"""
    print("🧪 Testing precognitive AI imports...")
    
    try:
        from precognitive_ai import precognitive_ai
        print("✅ Precognitive AI imports successful")
    except ImportError as e:
        print(f"❌ Precognitive AI import failed: {e}")
        return False
    
    return True

def test_optional_imports():
    """Test optional package imports"""
    print("🧪 Testing optional imports...")
    
    optional_packages = [
        ("numpy", "numpy"),
        ("ollama", "ollama"),
        ("pylint", "pylint.lint"),
        ("prompt_toolkit", "prompt_toolkit"),
        ("speech_recognition", "speech_recognition")
    ]
    
    results = []
    for package_name, import_name in optional_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} available")
            results.append(True)
        except ImportError:
            print(f"⚠️  {package_name} not available (optional)")
            results.append(False)
    
    return results

def main():
    """Run all import tests"""
    print("🚀 Import Test Suite - DevDollz: Atelier Edition")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Swarm Core", test_swarm_core_imports),
        ("Swarm Extensions", test_swarm_extensions_imports),
        ("Configuration", test_config_imports),
        ("Precognitive AI", test_precognitive_ai_imports),
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
    
    # Test optional imports
    print(f"\n🔍 Testing optional imports...")
    optional_results = test_optional_imports()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Import Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} required tests passed")
    
    if passed == total:
        print("🎉 All required imports are working! Your system is ready.")
        print("💡 Some optional packages may not be installed - this is normal.")
    else:
        print("⚠️  Some required imports failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
