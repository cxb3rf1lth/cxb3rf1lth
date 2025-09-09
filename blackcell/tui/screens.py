"""
BlackCell Security Toolkit - TUI Screens
"""

from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Static, Button, Input, TextArea, DataTable, Label
from rich.text import Text
from rich.panel import Panel
from datetime import datetime

from blackcell.tui.widgets import (
    StatusBar, TargetInput, ResultsTable, ProgressWidget,
    LogWidget, ModuleCard, PayloadManager, WordlistManager
)

class DashboardScreen(Screen):
    """Main dashboard screen"""
    
    def compose(self) -> ComposeResult:
        """Compose the dashboard"""
        
        with Container():
            with Grid(id="dashboard-grid"):
                yield ModuleCard(
                    "Reconnaissance", 
                    "Network scanning and information gathering",
                    id="recon-card"
                )
                yield ModuleCard(
                    "Exploits", 
                    "Vulnerability exploitation and testing",
                    id="exploit-card"
                )
                yield ModuleCard(
                    "Fuzzers", 
                    "Web application fuzzing and testing",
                    id="fuzzer-card"
                )
                yield ModuleCard(
                    "Payloads", 
                    "Payload generation and management",
                    id="payload-card"
                )
            
            with Horizontal():
                with Vertical():
                    yield Static(Panel(
                        Text("System Status: Online\nModules Loaded: 4\nLast Scan: Never", 
                             justify="left"),
                        title="System Info",
                        border_style="green"
                    ))
                    yield LogWidget()
                
                with Vertical():
                    yield Static(Panel(
                        Text("Recent Activities:\n• System initialized\n• Modules loaded\n• Ready for operations"),
                        title="Activity Log",
                        border_style="blue"
                    ))
    
    def on_button_pressed(self, event):
        """Handle button presses on dashboard"""
        if event.button.id.startswith("launch-"):
            module = event.button.id.replace("launch-", "")
            self.app.action_show_recon() if module == "reconnaissance" else None
            self.app.action_show_exploits() if module == "exploits" else None
            self.app.action_show_fuzzers() if module == "fuzzers" else None
            self.app.action_show_payloads() if module == "payloads" else None

class ReconScreen(Screen):
    """Reconnaissance module screen"""
    
    def compose(self) -> ComposeResult:
        """Compose the recon screen"""
        
        with Container():
            with Horizontal():
                with Vertical():
                    yield Static(Panel(
                        Text("Network Reconnaissance", style="bold red"),
                        border_style="red"
                    ))
                    yield TargetInput()
                    
                    with Horizontal():
                        yield Button("Port Scan", id="port-scan")
                        yield Button("Service Scan", id="service-scan")
                        yield Button("OS Detection", id="os-detect")
                        yield Button("Vuln Scan", id="vuln-scan")
                    
                    yield ProgressWidget()
                
                with Vertical():
                    yield Static(Panel(
                        Text("Scan Configuration", style="bold blue"),
                        border_style="blue"
                    ))
                    
                    from textual.widgets import Select
                    yield Select([
                        ("Fast Scan", "fast"),
                        ("Comprehensive", "full"),
                        ("Stealth", "stealth"),
                        ("Custom", "custom")
                    ], id="scan-type")
                    
                    yield Input(placeholder="Custom ports (e.g., 80,443,8080)", id="custom-ports")
                    yield Input(placeholder="Scan delay (seconds)", id="scan-delay")
            
            yield ResultsTable(["Target", "Port", "Service", "Version", "Status"])
            yield LogWidget()

class ExploitScreen(Screen):
    """Exploits module screen"""
    
    def compose(self) -> ComposeResult:
        """Compose the exploit screen"""
        
        with Container():
            with Horizontal():
                with Vertical():
                    yield Static(Panel(
                        Text("Exploit Framework", style="bold red"),
                        border_style="red"
                    ))
                    
                    yield TargetInput()
                    
                    from textual.widgets import Select
                    yield Select([
                        ("Web Application", "web"),
                        ("Network Service", "network"),
                        ("Operating System", "os"),
                        ("Database", "database")
                    ], id="exploit-category")
                    
                    yield DataTable(id="exploits-table")
                    
                with Vertical():
                    yield Static(Panel(
                        Text("Exploit Details", style="bold blue"),
                        border_style="blue"
                    ))
                    
                    yield TextArea(id="exploit-description", read_only=True)
                    yield Button("Test Exploit", id="test-exploit")
                    yield Button("Execute Exploit", id="execute-exploit")
                    yield ProgressWidget()
            
            yield LogWidget()

class FuzzerScreen(Screen):
    """Fuzzers module screen"""
    
    def compose(self) -> ComposeResult:
        """Compose the fuzzer screen"""
        
        with Container():
            with Horizontal():
                with Vertical():
                    yield Static(Panel(
                        Text("Web Application Fuzzer", style="bold red"),
                        border_style="red"
                    ))
                    
                    yield Input(placeholder="Target URL", id="fuzzer-target")
                    
                    from textual.widgets import Select
                    yield Select([
                        ("Directory Fuzzing", "dirs"),
                        ("Parameter Fuzzing", "params"),
                        ("Subdomain Fuzzing", "subdomains"),
                        ("Custom Fuzzing", "custom")
                    ], id="fuzzer-type")
                    
                    yield WordlistManager()
                    
                    with Horizontal():
                        yield Button("Start Fuzzing", id="start-fuzz")
                        yield Button("Stop", id="stop-fuzz")
                        yield Button("Pause", id="pause-fuzz")
                
                with Vertical():
                    yield Static(Panel(
                        Text("Fuzzing Configuration", style="bold blue"),
                        border_style="blue"
                    ))
                    
                    yield Input(placeholder="Threads (1-50)", id="fuzz-threads")
                    yield Input(placeholder="Delay (seconds)", id="fuzz-delay")
                    yield Input(placeholder="Filter by status code", id="fuzz-filter")
                    yield ProgressWidget()
            
            yield ResultsTable(["URL", "Status", "Size", "Words", "Time"])
            yield LogWidget()

class PayloadScreen(Screen):
    """Payloads module screen"""
    
    def compose(self) -> ComposeResult:
        """Compose the payload screen"""
        
        with Container():
            with Horizontal():
                with Vertical():
                    yield Static(Panel(
                        Text("Payload Generator", style="bold red"),
                        border_style="red"
                    ))
                    
                    yield PayloadManager()
                    
                    with Horizontal():
                        yield Button("Generate", id="generate-payload")
                        yield Button("Test", id="test-payload")
                        yield Button("Encode", id="encode-payload")
                
                with Vertical():
                    yield Static(Panel(
                        Text("Encoding Options", style="bold blue"),
                        border_style="blue"
                    ))
                    
                    from textual.widgets import Select, Checkbox
                    yield Select([
                        ("URL Encoding", "url"),
                        ("Base64", "base64"),
                        ("HTML Entities", "html"),
                        ("Unicode", "unicode")
                    ], id="encoding-type")
                    
                    yield TextArea(id="encoded-payload", read_only=True)
            
            yield LogWidget()

class SettingsScreen(Screen):
    """Settings and configuration screen"""
    
    def compose(self) -> ComposeResult:
        """Compose the settings screen"""
        
        with Container():
            with Horizontal():
                with Vertical():
                    yield Static(Panel(
                        Text("General Settings", style="bold blue"),
                        border_style="blue"
                    ))
                    
                    from textual.widgets import Checkbox, Select
                    
                    yield Checkbox("Debug Mode", id="debug-mode")
                    yield Checkbox("Auto-update", id="auto-update")
                    yield Checkbox("Safe Mode", id="safe-mode")
                    
                    yield Select([
                        ("Dark", "dark"),
                        ("Light", "light"),
                        ("Auto", "auto")
                    ], id="theme-select")
                    
                    yield Input(placeholder="Max threads", id="max-threads")
                    yield Input(placeholder="Default timeout", id="default-timeout")
                
                with Vertical():
                    yield Static(Panel(
                        Text("Paths Configuration", style="bold green"),
                        border_style="green"
                    ))
                    
                    yield Input(placeholder="Data directory", id="data-dir")
                    yield Input(placeholder="Output directory", id="output-dir")
                    yield Input(placeholder="Wordlists directory", id="wordlists-dir")
                    yield Input(placeholder="Payloads directory", id="payloads-dir")
                    
                    with Horizontal():
                        yield Button("Save Settings", id="save-settings")
                        yield Button("Reset to Defaults", id="reset-settings")
            
            yield LogWidget()