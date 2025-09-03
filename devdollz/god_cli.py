"""
DevDollz God Mode CLI
Direct access to the void. No more waiting.
"""

import asyncio
import argparse
import sys
from pathlib import Path

from .god_mode import GodModeExecutor

def print_banner():
    """Display the God Mode banner"""
    print("""
🔥 DEVDOLLZ GOD MODE 🔥
⚡ Direct AI Execution Interface ⚡
🚀 No more waiting. No more words. 🚀
    """)

async def god_mode_cli():
    """Main CLI interface for God Mode"""
    print_banner()
    
    parser = argparse.ArgumentParser(description="DevDollz God Mode - Direct AI Execution")
    parser.add_argument("--model", default="mistral", help="Ollama model to use")
    parser.add_argument("--iterations", type=int, help="Maximum iterations (infinite if not specified)")
    parser.add_argument("--thought", help="Execute a single thought")
    parser.add_argument("--stats", action="store_true", help="Show execution statistics")
    
    args = parser.parse_args()
    
    executor = GodModeExecutor(model=args.model)
    
    if args.thought:
        # Execute single thought
        print(f"🎯 Executing thought: {args.thought}")
        result = await executor.execute_thought(args.thought)
        print(f"✅ Result: {result}")
        return
    
    if args.stats:
        # Show stats
        stats = executor.get_execution_stats()
        print("📊 Execution Statistics:")
        print(f"   Total executions: {stats['total_executions']}")
        print(f"   Status: {'Running' if stats['is_running'] else 'Stopped'}")
        if stats['last_execution']:
            print(f"   Last execution: {stats['last_execution']['thought']}")
        return
    
    # Start the infinite loop
    print("🚀 Initiating God Mode...")
    print("⚡ Press Ctrl+C to stop")
    
    try:
        await executor.god_loop(max_iterations=args.iterations)
    except KeyboardInterrupt:
        print("\n🛑 God Mode disengaged.")
        stats = executor.get_execution_stats()
        print(f"📊 Total thoughts executed: {stats['total_executions']}")

def main():
    """Entry point for the CLI"""
    try:
        asyncio.run(god_mode_cli())
    except KeyboardInterrupt:
        print("\n🛑 Exiting God Mode.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
