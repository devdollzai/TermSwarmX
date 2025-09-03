#!/usr/bin/env python3
"""
DevDollz Constants
Core branding and theme constants for the DevDollz system
"""

# DevDollz ASCII Logo - The Signature Brand
DEV_DOLLZ_LOGO = """
██████╗ ██╗██╗   ██╗██╗  ██╗ ██████╗ ██╗     ██╗     ███████╗
██╔══██╗██║██║   ██║██║  ██║██╔═══██╗██║     ██║     ╚══███╔╝
██║  ██║██║██║   ██║██║  ██║██║   ██║██║     ██║       ███╔╝ 
██║  ██║██║██║   ██║██║  ██║██║   ██║██║     ██║      ███╔╝  
██████╔╝██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗███████╗
╚═════╝ ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝
"""

# Creator Tagline
CREATOR_TAGLINE = "DevDollz v1.0 | An Alexis Adams Creation ✨"

# Theme Icons - Unicode symbols for the DevDollz aesthetic
THEME_ICONS = {
    "success": "✨",
    "error": "☠️",
    "info": "💖",
    "log": "💖",
    "code": "🧠",
    "debug": "🔍",
    "security": "🛡️",
    "deploy": "🚀",
    "folder": "📁",
    "file": "📄",
    "loading": "★",
    "heart": "♥"
}

# Cyber Glam Color Palette - The signature DevDollz theme
CYBER_GLAM_COLORS = {
    "background": "#1e1e2e",    # Deep charcoal with hint of purple
    "primary": "#ff00ff",       # Electric Hacker Pink
    "secondary": "#00ffff",     # Cyber-Pop Cyan
    "tertiary": "#c792ea",      # Lavender Glow
    "success": "#c3e88d",       # Lime Sparkle
    "error": "#ff5370",         # Crimson Glitch
    "text": "#f0f0f0",          # Off-white Crystal
    "muted": "#888888",         # Cool Grey
    "surface": "#2a2a3a",       # Lighter charcoal
    "warning": "#ffcb8b",       # Warm Amber
    "info": "#89ddff"           # Sky Blue
}

# System Messages with DevDollz Tone
SYSTEM_MESSAGES = {
    "welcome": "Welcome to DevDollz! 💖 Press ? for help.",
    "help_header": "DevDollz Command Protocol:",
    "invalid_command": "That's not the password. Try again.",
    "loading": "★ Assembling the dolls...",
    "shutdown": "DevDollz shutting down gracefully... ✨"
}

# Command Protocol
COMMAND_PROTOCOL = {
    "generate": {
        "function": "generate function <description>",
        "class": "generate class <description>",
        "code": "generate code <description>"
    },
    "debug": {
        "syntax": "debug syntax <code>",
        "logic": "debug logic <code>",
        "code": "debug code <code>"
    }
}

# ASCII Art Decorations
ASCII_DECORATIONS = {
    "separator": "═" * 80,
    "header_line": "─" * 50,
    "bullet": "  • ",
    "arrow": "  → ",
    "star": "★",
    "heart": "♥",
    "sparkle": "✨"
}

# Utility functions for the demo
def print_welcome():
    """Print the DevDollz welcome message"""
    print(DEV_DOLLZ_LOGO)
    print(f"\n{CREATOR_TAGLINE}")
    print("✨ Where Code Meets Chaos - Elegantly ✨")

def get_devdollz_info():
    """Get comprehensive DevDollz information"""
    return {
        "logo": DEV_DOLLZ_LOGO,
        "creator": "Alexis Adams",
        "tagline": CREATOR_TAGLINE,
        "theme": "Cyber Glam",
        "version": "1.0.0",
        "colors": CYBER_GLAM_COLORS,
        "icons": THEME_ICONS
    }
