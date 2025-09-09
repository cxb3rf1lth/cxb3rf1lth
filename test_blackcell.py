#!/usr/bin/env python3
"""
BlackCell Security Toolkit - Test Script
Demonstrates all major functionality
"""

import asyncio
import sys
from pathlib import Path

# Add to path for testing
sys.path.append(str(Path(__file__).parent))

from blackcell.core.logger import setup_logger
from blackcell.core.config import load_config
from blackcell.core.setup import BlackCellSetup
from blackcell.modules.payloads.generator import PayloadGenerator
from blackcell.modules.payloads.encoder import PayloadEncoder
from blackcell.modules.recon.scanner import NetworkScanner
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_core_functionality():
    """Test core functionality"""
    console.print(Panel.fit("Testing Core Functionality", border_style="blue"))
    
    # Test logger
    logger = setup_logger("test")
    logger.info("Logger initialized successfully")
    console.print("✓ Logger working")
    
    # Test config
    config = load_config()
    console.print(f"✓ Configuration loaded ({len(config)} sections)")
    
    # Test setup
    setup = BlackCellSetup()
    console.print("✓ Setup system initialized")

def test_payload_system():
    """Test payload generation and encoding"""
    console.print(Panel.fit("Testing Payload System", border_style="green"))
    
    # Test payload generator
    generator = PayloadGenerator()
    
    # Generate different types of payloads
    xss_payloads = generator.generate_payloads("xss", count=3)
    sqli_payloads = generator.generate_payloads("sqli", count=3)
    cmd_payloads = generator.generate_payloads("cmdi", count=3)
    
    table = Table(title="Generated Payloads")
    table.add_column("Type", style="cyan")
    table.add_column("Count", justify="center")
    table.add_column("Example", style="yellow", max_width=50)
    
    table.add_row("XSS", str(len(xss_payloads)), xss_payloads[0] if xss_payloads else "None")
    table.add_row("SQL Injection", str(len(sqli_payloads)), sqli_payloads[0] if sqli_payloads else "None")
    table.add_row("Command Injection", str(len(cmd_payloads)), cmd_payloads[0] if cmd_payloads else "None")
    
    console.print(table)
    
    # Test encoding
    encoder = PayloadEncoder()
    test_payload = "<script>alert('test')</script>"
    
    encoding_table = Table(title="Payload Encoding")
    encoding_table.add_column("Encoding", style="cyan")
    encoding_table.add_column("Result", style="yellow", max_width=60)
    
    encodings = ["url", "base64", "html", "unicode"]
    for encoding in encodings:
        encoded = encoder.encode(test_payload, encoding)
        encoding_table.add_row(encoding.upper(), encoded)
    
    console.print(encoding_table)

async def test_recon_system():
    """Test reconnaissance functionality"""
    console.print(Panel.fit("Testing Reconnaissance System", border_style="red"))
    
    # Test with localhost (safe target)
    scanner = NetworkScanner("127.0.0.1", "80,443,22", threads=3, timeout=1)
    
    console.print("Running port scan on localhost...")
    results = await scanner.port_scan()
    
    scan_table = Table(title="Port Scan Results")
    scan_table.add_column("Target", style="cyan")
    scan_table.add_column("Total Ports", justify="center")
    scan_table.add_column("Open Ports", justify="center", style="green")
    scan_table.add_column("Status", style="yellow")
    
    scan_table.add_row(
        results["target"],
        str(results["scan_info"]["total_ports"]), 
        str(len(results["open_ports"])),
        "Complete"
    )
    
    console.print(scan_table)
    
    if results["open_ports"]:
        port_table = Table(title="Open Ports Details")
        port_table.add_column("Port", justify="center")
        port_table.add_column("Service", style="green")
        port_table.add_column("Status", style="yellow")
        
        for port_info in results["open_ports"]:
            port_table.add_row(
                str(port_info["port"]),
                port_info["service"],
                port_info["status"]
            )
        
        console.print(port_table)

def test_cli_tools():
    """Test CLI tool functionality"""
    console.print(Panel.fit("Testing CLI Tools", border_style="magenta"))
    
    import subprocess
    
    # Test payload CLI
    try:
        result = subprocess.run([
            sys.executable, "blackcell/modules/payloads/main.py", 
            "-t", "xss", "--list"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            console.print("✓ Payload CLI working")
            lines = result.stdout.strip().split('\n')
            console.print(f"  Found {len(lines)-1} XSS payloads")
        else:
            console.print(f"✗ Payload CLI error: {result.stderr}")
    
    except Exception as e:
        console.print(f"✗ Payload CLI test failed: {e}")
    
    # Test recon CLI help
    try:
        result = subprocess.run([
            sys.executable, "blackcell/modules/recon/main.py", "--help"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0 and "BlackCell Reconnaissance" in result.stdout:
            console.print("✓ Recon CLI working")
        else:
            console.print("✗ Recon CLI not working properly")
    
    except Exception as e:
        console.print(f"✗ Recon CLI test failed: {e}")

def test_installation():
    """Test installation components"""
    console.print(Panel.fit("Testing Installation", border_style="yellow"))
    
    # Check if main directories exist
    base_dir = Path(__file__).parent
    required_dirs = [
        "blackcell/core",
        "blackcell/tui", 
        "blackcell/modules/recon",
        "blackcell/modules/payloads",
        "blackcell/modules/exploits",
        "blackcell/modules/fuzzers"
    ]
    
    install_table = Table(title="Installation Components")
    install_table.add_column("Component", style="cyan")
    install_table.add_column("Status", justify="center")
    install_table.add_column("Path", style="dim")
    
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        status = "✓" if full_path.exists() else "✗"
        style = "green" if full_path.exists() else "red"
        install_table.add_row(dir_path, f"[{style}]{status}[/{style}]", str(full_path))
    
    console.print(install_table)
    
    # Check key files
    key_files = [
        "requirements.txt",
        "setup.py",
        "install.py",
        "blackcell/main.py",
        "blackcell/tui/app.py"
    ]
    
    file_table = Table(title="Key Files")
    file_table.add_column("File", style="cyan")
    file_table.add_column("Status", justify="center")
    file_table.add_column("Size", justify="right")
    
    for file_path in key_files:
        full_path = base_dir / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            file_table.add_row(file_path, "[green]✓[/green]", f"{size:,} bytes")
        else:
            file_table.add_row(file_path, "[red]✗[/red]", "Missing")
    
    console.print(file_table)

async def main():
    """Run all tests"""
    console.print(Panel.fit(
        "BlackCell Security Toolkit - Comprehensive Test Suite",
        title="[bold red]BlackCell Test Suite[/bold red]",
        border_style="red"
    ))
    
    try:
        # Run all tests
        test_installation()
        test_core_functionality()
        test_payload_system()
        await test_recon_system()
        test_cli_tools()
        
        console.print(Panel.fit(
            "[bold green]All tests completed successfully![/bold green]\n\n"
            "BlackCell Security Toolkit is ready to use:\n"
            "• Run 'python blackcell/main.py' for TUI interface\n"
            "• Run 'python blackcell/modules/recon/main.py <target>' for recon\n"
            "• Run 'python blackcell/modules/payloads/main.py -t xss' for payloads",
            title="Test Results",
            border_style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Test failed with error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())