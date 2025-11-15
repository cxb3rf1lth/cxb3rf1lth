#!/usr/bin/env python3
"""
Update README.md with the generated banner
"""

import subprocess
import sys
from pathlib import Path

# Markers to identify the banner section
BANNER_START = "<!-- DYNAMIC_BANNER_START -->"
BANNER_END = "<!-- DYNAMIC_BANNER_END -->"

def get_banner():
    """Generate the banner using the generate-banner.py script"""
    script_path = Path(__file__).parent / "generate-banner.py"
    
    result = subprocess.run(
        ['python3', str(script_path)],
        capture_output=True,
        text=True,
        check=True
    )
    
    return result.stdout

def update_readme(readme_path):
    """Update the README with a new banner"""
    
    # Read the current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate new banner
    banner = get_banner()
    
    # Check if markers exist
    if BANNER_START in content and BANNER_END in content:
        # Replace existing banner section
        start_idx = content.find(BANNER_START)
        end_idx = content.find(BANNER_END) + len(BANNER_END)
        
        new_content = (
            content[:start_idx] +
            f"{BANNER_START}\n{banner}\n{BANNER_END}" +
            content[end_idx:]
        )
    else:
        # Add banner at the very top
        new_content = f"{BANNER_START}\n{banner}\n{BANNER_END}\n\n{content}"
    
    # Write the updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ README updated successfully!", file=sys.stderr)

if __name__ == "__main__":
    readme_path = Path(__file__).parent.parent.parent / "README.md"
    
    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)
    
    update_readme(readme_path)
