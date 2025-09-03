#!/usr/bin/env python3
"""
DevDollz AI Swarm IDE - Main Entry Point
Where Code Meets Chaos ✨

A vibrant, girly aesthetic fused with sharp, professional hacker vibes.
Designed and signed by Alexis Adams.

Usage:
    python -m devdollz          # Run with TUI (preferred)
    python -m devdollz --cli    # Force CLI mode
    python -m devdollz --help   # Show help
"""

import sys
import argparse
import time
from pathlib import Path

# Add the parent directory to the path so we can import devdollz
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from devdollz import (
        DEV_DOLLZ_LOGO, CREATOR_TAGLINE, THEME_ICONS, 
        print_welcome, get_devdollz_info, run_devdollz_ui
    )
    from devdollz.core import get_devdollz_core
except ImportError as e:
    print(f"Error importing DevDollz: {e}")
    print("Please ensure the devdollz package is properly installed.")
    sys.exit(1)

def create_cli_interface():
    """Create a CLI interface for DevDollz when TUI is unavailable"""
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.lexers import PygmentsLexer
    from pygments.lexers.python import PythonLexer
    
    bindings = KeyBindings()
    
    @bindings.add('?')
    def show_help(event):
        event.app.exit(result='help')
    
    @bindings.add('ctrl+c')
    def quit_app(event):
        event.app.exit(result='quit')
    
    completer = WordCompleter([
        'generate function ', 'generate class ', 'generate code ',
        'debug syntax ', 'debug logic ', 'debug code ',
        'help', 'status', 'history', 'clear', 'quit', 'exit'
    ], ignore_case=True)
    
    session = PromptSession(
        'DevDollz > ', 
        completer=completer, 
        lexer=PygmentsLexer(PythonLexer),
        key_bindings=bindings
    )
    
    return session

def print_cli_help():
    """Print CLI help information"""
    print(f"{THEME_ICONS['info']} DevDollz Command Protocol:")
    print("  generate [function|class|code] <description>")
    print("  debug [syntax|logic|code] <code or description>")
    print("  status - Show system status")
    print("  history - Show recent tasks")
    print("  clear - Clear the screen")
    print("  help - Show this help")
    print("  quit/exit - Exit DevDollz")
    print("")
    print("Examples:")
    print("  generate function calculate_sum")
    print("  debug syntax def foo(: pass")
    print("")

def print_cli_status(core):
    """Print CLI system status"""
    try:
        status = core.get_info()
        print(f"{THEME_ICONS['info']} DevDollz System Status:")
        print(f"  System: {status['system_name']}")
        print(f"  Creator: {status['creator']}")
        print(f"  Theme: {status['theme']}")
        print(f"  Version: {status['version']}")
        print(f"  Active Tasks: {status['active_tasks']}")
        print(f"  Total Tasks: {status['total_tasks']}")
        print(f"  CodeGen Agent: {'🟢' if status['agents']['code_gen'] else '🔴'}")
        print(f"  Debug Agent: {'🟢' if status['agents']['debug'] else '🔴'}")
    except Exception as e:
        print(f"{THEME_ICONS['error']} Failed to get system status: {e}")

def print_cli_history(core):
    """Print CLI task history"""
    try:
        history = core.get_history(10)
        print(f"{THEME_ICONS['info']} Recent DevDollz Tasks:")
        
        if not history:
            print("  No tasks in history yet.")
        else:
            for task in history:
                status_icon = THEME_ICONS['success'] if task['status'] == 'success' else THEME_ICONS['error']
                print(f"  {status_icon} {task['task_id']}: {task['task'][:50]}...")
    except Exception as e:
        print(f"{THEME_ICONS['error']} Failed to get history: {e}")

def run_cli_mode():
    """Run DevDollz in CLI mode"""
    print(f"{THEME_ICONS['info']} Running DevDollz in CLI mode...")
    
    core = get_devdollz_core()
    session = create_cli_interface()
    
    try:
        while True:
            try:
                command = session.prompt()
                command = command.strip()
                
                if not command:
                    continue
                
                # Handle special commands
                if command.lower() in ['quit', 'exit']:
                    print(f"{THEME_ICONS['info']} Goodbye! ✨")
                    break
                
                if command == 'help':
                    print_cli_help()
                    continue
                
                if command == 'status':
                    print_cli_status(core)
                    continue
                
                if command == 'history':
                    print_cli_history(core)
                    continue
                
                if command == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_welcome()
                    continue
                
                # Parse and execute DevDollz commands
                parts = command.split(maxsplit=2)
                if len(parts) < 2:
                    print(f"{THEME_ICONS['error']} That's not the password. Try again.")
                    print_cli_help()
                    continue
                
                action, cmd_type = parts[0], parts[1]
                task_content = parts[2] if len(parts) > 2 else ""
                
                if action not in ["generate", "debug"] or cmd_type not in ["function", "class", "code", "syntax", "logic"]:
                    print(f"{THEME_ICONS['error']} That's not the password. Try again.")
                    print_cli_help()
                    continue
                
                # Execute task
                agent_type = "code_gen" if action == "generate" else "debug"
                print(f"{THEME_ICONS['loading']} Assembling the dolls...")
                
                task_id = core.execute_task(agent_type, cmd_type, task_content)
                print(f"{THEME_ICONS['info']} Task {task_id} submitted to {agent_type} agent")
                
                # Wait for results
                time.sleep(0.1)
                results = core.get_results()
                
                for result in results:
                    if result.status == "success":
                        print(f"{THEME_ICONS['success']} Task {result.task_id} completed by {result.agent}")
                        print(f"{result.content}")
                    else:
                        print(f"{THEME_ICONS['error']} Task {result.task_id} failed: {result.content}")
                    print("")
                
            except KeyboardInterrupt:
                print(f"\n{THEME_ICONS['info']} Interrupted. Type 'quit' to exit.")
            except Exception as e:
                print(f"{THEME_ICONS['error']} Error: {str(e)}")
                print_cli_help()
    
    finally:
        core.shutdown()
        print(f"{THEME_ICONS['success']} DevDollz CLI shutdown complete")

def main():
    """Main entry point for DevDollz"""
    parser = argparse.ArgumentParser(
        description="DevDollz AI Swarm IDE - Where Code Meets Chaos ✨",
        epilog=f"Created by Alexis Adams | Theme: Cyber Glam"
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true', 
        help='Force CLI mode (skip TUI)'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='DevDollz v1.0.0 - An Alexis Adams Creation'
    )
    
    parser.add_argument(
        '--info', 
        action='store_true', 
        help='Show system information and exit'
    )
    
    args = parser.parse_args()
    
    # Show welcome message
    print_welcome()
    
    # Show system info if requested
    if args.info:
        info = get_devdollz_info()
        print(f"\n{THEME_ICONS['info']} System Information:")
        for key, value in info.items():
            if key != 'logo':  # Skip the ASCII logo in info display
                print(f"  {key}: {value}")
        return
    
    # Try TUI mode first (unless --cli is specified)
    if not args.cli:
        try:
            print(f"{THEME_ICONS['info']} Starting DevDollz TUI...")
            if run_devdollz_ui():
                return
        except Exception as e:
            print(f"{THEME_ICONS['error']} TUI failed: {e}")
            print(f"{THEME_ICONS['info']} Falling back to CLI mode...")
    
    # Fall back to CLI mode
    run_cli_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{THEME_ICONS['info']} DevDollz interrupted. Goodbye! ✨")
    except Exception as e:
        print(f"{THEME_ICONS['error']} Fatal error: {e}")
        sys.exit(1)
