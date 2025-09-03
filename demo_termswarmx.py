#!/usr/bin/env python3
"""
TermSwarmX Integration Demo
Demonstrates the AI Swarm collaboration capabilities
"""

import asyncio
import json
import sys
from pathlib import Path

def main():
    """Main demo function"""
    print("🚀 TermSwarmX Integration Demo")
    print("🎯 Showcasing AI Swarm Collaboration Features")
    print("=" * 60)
    
    try:
        # Add devdollz to path
        devdollz_path = Path(__file__).parent / "devdollz"
        sys.path.insert(0, str(devdollz_path))
        
        # Import TermSwarmX components
        from devdollz.termswarmx_integration import (
            TermSwarmXTerminal, 
            SwarmCommand, 
            SwarmCommandType
        )
        
        print("✅ TermSwarmX integration loaded successfully!")
        
        # Run the demo
        asyncio.run(run_demo())
        
    except ImportError as e:
        print(f"❌ Failed to import TermSwarmX integration: {e}")
        return 1
        
    except Exception as e:
        print(f"💥 Error running demo: {e}")
        return 1
        
    return 0

async def run_demo():
    """Run the TermSwarmX integration demo"""
    print("\n🔥 Initializing TermSwarmX Terminal...")
    
    # Create terminal instance
    terminal = TermSwarmXTerminal()
    
    # Initialize the terminal
    await terminal.initialize_swarm_terminal()
    
    print("\n🎯 Creating AI Swarm Collaboration Session...")
    
    # Create a swarm session
    session_id = await terminal.create_swarm_session(
        "demo_session", 
        ["code_analyzer", "security_auditor", "performance_optimizer"]
    )
    
    print(f"\n🧠 Session created: {session_id}")
    
    # Execute some swarm commands
    print("\n⚡ Executing AI Swarm Commands...")
    
    # Command 1: Code Review
    print("\n📝 Command 1: Code Review Analysis")
    code_review_cmd = SwarmCommand(
        type=SwarmCommandType.CODE_REVIEW,
        target=session_id,
        payload={"file": "main.py", "focus": "security_and_performance"}
    )
    
    results1 = await terminal.execute_swarm_command(session_id, code_review_cmd)
    print("Results:")
    for collaborator, result in results1.items():
        print(f"  {collaborator}: {result['type']}")
    
    # Command 2: AI Brainstorming
    print("\n💭 Command 2: AI Brainstorming Session")
    brainstorm_cmd = SwarmCommand(
        type=SwarmCommandType.AI_BRAINSTORM,
        target=session_id,
        payload={"topic": "user_interface_improvements", "focus": "accessibility"}
    )
    
    results2 = await terminal.execute_swarm_command(session_id, brainstorm_cmd)
    print("Results:")
    for collaborator, result in results2.items():
        print(f"  {collaborator}: {result['type']}")
    
    # Show session history
    print("\n📚 Session History:")
    history = await terminal.get_swarm_history(session_id)
    for i, cmd in enumerate(history, 1):
        print(f"  {i}. {cmd.type.value} - {cmd.target}")
    
    # Show terminal status
    print("\n📊 Terminal Status:")
    status = terminal.get_terminal_status()
    print(f"  Active Swarms: {status['active_swarms']}")
    print(f"  AI Collaborators: {status['ai_collaborators']}")
    print(f"  Status: {status['status']}")
    
    # Close the session
    print("\n🔒 Closing Swarm Session...")
    await terminal.close_swarm_session(session_id)
    
    print("\n🎉 Demo Complete!")
    print("💡 To use the full CLI interface, run: python termswarmx_launcher.py")
    print("📖 For more information, see: TERMSWARMX_INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    sys.exit(main())
