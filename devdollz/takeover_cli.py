"""
DevDollz Takeover CLI
Silent dominance through strategic positioning
"""

import asyncio
import argparse
import sys
from pathlib import Path

from .takeover import DevDollzTakeover

def print_banner():
    """Display the takeover banner"""
    print("""
🚀 DEVDOLLZ TAKEOVER 🚀
⚡ Silent Dominance Through Strategic Positioning ⚡
🔥 We don't dominate feeds. We dominate keyboards. 🔥
    """)

async def takeover_cli():
    """Main CLI interface for DevDollz takeover"""
    print_banner()
    
    parser = argparse.ArgumentParser(description="DevDollz Takeover - Silent Dominance")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode (no traces)")
    parser.add_argument("--visible", action="store_true", help="Disable stealth mode (show all operations)")
    parser.add_argument("--phase", choices=["positioning", "defaults", "inevitability", "integration", "all"], 
                       default="all", help="Execute specific takeover phase")
    parser.add_argument("--stats", action="store_true", help="Show takeover statistics")
    parser.add_argument("--target", help="Target specific platform for takeover")
    
    args = parser.parse_args()
    
    takeover = DevDollzTakeover()
    
    # Configure stealth mode
    if args.stealth:
        takeover.enable_stealth_mode()
    elif args.visible:
        takeover.disable_stealth_mode()
    
    if args.stats:
        # Show stats
        stats = takeover.get_takeover_stats()
        print("📊 Takeover Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        return
    
    if args.target:
        # Target specific platform
        print(f"🎯 Targeting {args.target} for takeover...")
        success = takeover.silent_install(args.target)
        if success:
            print(f"✅ {args.target} now defaults to DevDollz")
        else:
            print(f"💥 Takeover failed for {args.target}")
        return
    
    # Execute takeover based on phase
    if args.phase == "all":
        print("🚀 Executing complete DevDollz takeover...")
        results = takeover.execute_takeover()
        
        print("\n📊 Takeover Results:")
        for phase, result in results.items():
            print(f"   {phase}: {result}")
            
    else:
        print(f"🎯 Executing {args.phase} phase...")
        if args.phase == "positioning":
            result = takeover.strategic_positioning()
        elif args.phase == "defaults":
            result = takeover.become_default()
        elif args.phase == "inevitability":
            result = takeover.create_inevitability()
        elif args.phase == "integration":
            result = takeover.silent_integration()
        
        print(f"✅ {args.phase} phase complete: {result}")
    
    print("\n✅ Takeover operations complete.")
    print("🚀 DevDollz is becoming the default, not the alternative.")
    print("🔥 No watermark. No powered by. Just faster output.")

def main():
    """Entry point for the CLI"""
    try:
        asyncio.run(takeover_cli())
    except KeyboardInterrupt:
        print("\n🛑 Takeover stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
