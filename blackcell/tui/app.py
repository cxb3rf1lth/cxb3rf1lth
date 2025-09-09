"""
BlackCell Security Toolkit - Main TUI Application
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, Static, Log, ProgressBar, 
    DataTable, Input, TextArea, TabbedContent, TabPane
)
from textual.binding import Binding
from textual.screen import Screen
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
import asyncio
from typing import Dict, Any

from blackcell.tui.screens import (
    DashboardScreen, ReconScreen, ExploitScreen, 
    FuzzerScreen, PayloadScreen, SettingsScreen
)
from blackcell.tui.widgets import StatusBar, MenuBar
from blackcell.core.logger import setup_logger

class BlackCellApp(App):
    """Main BlackCell Security Toolkit TUI Application"""
    
    CSS_PATH = "styles.css"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "show_dashboard", "Dashboard"),
        Binding("r", "show_recon", "Recon"),
        Binding("e", "show_exploits", "Exploits"),
        Binding("f", "show_fuzzers", "Fuzzers"),
        Binding("p", "show_payloads", "Payloads"),
        Binding("s", "show_settings", "Settings"),
        Binding("h", "show_help", "Help"),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__()
        self.config = config or {}
        self.logger = setup_logger("blackcell-app")
        self.console = Console()
        
        # Initialize screens
        self.dashboard_screen = DashboardScreen()
        self.recon_screen = ReconScreen()
        self.exploit_screen = ExploitScreen()
        self.fuzzer_screen = FuzzerScreen()
        self.payload_screen = PayloadScreen()
        self.settings_screen = SettingsScreen()
        
    def on_mount(self) -> None:
        """Called when app is mounted"""
        self.title = "BlackCell Security Toolkit v2.0.0"
        self.sub_title = "Advanced Cybersecurity Arsenal with TUI Interface"
        
        # Install screens
        self.install_screen(self.dashboard_screen, name="dashboard")
        self.install_screen(self.recon_screen, name="recon")
        self.install_screen(self.exploit_screen, name="exploits")
        self.install_screen(self.fuzzer_screen, name="fuzzers")
        self.install_screen(self.payload_screen, name="payloads")
        self.install_screen(self.settings_screen, name="settings")
        
        # Show dashboard by default
        self.push_screen("dashboard")
        
    def compose(self) -> ComposeResult:
        """Compose the main UI"""
        yield Header()
        yield MenuBar(id="menu-bar")
        yield Container(
            StatusBar(id="status-bar"),
            id="main-container"
        )
        yield Footer()
    
    def action_show_dashboard(self) -> None:
        """Show dashboard screen"""
        self.push_screen("dashboard")
    
    def action_show_recon(self) -> None:
        """Show reconnaissance screen"""
        self.push_screen("recon")
    
    def action_show_exploits(self) -> None:
        """Show exploits screen"""
        self.push_screen("exploits")
    
    def action_show_fuzzers(self) -> None:
        """Show fuzzers screen"""
        self.push_screen("fuzzers")
    
    def action_show_payloads(self) -> None:
        """Show payloads screen"""
        self.push_screen("payloads")
    
    def action_show_settings(self) -> None:
        """Show settings screen"""
        self.push_screen("settings")
    
    def action_show_help(self) -> None:
        """Show help information"""
        help_text = """
BlackCell Security Toolkit - Keyboard Shortcuts

Navigation:
  d - Dashboard
  r - Reconnaissance
  e - Exploits
  f - Fuzzers
  p - Payloads
  s - Settings
  h - Help
  q - Quit

Module Controls:
  Enter - Execute/Run
  Escape - Cancel/Back
  Tab - Next field
  Shift+Tab - Previous field
  
For detailed help, visit: https://github.com/cxb3rf1lth/cxb3rf1lth
        """
        
        from textual.widgets import Markdown
        from textual.screen import ModalScreen
        
        class HelpScreen(ModalScreen):
            def compose(self):
                yield Container(
                    Markdown(help_text),
                    Button("Close", id="close-help"),
                    id="help-dialog"
                )
            
            def on_button_pressed(self, event):
                if event.button.id == "close-help":
                    self.dismiss()
        
        self.push_screen(HelpScreen())
    
    def on_ready(self) -> None:
        """Called when app is ready"""
        self.logger.info("BlackCell Security Toolkit TUI started")
        
        # Update status bar
        status_bar = self.query_one("#status-bar")
        if hasattr(status_bar, 'update_status'):
            status_bar.update_status("Ready", "green")
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.logger.info("Quitting BlackCell Security Toolkit")
        self.exit()