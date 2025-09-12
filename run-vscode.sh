#!/bin/bash

# BlackCell Security - VSCode Setup Script
# This script helps set up the development environment

echo "🔥 Welcome to BlackCell Security Development Environment"
echo "======================================================="
echo

# Check if VSCode is available
if command -v code &> /dev/null; then
    echo "✓ VSCode detected"
    
    # Open the workspace
    echo "📂 Opening workspace in VSCode..."
    code cxb3rf1lth.code-workspace
    
    echo "🎯 Environment ready! Happy hacking!"
else
    echo "❌ VSCode not found. Please install VSCode first."
    echo "   Download from: https://code.visualstudio.com/"
fi

echo
echo "📋 Available VSCode tasks:"
echo "   - Preview README: Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Preview README'"
echo "   - Open Terminal: Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Open Terminal'"
echo "   - Git Status: Ctrl+Shift+P -> 'Tasks: Run Task' -> 'Git Status'"
echo
echo "🔧 Recommended extensions will be suggested when you open the workspace"