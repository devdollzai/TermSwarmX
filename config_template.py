# DevDollz: Atelier Edition - Configuration Template
# 
# IMPORTANT: Copy this file to config.py and add your actual secrets
# NEVER commit config.py with real secrets to version control
#
# Usage:
# 1. Copy this file: cp config_template.py config.py
# 2. Edit config.py with your actual values
# 3. Keep config.py in your .gitignore (already done)

import os
from pathlib import Path

# Base Configuration
BASE_DIR = Path(__file__).parent
PROJECT_NAME = "DevDollz: Atelier Edition"

# AI Model Configuration
AI_CONFIG = {
    "model": "llama3.1:8b",  # Default Ollama model
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
}

# Twitter API Configuration (Optional)
# Get these from https://developer.twitter.com/
TWITTER_CONFIG = {
    "consumer_key": os.getenv("TWITTER_CONSUMER_KEY", ""),
    "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET", ""),
    "access_token": os.getenv("TWITTER_ACCESS_TOKEN", ""),
    "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET", ""),
}

# Ollama Configuration
OLLAMA_CONFIG = {
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "api_key": os.getenv("OLLAMA_API_KEY", ""),
    "timeout": 30,
}

# Database Configuration
DATABASE_CONFIG = {
    "path": BASE_DIR / "data",
    "memory_db": "atelier_memory.db",
    "swarm_db": "swarm_memory.db",
    "whisper_db": "whisper_memory.db",
}

# UI Configuration
UI_CONFIG = {
    "theme": "dark",
    "font_size": 14,
    "max_lines": 1000,
    "auto_save": True,
    "auto_save_interval": 300,  # 5 minutes
}

# Development Configuration
DEV_CONFIG = {
    "debug": os.getenv("DEV_DEBUG", "false").lower() == "true",
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "enable_profiling": False,
    "cache_enabled": True,
}

# Voice Configuration
VOICE_CONFIG = {
    "enabled": True,
    "input_device": None,  # Auto-detect
    "output_device": None,  # Auto-detect
    "sample_rate": 16000,
    "chunk_size": 1024,
}

# Security Configuration
SECURITY_CONFIG = {
    "max_login_attempts": 3,
    "session_timeout": 3600,  # 1 hour
    "password_min_length": 8,
    "enable_2fa": False,  # Future feature
}

# Plugin Configuration
PLUGIN_CONFIG = {
    "enabled": True,
    "plugin_dir": BASE_DIR / "plugins",
    "auto_load": True,
    "sandboxed": True,
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    "max_threads": os.getenv("MAX_THREADS", "4"),
    "memory_limit": os.getenv("MEMORY_LIMIT", "2GB"),
    "cache_size": 1000,
    "enable_compression": True,
}

# Export all configurations
__all__ = [
    "AI_CONFIG",
    "TWITTER_CONFIG", 
    "OLLAMA_CONFIG",
    "DATABASE_CONFIG",
    "UI_CONFIG",
    "DEV_CONFIG",
    "VOICE_CONFIG",
    "SECURITY_CONFIG",
    "PLUGIN_CONFIG",
    "PERFORMANCE_CONFIG",
]
