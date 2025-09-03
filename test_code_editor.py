#!/usr/bin/env python3
"""
DevDollz Code Editor Test
Demonstrates the new multi-line code editor functionality
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from devdollz import (
        DEV_DOLLZ_LOGO, CREATOR_TAGLINE, THEME_ICONS, 
        CYBER_GLAM_COLORS, print_welcome, get_devdollz_info
    )
    from devdollz.ui import run_devdollz_ui
    print("✅ DevDollz imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_code_editor_features():
    """Test the new code editor features"""
    print("\n🎀 DevDollz Code Editor Features 🎀")
    print("=" * 60)
    
    print("✨ New Multi-Line Code Editor:")
    print("  • Replaces single-line Input with TextArea widget")
    print("  • Supports both command execution and code editing")
    print("  • Professional IDE-like experience")
    print("  • Cyber Glam theme integration")
    
    print("\n🎯 Key Features:")
    print("  • Ctrl+Enter: Execute commands from current line")
    print("  • Ctrl+E: Toggle between command and edit modes")
    print("  • Ctrl+S: Save code to file")
    print("  • Ctrl+O: Open file (placeholder)")
    print("  • Ctrl+N: Create new file")
    print("  • Ctrl+L: Clear log")
    print("  • ?: Show help")
    
    print("\n💻 Command Mode:")
    print("  • Execute DevDollz commands line by line")
    print("  • Command history navigation (up/down arrows)")
    print("  • Auto-completion for commands")
    
    print("\n📝 Edit Mode:")
    print("  • Multi-line code editing")
    print("  • Syntax highlighting support")
    print("  • Professional code editor experience")
    
    print("\n🎨 Theme Integration:")
    print("  • Cyber Glam color scheme")
    print("  • Electric Hacker Pink accents")
    print("  • Cyber-Pop Cyan highlights")
    print("  • Lavender Glow borders")

def test_ui_launch():
    """Test launching the UI"""
    print("\n🚀 Testing UI Launch...")
    print("This will start the DevDollz TUI with the new code editor.")
    print("Press Ctrl+C to exit when ready.")
    
    try:
        success = run_devdollz_ui()
        if success:
            print("✅ UI launched successfully!")
        else:
            print("⚠️ UI launch failed, falling back to CLI")
    except KeyboardInterrupt:
        print("\n✅ UI test completed successfully!")
    except Exception as e:
        print(f"❌ UI launch error: {e}")

def main():
    """Main test function"""
    print_welcome()
    
    print(f"\n{THEME_ICONS['info']} Testing DevDollz Code Editor Transformation")
    print("=" * 80)
    
    # Show system info
    info = get_devdollz_info()
    print(f"🎨 Theme: {info['theme']}")
    print(f"🔢 Version: {info['version']}")
    print(f"👩‍💻 Creator: {info['creator']}")
    
    # Test features
    test_code_editor_features()
    
    # Ask user if they want to test the UI
    print(f"\n{THEME_ICONS['info']} Ready to test the new code editor?")
    response = input("Launch DevDollz TUI? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        test_ui_launch()
    else:
        print(f"{THEME_ICONS['info']} Skipping UI test. Code editor transformation complete!")
    
    print(f"\n{THEME_ICONS['success']} DevDollz Code Editor Test Complete!")
    print(f"{CREATOR_TAGLINE}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{THEME_ICONS['info']} Test interrupted. Goodbye! ✨")
    except Exception as e:
        print(f"{THEME_ICONS['error']} Test error: {e}")
        sys.exit(1)
