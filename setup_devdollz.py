#!/usr/bin/env python3
"""
DevDollz: Atelier Edition - Quick Setup Script
Helps users get the IDE running quickly
"""

import subprocess
import sys
import os
import platform

def print_header():
    """Print the setup header"""
    print("🚀 DevDollz: Atelier Edition - Quick Setup")
    print("=" * 50)
    print("Setting up your local AI-powered development environment")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   DevDollz requires Python 3.9 or higher")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_pip_packages():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    packages = [
        "textual>=0.40.0",
        "prompt_toolkit>=3.0.0", 
        "pygments>=2.10.0",
        "pylint>=3.0.0",
        "numpy>=1.24.0"
    ]
    
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {package}")
            return False
    
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    print("\n🤖 Checking Ollama installation...")
    
    # Check if ollama command exists
    try:
        result = subprocess.run(
            ["ollama", "--version"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ Ollama is installed")
            version = result.stdout.strip()
            print(f"   Version: {version}")
        else:
            print("❌ Ollama command failed")
            return False
    except FileNotFoundError:
        print("❌ Ollama not found")
        print("   Installing Ollama...")
        return install_ollama()
    
    # Check if Ollama service is running
    try:
        result = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ Ollama service is running")
            return True
        else:
            print("❌ Ollama service not responding")
            print("   Starting Ollama service...")
            return start_ollama_service()
    except Exception as e:
        print(f"❌ Error checking Ollama service: {e}")
        return False

def install_ollama():
    """Install Ollama based on platform"""
    print("   Installing Ollama...")
    
    system = platform.system().lower()
    
    if system == "linux":
        try:
            subprocess.check_call([
                "curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"
            ], shell=True)
            print("   ✅ Ollama installed via script")
            return True
        except subprocess.CalledProcessError:
            print("   ❌ Failed to install Ollama via script")
            print("   Please install manually: https://ollama.ai/download")
            return False
    
    elif system == "darwin":  # macOS
        print("   Please install Ollama manually:")
        print("   https://ollama.ai/download")
        return False
    
    elif system == "windows":
        print("   Please install Ollama manually:")
        print("   https://ollama.ai/download")
        return False
    
    else:
        print(f"   Unsupported platform: {system}")
        return False

def start_ollama_service():
    """Start the Ollama service"""
    print("   Starting Ollama service...")
    
    try:
        # Start Ollama in background
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait a moment for service to start
        import time
        time.sleep(3)
        
        # Check if it's working
        result = subprocess.run(
            ["ollama", "list"], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print("   ✅ Ollama service started")
            return True
        else:
            print("   ❌ Failed to start Ollama service")
            return False
            
    except Exception as e:
        print(f"   ❌ Error starting Ollama: {e}")
        return False

def pull_mistral_model():
    """Pull the Mistral model for Ollama"""
    print("\n📥 Pulling Mistral AI model...")
    
    try:
        print("   This may take a few minutes...")
        subprocess.check_call([
            "ollama", "pull", "mistral"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("   ✅ Mistral model downloaded")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ Failed to download Mistral model")
        return False

def run_tests():
    """Run the core functionality tests"""
    print("\n🧪 Running functionality tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_devdollz_core.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed")
            print("   Check test output for details")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed!")
    print("=" * 50)
    print("Next steps:")
    print("1. Start DevDollz:")
    print("   python swarm_ide.py")
    print()
    print("2. Try the example plugin:")
    print("   plugin load example_plugin.py")
    print("   example_plugin hello world")
    print()
    print("3. Generate some code:")
    print("   generate function calculate_fibonacci")
    print()
    print("4. Debug some code:")
    print("   debug code def test(): pass")
    print()
    print("For help, type '?' in the IDE")
    print("=" * 50)

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install Python packages
    if not install_pip_packages():
        print("❌ Failed to install Python packages")
        return False
    
    # Check Ollama
    if not check_ollama():
        print("❌ Ollama setup failed")
        return False
    
    # Pull Mistral model
    if not pull_mistral_model():
        print("❌ Failed to download AI model")
        return False
    
    # Run tests
    if not run_tests():
        print("❌ Functionality tests failed")
        return False
    
    print_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
