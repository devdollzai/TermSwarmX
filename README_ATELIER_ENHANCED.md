# DevDollz: Atelier Edition ✨ Enhanced

**Where Code Meets Couture** - A sophisticated, minimalist, and luxurious development experience with advanced AI capabilities.

```
██████╗ ██╗██╗   ██╗██╗  ██╗ ██████╗ ██╗     ██╗     ███████╗
██╔══██╗██║██║   ██║██║  ██║██╔═══██╗██║     ██║     ╚══███╔╝
██║  ██║██║██║   ██║██║  ██║██║   ██║██║     ██║       ███╔╝ 
██║  ██║██║██║   ██║██║  ██║██║   ██║██║     ██║      ███╔╝  
██████╔╝██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗███████╗
╚═════╝ ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝
```

## 🎭 About DevDollz: Atelier Edition Enhanced

**DevDollz: Atelier Edition Enhanced** represents the pinnacle of the DevDollz brand - a high-profile, elite development environment that combines sophisticated minimalism with cutting-edge AI capabilities. Designed and signed by **Alexis Adams**, this system embodies the perfect fusion of "couture tech" aesthetics and professional-grade development tools.

The Enhanced Edition introduces revolutionary features that elevate the development experience to unprecedented levels of sophistication and productivity.

### ✨ Key Features

- **🎨 Onyx & Orchid Theme**: A sophisticated dark theme with deep blacks and a single, powerful Orchid purple accent
- **🧠 AI-Powered Code Generation**: Generate elegant, production-ready Python code with intelligent AI
- **🔍 Advanced Debugging**: Comprehensive code analysis and improvement suggestions
- **💫 Minimalist TUI Interface**: Clean, modern Textual-based terminal user interface
- **🔄 Multi-Agent Swarm**: Coordinated AI agents working together seamlessly
- **📚 Persistent Memory**: SQLite-based task history and system tracking
- **🎯 Professional Quality**: Built-in error handling, type hints, and documentation
- **🎤 Voice Recognition**: Natural voice commands for hands-free development
- **🔌 Plugin System**: Extensible architecture with custom agent support
- **📝 Multi-Line Code Editor**: Full-featured code editing with syntax highlighting
- **🛡️ Security Analysis**: Built-in vulnerability scanning and security recommendations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AiTSwarmX

# Install core dependencies
pip install textual prompt_toolkit pygments ollama

# Install voice recognition dependencies (optional)
pip install SpeechRecognition PyAudio

# Install Ollama (if not already installed)
curl https://ollama.ai/install.sh | sh
ollama pull mistral

# Start Ollama server
ollama serve

# Run DevDollz: Atelier Edition Enhanced
python swarm_ide_enhanced.py
```

### Basic Usage

```bash
# Start the Enhanced TUI (recommended)
python swarm_ide_enhanced.py

# The system will automatically fall back to CLI if Textual is unavailable
```

## 🎨 The Enhanced Atelier Experience

### Command Protocol

DevDollz: Atelier Edition Enhanced uses an intuitive command system that feels natural and powerful:

```bash
# Code Generation
generate function calculate_fibonacci_sequence
generate class DataProcessor
generate code web_scraper_with_requests

# Code Debugging
debug syntax def invalid_function(: pass
debug logic complex_algorithm
debug code user_input_validation

# Advanced Analysis (via plugins)
sample_plugin complexity <code>
sample_plugin performance <code>
sample_plugin security <code>
sample_plugin style <code>

# System Commands
history [limit]
plugin load <path>
help
quit/exit
```

### Voice Commands

Experience hands-free development with natural voice commands:

- **"Create function calculate sum"** → Generates a function
- **"Debug syntax my code"** → Analyzes syntax
- **"Check performance algorithm"** → Performance analysis
- **"Load plugin sample_plugin"** → Loads a custom plugin

**Keyboard Shortcut**: `Ctrl+V` to activate voice recognition

### Special Commands

- `help` - Show Atelier Protocol
- `history [limit]` - View command history
- `plugin load <path>` - Load custom plugins
- `quit/exit` - Exit DevDollz
- `?` - Quick help (keyboard shortcut)

## 🎭 Theme System

### Onyx & Orchid Color Palette

The signature Atelier aesthetic features:

- **Background**: Deep Onyx black (`#1A1A1B`) - A soft, deep black for the main interface
- **Primary**: Sophisticated Orchid purple (`#D944D4`) - The signature accent color
- **Panel**: Charcoal grey (`#2C2C2E`) - Subtle depth for panels and borders
- **Success**: Orchid accent (`#D944D4`) - Reinforces the brand's core color
- **Error**: Muted Rose Red (`#E06C75`) - Clear but not jarring
- **Text**: Soft off-white (`#EAEAEB`) - Highly legible for primary content
- **Muted**: Light cool grey (`#8A8A8E`) - Subtle secondary information

### Icon System

Every interaction is enhanced with elegant, minimalist symbols:

- ◆ Success operations (diamond, signifying quality)
- x Error messages (simple, clean)
- » Information and loading states (sharp forward guillemet)
- 📁 File tree folders (maintained for clarity)
- 📄 File tree files (maintained for clarity)

## 🔌 Plugin System

### Architecture

The Enhanced Edition features a sophisticated plugin architecture that allows developers to extend the system with custom AI agents:

```python
# Example plugin structure
def plugin_agent(input_queue, output_queue):
    """Custom plugin agent implementation"""
    while True:
        # Process tasks from input queue
        # Send results to output queue
        pass
```

### Loading Plugins

```bash
# Load a plugin from the project directory
plugin load sample_plugin.py

# Use the plugin's custom commands
sample_plugin complexity <code>
sample_plugin performance <code>
```

### Sample Plugin

The Enhanced Edition includes a comprehensive sample plugin (`sample_plugin.py`) that demonstrates:

- **Code Complexity Analysis**: Cyclomatic complexity scoring and recommendations
- **Performance Analysis**: Performance issue detection and optimization suggestions
- **Security Analysis**: Vulnerability scanning and security recommendations
- **Style Analysis**: PEP 8 compliance checking and style recommendations

## 🎤 Voice Recognition

### Features

- **Natural Language Processing**: Understands spoken development commands
- **Command Normalization**: Automatically converts natural speech to system commands
- **Ambient Noise Reduction**: Optimized for development environments
- **Timeout Handling**: Graceful fallback for audio issues

### Supported Voice Commands

- **Code Generation**: "Create function", "Generate class", "Make code for..."
- **Debugging**: "Check syntax", "Debug logic", "Analyze code"
- **System Commands**: "Show help", "Display history", "Load plugin"

## 📝 Code Editor

### Features

- **Multi-Line Editing**: Full-featured code editing capabilities
- **Syntax Highlighting**: Python syntax highlighting with the Orchid theme
- **File Integration**: Load and edit files directly from the file tree
- **Save Functionality**: `Ctrl+S` to save edited files
- **Debug Integration**: `Ctrl+D` to debug code from the editor

### File Operations

- **Load Files**: Click on files in the directory tree to load them
- **Edit Code**: Modify code directly in the integrated editor
- **Save Changes**: Use `Ctrl+S` or the save action to persist changes
- **Security**: Files can only be accessed within the project directory

## 🏗️ Architecture

### Core Components

1. **Enhanced Orchestrator**: Central task management with plugin support
2. **AI Agents**: Specialized code generation and debugging agents
3. **Voice Recognition Agent**: Natural language command processing
4. **Plugin Manager**: Dynamic plugin loading and management
5. **Code Editor**: Multi-line code editing with syntax highlighting
6. **SQLite Database**: Persistent storage for task history and results
7. **Textual TUI**: Beautiful, modern terminal user interface

### Agent Types

- **CodeGen Agent**: Generates elegant, production-ready Python code
- **Debug Agent**: Analyzes code for syntax, logic, and quality issues
- **Voice Agent**: Processes natural language commands
- **Plugin Agents**: Custom agents loaded dynamically

## 🎯 Use Cases

### For Elite Developers

- **Rapid Prototyping**: Generate boilerplate code instantly with voice commands
- **Code Review**: Automated analysis and improvement suggestions
- **Learning**: Understand best practices through AI-generated examples
- **Debugging**: Identify and fix issues quickly and elegantly
- **Security**: Built-in vulnerability scanning and security recommendations

### For Professional Teams

- **Consistency**: Standardized code generation across projects
- **Documentation**: AI-generated code with comprehensive docstrings
- **Quality**: Built-in error handling, type hints, and documentation
- **Collaboration**: Shared task history and system status
- **Extensibility**: Custom plugins for team-specific workflows

### For Development Environments

- **Voice-Controlled Development**: Hands-free coding for accessibility
- **Plugin Ecosystem**: Extensible architecture for custom workflows
- **Integrated Editing**: Full-featured code editor within the TUI
- **Security-First**: Built-in security analysis and recommendations

## 🛠️ Development

### Project Structure

```
swarm_ide_enhanced.py    # Enhanced Atelier Edition application
sample_plugin.py         # Sample plugin demonstrating the system
atelier_memory.db        # SQLite database for persistent storage
requirements_atelier.txt # Dependencies for the Enhanced Edition
README_ATELIER_ENHANCED.md # This comprehensive documentation
```

### Dependencies

- **textual**: Modern TUI framework for the beautiful interface
- **ollama**: Local AI capabilities for code generation and debugging
- **prompt_toolkit**: CLI fallback interface with advanced features
- **pygments**: Syntax highlighting for code display
- **SpeechRecognition**: Voice recognition capabilities
- **PyAudio**: Audio processing for voice commands

### Building Plugins

```python
# Plugin template
def plugin_agent(input_queue, output_queue):
    """Your custom plugin agent"""
    while True:
        try:
            raw_task = input_queue.get(timeout=1)
            if raw_task == "STOP":
                break
            
            # Process your custom logic here
            result = your_custom_function(raw_task)
            
            # Send result back
            meta = {"status": "success", "timestamp": time.time()}
            output_queue.put(create_message(result, meta))
            
        except Exception as e:
            meta = {"status": "error", "error": str(e)}
            output_queue.put(create_message(f"Plugin error: {e}", meta))
```

## 🌟 Creator Spotlight

**Alexis Adams** - The brilliant mind behind DevDollz, combining technical excellence with artistic vision to create a development experience that's both powerful and beautiful. The Enhanced Atelier Edition represents the pinnacle of this vision, offering unprecedented sophistication and functionality.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: This README and inline code documentation
- **Issues**: Report bugs and request features via GitHub Issues
- **Community**: Join our Discord/community channels
- **Email**: alexis@devdollz.dev

## 🎉 Acknowledgments

- **Textual**: For the beautiful TUI framework that enables the Atelier aesthetic
- **Ollama**: For powerful local AI capabilities
- **Python Community**: For the amazing ecosystem
- **Open Source Contributors**: For making this possible

## 🚀 Getting Started with the Enhanced Atelier

1. **Install Dependencies**: Ensure you have Python 3.9+ and the required packages
2. **Setup Ollama**: Install and start the Ollama server with the Mistral model
3. **Optional Voice Setup**: Install SpeechRecognition and PyAudio for voice commands
4. **Launch**: Run `python swarm_ide_enhanced.py` to experience the Enhanced Atelier
5. **Explore**: Navigate the file tree, use voice commands, load plugins, and edit code
6. **Extend**: Create custom plugins to enhance your development workflow

## 🎨 Design Philosophy

The Enhanced Atelier Edition embodies the principle that **sophistication enhances productivity**. By combining minimalist design with advanced AI capabilities, the interface becomes both beautiful and incredibly powerful. The single Orchid accent color creates a cohesive, sophisticated aesthetic that reflects the quality of the underlying technology.

Every design decision serves both form and function, creating an environment where developers can focus on their craft without distraction while leveraging cutting-edge AI capabilities.

## 🔮 Future Enhancements

The Enhanced Atelier Edition is designed for extensibility and future growth:

- **Multi-Language Support**: Extend beyond Python to other programming languages
- **Cloud Integration**: Connect to cloud-based AI services for enhanced capabilities
- **Collaborative Features**: Real-time collaboration and code sharing
- **Advanced Analytics**: Code quality metrics and performance profiling
- **Custom Themes**: User-configurable color schemes and layouts

---

**DevDollz: Atelier Edition Enhanced | By Alexis Adams ✨**

*Where Code Meets Couture - With Unprecedented Sophistication.*
