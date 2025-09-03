#!/usr/bin/env python3
"""
Installation script for DevDollz: Atelier Edition - Swarm Brain System
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ is required.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def install_optional_dependencies():
    """Install optional dependencies"""
    print("\n🎯 Installing optional dependencies...")
    
    optional_packages = [
        ("prompt_toolkit", "Enhanced CLI experience"),
        ("numpy", "Numerical computing support"),
        ("pylint", "Code quality analysis"),
        ("SpeechRecognition", "Voice command support"),
        ("PyAudio", "Audio processing for voice commands")
    ]
    
    for package, description in optional_packages:
        try:
            run_command(f"pip install {package}", f"Installing {package} ({description})")
        except Exception as e:
            print(f"⚠️  Failed to install {package}: {e}")

def check_ollama():
    """Check if Ollama is available"""
    print("\n🤖 Checking Ollama availability...")
    
    try:
        import ollama
        print("✅ Ollama Python client is available")
        
        # Try to connect to Ollama service
        try:
            # This will fail if Ollama service is not running, which is expected
            print("💡 Note: Make sure Ollama service is running with 'ollama serve'")
            print("💡 Install Ollama from: https://ollama.ai/")
        except Exception:
            pass
            
    except ImportError:
        print("❌ Ollama Python client not found")
        print("💡 Install with: pip install ollama")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "plugins",
        "logs",
        "data"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def run_tests():
    """Run the import tests"""
    print("\n🧪 Running import tests...")
    
    if not run_command("python test_imports.py", "Running import tests"):
        print("⚠️  Some tests failed, but the system may still work")
        return False
    
    return True

def main():
    """Main installation process"""
    print("🚀 DevDollz: Atelier Edition - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Installation cannot continue. Please upgrade Python.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install required dependencies.")
        return False
    
    # Install optional dependencies
    install_optional_dependencies()
    
    # Check Ollama
    check_ollama()
    
    # Create directories
    create_directories()
    
    # Run tests
    test_success = run_tests()
    
    print("\n" + "=" * 50)
    if test_success:
        print("🎉 Installation completed successfully!")
        print("\n🚀 Next steps:")
        print("1. Start Ollama service: ollama serve")
        print("2. Pull a model: ollama pull mistral")
        print("3. Test the system: python test_swarm.py")
        print("4. Start breathing: python swarm_core.py")
    else:
        print("⚠️  Installation completed with warnings.")
        print("Some features may not work correctly.")
        print("Check the output above for details.")
    
    return test_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
