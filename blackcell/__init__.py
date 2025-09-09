"""
BlackCell Security Toolkit
Advanced cybersecurity toolkit with TUI interface
"""

__version__ = "2.0.0"
__author__ = "BlackCell Security"
__description__ = "Advanced Cybersecurity Toolkit with Terminal User Interface"

# Core imports
from .core.logger import setup_logger
from .core.config import load_config

# TUI imports
try:
    from .tui.main import run_tui
except ImportError:
    pass