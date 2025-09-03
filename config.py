# config.py - Configuration constants for DevDollz: Atelier Edition

# Precognition AI Configuration
PRECOGNITION_CONFIG = {
    "precog_active": True,
    "precog_delay": 5,  # seconds between precognition cycles
    "learning_rate": 0.1,
    "max_memory": 1000
}

# AI Model Configuration
AI_CONFIG = {
    "default_model": "mistral",
    "fallback_model": "llama2",
    "max_tokens": 2048,
    "temperature": 0.7
}

# System Configuration
SYSTEM_CONFIG = {
    "max_agents": 10,
    "max_plugins": 20,
    "db_file": "devdollz_atelier_memory.db",
    "log_level": "INFO"
}

# Theme Configuration
THEME_CONFIG = {
    "name": "Onyx & Orchid",
    "primary_color": "#8B5CF6",
    "secondary_color": "#EC4899",
    "background_color": "#0F0F23",
    "text_color": "#F8FAFC"
}

# Plugin Configuration
PLUGIN_CONFIG = {
    "auto_load": False,
    "plugin_dir": "./plugins",
    "allowed_extensions": [".py", ".pyc"],
    "max_execution_time": 30
}
