#!/usr/bin/env python3
"""
BlackCell Security Toolkit - Main Entry Point
"""

import sys
import argparse
import asyncio
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from blackcell.core.logger import setup_logger
from blackcell.core.config import load_config
from blackcell.tui.main import run_tui


def main():
    """Main entry point for BlackCell Security Toolkit"""
    
    parser = argparse.ArgumentParser(
        description="BlackCell Security Toolkit - Advanced Cybersecurity Arsenal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  blackcell                    # Launch TUI interface (default)
  blackcell --tui              # Launch TUI interface explicitly
  blackcell --version          # Show version information
  blackcell --config           # Show configuration
        """
    )
    
    parser.add_argument(
        "--tui", 
        action="store_true", 
        default=True,
        help="Launch TUI interface (default)"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="BlackCell Security Toolkit v2.0.0"
    )
    parser.add_argument(
        "--config", 
        action="store_true",
        help="Show current configuration"
    )
    parser.add_argument(
        "--setup", 
        action="store_true",
        help="Run initial setup and configuration"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(debug=args.debug)
    
    # Load configuration
    config = load_config()
    
    if args.config:
        from blackcell.core.config import show_config
        show_config()
        return
        
    if args.setup:
        from blackcell.core.setup import run_setup
        run_setup()
        return
    
    # Default behavior: Launch TUI
    logger.info("Starting BlackCell Security Toolkit TUI")
    try:
        asyncio.run(run_tui())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()