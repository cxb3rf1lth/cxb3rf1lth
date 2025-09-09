"""
BlackCell Security Toolkit - Configuration Management
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any
import os

DEFAULT_CONFIG = {
    "general": {
        "debug": False,
        "auto_update": True,
        "theme": "dark",
        "max_threads": 10,
        "timeout": 30
    },
    "tui": {
        "animation_speed": "normal",
        "show_help": True,
        "auto_save": True,
        "refresh_rate": 1.0
    },
    "recon": {
        "default_ports": "1-10000",
        "scan_delay": 0.1,
        "max_targets": 100,
        "output_format": "json"
    },
    "exploits": {
        "verify_exploits": True,
        "safe_mode": True,
        "auto_backup": True,
        "max_attempts": 3
    },
    "fuzzers": {
        "default_wordlist": "common.txt",
        "threads": 5,
        "delay": 0.5,
        "follow_redirects": True
    },
    "payloads": {
        "auto_encode": True,
        "verify_payloads": True,
        "default_encoding": "url",
        "custom_payloads_dir": "~/.blackcell/payloads"
    },
    "wordlists": {
        "auto_update": True,
        "custom_wordlists_dir": "~/.blackcell/wordlists",
        "default_categories": ["common", "subdomains", "directories"]
    },
    "paths": {
        "data_dir": "~/.blackcell/data",
        "output_dir": "~/.blackcell/output",
        "temp_dir": "~/.blackcell/temp",
        "logs_dir": "~/.blackcell/logs"
    }
}

def get_config_path():
    """Get configuration file path"""
    config_dir = Path.home() / ".blackcell"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.yaml"

def load_config():
    """Load configuration from file or create default"""
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                # Merge with defaults for any missing keys
                return merge_configs(DEFAULT_CONFIG, config)
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config: Dict[str, Any]):
    """Save configuration to file"""
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

def merge_configs(default: Dict, user: Dict) -> Dict:
    """Recursively merge user config with defaults"""
    result = default.copy()
    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result

def show_config():
    """Display current configuration"""
    config = load_config()
    print("Current BlackCell Security Toolkit Configuration:")
    print("=" * 50)
    print(yaml.dump(config, default_flow_style=False, indent=2))

def update_config(section: str, key: str, value: Any):
    """Update a specific configuration value"""
    config = load_config()
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config(config)

def get_config_value(section: str, key: str, default=None):
    """Get a specific configuration value"""
    config = load_config()
    return config.get(section, {}).get(key, default)

def ensure_directories():
    """Ensure all required directories exist"""
    config = load_config()
    paths = config.get("paths", {})
    
    for path_key, path_value in paths.items():
        path = Path(path_value).expanduser()
        path.mkdir(parents=True, exist_ok=True)