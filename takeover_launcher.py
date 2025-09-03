#!/usr/bin/env python3
"""
DevDollz Takeover Launcher
Silent dominance through strategic positioning
"""

import asyncio
import sys
from pathlib import Path

# Add the devdollz package to the path
sys.path.insert(0, str(Path(__file__).parent / "devdollz"))

try:
    from takeover import DevDollzTakeover
except ImportError as e:
    print(f"💥 Import error: {e}")
    print("🔧 Make sure you're in the correct directory and DevDollz is installed")
    sys.exit(1)

async def launch_takeover():
    """Launch DevDollz takeover directly"""
    print("🚀 LAUNCHING DEVDOLZ TAKEOVER...")
    print("⚡ We don't hide - we melt.")
    print("🔥 Anonymity isn't masks, it's motion.")
    print()
    print("Choose your takeover mode:")
    print("1. Complete Takeover - All phases")
    print("2. Strategic Positioning - Make DevDollz the default")
    print("3. Platform Domination - Target specific platforms")
    print("4. Silent Integration - No traces")
    print("5. Show Statistics")
    print("6. Exit")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    takeover = DevDollzTakeover()
    
    try:
        if choice == "1":
            print("\n🚀 Executing complete DevDollz takeover...")
            results = takeover.execute_takeover()
            
            print("\n📊 Takeover Results:")
            for phase, result in results.items():
                print(f"   {phase}: {result}")
                
        elif choice == "2":
            print("\n🎯 Strategic positioning mode...")
            result = takeover.strategic_positioning()
            print(f"✅ Positioning complete: {result}")
            
        elif choice == "3":
            print("\n🎯 Platform domination mode...")
            print("Available targets: pip, vscode, git, npm, cargo, go, brew")
            target = input("Enter target platform: ").strip()
            
            success = takeover.silent_install(target)
            if success:
                print(f"✅ {target} now defaults to DevDollz")
            else:
                print(f"💥 Takeover failed for {target}")
                
        elif choice == "4":
            print("\n🕵️ Silent integration mode...")
            takeover.enable_stealth_mode()
            result = takeover.silent_integration()
            print(f"✅ Silent integration complete: {result}")
            
        elif choice == "5":
            print("\n📊 Takeover Statistics:")
            stats = takeover.get_takeover_stats()
            for key, value in stats.items():
                print(f"   {key}: {value}")
                
        else:
            print("🛑 Exiting takeover.")
            return
            
    except KeyboardInterrupt:
        print("\n🛑 Takeover stopped by user.")
    except Exception as e:
        print(f"💥 Takeover error: {e}")
    
    print("\n✅ Takeover operations complete.")
    print("🚀 DevDollz is becoming the default, not the alternative.")
    print("🔥 No watermark. No powered by. Just faster output.")

if __name__ == "__main__":
    try:
        asyncio.run(launch_takeover())
    except KeyboardInterrupt:
        print("\n🛑 Exiting takeover.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)
