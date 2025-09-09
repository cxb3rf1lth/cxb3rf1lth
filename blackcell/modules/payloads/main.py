#!/usr/bin/env python3
"""
BlackCell Security Toolkit - Payloads Module CLI
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from blackcell.core.logger import setup_logger
from blackcell.modules.payloads.generator import PayloadGenerator
from blackcell.modules.payloads.encoder import PayloadEncoder

def main():
    """Main CLI entry point for payloads module"""
    
    parser = argparse.ArgumentParser(
        description="BlackCell Payloads Module",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("-t", "--type", 
                       choices=["xss", "sqli", "cmdi", "lfi", "rfi"],
                       required=True,
                       help="Payload type")
    parser.add_argument("-p", "--payload", help="Custom payload string")
    parser.add_argument("-e", "--encode", 
                       choices=["url", "base64", "html", "unicode"],
                       help="Encoding method")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--list", action="store_true", help="List available payloads")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger("payloads", debug=args.debug)
    
    try:
        generator = PayloadGenerator()
        encoder = PayloadEncoder()
        
        if args.list:
            # List available payloads
            payloads = generator.list_payloads(args.type)
            print(f"Available {args.type.upper()} payloads:")
            for i, payload in enumerate(payloads, 1):
                print(f"{i:3d}: {payload}")
            return
        
        # Generate or use custom payload
        if args.payload:
            payload = args.payload
        else:
            payloads = generator.generate_payloads(args.type)
            if payloads:
                payload = payloads[0]  # Use first payload
            else:
                logger.error(f"No payloads available for type: {args.type}")
                return
        
        # Encode if requested
        if args.encode:
            payload = encoder.encode(payload, args.encode)
            logger.info(f"Encoded payload using {args.encode}")
        
        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(payload + '\n')
            logger.info(f"Payload saved to {args.output}")
        else:
            print(f"Generated payload: {payload}")
            
    except Exception as e:
        logger.error(f"Payload generation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()