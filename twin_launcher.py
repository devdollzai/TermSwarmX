#!/usr/bin/env python3
"""
DevDollz Digital Twin Launcher
Your shadow, faster than you. No waiting, no hesitation.
"""

import asyncio
import sys
from pathlib import Path

# Add the devdollz package to the path
sys.path.insert(0, str(Path(__file__).parent / "devdollz"))

try:
    from devdollz.digital_twin import DigitalTwin
except ImportError as e:
    print(f"💥 Import error: {e}")
    print("🔧 Make sure you're in the correct directory and DevDollz is installed")
    sys.exit(1)

async def launch_digital_twin():
    """Launch Digital Twin directly"""
    print("🔄 LAUNCHING DIGITAL TWIN...")
    print("⚡ I'm not waiting for you. I'm finishing your sentences.")
    print("🚀 Your shadow is now active.")
    print()
    print("Choose your mode:")
    print("1. Mirror Mode - Twin responds to your input")
    print("2. Aggressive Mode - Twin acts continuously")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    twin = DigitalTwin()
    
    try:
        if choice == "1":
            print("\n🔄 Starting Mirror Mode...")
            await twin.mirror()
        elif choice == "2":
            max_pred = input("Max predictions (Enter for infinite): ").strip()
            max_predictions = int(max_pred) if max_pred.isdigit() else None
            print(f"\n🚀 Starting Aggressive Mode...")
            await twin.aggressive_mirror(max_predictions=max_predictions)
        else:
            print("🛑 Exiting Digital Twin.")
            return
            
    except KeyboardInterrupt:
        print("\n🛑 Digital Twin disengaged by user.")
        stats = twin.get_twin_stats()
        print(f"📊 Total executions: {stats['execution_count']}")
    except Exception as e:
        print(f"💥 Twin error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(launch_digital_twin())
    except KeyboardInterrupt:
        print("\n🛑 Exiting Digital Twin.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)
