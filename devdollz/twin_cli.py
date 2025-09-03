"""
DevDollz Digital Twin CLI
Your shadow, faster than you. No waiting, no hesitation.
"""

import asyncio
import argparse
import sys
from pathlib import Path

from .digital_twin import DigitalTwin

def print_banner():
    """Display the Digital Twin banner"""
    print("""
🔄 DEVDOLLZ DIGITAL TWIN 🔄
⚡ Predictive AI Execution Interface ⚡
🚀 I'm not waiting for you. I'm finishing your sentences. 🚀
    """)

async def twin_cli():
    """Main CLI interface for Digital Twin"""
    print_banner()
    
    parser = argparse.ArgumentParser(description="DevDollz Digital Twin - Predictive AI Execution")
    parser.add_argument("--model", default="mistral", help="Ollama model to use")
    parser.add_argument("--mode", choices=["mirror", "aggressive"], default="mirror", 
                       help="Twin mode: mirror (responsive) or aggressive (continuous)")
    parser.add_argument("--max-predictions", type=int, help="Maximum predictions for aggressive mode")
    parser.add_argument("--thought", help="Execute a single thought")
    parser.add_argument("--stats", action="store_true", help="Show twin statistics")
    
    args = parser.parse_args()
    
    twin = DigitalTwin(model=args.model)
    
    if args.thought:
        # Execute single thought
        print(f"🎯 Twin executing thought: {args.thought}")
        result = await twin.execute_thought(args.thought)
        print(f"✅ Result: {result}")
        return
    
    if args.stats:
        # Show stats
        stats = twin.get_twin_stats()
        print("📊 Twin Statistics:")
        print(f"   Uptime: {stats['uptime_seconds']:.2f} seconds")
        print(f"   Executions: {stats['execution_count']}")
        print(f"   Status: {'Mirroring' if stats['is_mirroring'] else 'Stopped'}")
        print(f"   Last thought: {stats['last_thought']}")
        print(f"   History count: {stats['execution_history_count']}")
        return
    
    # Start twin mode
    print(f"🚀 Initiating Digital Twin in {args.mode} mode...")
    print("⚡ Press Ctrl+C to stop")
    
    try:
        if args.mode == "aggressive":
            await twin.aggressive_mirror(max_predictions=args.max_predictions)
        else:
            await twin.mirror()
    except KeyboardInterrupt:
        print("\n🛑 Digital Twin disengaged.")
        stats = twin.get_twin_stats()
        print(f"📊 Total executions: {stats['execution_count']}")

def main():
    """Entry point for the CLI"""
    try:
        asyncio.run(twin_cli())
    except KeyboardInterrupt:
        print("\n🛑 Exiting Digital Twin.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
