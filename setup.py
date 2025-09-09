#!/usr/bin/env python3
"""
BlackCell Security Toolkit Setup
Advanced cybersecurity toolkit with TUI interface
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="blackcell-security",
    version="2.0.0",
    author="BlackCell Security",
    author_email="cxb3rf1lth@blackcell.security",
    description="Advanced Cybersecurity Toolkit with Terminal User Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cxb3rf1lth/cxb3rf1lth",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "blackcell=blackcell.main:main",
            "bc-tui=blackcell.tui.main:run_tui",
            "bc-recon=blackcell.modules.recon.main:main",
            "bc-exploit=blackcell.modules.exploits.main:main",
            "bc-fuzzer=blackcell.modules.fuzzers.main:main",
            "bc-payload=blackcell.modules.payloads.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "blackcell": [
            "data/payloads/*",
            "data/wordlists/*",
            "data/exploits/*",
            "config/*.yaml",
            "config/*.json",
        ],
    },
)