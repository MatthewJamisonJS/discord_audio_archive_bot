#!/bin/bash
# Quick installation script for Audio Archive Bot package
# This installs the bot in development mode with all dependencies

set -e  # Exit on error

echo "========================================"
echo "Audio Archive Bot - Package Installation"
echo "========================================"
echo ""

# Check if we're in the project directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo "Python version: $PYTHON_VERSION - OK"
echo ""

# Ask user for installation type
echo "Select installation type:"
echo "1. Development (editable, recommended for contributors)"
echo "2. Production (standard installation)"
echo "3. Development with all tools (includes linters, formatters, etc.)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "Installing in development mode..."
        pip3 install -e .
        ;;
    2)
        echo ""
        echo "Installing in production mode..."
        pip3 install .
        ;;
    3)
        echo ""
        echo "Installing in development mode with all tools..."
        pip3 install -e ".[dev]"
        ;;
    *)
        echo "Invalid choice. Defaulting to development mode..."
        pip3 install -e .
        ;;
esac

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Package Information:"
python3 -c "import audio_archive_bot; print(f'  Name: audio-archive-bot'); print(f'  Version: {audio_archive_bot.__version__}')"
echo ""

echo "Available commands:"
echo "  audio_bot_run          - Start the bot (recommended)"
echo "  python3 -m audio_archive_bot  - Alternative way to start"
echo ""

echo "Next steps:"
echo "1. Configure your .env file:"
echo "   cp .env.example .env"
echo "   # Edit .env with your credentials"
echo ""
echo "2. Install Node.js dependencies:"
echo "   npm install"
echo ""
echo "3. Run the bot:"
echo "   audio_bot_run"
echo ""
echo "For more information, see:"
echo "  - PACKAGING_GUIDE.md (packaging and installation)"
echo "  - README.md (bot usage and configuration)"
echo "  - CONTRIBUTING.md (development guidelines)"
echo ""
