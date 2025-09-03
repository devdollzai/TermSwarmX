"""
DevDollz UI System
Beautiful, elegant interfaces that embody the DevDollz aesthetic
"""

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree, Log, Input, Header, Footer, Static, Button, TextArea
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import reactive
from textual.binding import Binding
from textual import events
# from prompt_toolkit.completion import WordCompleter  # Not needed for Textual TUI
import time
from typing import Optional, List

from . import (
    DEV_DOLLZ_LOGO, CREATOR_TAGLINE, THEME_ICONS, 
    CYBER_GLAM_COLORS, get_devdollz_core
)

class DevDollzHeader(Header):
    """Custom DevDollz header with branding"""
    
    def compose(self) -> ComposeResult:
        yield Static(DEV_DOLLZ_LOGO, id="logo")
        yield Static("AI Swarm IDE", id="subtitle")

class DevDollzFooter(Footer):
    """Custom DevDollz footer with creator tagline"""
    
    def compose(self) -> ComposeResult:
        yield Static(CREATOR_TAGLINE, id="creator-tagline")
        yield Static("Press ? for help | Ctrl+C to exit", id="help-text")

class DevDollzCodeEditor(TextArea):
    """Multi-line code editor with DevDollz styling and command execution"""
    
    def __init__(self, **kwargs):
        super().__init__(
            placeholder="💖 Enter DevDollz commands or edit code here...\n\nExamples:\ngenerate function calculate_sum\ndebug syntax def foo(: pass\n\nPress Ctrl+Enter to execute commands\nPress Ctrl+S to save code",
            **kwargs
        )
        # Textual has built-in completion, no need for WordCompleter
        self.command_suggestions = [
            'generate function ', 'generate class ', 'generate code ',
            'debug syntax ', 'debug logic ', 'debug code ',
            'help', 'status', 'history', 'clear'
        ]
        self.command_mode = True  # Toggle between command and edit mode
        self.current_file = None  # Track current file being edited

class DevDollzResultsLog(Log):
    """Enhanced results log with DevDollz formatting"""
    
    def write_success(self, message: str):
        """Write a success message with DevDollz styling"""
        self.write(f"{THEME_ICONS['success']} {message}")
    
    def write_error(self, message: str):
        """Write an error message with DevDollz styling"""
        self.write(f"{THEME_ICONS['error']} {message}")
    
    def write_info(self, message: str):
        """Write an info message with DevDollz styling"""
        self.write(f"{THEME_ICONS['info']} {message}")
    
    def write_warning(self, message: str):
        """Write a warning message with DevDollz styling"""
        self.write(f"{THEME_ICONS['warning']} {message}")
    
    def write_loading(self, message: str):
        """Write a loading message with DevDollz styling"""
        self.write(f"{THEME_ICONS['loading']} {message}")

class DevDollzFileTree(DirectoryTree):
    """Enhanced file tree with DevDollz styling"""
    
    def __init__(self, **kwargs):
        super().__init__("./", **kwargs)

class DevDollzMainApp(App):
    """Main DevDollz TUI Application with Cyber Glam Theme"""
    
    CSS = f"""
    /* DevDollz Cyber Glam Theme by Alexis Adams */
    
    $background: {CYBER_GLAM_COLORS['background']};
    $primary: {CYBER_GLAM_COLORS['primary']};
    $secondary: {CYBER_GLAM_COLORS['secondary']};
    $tertiary: {CYBER_GLAM_COLORS['tertiary']};
    $success: {CYBER_GLAM_COLORS['success']};
    $error: {CYBER_GLAM_COLORS['error']};
    $text: {CYBER_GLAM_COLORS['text']};
    $muted: {CYBER_GLAM_COLORS['muted']};

    Screen {{
        background: $background;
        color: $text;
    }}

    /* === HEADER & FOOTER === */
    DevDollzHeader {{
        background: $background;
        color: $primary;
        text-style: bold;
        height: auto;
        padding: 1;
    }}

    DevDollzHeader #logo {{
        color: $primary;
        text-align: center;
        width: 100%;
    }}

    DevDollzHeader #subtitle {{
        color: $secondary;
        text-align: center;
        width: 100%;
        text-style: italic;
    }}

    DevDollzFooter {{
        background: $background;
        color: $tertiary;
        height: auto;
        padding: 1;
    }}

    DevDollzFooter #creator-tagline {{
        color: $tertiary;
        text-align: center;
        width: 100%;
    }}

    DevDollzFooter #help-text {{
        color: $muted;
        text-align: center;
        width: 100%;
        font-size: 0.8;
    }}

    /* === PANELS & CONTAINERS === */
    Horizontal, Vertical {{
        background: $background;
    }}

    Container {{
        background: $surface;
        border: round $secondary;
        padding: 1;
    }}

    /* === CODE EDITOR === */
    DevDollzCodeEditor {{
        background: $surface;
        border: tall $primary;
        padding: 1;
        color: $text;
        height: 15;
        font-family: "JetBrains Mono", "Fira Code", monospace;
        font-size: 0.9;
    }}

    DevDollzCodeEditor:focus {{
        border: tall $secondary;
        box-shadow: 0 0 10px $secondary;
    }}

    DevDollzCodeEditor > .text-area--placeholder {{
        color: $muted;
        text-style: italic;
        font-size: 0.8;
    }}

    DevDollzCodeEditor > .text-area--cursor {{
        background: $secondary;
        color: $background;
    }}

    /* === FILE & DIRECTORY TREE === */
    DevDollzFileTree {{
        background: $surface;
        border: round $tertiary;
        padding: 1;
    }}

    DevDollzFileTree > .directory-tree--file {{
        color: $text;
    }}

    DevDollzFileTree > .directory-tree--folder {{
        color: $tertiary;
    }}

    DevDollzFileTree > .directory-tree--selected {{
        background: $primary;
        color: $background;
        text-style: bold;
    }}

    /* === RESULTS LOG === */
    DevDollzResultsLog {{
        background: $surface;
        border: round $secondary;
        padding: 1;
        color: $text;
    }}

    /* === BUTTONS === */
    Button {{
        background: $primary;
        color: $background;
        border: none;
        padding: 1 2;
        margin: 1;
    }}

    Button:hover {{
        background: $secondary;
        color: $background;
    }}

    /* === SCROLLBARS === */
    ::-webkit-scrollbar {{
        background: $surface;
        width: 1;
    }}

    ::-webkit-scrollbar-thumb {{
        background: $primary;
    }}

    /* === ANIMATIONS === */
    @keyframes glow {{
        0% {{ box-shadow: 0 0 5px $primary; }}
        50% {{ box-shadow: 0 0 20px $secondary; }}
        100% {{ box-shadow: 0 0 5px $primary; }}
    }}

    DevDollzCodeEditor:focus {{
        animation: glow 2s ease-in-out infinite;
    }}
    """

    BINDINGS = [
        Binding("?", "show_help", "Show Help"),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear_log", "Clear Log"),
        Binding("ctrl+s", "save_code", "Save Code"),
        Binding("ctrl+o", "open_file", "Open File"),
        Binding("ctrl+n", "new_file", "New File"),
        Binding("ctrl+e", "toggle_edit_mode", "Toggle Edit Mode"),
        Binding("ctrl+enter", "execute_command", "Execute Command"),
        Binding("tab", "focus_next", "Next Focus"),
        Binding("shift+tab", "focus_previous", "Previous Focus"),
    ]

    def __init__(self):
        super().__init__()
        self.core = get_devdollz_core()
        self.command_history: List[str] = []
        self.history_index = -1
        self.current_file: Optional[str] = None

    def compose(self) -> ComposeResult:
        yield DevDollzHeader()
        
        yield Horizontal(
            DevDollzFileTree(id="file-tree"),
            Vertical(
                DevDollzResultsLog(id="results"),
                DevDollzCodeEditor(id="code-editor"),
                id="main-panel"
            ),
            id="main-layout"
        )
        
        yield DevDollzFooter()

    def on_mount(self) -> None:
        """Initialize the DevDollz application"""
        self.query_one("#code-editor").focus()
        self.set_interval(0.1, self.check_results)
        
        # Welcome message
        results_log = self.query_one("#results", DevDollzResultsLog)
        results_log.write_info("Welcome to DevDollz! 💖 Press ? for help.")
        results_log.write_info(f"🎨 Theme: Cyber Glam")
        results_log.write_info(f"👩‍💻 Creator: Alexis Adams")
        results_log.write_info(f"🔢 Version: 1.0.0")
        results_log.write_info(f"💻 Code Editor: Press Ctrl+Enter to execute commands")
        results_log.write_info(f"📝 Edit Mode: Press Ctrl+E to toggle between command and edit modes")
        results_log.write("")

    def check_results(self) -> None:
        """Check for results from the DevDollz core system"""
        results = self.core.get_results()
        results_log = self.query_one("#results", DevDollzResultsLog)
        
        for result in results:
            if result.status == "success":
                results_log.write_success(f"Task {result.task_id} completed by {result.agent}")
                results_log.write(f"{result.content}")
                results_log.write("")
            else:
                results_log.write_error(f"Task {result.task_id} failed: {result.content}")
                results_log.write("")

    def execute_command_from_editor(self) -> None:
        """Execute commands from the code editor"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
        
        # Get the current line or selected text
        current_line = code_editor.get_line_at_index(code_editor.cursor_line)
        if not current_line or current_line.strip() == "":
            results_log.write_error("No command to execute. Type a command or select text.")
            return
        
        command = current_line.strip()
        
        # Add to command history
        if command and command not in self.command_history:
            self.command_history.append(command)
        self.history_index = -1
        
        # Handle special commands
        if command.lower() in ['quit', 'exit']:
            self.exit()
            return
        
        if command == 'help':
            self.show_help_command(results_log)
            return
        
        if command == 'status':
            self.show_status_command(results_log)
            return
        
        if command == 'history':
            self.show_history_command(results_log)
            return
        
        if command == 'clear':
            results_log.clear()
            results_log.write_info("Log cleared ✨")
            return
        
        # Parse and execute DevDollz commands
        parts = command.split(maxsplit=2)
        if len(parts) < 2:
            results_log.write_error("That's not the password. Try again.")
            self.show_help_command(results_log)
            return
        
        action, cmd_type = parts[0], parts[1]
        task_content = parts[2] if len(parts) > 2 else ""
        
        if action not in ["generate", "debug"] or cmd_type not in ["function", "class", "code", "syntax", "logic"]:
            results_log.write_error("That's not the password. Try again.")
            self.show_help_command(results_log)
            return
        
        # Execute task
        agent_type = "code_gen" if action == "generate" else "debug"
        results_log.write_loading(f"Assembling the dolls... {THEME_ICONS['loading']}")
        
        task_id = self.core.execute_task(agent_type, cmd_type, task_content)
        results_log.write_info(f"Task {task_id} submitted to {agent_type} agent")
        
        # Highlight the executed line
        results_log.write_info(f"Executed: {command}")

    def show_help_command(self, results_log: DevDollzResultsLog):
        """Show DevDollz command help"""
        results_log.write_info("DevDollz Command Protocol:")
        results_log.write("  generate [function|class|code] <description>")
        results_log.write("  debug [syntax|logic|code] <code or description>")
        results_log.write("  status - Show system status")
        results_log.write("  history - Show recent tasks")
        results_log.write("  clear - Clear the log")
        results_log.write("  help - Show this help")
        results_log.write("")
        results_log.write("Examples:")
        results_log.write("  generate function calculate_sum")
        results_log.write("  debug syntax def foo(: pass")
        results_log.write("")

    def show_status_command(self, results_log: DevDollzResultsLog):
        """Show DevDollz system status"""
        status = self.core.get_info()
        results_log.write_info("DevDollz System Status:")
        results_log.write(f"  System: {status['system_name']}")
        results_log.write(f"  Creator: {status['creator']}")
        results_log.write(f"  Theme: {status['theme']}")
        results_log.write(f"  Version: {status['version']}")
        results_log.write(f"  Active Tasks: {status['active_tasks']}")
        results_log.write(f"  Total Tasks: {status['total_tasks']}")
        results_log.write(f"  CodeGen Agent: {'🟢' if status['agents']['code_gen'] else '🔴'}")
        results_log.write(f"  Debug Agent: {'🟢' if status['agents']['debug'] else '🔴'}")
        results_log.write("")

    def show_history_command(self, results_log: DevDollzResultsLog):
        """Show recent task history"""
        history = self.core.get_history(10)
        results_log.write_info("Recent DevDollz Tasks:")
        
        if not history:
            results_log.write("  No tasks in history yet.")
        else:
            for task in history:
                status_icon = THEME_ICONS['success'] if task['status'] == 'success' else THEME_ICONS['error']
                results_log.write(f"  {status_icon} {task['task_id']}: {task['task'][:50]}...")
        
        results_log.write("")

    def action_show_help(self):
        """Action to show help"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        self.show_help_command(results_log)

    def action_show_status(self):
        """Action to show status"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        self.show_status_command(results_log)

    def action_show_history(self):
        """Action to show history"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        self.show_history_command(results_log)

    def action_clear_log(self):
        """Action to clear the log"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        results_log.clear()
        results_log.write_info("Log cleared ✨")

    def action_save_code(self):
        """Action to save code from the editor"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
        
        if not self.current_file:
            results_log.write_error("No file open. Use Ctrl+O to open a file first.")
            return
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(code_editor.text)
            results_log.write_success(f"Code saved to {self.current_file} ✨")
        except Exception as e:
            results_log.write_error(f"Failed to save code: {e}")

    def action_open_file(self):
        """Action to open a file in the editor"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
        
        # For now, we'll use a simple file selection
        # In a full implementation, this would show a file picker
        results_log.write_info("File opening functionality coming soon! 💖")
        results_log.write_info("For now, you can edit code directly in the editor.")

    def action_new_file(self):
        """Action to create a new file"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
        
        code_editor.text = ""
        self.current_file = None
        results_log.write_info("New file created ✨")

    def action_toggle_edit_mode(self):
        """Action to toggle between command and edit modes"""
        results_log = self.query_one("#results", DevDollzResultsLog)
        code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
        
        self.command_mode = not self.command_mode
        if self.command_mode:
            code_editor.placeholder = "💖 Enter DevDollz commands or edit code here...\n\nExamples:\ngenerate function calculate_sum\ndebug syntax def foo(: pass\n\nPress Ctrl+Enter to execute commands\nPress Ctrl+S to save code"
            results_log.write_info("Switched to Command Mode 💖")
        else:
            code_editor.placeholder = "📝 Code Editing Mode\n\nEdit your code here...\nPress Ctrl+S to save\nPress Ctrl+E to return to command mode"
            results_log.write_info("Switched to Edit Mode 📝")

    def action_execute_command(self):
        """Action to execute commands from the editor"""
        self.execute_command_from_editor()

    def on_key(self, event: events.Key):
        """Handle key events"""
        if event.key == "up":
            # Navigate command history up
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
                code_editor.text = self.command_history[-(self.history_index + 1)]
                code_editor.cursor_position = len(code_editor.text)
        
        elif event.key == "down":
            # Navigate command history down
            if self.history_index > 0:
                self.history_index -= 1
                code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
                code_editor.text = self.command_history[-(self.history_index + 1)]
                code_editor.cursor_position = len(code_editor.text)
            elif self.history_index == 0:
                self.history_index = -1
                code_editor = self.query_one("#code-editor", DevDollzCodeEditor)
                code_editor.text = ""

    def on_unmount(self):
        """Cleanup when the application unmounts"""
        self.core.shutdown()

class DevDollzUI:
    """Main DevDollz UI interface"""
    
    @staticmethod
    def run_tui():
        """Run the DevDollz TUI application"""
        try:
            app = DevDollzMainApp()
            app.run()
        except Exception as e:
            print(f"{THEME_ICONS['error']} Failed to start DevDollz TUI: {e}")
            print(f"{THEME_ICONS['info']} Falling back to CLI mode...")
            return False
        return True

# Convenience function to run the UI
def run_devdollz_ui():
    """Run the DevDollz UI system"""
    return DevDollzUI.run_tui()
