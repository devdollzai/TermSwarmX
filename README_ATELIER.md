# DevDollz: Atelier Edition ✨

**Where Code Meets Couture** - A sophisticated, minimalist, and luxurious development experience.

```
██████╗ ██╗██╗   ██╗██╗  ██╗ ██████╗ ██╗     ██╗     ███████╗
██╔══██╗██║██║   ██║██║  ██║██╔═══██╗██║     ██║     ╚══███╔╝
██║  ██║██║██║   ██║██║  ██║██║   ██║██║     ██║       ███╔╝ 
██║  ██║██║██║   ██║██║  ██║██║   ██║██║     ██║      ███╔╝  
██████╔╝██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗███████╗
╚═════╝ ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝
```

## 🎭 About DevDollz: Atelier Edition

**DevDollz: Atelier Edition** represents the evolution of the DevDollz brand into a high-profile, elite development environment. Designed and signed by **Alexis Adams**, this system embodies the perfect fusion of sophisticated minimalism and professional-grade development tools.

The Atelier Edition elevates the aesthetic from vibrant "girly hacker" to a refined "couture tech" experience - sharp, exclusive, and impeccably polished.

### ✨ Key Features

- **🎨 Onyx & Orchid Theme**: A sophisticated dark theme with deep blacks and a single, powerful floral accent
- **🧠 AI-Powered Code Generation**: Generate elegant, production-ready Python code with intelligent AI
- **🔍 Advanced Debugging**: Comprehensive code analysis and improvement suggestions
- **💫 Minimalist TUI Interface**: Clean, modern Textual-based terminal user interface
- **🔄 Multi-Agent Swarm**: Coordinated AI agents working together seamlessly
- **📚 Persistent Memory**: SQLite-based task history and system tracking
- **🎯 Professional Quality**: Built-in error handling, type hints, and documentation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AiTSwarmX

# Install dependencies
pip install textual prompt_toolkit pygments ollama

# Install Ollama (if not already installed)
curl https://ollama.ai/install.sh | sh
ollama pull mistral

# Start Ollama server
ollama serve

# Run DevDollz: Atelier Edition
python swarm_ide.py
```

### Basic Usage

```bash
# Start the TUI (recommended)
python swarm_ide.py

# The system will automatically fall back to CLI if Textual is unavailable
```

## 🎨 The Atelier Experience

### Command Protocol

DevDollz: Atelier Edition uses an intuitive command system that feels natural and powerful:

```bash
# Code Generation
generate function calculate_fibonacci_sequence
generate class DataProcessor
generate code web_scraper_with_requests

# Code Debugging
debug syntax def invalid_function(: pass
debug logic complex_algorithm
debug code user_input_validation
```

### Special Commands

- `help` - Show Atelier Protocol
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
- **Muted**: Light cool grey (`#8A8A8E`) - Subtle for secondary information

### Icon System

Every interaction is enhanced with elegant, minimalist symbols:

- ◆ Success operations (diamond, signifying quality)
- x Error messages (simple, clean)
- » Information and loading states (sharp forward guillemet)
- 📁 File tree folders (maintained for clarity)
- 📄 File tree files (maintained for clarity)

## 🏗️ Architecture

### Core Components

1. **Orchestrator**: Central task management and agent coordination
2. **Code Generation Agent**: Generates elegant, production-ready Python code
3. **Debug Agent**: Analyzes code for syntax, logic, and quality issues
4. **SQLite Database**: Persistent storage for task history and results
5. **Textual TUI**: Beautiful, modern terminal user interface

### Agent Types

- **CodeGen Agent**: Generates elegant, production-ready Python code with comprehensive error handling and type hints
- **Debug Agent**: Analyzes code for syntax, logic, and quality issues with professional precision

## 🎯 Use Cases

### For Elite Developers

- **Rapid Prototyping**: Generate boilerplate code instantly with Atelier precision
- **Code Review**: Automated analysis and improvement suggestions
- **Learning**: Understand best practices through AI-generated examples
- **Debugging**: Identify and fix issues quickly and elegantly

### For Professional Teams

- **Consistency**: Standardized code generation across projects
- **Documentation**: AI-generated code with comprehensive docstrings
- **Quality**: Built-in error handling and type hints
- **Collaboration**: Shared task history and system status

## 🛠️ Development

### Project Structure

```
swarm_ide.py          # Main DevDollz: Atelier Edition application
swarm_memory.db       # SQLite database for persistent storage
requirements.txt      # Python dependencies
```

### Dependencies

- **textual**: Modern TUI framework for the beautiful interface
- **ollama**: Local AI capabilities for code generation and debugging
- **prompt_toolkit**: CLI fallback interface
- **pygments**: Syntax highlighting for code display

## 🌟 Creator Spotlight

**Alexis Adams** - The brilliant mind behind DevDollz, combining technical excellence with artistic vision to create a development experience that's both powerful and beautiful. The Atelier Edition represents the pinnacle of this vision.

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

## 🚀 Getting Started with the Atelier

1. **Install Dependencies**: Ensure you have Python 3.9+ and the required packages
2. **Setup Ollama**: Install and start the Ollama server with the Mistral model
3. **Launch**: Run `python swarm_ide.py` to experience the Atelier
4. **Interact**: Use the intuitive command system to generate code and debug issues
5. **Explore**: Navigate the file tree, view results, and experience the sophisticated interface

## 🎨 Design Philosophy

The Atelier Edition embodies the principle that **less is more**. By reducing visual clutter and focusing on essential elements, the interface becomes more powerful and elegant. The single Orchid accent color creates a cohesive, sophisticated aesthetic that reflects the quality of the underlying AI technology.

Every design decision serves both form and function, creating an environment where developers can focus on their craft without distraction.

---

**DevDollz: Atelier Edition | By Alexis Adams ✨**

*Where Code Meets Couture - Elegantly.*
