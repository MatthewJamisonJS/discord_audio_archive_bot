#!/bin/bash

# Discord Audio Archive Bot - Hybrid Setup Script
# ===============================================
# Security-focused setup for Python + Node.js hybrid architecture

set -e  # Exit on error

echo "🎵 Discord Audio Archive Bot - Hybrid Setup"
echo "==========================================="
echo "⚠️  SECURITY NOTICE: This bot records voice communications."
echo "   Ensure proper consent and legal compliance before use."
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ "$EUID" -eq 0 ]]; then
    print_error "Do not run this setup as root for security reasons!"
    exit 1
fi

validation_errors=0

# Step 1: Check Python version
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $python_version"

    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        print_success "Python version is compatible (3.8+)"
    else
        print_error "Python 3.8+ required. Current version: $python_version"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.8+ first."
    echo "  Install via Homebrew: brew install python"
    exit 1
fi

# Step 2: Check Node.js and npm
print_status "Checking Node.js installation..."
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    node_version=$(node --version)
    npm_version=$(npm --version)
    print_success "Node.js found: $node_version"
    print_success "npm found: $npm_version"
else
    print_error "Node.js and/or npm not found. Please install Node.js first."
    echo "  Install via Homebrew: brew install node"
    echo "  Or download from: https://nodejs.org/"
    exit 1
fi

# Step 3: Check FFmpeg installation
print_status "Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>/dev/null | head -n1 | cut -d' ' -f3)
    print_success "FFmpeg found: $ffmpeg_version"
else
    print_warning "FFmpeg not found. Installing via Homebrew..."

    if command -v brew &> /dev/null; then
        print_status "Installing FFmpeg with Homebrew..."
        brew install ffmpeg
        print_success "FFmpeg installed successfully"
    else
        print_error "Homebrew not found. Please install FFmpeg manually:"
        echo "  macOS: Install Homebrew then run 'brew install ffmpeg'"
        echo "  Ubuntu/Debian: sudo apt install ffmpeg"
        echo "  Windows: Download from https://ffmpeg.org/download.html"
        exit 1
    fi
fi

# Step 4: Create Python virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Python virtual environment created"
else
    print_success "Python virtual environment already exists"
fi

# Step 5: Install Python dependencies
print_status "Installing Python dependencies..."
source venv/bin/activate

pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python dependencies installed successfully"

    # Check for Discord package conflicts
    if pip list | grep -q "^pycord "; then
        print_warning "Found conflicting 'pycord' package - removing it"
        pip uninstall pycord -y >/dev/null 2>&1 || true
    fi

    # Verify Discord import works
    if python3 -c "import discord; print('Discord version:', discord.__version__)" >/dev/null 2>&1; then
        discord_version=$(python3 -c "import discord; print(discord.__version__)")
        print_success "Discord.py working correctly (v$discord_version)"
    else
        print_error "Discord.py not working properly"
        validation_errors=$((validation_errors + 1))
    fi
else
    print_error "requirements.txt not found"
    exit 1
fi

# Step 6: Install Node.js dependencies
print_status "Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    npm install
    print_success "Node.js dependencies installed successfully"

    # Verify key packages
    if npm list discord.js @discordjs/voice nodemailer >/dev/null 2>&1; then
        discord_js_version=$(npm list discord.js --depth=0 2>/dev/null | grep discord.js | cut -d'@' -f2)
        print_success "Discord.js and dependencies working correctly (v$discord_js_version)"
    else
        print_warning "Some Node.js dependencies may not be properly installed"
    fi
else
    print_error "package.json not found"
    exit 1
fi

# Step 7: Setup environment configuration
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your configuration before running the bot"
    else
        print_error ".env.example file not found"
        exit 1
    fi
else
    print_success "Environment file already exists"
fi

# Step 8: Setup secure permissions
print_status "Setting secure file permissions..."
if [ -f ".env" ]; then
    chmod 600 .env
    print_success "Secure permissions set on .env file"
fi

# Step 9: Create recordings directory
print_status "Creating recordings directory..."
if [ ! -d "recordings" ]; then
    mkdir -p recordings
    print_success "Recordings directory created"
else
    print_success "Recordings directory already exists"
fi

# Step 10: Validate configuration
print_status "Validating configuration..."
source .env 2>/dev/null || true

# Check required variables
if [ -z "${DISCORD_TOKEN}" ] || [[ "${DISCORD_TOKEN}" =~ your_.*_here ]]; then
    print_error "Please configure DISCORD_TOKEN in .env file"
    validation_errors=$((validation_errors + 1))
fi

if [ -z "${TARGET_USER_ID}" ] || [[ "${TARGET_USER_ID}" =~ 123456789 ]]; then
    print_error "Please configure TARGET_USER_ID in .env file"
    validation_errors=$((validation_errors + 1))
fi

# Optional email validation
if [ -n "${EMAIL_USER}" ] && [ -n "${EMAIL_PASS}" ] && [ -n "${EMAIL_RECIPIENT}" ]; then
    if [[ "${EMAIL_USER}" =~ your_.*_here ]] || [[ "${EMAIL_PASS}" =~ your_.*_here ]]; then
        print_warning "Email configuration contains placeholder values"
    else
        print_success "Email configuration detected and appears valid"
    fi
fi

# Step 11: Run system tests
print_status "Running system validation tests..."
if python test_hybrid_system.py >/dev/null 2>&1; then
    print_success "All system tests passed"
else
    print_warning "Some system tests failed - run 'python test_hybrid_system.py' for details"
fi

# Step 12: Setup complete summary
echo
echo "🎉 Hybrid Setup Complete!"
echo "========================="
echo

if [ $validation_errors -eq 0 ]; then
    print_success "All requirements installed and configured successfully"
    echo
    echo "🔐 SECURITY REMINDERS:"
    echo "- Never share your Discord token or email credentials"
    echo "- .env file permissions set to 600 (owner read/write only)"
    echo "- Use Gmail App Passwords, not regular passwords"
    echo "- Obtain explicit consent before recording anyone"
    echo
    echo "📋 Next steps:"
    echo "1. Edit .env with your actual credentials:"
    echo "   - DISCORD_TOKEN (from Discord Developer Portal)"
    echo "   - TARGET_USER_ID (Discord user ID to record)"
    echo "   - EMAIL_* variables (optional, for email notifications)"
    echo
    echo "2. Invite bot to Discord server with minimal permissions:"
    echo "   ✓ Connect (to join voice channels)"
    echo "   ✓ Speak (for voice activity)"
    echo "   ✓ Use Voice Activity (for recording)"
    echo
    echo "3. Start the hybrid bot:"
    echo "   ./run_hybrid.sh"
    echo
    echo "🎮 Bot commands (in Discord):"
    echo "- !status - Check voice recorder status"
    echo "- !test_recording - Test recording functionality (admin only)"
    echo
else
    print_warning "Setup completed with $validation_errors configuration issues"
    echo
    echo "🔧 Please fix the configuration issues above before running the bot"
fi

echo "📚 Documentation:"
echo "- README.md - Complete usage guide"
echo "- HYBRID_DEPLOYMENT_GUIDE.md - Detailed deployment instructions"
echo "- test_hybrid_system.py - System health check"
echo "- .env.example - Configuration template"
echo
echo "🔗 Essential links:"
echo "- Discord Developer Portal: https://discord.com/developers/applications"
echo "- Gmail App Passwords: https://myaccount.google.com/apppasswords"
echo
echo "🛡️  Legal Reminder: Ensure compliance with local recording laws!"

deactivate  # Deactivate virtual environment
print_success "Hybrid setup script completed successfully!"
