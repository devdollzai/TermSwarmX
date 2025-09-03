#!/usr/bin/env python3
"""
Simple test to verify Ollama integration works
"""

import ollama

def test_ollama():
    print("🧪 Testing basic Ollama integration...")
    
    try:
        # Test 1: Simple prompt
        print("\n1. Testing simple prompt...")
        response = ollama.generate(model='mistral', prompt='Hello, test')
        print(f"✅ Response: {response['response'][:100]}...")
        
        # Test 2: Code generation prompt
        print("\n2. Testing code generation prompt...")
        prompt = "Generate a Python function that reads a CSV file. Return only the code."
        response = ollama.generate(model='mistral', prompt=prompt)
        print(f"✅ Response: {response['response'][:100]}...")
        
        # Test 3: Debug prompt
        print("\n3. Testing debug prompt...")
        prompt = "Analyze this Python code for syntax errors: def foo(: pass"
        response = ollama.generate(model='mistral', prompt=prompt)
        print(f"✅ Response: {response['response'][:100]}...")
        
        print("\n🎉 All Ollama tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ollama()
