#!/usr/bin/env python3
"""
DevDollz Theme System
Girly Hacker Aesthetics for the Elite
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
import json
from pathlib import Path

class ThemeStyle(Enum):
    """Available theme styles"""
    HACKER_BARBIE = "hacker-barbie"
    CYBER_GOTH = "cyber-goth"
    PASTEL_HACKER = "pastel-hacker"
    NEON_DREAMS = "neon-dreams"
    CLASSIC_TERMINAL = "classic-terminal"
    CYBER_GLAM = "cyber-glam"
    CUSTOM = "custom"

@dataclass
class ColorPalette:
    """Color palette for DevDollz themes"""
    primary: str          # Main brand color
    secondary: str        # Secondary brand color
    accent: str           # Accent/highlight color
    background: str       # Background color
    surface: str          # Surface/elevated background
    text: str            # Primary text color
    text_secondary: str  # Secondary text color
    success: str         # Success/positive color
    warning: str         # Warning/caution color
    error: str           # Error/danger color
    info: str            # Info/neutral color

@dataclass
class ThemeConfig:
    """Complete theme configuration"""
    name: str
    description: str
    author: str
    version: str
    style: ThemeStyle
    colors: ColorPalette
    fonts: Dict[str, str]
    icons: Dict[str, str]
    animations: Dict[str, bool]
    custom_css: Optional[str] = None

class DevDollzThemeManager:
    """Manages DevDollz themes and aesthetics"""
    
    def __init__(self):
        self.themes: Dict[str, ThemeConfig] = {}
        self.current_theme: Optional[ThemeConfig] = None
        self.load_default_themes()
    
    def load_default_themes(self):
        """Load all default DevDollz themes"""
        
        # Hacker Barbie - Default Theme
        self.themes["hacker-barbie"] = ThemeConfig(
            name="Hacker Barbie",
            description="Hot pink meets hacker culture. The signature DevDollz look.",
            author="Alexis Adams",
            version="1.0.0",
            style=ThemeStyle.HACKER_BARBIE,
            colors=ColorPalette(
                primary="#FF69B4",      # Hot Pink
                secondary="#8A2BE2",    # Electric Purple
                accent="#39FF14",       # Neon Green
                background="#2F4F4F",   # Dark Slate
                surface="#3F5F5F",      # Lighter Slate
                text="#FFFFFF",         # White
                text_secondary="#FFB6C1", # Light Pink
                success="#00FF7F",      # Spring Green
                warning="#FFD700",      # Gold
                error="#FF1493",        # Deep Pink
                info="#00BFFF"          # Deep Sky Blue
            ),
            fonts={
                "heading": "Inter",
                "body": "JetBrains Mono",
                "code": "Fira Code",
                "ui": "Segoe UI"
            },
            icons={
                "success": "🎀",
                "warning": "💖",
                "error": "🖤",
                "info": "💕",
                "code": "🧠",
                "debug": "🔍",
                "security": "🛡️",
                "deploy": "🚀"
            },
            animations={
                "typing": True,
                "loading": True,
                "transitions": True,
                "particles": False
            }
        )
        
        # Cyber Goth
        self.themes["cyber-goth"] = ThemeConfig(
            name="Cyber Goth",
            description="Dark, edgy, and mysterious. For the gothic hackers.",
            author="Alexis Adams",
            version="1.0.0",
            style=ThemeStyle.CYBER_GOTH,
            colors=ColorPalette(
                primary="#FF1493",      # Deep Pink
                secondary="#8B008B",    # Dark Magenta
                accent="#00FFFF",       # Cyan
                background="#000000",   # Black
                surface="#1A1A1A",      # Dark Gray
                text="#FFFFFF",         # White
                text_secondary="#FF69B4", # Hot Pink
                success="#00FF7F",      # Spring Green
                warning="#FFD700",      # Gold
                error="#FF0000",        # Red
                info="#00BFFF"          # Deep Sky Blue
            ),
            fonts={
                "heading": "Orbitron",
                "body": "Source Code Pro",
                "code": "Fira Code",
                "ui": "Consolas"
            },
            icons={
                "success": "🖤",
                "warning": "💀",
                "error": "☠️",
                "info": "⚡",
                "code": "🧠",
                "debug": "🔍",
                "security": "🛡️",
                "deploy": "🚀"
            },
            animations={
                "typing": True,
                "loading": True,
                "transitions": True,
                "particles": True
            }
        )
        
        # Pastel Hacker
        self.themes["pastel-hacker"] = ThemeConfig(
            name="Pastel Hacker",
            description="Soft, gentle, and approachable. Hacking with a gentle touch.",
            author="Alexis Adams",
            version="1.0.0",
            style=ThemeStyle.PASTEL_HACKER,
            colors=ColorPalette(
                primary="#FFB6C1",      # Light Pink
                secondary="#DDA0DD",    # Plum
                accent="#98FB98",       # Pale Green
                background="#F0F8FF",   # Alice Blue
                surface="#FFFFFF",      # White
                text="#2F4F4F",         # Dark Slate
                text_secondary="#696969", # Dim Gray
                success="#90EE90",      # Light Green
                warning="#F0E68C",      # Khaki
                error="#F08080",        # Light Coral
                info="#87CEEB"          # Sky Blue
            ),
            fonts={
                "heading": "Quicksand",
                "body": "Open Sans",
                "code": "JetBrains Mono",
                "ui": "Segoe UI"
            },
            icons={
                "success": "🌸",
                "warning": "🌺",
                "error": "🌷",
                "info": "🌼",
                "code": "🧠",
                "debug": "🔍",
                "security": "🛡️",
                "deploy": "🚀"
            },
            animations={
                "typing": True,
                "loading": True,
                "transitions": True,
                "particles": False
            }
        )
        
        # Neon Dreams
        self.themes["neon-dreams"] = ThemeConfig(
            name="Neon Dreams",
            description="Bright, vibrant, and futuristic. For the cyberpunk enthusiasts.",
            author="Alexis Adams",
            version="1.0.0",
            style=ThemeStyle.NEON_DREAMS,
            colors=ColorPalette(
                primary="#FF00FF",      # Magenta
                secondary="#00FFFF",    # Cyan
                accent="#FFFF00",       # Yellow
                background="#000000",   # Black
                surface="#1A1A1A",      # Dark Gray
                text="#FFFFFF",         # White
                text_secondary="#FF69B4", # Hot Pink
                success="#00FF00",      # Lime
                warning="#FFA500",      # Orange
                error="#FF0000",        # Red
                info="#0080FF"          # Blue
            ),
            fonts={
                "heading": "Orbitron",
                "body": "Source Code Pro",
                "code": "Fira Code",
                "ui": "Consolas"
            },
            icons={
                "success": "✨",
                "warning": "💫",
                "error": "🌟",
                "info": "⭐",
                "code": "🧠",
                "debug": "🔍",
                "security": "🛡️",
                "deploy": "🚀"
            },
            animations={
                "typing": True,
                "loading": True,
                "transitions": True,
                "particles": True
            }
        )
        
        # Classic Terminal
        self.themes["classic-terminal"] = ThemeConfig(
            name="Classic Terminal",
            description="Traditional green on black. For the purists.",
            author="Alexis Adams",
            version="1.0.0",
            style=ThemeStyle.CLASSIC_TERMINAL,
            colors=ColorPalette(
                primary="#00FF00",      # Green
                secondary="#32CD32",    # Lime Green
                accent="#7FFF00",       # Chartreuse
                background="#000000",   # Black
                surface="#0A0A0A",      # Very Dark Gray
                text="#00FF00",         # Green
                text_secondary="#32CD32", # Lime Green
                success="#00FF00",      # Green
                warning="#FFFF00",      # Yellow
                error="#FF0000",        # Red
                info="#00FFFF"          # Cyan
            ),
            fonts={
                "heading": "Courier New",
                "body": "Courier New",
                "code": "Courier New",
                "ui": "Courier New"
            },
            icons={
                "success": "✓",
                "warning": "⚠",
                "error": "✗",
                "info": "ℹ",
                "code": ">",
                "debug": "?",
                "security": "#",
                "deploy": "$"
            },
            animations={
                "typing": False,
                "loading": False,
                "transitions": False,
                "particles": False
            }
        )
        
        # Cyber Glam - The New DevDollz Signature Theme
        self.themes["cyber-glam"] = ThemeConfig(
            name="Cyber Glam",
            description="A dark theme that blends deep, moody tones with electric, neon-bright accents. The signature DevDollz look.",
            author="Alexis Adams",
            version="1.0.0",
            style=ThemeStyle.CYBER_GLAM,
            colors=ColorPalette(
                primary="#ff00ff",      # Electric Hacker Pink
                secondary="#00ffff",    # Cyber-Pop Cyan
                accent="#c792ea",       # Lavender Glow
                background="#1e1e2e",   # Deep charcoal with hint of purple
                surface="#2a2a3a",      # Lighter charcoal
                text="#f0f0f0",         # Off-white Crystal
                text_secondary="#888888", # Cool Grey
                success="#c3e88d",      # Lime Sparkle
                warning="#ffcb8b",      # Warm Amber
                error="#ff5370",        # Crimson Glitch
                info="#89ddff"          # Sky Blue
            ),
            fonts={
                "heading": "JetBrains Mono",
                "body": "JetBrains Mono",
                "code": "Fira Code",
                "ui": "JetBrains Mono"
            },
            icons={
                "success": "✨",
                "warning": "💖",
                "error": "☠️",
                "info": "💖",
                "code": "🧠",
                "debug": "🔍",
                "security": "🛡️",
                "deploy": "🚀"
            },
            animations={
                "typing": True,
                "loading": True,
                "transitions": True,
                "particles": False
            }
        )
    
    def get_theme(self, theme_name: str) -> Optional[ThemeConfig]:
        """Get a theme by name"""
        return self.themes.get(theme_name)
    
    def list_themes(self) -> List[str]:
        """List all available theme names"""
        return list(self.themes.keys())
    
    def set_current_theme(self, theme_name: str) -> bool:
        """Set the current active theme"""
        theme = self.get_theme(theme_name)
        if theme:
            self.current_theme = theme
            return True
        return False
    
    def get_current_theme(self) -> Optional[ThemeConfig]:
        """Get the current active theme"""
        return self.current_theme
    
    def create_custom_theme(self, name: str, colors: ColorPalette, **kwargs) -> ThemeConfig:
        """Create a custom theme"""
        custom_theme = ThemeConfig(
            name=name,
            description=kwargs.get("description", "Custom DevDollz theme"),
            author=kwargs.get("author", "Custom Creator"),
            version=kwargs.get("version", "1.0.0"),
            style=ThemeStyle.CUSTOM,
            colors=colors,
            fonts=kwargs.get("fonts", self.themes["hacker-barbie"].fonts),
            icons=kwargs.get("icons", self.themes["hacker-barbie"].icons),
            animations=kwargs.get("animations", self.themes["hacker-barbie"].animations),
            custom_css=kwargs.get("custom_css")
        )
        
        self.themes[name] = custom_theme
        return custom_theme
    
    def export_theme(self, theme_name: str, file_path: Path) -> bool:
        """Export a theme to a JSON file"""
        theme = self.get_theme(theme_name)
        if not theme:
            return False
        
        try:
            with open(file_path, 'w') as f:
                json.dump(theme.__dict__, f, indent=2, default=str)
            return True
        except Exception:
            return False
    
    def import_theme(self, file_path: Path) -> Optional[ThemeConfig]:
        """Import a theme from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Reconstruct the theme
            colors = ColorPalette(**data["colors"])
            theme = ThemeConfig(
                name=data["name"],
                description=data["description"],
                author=data["author"],
                version=data["version"],
                style=ThemeStyle(data["style"]),
                colors=colors,
                fonts=data["fonts"],
                icons=data["icons"],
                animations=data["animations"],
                custom_css=data.get("custom_css")
            )
            
            self.themes[theme.name] = theme
            return theme
        except Exception:
            return None
    
    def get_theme_preview(self, theme_name: str) -> str:
        """Get a text preview of a theme"""
        theme = self.get_theme(theme_name)
        if not theme:
            return f"Theme '{theme_name}' not found"
        
        preview = f"""
🎀 {theme.name} Theme Preview 🎀
{'=' * 50}

📝 Description: {theme.description}
👩‍💻 Author: {theme.author}
🔢 Version: {theme.version}
🎨 Style: {theme.style.value}

🎨 Color Palette:
  Primary: {theme.colors.primary}
  Secondary: {theme.colors.secondary}
  Accent: {theme.colors.accent}
  Background: {theme.colors.background}
  Surface: {theme.colors.surface}

🔤 Fonts:
  Heading: {theme.fonts['heading']}
  Body: {theme.fonts['body']}
  Code: {theme.fonts['code']}
  UI: {theme.fonts['ui']}

✨ Features:
  Typing Animation: {'✅' if theme.animations['typing'] else '❌'}
  Loading Animation: {'✅' if theme.animations['loading'] else '❌'}
  Transitions: {'✅' if theme.animations['transitions'] else '❌'}
  Particles: {'✅' if theme.animations['particles'] else '❌'}

🎭 Icons:
  Success: {theme.icons['success']}
  Warning: {theme.icons['warning']}
  Error: {theme.icons['error']}
  Info: {theme.icons['info']}
"""
        return preview
    
    def apply_theme_to_terminal(self, theme_name: str) -> bool:
        """Apply a theme to the current terminal session"""
        theme = self.get_theme(theme_name)
        if not theme:
            return False
        
        # Set the current theme
        self.current_theme = theme
        
        # Apply colors to terminal (platform-specific)
        try:
            import os
            if os.name == 'nt':  # Windows
                os.system(f'color 0{theme.colors.background[1:]}')
            else:  # Unix/Linux/macOS
                # Set terminal colors using ANSI escape codes
                print(f"\033[48;2;{int(theme.colors.background[1:3], 16)};{int(theme.colors.background[3:5], 16)};{int(theme.colors.background[5:7], 16)}m")
                print(f"\033[38;2;{int(theme.colors.text[1:3], 16)};{int(theme.colors.text[3:5], 16)};{int(theme.colors.text[5:7], 16)}m")
            
            return True
        except Exception:
            return False

# Global theme manager instance
theme_manager = DevDollzThemeManager()

def get_theme_manager() -> DevDollzThemeManager:
    """Get the global theme manager instance"""
    return theme_manager

def quick_theme_preview():
    """Show a quick preview of all available themes"""
    print("🎀 DevDollz Theme Gallery 🎀")
    print("=" * 60)
    
    for theme_name in theme_manager.list_themes():
        print(f"\n{theme_manager.get_theme_preview(theme_name)}")
        print("-" * 60)

if __name__ == "__main__":
    # Demo the theme system
    quick_theme_preview()
    
    # Show current theme
    theme_manager.set_current_theme("hacker-barbie")
    current = theme_manager.get_current_theme()
    print(f"\n🎯 Current Theme: {current.name}")
    print(f"🎨 Primary Color: {current.colors.primary}")
