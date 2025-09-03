#!/usr/bin/env python3
"""
DevDollz Spine Canvas - The Pulse That Never Sleeps
One canvas: code left, pulse feed right, voice always listening
"""

import asyncio
import threading
import time
import json
import queue
import speech_recognition as sr
from pathlib import Path
from typing import Dict, List, Optional, Any
import textwrap

# Import our spine
from .spine import DevDollzSpine, SpinePulse

try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("⚠️ Tkinter not available, falling back to console mode")

try:
    import pyaudio
    import wave
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ PyAudio not available, voice input disabled")

class VoiceListener:
    """Always-on voice listener for 'go' triggers"""
    
    def __init__(self, spine: DevDollzSpine):
        self.spine = spine
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.trigger_word = "go"
        self.command_queue = queue.Queue()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("🎤 Voice listener initialized - say 'go' to trigger commands")
    
    def start_listening(self):
        """Start continuous voice listening"""
        self.listening = True
        self._listen_loop()
    
    def stop_listening(self):
        """Stop voice listening"""
        self.listening = False
    
    def _listen_loop(self):
        """Continuous listening loop"""
        def listen():
            while self.listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    try:
                        text = self.recognizer.recognize_google(audio).lower()
                        print(f"🎤 Heard: {text}")
                        
                        if self.trigger_word in text:
                            # Extract command after "go"
                            command = text.split(self.trigger_word, 1)[1].strip()
                            if command:
                                print(f"🚀 Voice command: {command}")
                                self.command_queue.put(command)
                                
                    except sr.UnknownValueError:
                        pass  # No speech detected
                    except sr.RequestError as e:
                        print(f"🎤 Speech recognition error: {e}")
                        
                except Exception as e:
                    print(f"🎤 Voice listener error: {e}")
                    time.sleep(0.1)
        
        # Start in background thread
        voice_thread = threading.Thread(target=listen, daemon=True)
        voice_thread.start()
    
    def get_command(self) -> Optional[str]:
        """Get next voice command if available"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

class SpineCanvas:
    """The main canvas - code left, pulse feed right"""
    
    def __init__(self, spine: DevDollzSpine):
        self.spine = spine
        self.voice_listener = VoiceListener(spine) if AUDIO_AVAILABLE else None
        self.root = None
        self.code_editor = None
        self.pulse_feed = None
        self.status_bar = None
        self.command_entry = None
        self.running = False
        
        # User preferences (will be learned over time)
        self.user_prefs = {
            "ignore_warnings": ["W1202"],  # Skip spaces warnings
            "short_errors": True,  # Shorten verbose errors
            "auto_collapse": True,  # Auto-collapse pulse feed
            "voice_enabled": True
        }
    
    def start(self):
        """Start the canvas UI"""
        if not TKINTER_AVAILABLE:
            self._start_console_mode()
            return
        
        self.root = tk.Tk()
        self.root.title("🔥 DevDollz Spine - The Current That Flows")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)  # Code editor
        self.root.grid_columnconfigure(1, weight=1)  # Pulse feed
        
        self._create_widgets()
        self._start_spine()
        
        # Start voice listener if available
        if self.voice_listener and self.user_prefs["voice_enabled"]:
            self.voice_listener.start_listening()
        
        # Start update loop
        self._update_loop()
        
        self.root.mainloop()
    
    def _create_widgets(self):
        """Create the main UI widgets"""
        # Code Editor (Left Side)
        code_frame = tk.Frame(self.root, bg='#1a1a1a', relief='raised', bd=2)
        code_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        code_frame.grid_rowconfigure(0, weight=1)
        code_frame.grid_columnconfigure(0, weight=1)
        
        # Code editor label
        code_label = tk.Label(code_frame, text="💻 Code Canvas", 
                            font=('Consolas', 12, 'bold'), 
                            bg='#1a1a1a', fg='#00ff00')
        code_label.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Code editor
        self.code_editor = scrolledtext.ScrolledText(
            code_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#00ff00',
            selectbackground='#404040',
            height=30,
            width=80
        )
        self.code_editor.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Command entry
        cmd_frame = tk.Frame(code_frame, bg='#1a1a1a')
        cmd_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        cmd_frame.grid_columnconfigure(0, weight=1)
        
        cmd_label = tk.Label(cmd_frame, text="🚀 Command:", 
                           font=('Consolas', 10), 
                           bg='#1a1a1a', fg='#00ff00')
        cmd_label.grid(row=0, column=0, sticky='w', padx=(0, 5))
        
        self.command_entry = tk.Entry(cmd_frame, font=('Consolas', 10), 
                                    bg='#2d2d2d', fg='#ffffff',
                                    insertbackground='#00ff00')
        self.command_entry.grid(row=0, column=1, sticky='ew', padx=(0, 5))
        self.command_entry.bind('<Return>', self._execute_command)
        
        execute_btn = tk.Button(cmd_frame, text="Execute", 
                              command=self._execute_command,
                              bg='#00ff00', fg='#000000',
                              font=('Consolas', 10, 'bold'))
        execute_btn.grid(row=0, column=2)
        
        # Pulse Feed (Right Side)
        pulse_frame = tk.Frame(self.root, bg='#1a1a1a', relief='raised', bd=2)
        pulse_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        pulse_frame.grid_rowconfigure(1, weight=1)
        pulse_frame.grid_columnconfigure(0, weight=1)
        
        # Pulse feed header
        pulse_header = tk.Frame(pulse_frame, bg='#1a1a1a')
        pulse_header.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        pulse_header.grid_columnconfigure(0, weight=1)
        
        pulse_label = tk.Label(pulse_header, text="💓 Live Pulse Feed", 
                             font=('Consolas', 12, 'bold'), 
                             bg='#1a1a1a', fg='#ff00ff')
        pulse_label.grid(row=0, column=0, sticky='w')
        
        # Collapse button
        self.collapse_btn = tk.Button(pulse_header, text="📉", 
                                    command=self._toggle_pulse_feed,
                                    bg='#ff00ff', fg='#000000',
                                    font=('Consolas', 10))
        self.collapse_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Pulse feed
        self.pulse_feed = scrolledtext.ScrolledText(
            pulse_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='#2d2d2d',
            fg='#ffffff',
            height=30,
            width=50
        )
        self.pulse_feed.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="🔥 DevDollz Spine Ready", 
                                 relief='sunken', anchor='w',
                                 bg='#1a1a1a', fg='#00ff00',
                                 font=('Consolas', 9))
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky='ew')
        
        # Welcome message
        welcome_text = """# Hello, DevDollz! 

Welcome to the spine that flows.

## Quick Start:
- Type commands in the input below
- Watch agents spawn like lightning
- See live pulses in the right panel
- Say "go" + command for voice control

## Example Commands:
- generate Python function for data processing
- scrape website for content
- analyze code structure
- deploy to production

The pulse never sleeps. The current never stops.
"""
        self.code_editor.insert('1.0', welcome_text)
    
    def _start_spine(self):
        """Start the DevDollz spine"""
        try:
            self.spine.start()
            self.status_bar.config(text="🎭 DevDollz Spine is alive!")
            self.running = True
        except Exception as e:
            self.status_bar.config(text=f"❌ Failed to start spine: {e}")
    
    def _execute_command(self, event=None):
        """Execute a command through the spine"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Clear command entry
        self.command_entry.delete(0, tk.END)
        
        # Execute through spine
        try:
            result = self.spine.execute(command)
            
            # Log command in code editor
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"\n\n[{timestamp}] 🚀 Command: {command}\n"
            log_entry += f"[{timestamp}] 📊 Result: {result}\n"
            
            self.code_editor.insert(tk.END, log_entry)
            self.code_editor.see(tk.END)
            
            # Update status
            if result.get("status") == "spawned":
                self.status_bar.config(text=f"⚡ Agent spawned: {result.get('agent_type', 'unknown')}")
            elif result.get("status") == "blocked":
                self.status_bar.config(text=f"🛡️ Command blocked: {result.get('message', '')}")
            else:
                self.status_bar.config(text=f"📝 Command processed: {command}")
                
        except Exception as e:
            error_msg = f"❌ Error executing command: {e}"
            self.status_bar.config(text=error_msg)
            
            # Log error in code editor
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"\n[{timestamp}] {error_msg}\n"
            self.code_editor.insert(tk.END, log_entry)
            self.code_editor.see(tk.END)
    
    def _toggle_pulse_feed(self):
        """Toggle pulse feed visibility"""
        if self.pulse_feed.winfo_viewable():
            self.pulse_feed.grid_remove()
            self.collapse_btn.config(text="📈")
        else:
            self.pulse_feed.grid()
            self.collapse_btn.config(text="📉")
    
    def _update_loop(self):
        """Main update loop for live data"""
        if not self.running:
            return
        
        try:
            # Check for voice commands
            if self.voice_listener:
                voice_cmd = self.voice_listener.get_command()
                if voice_cmd:
                    self.command_entry.delete(0, tk.END)
                    self.command_entry.insert(0, voice_cmd)
                    self._execute_command()
            
            # Update pulse feed
            self._update_pulse_feed()
            
            # Update status
            self._update_status()
            
        except Exception as e:
            print(f"Update loop error: {e}")
        
        # Schedule next update
        if self.root:
            self.root.after(100, self._update_loop)
    
    def _update_pulse_feed(self):
        """Update the live pulse feed"""
        try:
            pulses = self.spine.get_pulse_feed(50)  # Last 50 pulses
            
            if not pulses:
                return
            
            # Clear feed
            self.pulse_feed.delete('1.0', tk.END)
            
            # Add pulses (most recent first)
            for pulse in reversed(pulses):
                timestamp = time.strftime("%H:%M:%S", time.localtime(pulse.timestamp))
                
                # Color code by level
                level_colors = {
                    "info": "#00ffff",
                    "warning": "#ffff00", 
                    "error": "#ff0000",
                    "success": "#00ff00"
                }
                
                color = level_colors.get(pulse.level, "#ffffff")
                
                # Format pulse entry
                entry = f"[{timestamp}] {pulse.agent_name}: {pulse.message}\n"
                
                # Insert with color (basic coloring)
                self.pulse_feed.insert(tk.END, entry)
                
                # Apply color to the last line
                last_line = self.pulse_feed.index(tk.END + "-2l")
                self.pulse_feed.tag_add(f"level_{pulse.level}", last_line, tk.END + "-1l")
                self.pulse_feed.tag_config(f"level_{pulse.level}", foreground=color)
            
            # Auto-scroll to bottom
            self.pulse_feed.see(tk.END)
            
        except Exception as e:
            print(f"Pulse feed update error: {e}")
    
    def _update_status(self):
        """Update status bar with current spine status"""
        try:
            status = self.spine.get_status()
            
            # Count active agents
            active_agents = len([a for a in status.get("agents", {}).values() 
                               if a.get("status") == "running"])
            
            # Get pulse summary
            pulse_summary = status.get("pulse_summary", {})
            total_pulses = pulse_summary.get("total", 0)
            
            status_text = f"🔥 Spine: {status.get('status', 'unknown')} | "
            status_text += f"⚡ Agents: {active_agents} | "
            status_text += f"💓 Pulses: {total_pulses} | "
            status_text += f"🎤 Voice: {'ON' if self.voice_listener and self.user_prefs['voice_enabled'] else 'OFF'}"
            
            self.status_bar.config(text=status_text)
            
        except Exception as e:
            print(f"Status update error: {e}")
    
    def _start_console_mode(self):
        """Fallback console mode when Tkinter is not available"""
        print("🔥 DevDollz Spine Canvas - Console Mode")
        print("=" * 50)
        print("Tkinter not available, running in console mode")
        print("Voice input and GUI features disabled")
        print("=" * 50)
        
        # Start spine
        self.spine.start()
        self.running = True
        
        # Start voice listener if available
        if self.voice_listener and self.user_prefs["voice_enabled"]:
            self.voice_listener.start_listening()
        
        # Console command loop
        try:
            while self.running:
                print("\n💻 Enter command (or 'quit' to exit):")
                command = input("🚀 > ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                
                if command:
                    try:
                        result = self.spine.execute(command)
                        print(f"📊 Result: {result}")
                        
                        # Show recent pulses
                        pulses = self.spine.get_pulse_feed(5)
                        if pulses:
                            print("\n💓 Recent pulses:")
                            for pulse in pulses[-5:]:
                                timestamp = time.strftime("%H:%M:%S", time.localtime(pulse.timestamp))
                                print(f"  [{timestamp}] {pulse.agent_name}: {pulse.message}")
                        
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                # Check for voice commands
                if self.voice_listener:
                    voice_cmd = self.voice_listener.get_command()
                    if voice_cmd:
                        print(f"🎤 Voice command detected: {voice_cmd}")
                        try:
                            result = self.spine.execute(voice_cmd)
                            print(f"📊 Voice result: {result}")
                        except Exception as e:
                            print(f"❌ Voice command error: {e}")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Interrupted by user")
        finally:
            self.spine.stop()
            print("👋 DevDollz Spine Canvas shutdown complete")

class DevDollzCanvasLauncher:
    """Launcher for the DevDollz Canvas"""
    
    def __init__(self):
        self.spine = DevDollzSpine()
        self.canvas = SpineCanvas(self.spine)
    
    def launch(self):
        """Launch the DevDollz Canvas"""
        print("🔥 Launching DevDollz Spine Canvas...")
        print("🎭 The Current That Flows")
        print("💓 The Pulse That Never Sleeps")
        print("🚀 Lightning-Fast Agent Spawning")
        print("🎤 Voice Always Listening")
        print("=" * 50)
        
        try:
            self.canvas.start()
        except Exception as e:
            print(f"❌ Canvas launch error: {e}")
            print("🔄 Falling back to console mode...")
            self.canvas._start_console_mode()
        finally:
            self.spine.stop()

# Main execution
if __name__ == "__main__":
    print("🔥 DevDollz Spine Canvas - The Pulse That Never Sleeps")
    print("=" * 60)
    
    launcher = DevDollzCanvasLauncher()
    launcher.launch()
