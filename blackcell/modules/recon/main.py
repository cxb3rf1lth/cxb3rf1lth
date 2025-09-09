#!/usr/bin/env python3
"""
BlackCell Security Toolkit - Reconnaissance Module CLI
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from blackcell.core.logger import setup_logger
from blackcell.modules.recon.scanner import NetworkScanner, PortScanner

def main():
    """Main CLI entry point for reconnaissance module"""
    
    parser = argparse.ArgumentParser(
        description="BlackCell Reconnaissance Module",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("target", help="Target IP, domain, or network range")
    parser.add_argument("-p", "--ports", default="1-10000", help="Port range to scan")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    parser.add_argument("-T", "--timeout", type=int, default=5, help="Connection timeout")
    parser.add_argument("--service-scan", action="store_true", help="Perform service detection")
    parser.add_argument("--os-detect", action="store_true", help="Perform OS detection")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger("recon", debug=args.debug)
    
    async def run_scan():
        """Run the reconnaissance scan"""
        try:
            logger.info(f"Starting reconnaissance scan on {args.target}")
            
            # Initialize scanner
            scanner = NetworkScanner(
                target=args.target,
                ports=args.ports,
                threads=args.threads,
                timeout=args.timeout
            )
            
            # Run port scan
            logger.info("Running port scan...")
            results = await scanner.port_scan()
            
            # Service detection if requested
            if args.service_scan:
                logger.info("Running service detection...")
                service_results = await scanner.service_scan(results)
                results.update(service_results)
            
            # OS detection if requested
            if args.os_detect:
                logger.info("Running OS detection...")
                os_info = await scanner.os_detect()
                results["os_info"] = os_info
            
            # Output results
            if args.output:
                scanner.save_results(results, args.output)
                logger.info(f"Results saved to {args.output}")
            else:
                scanner.print_results(results)
                
            logger.info("Reconnaissance scan completed")
            
        except KeyboardInterrupt:
            logger.info("Scan interrupted by user")
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            sys.exit(1)
    
    # Run the scan
    asyncio.run(run_scan())

if __name__ == "__main__":
    main()