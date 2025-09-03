# DevDollz: Atelier Edition 🎭✨

> **Where Code Meets Couture - Built by Alexis Adams for the Hacker Elite**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)](https://github.com/devdollzai/ai-swarm-ide)
[![Creator](https://img.shields.io/badge/Creator-Alexis%20Adams-pink.svg)](https://github.com/devdollzai)

## 🎨 **The Vision**

DevDollz: Atelier Edition represents the evolution of development tools - combining artificial intelligence, sophisticated design, and professional-grade functionality in a package that's both beautiful and powerful. It's not just a tool; it's a statement about what development environments can and should be.

**"Where Code Meets Couture - Professionally."**

## ✨ **Key Features**

### 🧠 **AI-Powered Development**
- **Local AI Models**: Uses Ollama with models like Mistral for code generation
- **Async Operations**: True asynchronous processing for speed
- **Intelligent Agents**: Specialized AI agents for different tasks

### 🔍 **Advanced Code Analysis**
- **Pylint Integration**: Automated code quality validation
- **Static Analysis**: Comprehensive code review and optimization
- **Performance Metrics**: Code scoring and improvement suggestions

### 🖥️ **Professional Terminal Interface**
- **Textual TUI**: Modern, responsive terminal user interface
- **File Management**: Integrated file tree and code editor
- **Command History**: Persistent storage of all operations
- **Plugin System**: Extensible architecture for custom tools

### 🎤 **Voice Integration**
- **Speech Recognition**: Voice command capabilities
- **Biofeedback Simulation**: Revolutionary "breath-to-code" interface
- **Natural Language**: Speak your intentions, get working code

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+
- Ollama (for AI models)
- Git

### **Installation**

```bash
# Clone the repository
git clone https://github.com/devdollzai/ai-swarm-ide.git
cd ai-swarm-ide

# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Pull a model
ollama pull mistral
```

### **Usage**

```bash
# Run the main IDE
python swarm_ide.py

# Or use the CLI version
python devdollz_cli.py

# Launch the Whisper System
python whisper_core.py
```

## 🎯 **Command Protocol**

### **Code Generation**
```bash
generate function calculate_sum
generate class DataProcessor
generate code web_scraper
```

### **Code Debugging**
```bash
debug syntax def my_func(x: pass
debug logic complex_algorithm
debug code <your_code_here>
```

### **System Commands**
```bash
help          # Show command help
status        # System status
history       # Command history
clear         # Clear log
```

## 🎨 **Design Philosophy**

### **Atelier Edition Aesthetic**
- **Color Palette**: "Onyx & Orchid" - Deep black with rich purple accents
- **Typography**: Elegant, readable fonts with consistent spacing
- **Icons**: Minimalist, professional symbols
- **Layout**: Clean, uncluttered user experience

### **Cyber Glam Theme**
- **Primary**: Hot Pink (#FF69B4)
- **Secondary**: Electric Purple (#8A2BE2)
- **Accent**: Neon Green (#39FF14)
- **Background**: Dark Slate (#2F4F4F)

## 🏗️ **Architecture**

### **Core Components**
- **`swarm_ide.py`**: Main application with TUI interface
- **`whisper_core.py`**: Advanced voice/biofeedback system
- **`devdollz/`**: Core package with themes and utilities
- **`sample_plugin.py`**: Example plugin system

### **Technology Stack**
- **Python**: Core language and runtime
- **Textual**: Modern TUI framework
- **Ollama**: Local AI model integration
- **Pylint**: Code quality analysis
- **SQLite**: Persistent data storage
- **SpeechRecognition**: Voice input processing

## 🔌 **Plugin System**

DevDollz features a powerful plugin architecture that allows you to extend functionality:

```python
# Example plugin
def plugin_agent(code: str, task: str) -> str:
    """Custom analysis plugin"""
    if task == "analyze":
        return f"Analysis of {len(code)} characters"
    return "Task not supported"

# Load plugin
plugin load my_plugin.py
my_plugin analyze <code>
```

## 🆚 **Competitive Advantages**

### **vs. Warp AI**
- **Cost**: Free vs. $25-$100/month subscription
- **Privacy**: Local operation vs. cloud dependency
- **Speed**: Async local processing vs. network delays
- **Customization**: Plugin system vs. closed ecosystem

### **vs. Traditional IDEs**
- **AI Integration**: Built-in AI assistance
- **Voice Commands**: Natural language coding
- **Terminal-First**: Developer workflow optimized
- **Extensibility**: Custom plugin support

## 📊 **Performance**

- **Response Time**: <1 second for AI operations
- **Memory Usage**: Low footprint (256MB+)
- **Platform Support**: Windows, macOS, Linux
- **Offline Capability**: Full functionality without internet

## 🛠️ **Development**

### **Contributing**
We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Building from Source**
```bash
git clone https://github.com/devdollzai/ai-swarm-ide.git
cd ai-swarm-ide
pip install -e .
```

### **Testing**
```bash
# Run tests
python -m pytest tests/

# Run specific test
python test_axiom.py
```

## 📚 **Documentation**

- [Installation Guide](docs/INSTALLATION.md)
- [User Manual](docs/USER_MANUAL.md)
- [Plugin Development](docs/PLUGIN_DEVELOPMENT.md)
- [API Reference](docs/API_REFERENCE.md)

## 🌟 **Creator Spotlight**

**Alexis Adams** - Creator & Hacker

> *"I built this because I was tired of slow, boring AI tools. Real hackers need speed, style, and substance. DevDollz delivers all three."*

- **GitHub**: [@devdollzai](https://github.com/devdollzai)
- **Twitter**: [@DevDollzAI](https://twitter.com/DevDollzAI)
- **Discord**: [DevDollz Community](https://discord.gg/devdollz)

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Textual**: For the amazing TUI framework
- **Ollama**: For local AI model support
- **Pylint**: For code quality analysis
- **Python Community**: For the incredible ecosystem

## 🚀 **Roadmap**

- [ ] **v1.0**: Production-ready release
- [ ] **v1.1**: Advanced AI models integration
- [ ] **v1.2**: Team collaboration features
- [ ] **v2.0**: Enterprise deployment options

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/devdollzai/ai-swarm-ide/issues)
- **Discussions**: [GitHub Discussions](https://github.com/devdollzai/ai-swarm-ide/discussions)
- **Discord**: [Community Server](https://discord.gg/devdollz)
- **Email**: [alexis@devdollz.dev](mailto:alexis@devdollz.dev)

---

**DevDollz: Atelier Edition** - Where Code Meets Couture, Built for Power Users by Power Users.

**Ready to hack with style?** 🚀✨
