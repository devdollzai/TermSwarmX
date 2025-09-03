#!/usr/bin/env python3
"""
DevDollz CLI Launcher
Quick access to the DevDollz AI Swarm IDE from anywhere
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from devdollz.main import main
except ImportError:
    print("Error: Could not import DevDollz. Please ensure the package is properly installed.")
    print("Try running: pip install -e .")
    sys.exit(1)

if __name__ == "__main__":
    main()
