"""
DevDollz Warp Bypass CLI
Their trial, our house. No limits, no payments.
"""

import asyncio
import argparse
import sys
from pathlib import Path

from .warp_bypass import WarpBypass

def print_banner():
    """Display the Warp bypass banner"""
    print("""
🔥 DEVDOLLZ WARP BYPASS 🔥
⚡ Their Trial, Our House ⚡
🚀 No limits. No payments. No waiting. 🚀
    """)

async def bypass_cli():
    """Main CLI interface for Warp bypass"""
    print_banner()
    
    parser = argparse.ArgumentParser(description="DevDollz Warp Bypass - Their Trial, Our House")
    parser.add_argument("--model", default="mistral", help="Ollama model to use")
    parser.add_argument("--feature", choices=["pair_programming", "code_completion", "error_explanation", 
                                            "refactoring", "documentation", "testing"], 
                       help="Generate specific Warp feature")
    parser.add_argument("--context", help="Context for feature generation")
    parser.add_argument("--file", help="Analyze specific file with IDE integration")
    parser.add_argument("--compare", action="store_true", help="Compare with Warp limitations")
    parser.add_argument("--stats", action="store_true", help="Show bypass statistics")
    
    args = parser.parse_args()
    
    bypass = WarpBypass(model=args.model)
    
    if args.feature:
        # Generate specific feature
        print(f"🎯 Generating Warp feature: {args.feature}")
        result = bypass.generate_feature(args.feature, args.context or "")
        print(f"✅ Result: {result}")
        return
    
    if args.file:
        # Analyze file
        print(f"📁 Analyzing file: {args.file}")
        result = bypass.run_local_ide_integration(args.file)
        print(f"✅ Analysis: {result}")
        return
    
    if args.compare:
        # Compare with Warp
        print(bypass.compare_with_warp())
        return
    
    if args.stats:
        # Show stats
        stats = bypass.get_bypass_stats()
        print("📊 Bypass Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        return
    
    # Default: Execute full bypass
    print("🎯 Executing Warp bypass...")
    result = bypass.steal_their_speed()
    
    print("\n📊 Bypass Statistics:")
    stats = bypass.get_bypass_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + bypass.compare_with_warp())
    
    print("\n✅ Warp bypass complete. You're now running their features locally.")
    print("🚀 No trial expiration. No usage limits. Just execution.")

def main():
    """Entry point for the CLI"""
    try:
        asyncio.run(bypass_cli())
    except KeyboardInterrupt:
        print("\n🛑 Warp bypass stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
