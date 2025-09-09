"""
BlackCell Security Toolkit - Network Scanner
"""

import asyncio
import socket
import subprocess
import json
import ipaddress
from typing import Dict, List, Any, Optional
from pathlib import Path
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

from blackcell.core.logger import setup_logger

class PortScanner:
    """Basic port scanner implementation"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.logger = setup_logger("port_scanner")
    
    async def scan_port(self, target: str, port: int) -> Dict[str, Any]:
        """Scan a single port"""
        try:
            # Create socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                return {
                    "port": port,
                    "status": "open",
                    "service": self.get_service_name(port)
                }
            else:
                return {
                    "port": port,
                    "status": "closed",
                    "service": None
                }
                
        except Exception as e:
            return {
                "port": port,
                "status": "error",
                "service": None,
                "error": str(e)
            }
    
    def get_service_name(self, port: int) -> str:
        """Get common service name for port"""
        common_ports = {
            21: "ftp",
            22: "ssh",
            23: "telnet",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            143: "imap",
            443: "https",
            993: "imaps",
            995: "pop3s",
            3389: "rdp",
            5432: "postgresql",
            3306: "mysql",
            1433: "mssql",
            6379: "redis",
            27017: "mongodb"
        }
        return common_ports.get(port, "unknown")

class ServiceScanner:
    """Service detection and banner grabbing"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.logger = setup_logger("service_scanner")
    
    async def detect_service(self, target: str, port: int) -> Dict[str, Any]:
        """Detect service and grab banner"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target, port),
                timeout=self.timeout
            )
            
            # Try to read banner
            try:
                banner_data = await asyncio.wait_for(
                    reader.read(1024),
                    timeout=2
                )
                banner = banner_data.decode('utf-8', errors='ignore').strip()
            except:
                banner = ""
            
            # Send HTTP request if port 80/443
            if port in [80, 443]:
                http_request = b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n"
                writer.write(http_request)
                await writer.drain()
                
                try:
                    response_data = await asyncio.wait_for(
                        reader.read(1024),
                        timeout=2
                    )
                    response = response_data.decode('utf-8', errors='ignore')
                    
                    # Extract server info
                    if "Server:" in response:
                        server_line = [line for line in response.split('\n') if 'Server:' in line]
                        if server_line:
                            banner = server_line[0].split('Server:')[1].strip()
                except:
                    pass
            
            writer.close()
            await writer.wait_closed()
            
            return {
                "port": port,
                "service": self.identify_service(port, banner),
                "banner": banner,
                "version": self.extract_version(banner)
            }
            
        except Exception as e:
            return {
                "port": port,
                "service": "unknown",
                "banner": "",
                "version": "",
                "error": str(e)
            }
    
    def identify_service(self, port: int, banner: str) -> str:
        """Identify service based on port and banner"""
        if "SSH" in banner.upper():
            return "ssh"
        elif "HTTP" in banner.upper() or "Apache" in banner:
            return "http"
        elif "FTP" in banner.upper():
            return "ftp"
        elif "SMTP" in banner.upper():
            return "smtp"
        else:
            # Fallback to port-based detection
            return PortScanner(self.timeout).get_service_name(port)
    
    def extract_version(self, banner: str) -> str:
        """Extract version information from banner"""
        if not banner:
            return ""
        
        # Common version patterns
        import re
        patterns = [
            r'(\d+\.\d+\.\d+)',
            r'(\d+\.\d+)',
            r'Version\s+(\S+)',
            r'v(\d+\.\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""

class NetworkScanner:
    """Main network scanner class"""
    
    def __init__(self, target: str, ports: str = "1-10000", 
                 threads: int = 10, timeout: int = 5):
        self.target = target
        self.ports = self.parse_ports(ports)
        self.threads = threads
        self.timeout = timeout
        self.logger = setup_logger("network_scanner")
        
        self.port_scanner = PortScanner(timeout)
        self.service_scanner = ServiceScanner(timeout)
    
    def parse_ports(self, port_string: str) -> List[int]:
        """Parse port string into list of ports"""
        ports = []
        
        for part in port_string.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
        
        return sorted(list(set(ports)))
    
    async def port_scan(self) -> Dict[str, Any]:
        """Perform port scan"""
        self.logger.info(f"Scanning {len(self.ports)} ports on {self.target}")
        
        results = {
            "target": self.target,
            "open_ports": [],
            "closed_ports": [],
            "scan_info": {
                "total_ports": len(self.ports),
                "threads": self.threads,
                "timeout": self.timeout
            }
        }
        
        # Create semaphore to limit concurrent connections
        semaphore = asyncio.Semaphore(self.threads)
        
        async def scan_with_semaphore(port):
            async with semaphore:
                return await self.port_scanner.scan_port(self.target, port)
        
        # Run scans concurrently
        tasks = [scan_with_semaphore(port) for port in self.ports]
        scan_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in scan_results:
            if isinstance(result, dict):
                if result["status"] == "open":
                    results["open_ports"].append(result)
                else:
                    results["closed_ports"].append(result)
        
        self.logger.info(f"Found {len(results['open_ports'])} open ports")
        return results
    
    async def service_scan(self, port_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform service detection on open ports"""
        open_ports = port_results.get("open_ports", [])
        
        if not open_ports:
            return {"services": []}
        
        self.logger.info(f"Detecting services on {len(open_ports)} open ports")
        
        semaphore = asyncio.Semaphore(self.threads)
        
        async def service_scan_with_semaphore(port_info):
            async with semaphore:
                return await self.service_scanner.detect_service(
                    self.target, port_info["port"]
                )
        
        tasks = [service_scan_with_semaphore(port_info) for port_info in open_ports]
        service_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        services = []
        for result in service_results:
            if isinstance(result, dict):
                services.append(result)
        
        return {"services": services}
    
    async def os_detect(self) -> Dict[str, Any]:
        """Basic OS detection using TTL and other techniques"""
        try:
            # Simple ping to get TTL
            cmd = f"ping -c 1 {self.target}"
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            output = stdout.decode('utf-8', errors='ignore')
            
            # Extract TTL
            import re
            ttl_match = re.search(r'ttl=(\d+)', output, re.IGNORECASE)
            
            if ttl_match:
                ttl = int(ttl_match.group(1))
                
                # Guess OS based on TTL
                if ttl <= 64:
                    os_guess = "Linux/Unix"
                elif ttl <= 128:
                    os_guess = "Windows"
                else:
                    os_guess = "Unknown"
                
                return {
                    "ttl": ttl,
                    "os_guess": os_guess,
                    "method": "TTL analysis"
                }
            
        except Exception as e:
            self.logger.error(f"OS detection failed: {e}")
        
        return {"os_guess": "Unknown", "method": "Failed"}
    
    def save_results(self, results: Dict[str, Any], output_file: str):
        """Save results to file"""
        output_path = Path(output_file)
        
        if output_path.suffix.lower() == '.json':
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            # Save as text
            with open(output_path, 'w') as f:
                self.write_text_results(f, results)
    
    def write_text_results(self, f, results: Dict[str, Any]):
        """Write results in text format"""
        f.write(f"BlackCell Network Scan Results\n")
        f.write(f"{'='*50}\n")
        f.write(f"Target: {results['target']}\n")
        f.write(f"Total Ports Scanned: {results['scan_info']['total_ports']}\n")
        f.write(f"Open Ports Found: {len(results['open_ports'])}\n\n")
        
        if results['open_ports']:
            f.write("Open Ports:\n")
            f.write("-" * 30 + "\n")
            for port_info in results['open_ports']:
                f.write(f"Port {port_info['port']}: {port_info['service']}\n")
        
        if 'services' in results:
            f.write("\nService Detection:\n")
            f.write("-" * 30 + "\n")
            for service in results['services']:
                f.write(f"Port {service['port']}: {service['service']}")
                if service.get('version'):
                    f.write(f" ({service['version']})")
                if service.get('banner'):
                    f.write(f" - {service['banner'][:50]}...")
                f.write("\n")
    
    def print_results(self, results: Dict[str, Any]):
        """Print results to console"""
        print(f"\nBlackCell Network Scan Results")
        print(f"{'='*50}")
        print(f"Target: {results['target']}")
        print(f"Total Ports Scanned: {results['scan_info']['total_ports']}")
        print(f"Open Ports Found: {len(results['open_ports'])}")
        
        if results['open_ports']:
            print(f"\nOpen Ports:")
            print(f"{'-'*30}")
            for port_info in results['open_ports']:
                print(f"Port {port_info['port']}: {port_info['service']}")
        
        if 'services' in results:
            print(f"\nService Detection:")
            print(f"{'-'*30}")
            for service in results['services']:
                print(f"Port {service['port']}: {service['service']}", end="")
                if service.get('version'):
                    print(f" ({service['version']})", end="")
                if service.get('banner'):
                    print(f" - {service['banner'][:50]}...", end="")
                print()
        
        if 'os_info' in results:
            print(f"\nOS Detection:")
            print(f"{'-'*30}")
            os_info = results['os_info']
            print(f"OS Guess: {os_info.get('os_guess', 'Unknown')}")
            if 'ttl' in os_info:
                print(f"TTL: {os_info['ttl']}")