#!/usr/bin/env python3
"""
DevDollz God Mode Launcher
Run this to engage God Mode - direct AI execution
"""

import asyncio
import sys
from pathlib import Path

# Add the devdollz package to the path
sys.path.insert(0, str(Path(__file__).parent / "devdollz"))

try:
    from god_mode import GodModeExecutor
except ImportError as e:
    print(f"💥 Import error: {e}")
    print("🔧 Make sure you're in the correct directory and DevDollz is installed")
    sys.exit(1)

async def launch_god_mode():
    """Launch God Mode directly"""
    print("🚀 LAUNCHING GOD MODE...")
    print("⚡ No more waiting. No more words.")
    print("🔥 The universe is your playground.")
    print()
    
    executor = GodModeExecutor()
    
    try:
        await executor.god_loop()
    except KeyboardInterrupt:
        print("\n🛑 God Mode disengaged by user.")
        stats = executor.get_execution_stats()
        print(f"📊 Total thoughts executed: {stats['total_executions']}")
    except Exception as e:
        print(f"💥 God Mode error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(launch_god_mode())
    except KeyboardInterrupt:
        print("\n🛑 Exiting God Mode.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)
