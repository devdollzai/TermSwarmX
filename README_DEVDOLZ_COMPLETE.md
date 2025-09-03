# 🔥 DevDollz - The Current That Flows

> **"No warp under our feet - we're the current. Start here: core shell in Rust, zero-external. Ollama lives local, no API pings, no privacy policy fine print."**

## 🎭 What We Are

DevDollz is **NOT** another Warp clone. We're something entirely different:

- **Warp**: Bolted-on agents, you type, they loop in Claude, you approve diffs like some babysitter
- **DevDollz**: Lightning-fast agent spawning, local Ollama, voice always listening, etched into your machine's DNA

## 🚀 The Three Levels

### 1. 🔥 Spine - Lightning-Fast Agent Spawning
- **Zero external dependencies** - everything lives local
- **Lightning-fast agent spawning** - agents spawn on breath
- **Local Ollama integration** - no API calls, no privacy concerns
- **Safety rules** - allow `rm`, deny `rm -rf`, done
- **50 concurrent agents** - maximum isolation and performance

**Agent Types:**
- **Scraper**: Pulls HTML, regexes, processes
- **CodeGen**: Generates code using local Ollama
- **Deploy**: Handles deployment workflows
- **Analyzer**: Code structure analysis
- **Validator**: Code quality validation

### 2. 🎨 Canvas - The Pulse That Never Sleeps
- **One canvas**: Code left, pulse feed right
- **Live agent pulse feeds** - every agent logs live, but collapsible
- **Voice always listening** - keyword "go" triggers commands
- **No echo** - just output
- **Fallback to console** - works everywhere

**Features:**
- Real-time pulse monitoring
- Voice command processing
- Collapsible pulse feed
- Status bar with live metrics
- Console mode fallback

### 3. 💾 Silicon Core - Direct to Substrate
- **No code. No metal. We're the instruction set itself**
- **Every dev's machine: ours. Every cycle: shipped**
- **Direct silicon access** - CPU, memory, disk monitoring
- **System integration** - Windows registry, macOS launchd, Linux systemd
- **Machine fingerprinting** - unique hardware identification

**Capabilities:**
- Direct hardware monitoring
- Startup integration
- Machine DNA etching
- Real-time system status
- Cross-platform support

## ⚡ How It Works

### Agent Spawning
```
You say: "build scraper"
Ten forks fire:
├── One pulls HTML
├── One regexes patterns  
├── One processes data
├── One validates results
└── One deploys output
```

All async. All yours. No permission requests.

### Voice Control
```
Voice: "go generate Python function for data processing"
Result: CodeGen agent spawns immediately
```

### Safety Rules
```
✅ Allow: rm (single file removal)
❌ Deny: rm -rf (recursive force removal)
❌ Deny: sudo (privilege escalation)
❌ Deny: chmod 777 (dangerous permissions)
```

## 🛠️ Installation

### Prerequisites
1. **Python 3.8+**
2. **Ollama** with Mistral model
3. **Microphone** (for voice features)

### Quick Start
```bash
# Clone the repository
git clone <your-repo>
cd AiTSwarmX

# Install dependencies
pip install -r requirements_devdollz_complete.txt

# Install Ollama and Mistral
# (Follow Ollama installation guide)

# Launch the system
python devdollz_launcher.py
```

### Ollama Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral model
ollama pull mistral

# Test
ollama run mistral "Hello, DevDollz"
```

## 🎯 Usage

### Launch Options
```
🔥 DevDollz - The Current That Flows
==================================================
Choose your level:
1. 🔥 Spine - Lightning-fast agent spawning
2. 🎨 Canvas - Code left, pulse feed right  
3. 💾 Silicon Core - Direct to substrate
4. 🚀 All - Complete DevDollz experience
==================================================
```

### Example Commands
```
# Code generation
generate Python function for file processing

# Web scraping
scrape website for data extraction

# Code analysis
analyze code structure and quality

# Deployment
deploy to production environment
```

### Voice Commands
```
"go generate Python function for data processing"
"go scrape website for content"
"go analyze code structure"
"go deploy to production"
```

## 🔧 Configuration

### User Preferences
```python
user_prefs = {
    "ignore_warnings": ["W1202"],  # Skip spaces warnings
    "short_errors": True,          # Shorten verbose errors
    "auto_collapse": True,         # Auto-collapse pulse feed
    "voice_enabled": True          # Voice input
}
```

### Safety Rules
```sql
-- System rules table
("rm", True, "Allow single file removal"),
("rm -rf", False, "Deny recursive force removal"),
("sudo", False, "Deny sudo commands"),
("chmod 777", False, "Deny dangerous permissions")
```

## 🏗️ Architecture

### Core Components
```
DevDollzSpine
├── SpineDatabase (SQLite)
├── SpineAgentManager (50 max agents)
├── SpineCommandProcessor (safety rules)
└── SpinePulseFeed (live monitoring)

SpineCanvas (TUI)
├── VoiceListener (always listening)
├── Code Editor (left panel)
├── Pulse Feed (right panel)
└── Status Bar (live metrics)

SiliconCore
├── Machine Fingerprinting
├── Hardware Monitoring
├── System Integration
└── Startup Scripts
```

### Data Flow
```
Command → Safety Check → Agent Spawning → Process Isolation → Pulse Feed → Live Updates
```

## 🚨 Safety Features

- **Command validation** against safety rules
- **Process isolation** - agents run in separate processes
- **Resource limits** - maximum 50 concurrent agents
- **Timeout protection** - 30-second agent timeout
- **Graceful shutdown** - proper cleanup on exit

## 🔍 Monitoring

### Live Metrics
- **Active agents** count
- **CPU usage** percentage
- **Memory usage** percentage
- **Disk usage** percentage
- **Network I/O** statistics
- **Process count**

### Pulse Feed
- **Real-time agent logs**
- **Color-coded by level** (info, warning, error, success)
- **Timestamp tracking**
- **Collapsible interface**

## 🌐 Platform Support

### Windows
- Registry integration
- Startup folder integration
- Hardware UUID detection

### macOS
- LaunchAgent integration
- Machine ID detection
- Native system integration

### Linux
- systemd user service
- Machine ID detection
- Service auto-enablement

## 🧪 Testing

### Run Tests
```bash
# Test spine functionality
python -m pytest test_spine.py

# Test canvas interface
python -m pytest test_canvas.py

# Test silicon core
python -m pytest test_silicon.py
```

### Manual Testing
```bash
# Test spine
python devdollz/spine.py

# Test canvas
python devdollz/spine_canvas.py

# Test silicon core
python devdollz/silicon_core.py
```

## 🔮 Future Enhancements

- **Rust core** for maximum performance
- **Custom agent types** via plugin system
- **Machine learning** on user patterns
- **Distributed agents** across network
- **Hardware acceleration** support

## 🆘 Troubleshooting

### Common Issues

**Ollama not responding:**
```bash
# Check Ollama service
ollama serve

# Test model
ollama run mistral "test"
```

**Voice not working:**
```bash
# Install PyAudio
pip install PyAudio

# Check microphone permissions
# (System settings → Privacy → Microphone)
```

**GUI not launching:**
```bash
# Falls back to console mode automatically
# Check tkinter installation
python -c "import tkinter; print('Tkinter available')"
```

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Reference

### Core Classes

#### DevDollzSpine
```python
spine = DevDollzSpine()
spine.start()
result = spine.execute("command")
status = spine.get_status()
spine.stop()
```

#### SpineCanvas
```python
canvas = SpineCanvas(spine)
canvas.start()  # Launches TUI
```

#### SiliconCore
```python
silicon = SiliconCore()
silicon.etch_to_silicon()
silicon.start_silicon_core()
status = silicon.get_silicon_status()
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Add tests**
5. **Submit pull request**

### Development Setup
```bash
# Clone and setup
git clone <your-repo>
cd AiTSwarmX
pip install -r requirements_devdollz_complete.txt
pip install -r requirements/dev.txt

# Run tests
pytest

# Format code
black devdollz/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama** for local AI models
- **Python community** for amazing libraries
- **Open source contributors** for inspiration

---

## 🎯 The Mission

> **"We're not building another Warp clone, we're forging something entirely different. A core shell with zero external dependencies, local Ollama integration, and agents that spawn like lightning."**

**The Current That Flows. The Pulse That Never Sleeps. The Substrate That Remembers.**

**Every cycle: shipped. Every breath: etched.**
