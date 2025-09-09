#!/usr/bin/env python3
"""
BlackCell Security Toolkit - Installation Script
"""

import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def check_python_version():
    """Check Python version requirements"""
    if sys.version_info < (3, 8):
        console.print("[red]Error: Python 3.8 or higher is required[/red]")
        sys.exit(1)
    
    console.print(f"[green]✓[/green] Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python dependencies"""
    console.print("[cyan]Installing Python dependencies...[/cyan]")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True, text=True)
        
        console.print("[green]✓[/green] Dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error installing dependencies: {e.stderr}[/red]")
        sys.exit(1)

def create_symlinks():
    """Create symbolic links for easy access"""
    script_path = Path(__file__).parent.absolute()
    
    # Common locations for user binaries
    bin_locations = [
        Path.home() / ".local" / "bin",
        Path("/usr/local/bin"),
        Path("/usr/bin")
    ]
    
    # Find writable bin directory
    target_bin = None
    for bin_path in bin_locations:
        if bin_path.exists() and os.access(bin_path, os.W_OK):
            target_bin = bin_path
            break
    
    if not target_bin:
        console.print("[yellow]Warning: Could not find writable bin directory for symlinks[/yellow]")
        return
    
    # Create symlinks
    symlinks = {
        "blackcell": script_path / "blackcell" / "main.py",
        "bc-tui": script_path / "blackcell" / "tui" / "main.py",
        "bc-recon": script_path / "blackcell" / "modules" / "recon" / "main.py",
        "bc-payload": script_path / "blackcell" / "modules" / "payloads" / "main.py"
    }
    
    for name, target in symlinks.items():
        symlink_path = target_bin / name
        
        try:
            if symlink_path.exists():
                symlink_path.unlink()
            
            symlink_path.symlink_to(target)
            symlink_path.chmod(0o755)
            console.print(f"[green]✓[/green] Created symlink: {name}")
            
        except Exception as e:
            console.print(f"[yellow]Warning: Could not create symlink {name}: {e}[/yellow]")

def run_setup():
    """Run the BlackCell setup process"""
    try:
        from blackcell.core.setup import run_setup as setup_func
        setup_func()
        console.print("[green]✓[/green] BlackCell setup completed")
    except Exception as e:
        console.print(f"[red]Error running setup: {e}[/red]")

def main():
    """Main installation function"""
    console.print(Panel.fit(
        Text("BlackCell Security Toolkit Installation", style="bold red"),
        border_style="red"
    ))
    
    console.print("\n[cyan]Starting BlackCell Security Toolkit installation...[/cyan]\n")
    
    # Check requirements
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create symlinks for easy access
    create_symlinks()
    
    # Run setup
    run_setup()
    
    console.print("\n[bold green]🎉 Installation completed successfully![/bold green]")
    console.print("\n[cyan]You can now use BlackCell Security Toolkit:[/cyan]")
    console.print("[white]• blackcell[/white] - Start the main TUI interface")
    console.print("[white]• bc-tui[/white] - Start TUI interface directly")
    console.print("[white]• bc-recon <target>[/white] - Run reconnaissance")
    console.print("[white]• bc-payload -t xss[/white] - Generate payloads")
    
    console.print(f"\n[dim]For more information: https://github.com/cxb3rf1lth/cxb3rf1lth[/dim]")

if __name__ == "__main__":
    main()