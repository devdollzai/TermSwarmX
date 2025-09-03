"""
DevDollz AI Swarm IDE
Where Code Meets Chaos - Built by Alexis Adams for the Hacker Elite

A multi-agent AI development environment that outperforms traditional tools
with style, speed, and substance.
"""

__version__ = "0.1.0"
__author__ = "Alexis Adams"
__email__ = "alexis@devdollz.dev"
__description__ = "Where Code Meets Chaos - Built by Alexis Adams for the Hacker Elite"
__url__ = "https://github.com/devdollzai/ai-swarm-ide"

# Import main components
from .themes import get_theme_manager, DevDollzThemeManager, ThemeStyle, ThemeConfig, ColorPalette
from .constants import (
    DEV_DOLLZ_LOGO, CREATOR_TAGLINE, THEME_ICONS, CYBER_GLAM_COLORS,
    SYSTEM_MESSAGES, COMMAND_PROTOCOL, ASCII_DECORATIONS,
    print_welcome, get_devdollz_info
)
from .core import get_devdollz_core

# Export main functions and constants
__all__ = [
    "get_theme_manager",
    "DevDollzThemeManager", 
    "ThemeStyle",
    "ThemeConfig",
    "ColorPalette",
    "DEV_DOLLZ_LOGO",
    "CREATOR_TAGLINE", 
    "THEME_ICONS",
    "CYBER_GLAM_COLORS",
    "SYSTEM_MESSAGES",
    "COMMAND_PROTOCOL",
    "ASCII_DECORATIONS",
    "print_welcome",
    "get_devdollz_info",
    "get_devdollz_core"
]

def get_creator_info():
    """Get information about the creator"""
    return {
        "name": "Alexis Adams",
        "title": "Creator & Hacker",
        "quote": "I built this because I was tired of slow, boring AI tools. Real hackers need speed, style, and substance. DevDollz delivers all three.",
        "github": "https://github.com/devdollzai",
        "twitter": "https://twitter.com/DevDollzAI",
        "discord": "https://discord.gg/devdollz"
    }

def get_brand_info():
    """Get brand information"""
    return {
        "name": "DevDollz",
        "tagline": "Where Code Meets Chaos",
        "description": "Built by Alexis Adams for the Hacker Elite",
        "colors": {
            "primary": "#FF69B4",      # Hot Pink
            "secondary": "#8A2BE2",    # Electric Purple
            "accent": "#39FF14",       # Neon Green
            "background": "#2F4F4F"    # Dark Slate
        },
        "themes": [
            "hacker-barbie",
            "cyber-goth", 
            "pastel-hacker",
            "neon-dreams",
            "classic-terminal"
        ]
    }

# Print banner when imported
if __name__ != "__main__":
    import sys
    if "--quiet" not in sys.argv:
        print("🎀 DevDollz AI Swarm IDE loaded successfully!")
        print("👩‍💻 Creator: Alexis Adams")
        print("🚀 Ready to hack with style!")
