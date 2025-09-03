#!/usr/bin/env python3
"""
Test script for DevDollz Spine
"""

import time
from devdollz.spine import DevDollzSpine

def test_spine():
    print("🧪 Testing DevDollz Spine...")
    print("=" * 40)
    
    # Create spine
    spine = DevDollzSpine()
    
    try:
        # Start spine
        print("🚀 Starting spine...")
        spine.start()
        
        # Test agent spawning
        print("\n🧪 Testing agent spawning...")
        
        # Test 1: Code generation
        print("\n1️⃣ Testing CodeGen agent...")
        result1 = spine.execute("generate Python function for data processing")
        print(f"Result: {result1}")
        
        # Test 2: Scraper
        print("\n2️⃣ Testing Scraper agent...")
        result2 = spine.execute("scrape website for content")
        print(f"Result: {result2}")
        
        # Test 3: Analyzer
        print("\n3️⃣ Testing Analyzer agent...")
        result3 = spine.execute("analyze code structure")
        print(f"Result: {result3}")
        
        # Let agents work
        print("\n⏳ Letting agents work...")
        time.sleep(3)
        
        # Get status
        print("\n📊 Getting spine status...")
        status = spine.get_status()
        print(f"Status: {status}")
        
        # Get pulse feed
        print("\n💓 Getting pulse feed...")
        pulses = spine.get_pulse_feed(10)
        print(f"Pulses: {len(pulses)} recent pulses")
        for pulse in pulses[-3:]:  # Show last 3
            print(f"  [{pulse.level.upper()}] {pulse.agent_name}: {pulse.message}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Stop spine
        print("\n🛑 Stopping spine...")
        spine.stop()
        print("👋 Test complete")

if __name__ == "__main__":
    test_spine()
