#!/usr/bin/env python3
"""
BlackCell Security Toolkit - TUI Main Entry Point
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from blackcell.tui.app import BlackCellApp
from blackcell.core.logger import setup_logger
from blackcell.core.config import load_config, ensure_directories

async def run_tui():
    """Run the BlackCell TUI application"""
    
    # Setup logging
    logger = setup_logger("blackcell-tui")
    
    try:
        # Ensure directories exist
        ensure_directories()
        
        # Load configuration
        config = load_config()
        
        # Create and run the app
        app = BlackCellApp(config=config)
        await app.run_async()
        
    except KeyboardInterrupt:
        logger.info("TUI terminated by user")
    except Exception as e:
        logger.error(f"TUI error: {e}")
        raise

def main():
    """Main entry point for TUI"""
    asyncio.run(run_tui())

if __name__ == "__main__":
    main()