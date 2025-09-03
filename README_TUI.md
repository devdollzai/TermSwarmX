# 🚀 AI Swarm IDE - Textual TUI Interface

**Professional split-panel interface with file tree, code editor, and results pane**

The AI Swarm IDE now features a modern Textual-based TUI (Terminal User Interface) that provides a professional development environment right in your terminal. This interface combines the power of our AI swarm architecture with an intuitive, keyboard-driven interface.

## ✨ **Features**

### **🎯 Split-Panel Interface**
- **Left Panel**: File tree navigation with project structure
- **Center Panel**: Code editor area (placeholder for future enhancements)
- **Right Panel**: Results pane showing agent outputs and status
- **Bottom Panel**: Command input with autocomplete

### **🤖 AI-Powered Development**
- **Code Generation**: Generate functions, classes, and code snippets
- **Debug Analysis**: Syntax, logic, and general code debugging
- **Multi-Agent Architecture**: Leverages our proven swarm system
- **Ollama Integration**: Local AI model support for code generation

### **⌨️ Keyboard-Driven Interface**
- **Tab Navigation**: Cycle between panels
- **Quick Commands**: `?` for help, `Ctrl+C` to quit
- **File Selection**: Navigate and select files in the tree
- **Command History**: SQLite-based logging of all operations

## 🚀 **Quick Start**

### **1. Installation**
```bash
# Run the installation script
python install.py

# Or install manually
pip install textual>=0.40.0 ollama>=0.1.0
```

### **2. Launch the TUI**
```bash
python swarm_ide.py
```

### **3. Basic Usage**
```
# Generate code
generate function calculate_fibonacci
generate class UserManager
generate code web_scraper

# Debug code
debug syntax def foo(: pass
debug logic if x > 0: return x
debug code print("hello world")

# Navigation
Tab          - Cycle between panels
Shift+Tab   - Reverse cycle
?           - Show help
Ctrl+C      - Quit
```

## 🏗️ **Architecture**

### **Enhanced Orchestrator**
- **Swarm Integration**: Uses our existing `SwarmOrchestrator`
- **Agent Management**: `EnhancedCodeAgent` and `EnhancedDebugAgent`
- **Fallback Support**: Ollama integration when agents are unavailable
- **Database Logging**: SQLite-based command history

### **TUI Components**
```python
class SwarmIDEApp(App):
    # File tree (left)
    DirectoryTree("./", id="file-tree")
    
    # Main content area (center + right)
    Vertical(
        Container("Code Editor", id="code-editor"),
        Container(TextLog(), id="results-pane")
    )
    
    # Command input (bottom)
    Input(placeholder="> Enter command...", id="command-input")
```

### **Command Processing**
1. **Input Parsing**: Parse commands like `generate function <description>`
2. **Task Routing**: Route to appropriate agent (code_gen or debug)
3. **Agent Execution**: Use swarm agents or Ollama fallback
4. **Result Display**: Show output in results pane with status indicators

## 🔧 **Configuration**

### **Dependencies**
```txt
textual>=0.40.0      # TUI framework
ollama>=0.1.0        # AI model integration
typer[all]>=0.9.0    # CLI framework
rich>=13.0.0         # Terminal formatting
pydantic>=2.0.0      # Data validation
```

### **Environment Setup**
```bash
# Install Ollama (optional, for AI features)
curl https://ollama.ai/install.sh | sh
ollama pull mistral
ollama serve

# Or use the swarm agents (default)
python main.py init myproject
```

## 📱 **Interface Layout**

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Swarm IDE                            │
├─────────────┬─────────────────────┬───────────────────────┤
│ File Tree   │   Code Editor      │    Results Pane       │
│ (25%)       │   (40%)            │    (35%)              │
│             │                     │                       │
│ ./          │ [Editor Area]      │ [SUCCESS] Generated...│
│ ├── src/    │                     │ [INFO] File selected  │
│ ├── tests/  │                     │ [PROCESSING] Task...  │
│ └── docs/   │                     │                       │
├─────────────────────────────────────────────────────────────┤
│ > Enter command (e.g., generate function ...)             │
└─────────────────────────────────────────────────────────────┘
```

## 🎮 **Key Bindings**

| Key | Action | Description |
|-----|--------|-------------|
| `Tab` | Next Panel | Cycle focus between panels |
| `Shift+Tab` | Previous Panel | Reverse cycle |
| `?` | Show Help | Display usage information |
| `Ctrl+C` | Quit | Exit the application |
| `Enter` | Submit Command | Execute command from input |

## 🔍 **Command Reference**

### **Code Generation**
```bash
generate function <description>    # Generate a function
generate class <description>       # Generate a class
generate code <description>        # Generate general code
```

### **Debug Analysis**
```bash
debug syntax <code>                # Syntax error analysis
debug logic <code>                 # Logical error analysis
debug code <code>                  # General debugging
```

### **Navigation**
```bash
help                              # Show help
quit/exit                         # Exit application
```

## 🚀 **Advanced Features**

### **File Tree Integration**
- **File Selection**: Click files to view information
- **Python Detection**: Automatic suggestions for Python files
- **Project Structure**: Navigate complex project hierarchies

### **Database Logging**
- **Command History**: All commands logged to SQLite
- **Result Tracking**: Success/failure status tracking
- **Performance Metrics**: Execution time and agent usage

### **Fallback Systems**
- **Swarm Agents**: Primary execution via our agent system
- **Ollama Integration**: Local AI model fallback
- **Simulated Responses**: Basic functionality without AI

## 🔧 **Development & Customization**

### **Adding New Commands**
```python
# In SwarmIDEApp.process_command()
if action == "custom":
    result = await self.handle_custom_command(cmd_type, task_content)
```

### **Customizing the Interface**
```python
# Modify CSS for styling
CSS = """
DirectoryTree { 
    width: 30%; 
    border: solid green;
}
"""
```

### **Extending Agents**
```python
class CustomAgent:
    async def process_task(self, task_type: str, content: str) -> str:
        # Custom task processing logic
        pass
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Textual Not Available**
```bash
# Install Textual
pip install textual>=0.40.0

# Or use CLI fallback
python main.py
```

#### **Ollama Connection Issues**
```bash
# Check Ollama service
ollama serve

# Test connection
python -c "import ollama; print(ollama.list())"
```

#### **Import Errors**
```bash
# Ensure src directory is in path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or run from project root
cd /path/to/ai-swarm-ide
python swarm_ide.py
```

### **Performance Issues**
- **Memory Usage**: Monitor with `htop` or `top`
- **Response Time**: Check agent health status
- **Database Size**: Monitor `swarm_memory.db` growth

## 🚀 **Future Enhancements**

### **Planned Features**
- **Multi-line Code Editor**: True code editing capabilities
- **File Content Display**: View and edit file contents
- **Plugin System**: Extensible agent architecture
- **Voice Commands**: Speech-to-text integration
- **Git Integration**: Version control operations

### **UI Improvements**
- **Syntax Highlighting**: Code-aware coloring
- **Auto-completion**: Intelligent command suggestions
- **Split Views**: Multiple file editing
- **Search & Replace**: Find and modify text

## 🤝 **Contributing**

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd ai-swarm-ide

# Install development dependencies
pip install -e .

# Run tests
python -m pytest tests/

# Launch TUI
python swarm_ide.py
```

### **Code Style**
- **Type Hints**: Use Python type annotations
- **Async/Await**: Leverage asyncio for I/O operations
- **Error Handling**: Comprehensive exception management
- **Documentation**: Clear docstrings and comments

## 📚 **Additional Resources**

### **Documentation**
- [Textual Framework](https://textual.textualize.io/)
- [Ollama Documentation](https://ollama.ai/docs)
- [AI Swarm IDE Core](README.md)

### **Examples**
- [Basic Usage](demo.py)
- [CLI Interface](main.py)
- [Agent System](src/agents/)

### **Support**
- **Issues**: Report bugs and feature requests
- **Discussions**: Community support and ideas
- **Wiki**: Detailed usage guides and tutorials

---

## 🎉 **Ready to Transform Your Development Experience?**

The AI Swarm IDE TUI combines the power of autonomous AI agents with a professional, keyboard-driven interface. Whether you're generating code, debugging issues, or exploring project structures, the TUI provides an intuitive and efficient development environment.

**Start building with AI-powered development today!** 🚀
