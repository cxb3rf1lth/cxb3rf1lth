"""
BlackCell Security Toolkit - Custom TUI Widgets
"""

from textual.widgets import Static, Button, DataTable, ProgressBar
from textual.containers import Horizontal, Vertical
from textual.app import ComposeResult
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from datetime import datetime

class StatusBar(Static):
    """Status bar widget for displaying current status"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = "Initializing..."
        self.status_color = "yellow"
        
    def on_mount(self) -> None:
        """Called when widget is mounted"""
        self.update_display()
        
    def update_status(self, status: str, color: str = "white"):
        """Update the status message"""
        self.status = status
        self.status_color = color
        self.update_display()
        
    def update_display(self):
        """Update the display with current status"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_text = Text()
        status_text.append("Status: ", style="bold")
        status_text.append(self.status, style=f"bold {self.status_color}")
        status_text.append(f" | Time: {timestamp}", style="dim")
        
        self.update(Panel(status_text, title="BlackCell Status", border_style="blue"))

class MenuBar(Static):
    """Menu bar widget for navigation"""
    
    def compose(self) -> ComposeResult:
        """Compose the menu bar"""
        with Horizontal(id="menu-container"):
            yield Button("Dashboard [d]", id="btn-dashboard", variant="primary")
            yield Button("Recon [r]", id="btn-recon")
            yield Button("Exploits [e]", id="btn-exploits")
            yield Button("Fuzzers [f]", id="btn-fuzzers")
            yield Button("Payloads [p]", id="btn-payloads")
            yield Button("Settings [s]", id="btn-settings")
            yield Button("Help [h]", id="btn-help")
            yield Button("Quit [q]", id="btn-quit", variant="error")
    
    def on_button_pressed(self, event):
        """Handle menu button presses"""
        button_actions = {
            "btn-dashboard": "show_dashboard",
            "btn-recon": "show_recon", 
            "btn-exploits": "show_exploits",
            "btn-fuzzers": "show_fuzzers",
            "btn-payloads": "show_payloads",
            "btn-settings": "show_settings",
            "btn-help": "show_help",
            "btn-quit": "quit"
        }
        
        action = button_actions.get(event.button.id)
        if action:
            self.app.call_from_thread(getattr(self.app, f"action_{action}"))

class TargetInput(Static):
    """Widget for target input with validation"""
    
    def compose(self) -> ComposeResult:
        """Compose the target input widget"""
        from textual.widgets import Input, Label
        
        with Vertical():
            yield Label("Target:")
            yield Input(placeholder="Enter target (IP, domain, URL...)", id="target-input")
            yield Button("Validate", id="validate-target")

class ResultsTable(Static):
    """Widget for displaying scan/test results"""
    
    def __init__(self, columns=None, **kwargs):
        super().__init__(**kwargs)
        self.columns = columns or ["Target", "Status", "Result", "Time"]
        
    def compose(self) -> ComposeResult:
        """Compose the results table"""
        table = DataTable()
        for column in self.columns:
            table.add_column(column)
        yield table
        
    def add_result(self, *values):
        """Add a result row to the table"""
        table = self.query_one(DataTable)
        table.add_row(*values)

class ProgressWidget(Static):
    """Widget for showing progress of operations"""
    
    def compose(self) -> ComposeResult:
        """Compose the progress widget"""
        from textual.widgets import Label
        
        with Vertical():
            yield Label("Progress:", id="progress-label")
            yield ProgressBar(id="progress-bar")
            yield Label("Idle", id="progress-status")
    
    def update_progress(self, current: int, total: int, status: str = ""):
        """Update progress bar and status"""
        progress_bar = self.query_one("#progress-bar", ProgressBar)
        progress_label = self.query_one("#progress-status", Label)
        
        if total > 0:
            progress_bar.update(progress=current / total * 100)
        progress_label.update(status or f"{current}/{total}")

class LogWidget(Static):
    """Widget for displaying logs"""
    
    def compose(self) -> ComposeResult:
        """Compose the log widget"""
        from textual.widgets import Log
        
        yield Log(id="log-display", auto_scroll=True)
    
    def add_log(self, message: str, level: str = "info"):
        """Add a log message"""
        log_widget = self.query_one("#log-display", Log)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "info": "white",
            "success": "green", 
            "warning": "yellow",
            "error": "red",
            "debug": "cyan"
        }
        
        color = colors.get(level, "white")
        log_widget.write_line(f"[{color}][{timestamp}] {message}[/{color}]")

class ModuleCard(Static):
    """Card widget for displaying module information"""
    
    def __init__(self, title: str, description: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        
    def compose(self) -> ComposeResult:
        """Compose the module card"""
        from textual.widgets import Label
        
        with Vertical():
            yield Label(self.title, classes="module-title")
            yield Label(self.description, classes="module-description")
            yield Button(f"Launch {self.title}", id=f"launch-{self.title.lower()}")

class PayloadManager(Static):
    """Widget for managing payloads"""
    
    def compose(self) -> ComposeResult:
        """Compose the payload manager"""
        from textual.widgets import Input, Select, TextArea
        
        with Vertical():
            with Horizontal():
                yield Select(
                    [("XSS", "xss"), ("SQLi", "sqli"), ("Command Injection", "cmdi")],
                    id="payload-type"
                )
                yield Button("Load", id="load-payload")
                yield Button("Save", id="save-payload")
            yield TextArea(id="payload-content", language="text")

class WordlistManager(Static):
    """Widget for managing wordlists"""
    
    def compose(self) -> ComposeResult:
        """Compose the wordlist manager"""
        from textual.widgets import Select, Input
        
        with Vertical():
            with Horizontal():
                yield Select(
                    [("Directories", "dirs"), ("Subdomains", "subs"), ("Files", "files")],
                    id="wordlist-type"
                )
                yield Input(placeholder="Custom wordlist path...", id="custom-wordlist")
                yield Button("Browse", id="browse-wordlist")
            yield DataTable(id="wordlist-preview")