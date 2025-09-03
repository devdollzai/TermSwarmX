#!/usr/bin/env python3
"""
DevDollz Warp Bypass Launcher
Their trial, our house. No limits, no payments.
"""

import asyncio
import sys
from pathlib import Path

# Add the devdollz package to the path
sys.path.insert(0, str(Path(__file__).parent / "devdollz"))

try:
    from warp_bypass import WarpBypass
except ImportError as e:
    print(f"💥 Import error: {e}")
    print("🔧 Make sure you're in the correct directory and DevDollz is installed")
    sys.exit(1)

async def launch_warp_bypass():
    """Launch Warp bypass directly"""
    print("🚀 LAUNCHING WARP BYPASS...")
    print("⚡ Their trial, our house.")
    print("🔥 No limits. No payments. No waiting.")
    print()
    print("Choose your bypass mode:")
    print("1. Full Bypass - Steal their speed")
    print("2. Feature Generation - Specific Warp features")
    print("3. File Analysis - IDE integration")
    print("4. Compare with Warp")
    print("5. Show Statistics")
    print("6. Exit")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    bypass = WarpBypass()
    
    try:
        if choice == "1":
            print("\n🎯 Executing full Warp bypass...")
            result = bypass.steal_their_speed()
            
            print("\n📊 Bypass Statistics:")
            stats = bypass.get_bypass_stats()
            for key, value in stats.items():
                print(f"   {key}: {value}")
            
            print("\n" + bypass.compare_with_warp())
            print("\n✅ Warp bypass complete. You're now running their features locally.")
            
        elif choice == "2":
            print("\n🎯 Feature Generation Mode:")
            print("Available features: pair_programming, code_completion, error_explanation, refactoring, documentation, testing")
            feature = input("Enter feature name: ").strip()
            context = input("Enter context (optional): ").strip()
            
            result = bypass.generate_feature(feature, context)
            print(f"✅ Generated: {result}")
            
        elif choice == "3":
            print("\n📁 File Analysis Mode:")
            file_path = input("Enter file path to analyze: ").strip()
            
            result = bypass.run_local_ide_integration(file_path)
            print(f"✅ Analysis: {result}")
            
        elif choice == "4":
            print("\n" + bypass.compare_with_warp())
            
        elif choice == "5":
            print("\n📊 Bypass Statistics:")
            stats = bypass.get_bypass_stats()
            for key, value in stats.items():
                print(f"   {key}: {value}")
                
        else:
            print("🛑 Exiting Warp bypass.")
            return
            
    except KeyboardInterrupt:
        print("\n🛑 Warp bypass stopped by user.")
    except Exception as e:
        print(f"💥 Bypass error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(launch_warp_bypass())
    except KeyboardInterrupt:
        print("\n🛑 Exiting Warp bypass.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)
