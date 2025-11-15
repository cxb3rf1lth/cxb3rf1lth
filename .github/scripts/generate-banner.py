#!/usr/bin/env python3
"""
Generate randomized ASCII art banner for cxb3rf1lth using figlet
"""

import subprocess
import random
import sys
from pathlib import Path

# Available figlet fonts (from default Ubuntu figlet package)
BANNER_FONTS = [
    'standard',
    'slant',
    'big',
    'block',
    'bubble',
    'digital',
    'ivrit',
    'lean',
    'mini',
    'script',
    'shadow',
    'small',
    'smscript',
    'smshadow',
    'smslant',
    'banner'
]

def generate_banner(text="cxb3rf1lth"):
    """Generate ASCII art banner with random font"""
    
    # Select a random font
    font = random.choice(BANNER_FONTS)
    
    print(f"Selected font: {font}", file=sys.stderr)
    
    try:
        # Generate the banner
        result = subprocess.run(
            ['figlet', '-f', font, text],
            capture_output=True,
            text=True,
            check=True
        )
        
        banner = result.stdout
        
        # Create the markdown section with the banner
        markdown_output = f"""
<div align="center">

```
{banner.rstrip()}
```

<sub>🎲 Randomly generated banner using figlet font: **{font}** | Updates on every commit</sub>

</div>

---
"""
        
        return markdown_output
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating banner: {e}", file=sys.stderr)
        # Fallback to a simple banner
        return f"""
<div align="center">

```
  _____  ____  ___  _ __  __| || | | |_  | |__  
 / __\\ \\/ /\\ \\/ / |/ _ \\| '__/ _| || | | __|  '_ \\ 
| (__| >  <  >  <| | (_) | | | | || | | |_| | | |
 \\___/_/\\_\\/_/\\_\\_|\\___/|_| |_|  |_|_|\\__|_| |_|
                                                    
  cxb3rf1lth
```

<sub>🎲 Dynamic banner | Font: {font}</sub>

</div>

---
"""
    except FileNotFoundError:
        print("figlet not found!", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    banner = generate_banner()
    print(banner)
