#!/usr/bin/env python3
"""
TermSwarmX Launcher
Launches the TermSwarmX AI Swarm Collaboration Terminal
"""

import asyncio
import sys
from pathlib import Path

def main():
    """Main launcher function"""
    print("🚀 Launching TermSwarmX AI Swarm Collaboration Terminal...")
    print("🎯 Bridging AiTSwarmX IDE with TermSwarmX CLI concepts")
    
    try:
        # Add devdollz to path
        devdollz_path = Path(__file__).parent / "devdollz"
        sys.path.insert(0, str(devdollz_path))
        
        # Import and run TermSwarmX integration
        from devdollz.termswarmx_integration import main as termswarmx_main
        
        print("✅ TermSwarmX integration loaded successfully!")
        print("🔥 Starting AI Swarm Collaboration Terminal...\n")
        
        # Run the async main function
        asyncio.run(termswarmx_main())
        
    except ImportError as e:
        print(f"❌ Failed to import TermSwarmX integration: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return 1
        
    except Exception as e:
        print(f"💥 Error launching TermSwarmX: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
