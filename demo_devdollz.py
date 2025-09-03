#!/usr/bin/env python3
"""
DevDollz Demo Script
Showcase the beautiful DevDollz system and its capabilities
"""

import sys
import time
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from devdollz import (
        DEV_DOLLZ_LOGO, CREATOR_TAGLINE, THEME_ICONS, 
        CYBER_GLAM_COLORS, print_welcome, get_devdollz_info
    )
    from devdollz.core import get_devdollz_core
except ImportError as e:
    print(f"Error importing DevDollz: {e}")
    print("Please ensure the devdollz package is properly installed.")
    sys.exit(1)

def demo_welcome():
    """Demonstrate the DevDollz welcome experience"""
    print("\n" + "="*80)
    print("🎀 DevDollz Demo - Welcome Experience 🎀")
    print("="*80)
    
    print_welcome()
    
    print(f"\n{THEME_ICONS['info']} System Information:")
    info = get_devdollz_info()
    for key, value in info.items():
        if key != 'logo':
            print(f"  {key}: {value}")

def demo_theme_system():
    """Demonstrate the DevDollz theme system"""
    print(f"\n{THEME_ICONS['info']} Theme System Demo:")
    print("-" * 50)
    
    print(f"🎨 Cyber Glam Color Palette:")
    for color_name, hex_value in CYBER_GLAM_COLORS.items():
        print(f"  {color_name}: {hex_value}")
    
    print(f"\n✨ Theme Icons:")
    for icon_name, icon_symbol in THEME_ICONS.items():
        print(f"  {icon_name}: {icon_symbol}")

def demo_command_protocol():
    """Demonstrate the DevDollz command protocol"""
    print(f"\n{THEME_ICONS['info']} Command Protocol Demo:")
    print("-" * 50)
    
    print("Available Commands:")
    print("  generate [function|class|code] <description>")
    print("  debug [syntax|logic|code] <code or description>")
    print("  help, status, history, clear, quit/exit")
    
    print(f"\n{THEME_ICONS['code']} Example Commands:")
    print("  generate function calculate_fibonacci")
    print("  generate class DataProcessor")
    print("  debug syntax def invalid_function(: pass")
    print("  debug logic complex_algorithm")

def demo_system_status():
    """Demonstrate the DevDollz system status"""
    print(f"\n{THEME_ICONS['info']} System Status Demo:")
    print("-" * 50)
    
    try:
        core = get_devdollz_core()
        status = core.get_info()
        
        print(f"System: {status['system_name']}")
        print(f"Creator: {status['creator']}")
        print(f"Theme: {status['theme']}")
        print(f"Version: {status['version']}")
        print(f"Active Tasks: {status['active_tasks']}")
        print(f"Total Tasks: {status['total_tasks']}")
        print(f"CodeGen Agent: {'🟢' if status['agents']['code_gen'] else '🔴'}")
        print(f"Debug Agent: {'🟢' if status['agents']['debug'] else '🔴'}")
        
        # Cleanup
        core.shutdown()
        
    except Exception as e:
        print(f"{THEME_ICONS['error']} Failed to get system status: {e}")

def demo_interactive_mode():
    """Demonstrate interactive DevDollz mode"""
    print(f"\n{THEME_ICONS['info']} Interactive Mode Demo:")
    print("-" * 50)
    
    print("To experience the full DevDollz system:")
    print("  1. Run: python -m devdollz")
    print("  2. Or: python devdollz_cli.py")
    print("  3. Or: python -m devdollz --cli")
    
    print(f"\n{THEME_ICONS['info']} The TUI provides:")
    print("  - Beautiful file tree navigation")
    print("  - Real-time results display")
    print("  - Command history and completion")
    print("  - Full Cyber Glam theming")

def demo_features():
    """Demonstrate key DevDollz features"""
    print(f"\n{THEME_ICONS['info']} Key Features Demo:")
    print("-" * 50)
    
    features = [
        ("🎨 Cyber Glam Theme", "Stunning dark theme with electric pink, cyan, and lavender accents"),
        ("🧠 AI-Powered Code Generation", "Generate elegant, production-ready Python code"),
        ("🔍 Advanced Debugging", "Comprehensive code analysis and improvement suggestions"),
        ("💫 Beautiful TUI Interface", "Modern Textual-based terminal user interface"),
        ("🔄 Multi-Agent Swarm", "Coordinated AI agents working together seamlessly"),
        ("📚 Persistent Memory", "SQLite-based task history and system tracking"),
        ("🎯 Professional Quality", "Built-in error handling, type hints, and documentation")
    ]
    
    for feature, description in features:
        print(f"  {feature}")
        print(f"    {description}")
        print()

def main():
    """Main demo function"""
    print("🎀 Welcome to the DevDollz Demo! 🎀")
    print("This script showcases the beautiful DevDollz AI Swarm IDE")
    print("Created by Alexis Adams with love and precision ✨")
    
    # Run all demos
    demo_welcome()
    demo_theme_system()
    demo_command_protocol()
    demo_system_status()
    demo_features()
    demo_interactive_mode()
    
    print(f"\n{THEME_ICONS['success']} Demo Complete!")
    print(f"{THEME_ICONS['info']} Ready to experience DevDollz? Run:")
    print("  python -m devdollz")
    print(f"\n{CREATOR_TAGLINE}")
    print("✨ Where Code Meets Chaos - Elegantly ✨")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{THEME_ICONS['info']} Demo interrupted. Goodbye! ✨")
    except Exception as e:
        print(f"{THEME_ICONS['error']} Demo error: {e}")
        sys.exit(1)
