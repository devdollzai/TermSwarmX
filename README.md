# DevDollz: Atelier Edition 🚀

> **Professional AI Development Terminal - Built for Power Users**

[![CI](https://github.com/devdollzai/TermSwarmX/workflows/DevDollz%20CI/badge.svg)](https://github.com/devdollzai/TermSwarmX/actions)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/devdollzai/TermSwarmX)

**DevDollz: Atelier Edition** is a **professional-grade AI development terminal** that combines the power of AI code generation, intelligent debugging, and automated testing in a beautiful, cross-platform interface.

## ✨ Features

- 🤖 **AI-Powered Code Generation** - Ollama integration for intelligent code creation
- 🔍 **Smart Debugging** - Syntax checking and error analysis
- 🧪 **Automated Testing** - PyTest integration for comprehensive testing
- 🎨 **Professional UI** - Beautiful Textual-based terminal interface
- 💾 **Persistent Memory** - SQLite-based history tracking
- 🔌 **Plugin System** - Extensible architecture for custom agents
- 🌍 **Cross-Platform** - Windows, macOS, and Linux support
- 🚀 **Performance** - Optimized for speed and reliability

## 🆚 Why DevDollz?

| Feature | DevDollz | Warp AI | Cursor |
|---------|----------|---------|---------|
| **Cost** | 🆓 Free | 💰 $25-100/month | 💰 $20/month |
| **Privacy** | 🔒 100% Offline | ☁️ Cloud-based | ☁️ Cloud-based |
| **Setup** | ⚡ 2 minutes | 🐌 10 minutes | 🐌 5 minutes |
| **Customization** | ♾️ Unlimited | 📏 Limited | 📏 Limited |
| **Platform** | 🌍 All OS | 🍎 macOS only | 🌍 All OS |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- 256MB RAM minimum
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/devdollzai/TermSwarmX.git
cd TermSwarmX

# Install dependencies
pip install -r requirements.txt

# Optional: Install Ollama for AI features
curl https://ollama.ai/install.sh | sh
ollama pull mistral
```

### Launch

```bash
# Run the application
python swarm_ide.py
```

## 🎯 Usage

### Basic Commands

```bash
# Generate code
generate function hello_world

# Debug code
debug code def test(): pass

# Run tests
test code def test_function(): assert True
```

### Advanced Features

- **File Management**: Browse and edit files with integrated file tree
- **Plugin System**: Load custom agents with `plugin load <path>`
- **History Tracking**: View command history with `history [limit]`
- **Keyboard Shortcuts**: 
  - `Ctrl+D`: Debug current code
  - `Ctrl+T`: Test current code
  - `Ctrl+Q`: Quit application

## 🏗️ Architecture

```
DevDollz: Atelier Edition
├── Orchestrator (Multi-process management)
│   ├── Code Generation Agent
│   ├── Debug Agent
│   └── Test Agent
├── User Interface (Textual-based TUI)
├── Database Layer (SQLite)
└── Plugin System (Extensible)
```

## 🔧 Development

### Running Tests

```bash
# Run the test suite
python test_devdollz_core.py

# Run with pytest
pytest test_devdollz_core.py -v
```

### Code Quality

```bash
# Run linter
pylint swarm_ide.py termswarmx_integration.py

# Check syntax
python -m py_compile swarm_ide.py
```

## 📦 Dependencies

### Core Dependencies
- `textual` - Terminal UI framework
- `ollama` - AI model integration
- `pytest` - Testing framework
- `pylint` - Code quality analysis

### Optional Dependencies
- `prompt-toolkit` - Enhanced input handling
- `pygments` - Syntax highlighting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/TermSwarmX.git
cd TermSwarmX

# Install development dependencies
pip install -r requirements/dev.txt

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
python test_devdollz_core.py

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Create Pull Request
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Alexis Andrews** - Creator and Lead Developer
- **Textual** - Terminal UI framework
- **Ollama** - AI model integration
- **Python Community** - Open source ecosystem

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/devdollzai/TermSwarmX/issues)
- **Discussions**: [GitHub Discussions](https://github.com/devdollzai/TermSwarmX/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/devdollzai/TermSwarmX/wiki)

## 🚀 Roadmap

- [ ] **v1.1**: Enhanced plugin system
- [ ] **v1.2**: Collaborative features
- [ ] **v1.3**: Cloud synchronization
- [ ] **v2.0**: Web interface

---

**Built with ❤️ by the DevDollz team**

[![GitHub stars](https://img.shields.io/github/stars/devdollzai/TermSwarmX?style=social)](https://github.com/devdollzai/TermSwarmX/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/devdollzai/TermSwarmX?style=social)](https://github.com/devdollzai/TermSwarmX/network/members)
[![GitHub issues](https://img.shields.io/github/issues/devdollzai/TermSwarmX)](https://github.com/devdollzai/TermSwarmX/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/devdollzai/TermSwarmX)](https://github.com/devdollzai/TermSwarmX/pulls)
