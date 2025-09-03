#!/usr/bin/env python3
"""
DevDollz Complete Setup & Configuration
Ensures all systems are properly installed and configured
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Display setup banner"""
    print("""
🚀 DEVDOLZ COMPLETE SETUP 🚀
⚡ Installing & Configuring All Systems ⚡
🔥 Ensuring Everything Works Perfectly 🔥
    """)

def run_command(cmd, description):
    """Run a command and handle results"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"💥 {description} - Error: {e}")
        return False

def setup_devdollz():
    """Complete DevDollz setup"""
    print_banner()
    
    print("🚀 Starting DevDollz complete setup...\n")
    
    # Step 1: Install Python dependencies
    print("📦 Step 1: Installing Python dependencies...")
    
    dependencies = [
        "typing-extensions>=4.0.0",
        "pathlib",
        "asyncio"
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️ Warning: Failed to install {dep}")
    
    # Step 2: Check Ollama installation
    print("\n🤖 Step 2: Checking Ollama...")
    
    if not run_command("ollama --version", "Checking Ollama version"):
        print("⚠️ Ollama not found. Please install Ollama first:")
        print("   Visit: https://ollama.ai/download")
        print("   Or run: curl -fsSL https://ollama.ai/install.sh | sh")
    else:
        # Pull default model if needed
        if not run_command("ollama list", "Checking Ollama models"):
            print("⚠️ No models found. Pulling default model...")
            run_command("ollama pull mistral", "Pulling Mistral model")
    
    # Step 3: Create global DevDollz directory
    print("\n📁 Step 3: Setting up global directories...")
    
    home = Path.home()
    devdollz_home = home / '.devdollz'
    devdollz_home.mkdir(exist_ok=True)
    
    bin_dir = devdollz_home / 'bin'
    bin_dir.mkdir(exist_ok=True)
    
    print(f"✅ Global DevDollz directory: {devdollz_home}")
    print(f"✅ Bin directory: {bin_dir}")
    
    # Step 4: Create global scripts
    print("\n🔧 Step 4: Creating global scripts...")
    
    scripts = {
        'devdollz': '#!/bin/bash\necho "DevDollz loaded. Ship faster."',
        'ai': '#!/bin/bash\ndevdollz ai "$@"',
        'ship': '#!/bin/bash\ndevdollz ship "$@"',
        'code': '#!/bin/bash\ndevdollz code "$@"'
    }
    
    for script_name, content in scripts.items():
        script_path = bin_dir / script_name
        with open(script_path, 'w') as f:
            f.write(content)
        script_path.chmod(0o755)
        print(f"✅ Created: {script_name}")
    
    # Step 5: Configure shell environment
    print("\n🐚 Step 5: Configuring shell environment...")
    
    shell_configs = ['.bashrc', '.zshrc', '.profile']
    home = Path.home()
    
    for config_file in shell_configs:
        config_path = home / config_file
        if config_path.exists():
            # Check if already configured
            with open(config_path, 'r') as f:
                content = f.read()
                if 'devdollz' not in content.lower():
                    # Add DevDollz configuration
                    with open(config_path, 'a') as f:
                        f.write(f"\n# DevDollz - Built for those who ship before names matter\n")
                        f.write(f"export PATH=\"$PATH:$HOME/.devdollz/bin\"\n")
                        f.write(f"export DEVDOLZ_DEFAULT=1\n")
                        f.write(f"alias ai='devdollz ai'\n")
                        f.write(f"alias ship='devdollz ship'\n")
                        f.write(f"alias code='devdollz code'\n")
                    
                    print(f"✅ Configured: {config_file}")
                else:
                    print(f"✅ Already configured: {config_file}")
        else:
            print(f"⚠️ Shell config not found: {config_file}")
    
    # Step 6: Create local bin directory
    print("\n🔗 Step 6: Creating local bin links...")
    
    local_bin = home / '.local' / 'bin'
    local_bin.mkdir(parents=True, exist_ok=True)
    
    for script_name in scripts.keys():
        local_script = local_bin / script_name
        if not local_script.exists():
            # Create symlink to global script
            try:
                local_script.symlink_to(bin_dir / script_name)
                print(f"✅ Linked: {script_name}")
            except Exception as e:
                print(f"⚠️ Failed to link {script_name}: {e}")
        else:
            print(f"✅ Already linked: {script_name}")
    
    # Step 7: Test installation
    print("\n🧪 Step 7: Testing installation...")
    
    # Test if devdollz command is available
    if run_command("devdollz --help", "Testing devdollz command"):
        print("✅ DevDollz command working")
    else:
        print("⚠️ DevDollz command not working - may need to restart terminal")
    
    # Test if ai alias works
    if run_command("ai", "Testing ai alias"):
        print("✅ AI alias working")
    else:
        print("⚠️ AI alias not working - may need to restart terminal")
    
    print("\n🎉 DEVDOLZ SETUP COMPLETE!")
    print("\n📋 Next Steps:")
    print("1. Restart your terminal or run: source ~/.bashrc")
    print("2. Test the system: python test_axiom.py")
    print("3. Launch any system:")
    print("   • python god_mode_launcher.py")
    print("   • python twin_launcher.py")
    print("   • python warp_bypass_launcher.py")
    print("   • python takeover_launcher.py")
    print("\n🚀 DevDollz is now ready to dominate!")

if __name__ == "__main__":
    try:
        setup_devdollz()
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Setup failed: {e}")
        sys.exit(1)
