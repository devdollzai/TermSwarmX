#!/usr/bin/env python3
"""
DevDollz System Verification & Setup
Comprehensive testing of all components and systems
"""

import sys
import os
import subprocess
import importlib
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

class DevDollzVerifier:
    """Comprehensive system verification for DevDollz"""
    
    def __init__(self):
        self.results = {}
        self.errors = []
        self.warnings = []
        self.start_time = time.time()
        
    def print_banner(self):
        """Display verification banner"""
        print("""
🔥 DEVDOLLZ SYSTEM VERIFICATION 🔥
⚡ Testing All Components & Systems ⚡
🚀 Ensuring Everything Works Perfectly 🚀
        """)
    
    def check_python_environment(self) -> bool:
        """Check Python environment and dependencies"""
        print("🐍 Checking Python environment...")
        
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version.major >= 3 and python_version.minor >= 8:
                print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Compatible")
                self.results['python_version'] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
            else:
                print(f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Requires 3.8+")
                self.errors.append(f"Python version {python_version.major}.{python_version.minor} too old")
                return False
            
            # Check required packages
            required_packages = ['asyncio', 'pathlib', 'typing', 'json', 'time', 'uuid']
            missing_packages = []
            
            for package in required_packages:
                try:
                    importlib.import_module(package)
                    print(f"✅ {package} - Available")
                except ImportError:
                    missing_packages.append(package)
                    print(f"❌ {package} - Missing")
            
            if missing_packages:
                self.errors.append(f"Missing packages: {', '.join(missing_packages)}")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Python environment check failed: {e}")
            return False
    
    def check_devdollz_installation(self) -> bool:
        """Check DevDollz package installation"""
        print("\n📦 Checking DevDollz installation...")
        
        try:
            # Check if devdollz directory exists
            devdollz_path = Path(__file__).parent / "devdollz"
            if devdollz_path.exists():
                print(f"✅ DevDollz directory found at {devdollz_path}")
                self.results['devdollz_path'] = str(devdollz_path)
            else:
                print("❌ DevDollz directory not found")
                self.errors.append("DevDollz directory missing")
                return False
            
            # Check core modules
            core_modules = ['core', 'constants', 'god_mode', 'digital_twin', 'warp_bypass', 'takeover']
            missing_modules = []
            
            for module in core_modules:
                module_path = devdollz_path / f"{module}.py"
                if module_path.exists():
                    print(f"✅ {module}.py - Available")
                else:
                    missing_modules.append(module)
                    print(f"❌ {module}.py - Missing")
            
            if missing_modules:
                self.warnings.append(f"Missing modules: {', '.join(missing_modules)}")
            
            return True
            
        except Exception as e:
            self.errors.append(f"DevDollz installation check failed: {e}")
            return False
    
    def check_ollama_availability(self) -> bool:
        """Check if Ollama is available and working"""
        print("\n🤖 Checking Ollama availability...")
        
        try:
            # Try to import ollama
            try:
                import ollama
                print("✅ Ollama Python package - Available")
                self.results['ollama_package'] = True
            except ImportError:
                print("❌ Ollama Python package - Missing")
                self.warnings.append("Ollama Python package not installed")
                return False
            
            # Check if Ollama service is running
            try:
                result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("✅ Ollama service - Running")
                    self.results['ollama_service'] = True
                    
                    # Check available models
                    models = result.stdout.strip().split('\n')[1:]  # Skip header
                    if models and models[0]:
                        print(f"✅ Available models: {len(models)}")
                        self.results['ollama_models'] = len(models)
                    else:
                        print("⚠️ No models found - Consider running 'ollama pull mistral'")
                        self.warnings.append("No Ollama models available")
                else:
                    print("❌ Ollama service - Not responding")
                    self.errors.append("Ollama service not responding")
                    return False
                    
            except subprocess.TimeoutExpired:
                print("❌ Ollama service - Timeout")
                self.errors.append("Ollama service timeout")
                return False
            except FileNotFoundError:
                print("❌ Ollama command - Not found")
                self.errors.append("Ollama command not found")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"Ollama check failed: {e}")
            return False
    
    def check_system_integration(self) -> bool:
        """Check system integration and configuration"""
        print("\n🔧 Checking system integration...")
        
        try:
            # Check shell configuration
            home = Path.home()
            shell_configs = ['.bashrc', '.zshrc', '.profile']
            configured_shells = []
            
            for config_file in shell_configs:
                config_path = home / config_file
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        content = f.read()
                        if 'devdollz' in content.lower():
                            configured_shells.append(config_file)
                            print(f"✅ {config_file} - DevDollz configured")
                        else:
                            print(f"⚠️ {config_file} - No DevDollz configuration")
            
            if configured_shells:
                self.results['configured_shells'] = configured_shells
            else:
                self.warnings.append("No shell configurations found")
            
            # Check global DevDollz directory
            devdollz_home = home / '.devdollz'
            if devdollz_home.exists():
                print("✅ Global DevDollz directory - Exists")
                self.results['global_devdollz'] = True
            else:
                print("⚠️ Global DevDollz directory - Not found")
                self.warnings.append("Global DevDollz directory not created")
            
            # Check PATH integration
            path_dirs = os.environ.get('PATH', '').split(os.pathsep)
            devdollz_in_path = any('devdollz' in path for path in path_dirs)
            
            if devdollz_in_path:
                print("✅ DevDollz in PATH - Available")
                self.results['path_integration'] = True
            else:
                print("⚠️ DevDollz not in PATH")
                self.warnings.append("DevDollz not in system PATH")
            
            return True
            
        except Exception as e:
            self.errors.append(f"System integration check failed: {e}")
            return False
    
    def test_core_functionality(self) -> bool:
        """Test core DevDollz functionality"""
        print("\n🧪 Testing core functionality...")
        
        try:
            # Test database functionality
            try:
                from devdollz.core import DevDollzDatabase
                db = DevDollzDatabase()
                print("✅ Database - Working")
                self.results['database'] = True
            except Exception as e:
                print(f"❌ Database - Failed: {e}")
                self.errors.append(f"Database test failed: {e}")
                return False
            
            # Test constants
            try:
                from devdollz.constants import CYBER_GLAM_COLORS
                if CYBER_GLAM_COLORS:
                    print("✅ Constants - Available")
                    self.results['constants'] = True
                else:
                    print("⚠️ Constants - Empty")
                    self.warnings.append("Constants appear to be empty")
            except Exception as e:
                print(f"❌ Constants - Failed: {e}")
                self.errors.append(f"Constants test failed: {e}")
            
            # Test God Mode
            try:
                from devdollz.god_mode import GodModeExecutor
                executor = GodModeExecutor()
                print("✅ God Mode - Available")
                self.results['god_mode'] = True
            except Exception as e:
                print(f"❌ God Mode - Failed: {e}")
                self.errors.append(f"God Mode test failed: {e}")
            
            # Test Digital Twin
            try:
                from devdollz.digital_twin import DigitalTwin
                twin = DigitalTwin()
                print("✅ Digital Twin - Available")
                self.results['digital_twin'] = True
            except Exception as e:
                print(f"❌ Digital Twin - Failed: {e}")
                self.errors.append(f"Digital Twin test failed: {e}")
            
            # Test Warp Bypass
            try:
                from devdollz.warp_bypass import WarpBypass
                bypass = WarpBypass()
                print("✅ Warp Bypass - Available")
                self.results['warp_bypass'] = True
            except Exception as e:
                print(f"❌ Warp Bypass - Failed: {e}")
                self.errors.append(f"Warp Bypass test failed: {e}")
            
            # Test Takeover
            try:
                from devdollz.takeover import DevDollzTakeover
                takeover = DevDollzTakeover()
                print("✅ Takeover - Available")
                self.results['takeover'] = True
            except Exception as e:
                print(f"❌ Takeover - Failed: {e}")
                self.errors.append(f"Takeover test failed: {e}")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Core functionality test failed: {e}")
            return False
    
    def check_launcher_scripts(self) -> bool:
        """Check launcher scripts availability"""
        print("\n🚀 Checking launcher scripts...")
        
        try:
            launchers = [
                'god_mode_launcher.py',
                'twin_launcher.py', 
                'warp_bypass_launcher.py',
                'takeover_launcher.py'
            ]
            
            available_launchers = []
            for launcher in launchers:
                launcher_path = Path(__file__).parent / launcher
                if launcher_path.exists():
                    print(f"✅ {launcher} - Available")
                    available_launchers.append(launcher)
                else:
                    print(f"❌ {launcher} - Missing")
                    self.errors.append(f"Launcher missing: {launcher}")
            
            if available_launchers:
                self.results['available_launchers'] = available_launchers
            
            return len(available_launchers) == len(launchers)
            
        except Exception as e:
            self.errors.append(f"Launcher check failed: {e}")
            return False
    
    def generate_report(self) -> str:
        """Generate comprehensive verification report"""
        print("\n📊 Generating verification report...")
        
        total_checks = len(self.results)
        total_errors = len(self.errors)
        total_warnings = len(self.warnings)
        
        report = f"""
🔥 DEVDOLZ SYSTEM VERIFICATION REPORT 🔥
⚡ Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
🚀 Duration: {time.time() - self.start_time:.2f} seconds

📊 SUMMARY:
✅ Successful Checks: {total_checks}
❌ Errors: {total_errors}
⚠️ Warnings: {total_warnings}

🎯 RESULTS:
"""
        
        for key, value in self.results.items():
            report += f"   {key}: {value}\n"
        
        if self.errors:
            report += f"\n❌ ERRORS:\n"
            for error in self.errors:
                report += f"   • {error}\n"
        
        if self.warnings:
            report += f"\n⚠️ WARNINGS:\n"
            for warning in self.warnings:
                report += f"   • {warning}\n"
        
        # Overall status
        if total_errors == 0:
            status = "🟢 SYSTEM READY - All components working"
        elif total_errors <= 2:
            status = "🟡 SYSTEM PARTIALLY READY - Minor issues detected"
        else:
            status = "🔴 SYSTEM NOT READY - Critical issues detected"
        
        report += f"\n{status}\n"
        
        return report
    
    def run_full_verification(self) -> bool:
        """Run complete system verification"""
        self.print_banner()
        
        print("🚀 Starting comprehensive DevDollz system verification...\n")
        
        # Run all checks
        checks = [
            ("Python Environment", self.check_python_environment),
            ("DevDollz Installation", self.check_devdollz_installation),
            ("Ollama Availability", self.check_ollama_availability),
            ("System Integration", self.check_system_integration),
            ("Core Functionality", self.test_core_functionality),
            ("Launcher Scripts", self.check_launcher_scripts)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"\n{'='*50}")
            print(f"🔍 {check_name.upper()} CHECK")
            print(f"{'='*50}")
            
            try:
                if check_func():
                    print(f"✅ {check_name} - PASSED")
                else:
                    print(f"❌ {check_name} - FAILED")
                    all_passed = False
            except Exception as e:
                print(f"💥 {check_name} - ERROR: {e}")
                self.errors.append(f"{check_name} check error: {e}")
                all_passed = False
        
        # Generate and display report
        report = self.generate_report()
        print(report)
        
        return all_passed

def main():
    """Main verification function"""
    verifier = DevDollzVerifier()
    
    try:
        success = verifier.run_full_verification()
        
        if success:
            print("\n🎉 DEVDOLZ SYSTEM VERIFICATION COMPLETE!")
            print("🚀 All systems are ready for operation.")
            print("🔥 You can now use any of the launcher scripts:")
            print("   • python god_mode_launcher.py")
            print("   • python twin_launcher.py")
            print("   • python warp_bypass_launcher.py")
            print("   • python takeover_launcher.py")
        else:
            print("\n⚠️ VERIFICATION COMPLETE WITH ISSUES")
            print("🔧 Please address the errors above before proceeding.")
            print("💡 Check the warnings for optimization opportunities.")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Verification interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n💥 Fatal verification error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
