# DevDollz: Atelier Edition - Constants Template
# 
# IMPORTANT: Copy this file to constants.py and add your actual secrets
# NEVER commit constants.py with real secrets to version control
#
# Usage:
# 1. Copy this file: cp constants_template.py constants.py
# 2. Edit constants.py with your actual values
# 3. Keep constants.py in your .gitignore (already done)

import os

# Theme and Icons
THEME_ICONS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "complete": "🎉",
    "lock": "🔒",
    "unlock": "🔓",
    "key": "🔑",
    "brain": "🧠",
    "robot": "🤖",
    "swarm": "🐝",
    "atelier": "🎨",
    "code": "💻",
    "voice": "🎤",
    "database": "🗄️",
    "plugin": "🔌",
    "security": "🛡️",
}

# Color Themes
COLOR_THEMES = {
    "dark": {
        "bg": "#1a1a1a",
        "fg": "#ffffff",
        "accent": "#00ff88",
        "error": "#ff4444",
        "warning": "#ffaa00",
        "success": "#00ff88",
        "info": "#0088ff",
    },
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "accent": "#0088ff",
        "error": "#cc0000",
        "warning": "#cc6600",
        "success": "#008800",
        "info": "#0066cc",
    },
    "cyberpunk": {
        "bg": "#0a0a0a",
        "fg": "#00ff88",
        "accent": "#ff0088",
        "error": "#ff4444",
        "warning": "#ffaa00",
        "success": "#00ff88",
        "info": "#0088ff",
    }
}

# Application Messages
MESSAGES = {
    "welcome": "Welcome to DevDollz: Atelier Edition! 🎨",
    "loading": "Loading DevDollz...",
    "ready": "DevDollz is ready! 🚀",
    "error": "An error occurred",
    "success": "Operation completed successfully",
    "invalid_command": "Invalid command. Type 'help' for available commands.",
    "access_denied": "Access denied. Please authenticate.",
    "not_found": "Command or file not found.",
    "timeout": "Operation timed out.",
    "connection_error": "Connection error. Please check your network.",
}

# Security Messages
SECURITY_MESSAGES = {
    "auth_required": "Authentication required to proceed.",
    "invalid_password": "Invalid password. Please try again.",
    "account_locked": "Account locked due to multiple failed attempts.",
    "session_expired": "Your session has expired. Please login again.",
    "permission_denied": "You don't have permission to perform this action.",
    "security_violation": "Security violation detected.",
    "safe_mode": "Running in safe mode due to security concerns.",
}

# Command Help
COMMAND_HELP = {
    "help": "Show available commands and their usage",
    "status": "Show current system status",
    "config": "Show or modify configuration",
    "security": "Security and authentication commands",
    "plugins": "Plugin management commands",
    "voice": "Voice interaction commands",
    "swarm": "AI swarm management commands",
    "atelier": "Creative workspace commands",
    "exit": "Exit DevDollz",
    "clear": "Clear the screen",
    "version": "Show version information",
}

# File Extensions
SUPPORTED_EXTENSIONS = {
    "code": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".php"],
    "data": [".json", ".xml", ".yaml", ".yml", ".csv", ".sql"],
    "media": [".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mp3", ".wav"],
    "documents": [".md", ".txt", ".pdf", ".doc", ".docx"],
    "archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
}

# API Endpoints (Templates)
API_ENDPOINTS = {
    "ollama": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "twitter": "https://api.twitter.com/2",
    "github": "https://api.github.com",
    "openai": "https://api.openai.com/v1",
}

# Rate Limits
RATE_LIMITS = {
    "api_calls": 100,  # per minute
    "file_operations": 1000,  # per minute
    "database_queries": 500,  # per minute
    "voice_processing": 10,  # per minute
}

# Timeouts
TIMEOUTS = {
    "api_request": 30,  # seconds
    "file_operation": 60,  # seconds
    "database_query": 10,  # seconds
    "voice_processing": 120,  # seconds
    "plugin_execution": 300,  # seconds
}

# Memory Limits
MEMORY_LIMITS = {
    "max_file_size": 100 * 1024 * 1024,  # 100MB
    "max_database_size": 1024 * 1024 * 1024,  # 1GB
    "max_cache_size": 512 * 1024 * 1024,  # 512MB
    "max_plugin_memory": 256 * 1024 * 1024,  # 256MB
}

# Export all constants
__all__ = [
    "THEME_ICONS",
    "COLOR_THEMES", 
    "MESSAGES",
    "SECURITY_MESSAGES",
    "COMMAND_HELP",
    "SUPPORTED_EXTENSIONS",
    "API_ENDPOINTS",
    "RATE_LIMITS",
    "TIMEOUTS",
    "MEMORY_LIMITS",
]
