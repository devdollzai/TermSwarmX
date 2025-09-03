#!/usr/bin/env python3
"""
DevDollz Launcher - The Complete System
Choose your level: Spine, Canvas, or Silicon Core
"""

import sys
import os
from pathlib import Path

def main():
    print("🔥 DevDollz - The Current That Flows")
    print("=" * 50)
    print("Choose your level:")
    print("1. 🔥 Spine - Lightning-fast agent spawning")
    print("2. 🎨 Canvas - Code left, pulse feed right")
    print("3. 💾 Silicon Core - Direct to substrate")
    print("4. 🚀 All - Complete DevDollz experience")
    print("=" * 50)
    
    try:
        choice = input("Select (1-4): ").strip()
        
        if choice == "1":
            print("\n🚀 Launching DevDollz Spine...")
            from devdollz.spine import DevDollzSpine
            spine = DevDollzSpine()
            spine.start()
            
            # Demo mode
            print("\n🧪 Testing agent spawning...")
            spine.execute("generate Python function for data processing")
            spine.execute("scrape website for content")
            spine.execute("analyze code structure")
            
            input("\nPress Enter to continue...")
            spine.stop()
            
        elif choice == "2":
            print("\n🎨 Launching DevDollz Canvas...")
            from devdollz.spine_canvas import DevDollzCanvasLauncher
            launcher = DevDollzCanvasLauncher()
            launcher.launch()
            
        elif choice == "3":
            print("\n💾 Launching DevDollz Silicon Core...")
            from devdollz.silicon_core import DevDollzSiliconLauncher
            launcher = DevDollzSiliconLauncher()
            launcher.launch()
            
        elif choice == "4":
            print("\n🚀 Launching Complete DevDollz System...")
            print("🔥 Starting with Spine...")
            from devdollz.spine import DevDollzSpine
            spine = DevDollzSpine()
            spine.start()
            
            print("🎨 Adding Canvas...")
            from devdollz.spine_canvas import DevDollzCanvasLauncher
            canvas_launcher = DevDollzCanvasLauncher()
            
            print("💾 Etching to Silicon...")
            from devdollz.silicon_core import DevDollzSiliconLauncher
            silicon_launcher = DevDollzSiliconLauncher()
            
            print("✅ Complete DevDollz system active!")
            print("🔥 The Current That Flows")
            print("💓 The Pulse That Never Sleeps")
            print("⚡ Lightning-Fast Agent Spawning")
            print("🎤 Voice Always Listening")
            print("💾 Direct to Substrate")
            
            input("\nPress Enter to continue...")
            spine.stop()
            
        else:
            print("❌ Invalid choice")
            return
            
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Launch error: {e}")
        print("🔄 Check dependencies and try again")

if __name__ == "__main__":
    main()
