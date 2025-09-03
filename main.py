#!/usr/bin/env python3
"""
AI Swarm IDE - Main Entry Point
Autonomous AI Development Environment
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli import app

if __name__ == "__main__":
    app()
