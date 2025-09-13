#!/bin/bash

# Discord Audio Archive Bot - Universal Cross-Platform Setup
# =========================================================
# Supports macOS, Linux (Ubuntu/Debian/CentOS/Arch), and Windows (via WSL/Git Bash)
# Automatically detects platform and installs all required dependencies

set -e

echo "🎵 Discord Audio Archive Bot - Universal Setup"
echo "=============================================="
echo "🌍 Automatically detecting your platform and setting up everything you need..."
echo

# Colors for output (with fallbacks for Windows)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows Git Bash - simplified output
    print_status() { echo "[INFO] $1"; }
    print_success() { echo "[SUCCESS] $1"; }
    print_warning() { echo "[WARNING] $1"; }
    print_error() { echo "[ERROR] $1"; }
else
    # Unix-like systems - colored output
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    NC='\033[0m'

    print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
    print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
    print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
    print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
    print_platform() { echo -e "${CYAN}[PLATFORM]${NC} $1"; }
fi

# Platform detection
detect_platform() {
    print_status "Detecting your operating system..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
        PLATFORM="macOS"
        PACKAGE_MANAGER="brew"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        PLATFORM="Linux"
        # Detect Linux distribution
        if command -v apt-get &> /dev/null; then
            DISTRO="Ubuntu/Debian"
            PACKAGE_MANAGER="apt"
        elif command -v yum &> /dev/null; then
            DISTRO="CentOS/RHEL"
            PACKAGE_MANAGER="yum"
        elif command -v pacman &> /dev/null; then
            DISTRO="Arch Linux"
            PACKAGE_MANAGER="pacman"
        elif command -v zypper &> /dev/null; then
            DISTRO="openSUSE"
            PACKAGE_MANAGER="zypper"
        else
            DISTRO="Unknown"
            PACKAGE_MANAGER="unknown"
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        PLATFORM="Windows"
        if command -v choco &> /dev/null; then
            PACKAGE_MANAGER="chocolatey"
        elif command -v winget &> /dev/null; then
            PACKAGE_MANAGER="winget"
        else
            PACKAGE_MANAGER="manual"
        fi
    elif [[ "$OSTYPE" == "cygwin" ]]; then
        PLATFORM="Windows (Cygwin)"
        PACKAGE_MANAGER="apt-cyg"
    else
        PLATFORM="Unknown"
        PACKAGE_MANAGER="unknown"
    fi

    print_platform "Detected: $PLATFORM"
    if [[ "$PLATFORM" == "Linux" ]]; then
        print_platform "Distribution: $DISTRO"
    fi
    print_platform "Package Manager: $PACKAGE_MANAGER"
    echo
}

# Enhanced version checking utilities
check_version() {
    local tool="$1"
    local required_version="$2"
    local current_version="$3"

    if command -v "$tool" &> /dev/null; then
        print_success "$tool found (version: $current_version)"
        return 0
    else
        print_warning "$tool not found (required: $required_version+)"
        return 1
    fi
}

# Robust semantic version comparison
version_compare() {
    # Compare version strings (returns 0 if $1 >= $2)
    # Handles versions like 3.11.0, 18.17.1, 4.4.0-1ubuntu1, etc.

    local current="$1"
    local required="$2"

    # Extract numeric parts only (remove letters, build info)
    current_clean=$(echo "$current" | sed 's/[^0-9.].*$//' | sed 's/\.$//')
    required_clean=$(echo "$required" | sed 's/[^0-9.].*$//' | sed 's/\.$//')

    # Use sort with version sorting if available
    if sort --version-sort </dev/null >/dev/null 2>&1; then
        highest=$(printf '%s\n%s\n' "$required_clean" "$current_clean" | sort --version-sort | tail -n1)
        [[ "$highest" == "$current_clean" ]]
    else
        # Fallback to basic comparison for systems without sort -V
        printf '%s\n%s\n' "$required_clean" "$current_clean" | sort -V | head -n1 | grep -q "^$required_clean$"
    fi
}

# Package manager version checking
check_package_manager_versions() {
    print_status "Checking package manager versions..."

    case "$PACKAGE_MANAGER" in
        "brew")
            if command -v brew &> /dev/null; then
                local brew_version=$(brew --version | head -n1 | cut -d' ' -f2)
                print_success "Homebrew found (version: $brew_version)"
            fi
            ;;
        "apt")
            if command -v apt &> /dev/null; then
                local apt_version=$(apt --version | cut -d' ' -f2)
                print_success "APT found (version: $apt_version)"
            fi
            ;;
        "yum")
            if command -v yum &> /dev/null; then
                local yum_version=$(yum --version | head -n1)
                print_success "YUM found (version: $yum_version)"
            fi
            ;;
        "pacman")
            if command -v pacman &> /dev/null; then
                local pacman_version=$(pacman --version | head -n1 | cut -d' ' -f3)
                print_success "Pacman found (version: $pacman_version)"
            fi
            ;;
        "chocolatey")
            if command -v choco &> /dev/null; then
                local choco_version=$(choco --version)
                print_success "Chocolatey found (version: $choco_version)"
            fi
            ;;
        "winget")
            if command -v winget &> /dev/null; then
                local winget_version=$(winget --version)
                print_success "Winget found (version: $winget_version)"
            fi
            ;;
    esac
}

# Python version checking
check_python() {
    print_status "Checking Python installation..."
    local required_version="3.8"

    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
        if version_compare "$python_version" "$required_version"; then
            print_success "Python 3 found (version: $python_version)"

            # Check pip
            if command -v pip3 &> /dev/null; then
                local pip_version=$(pip3 --version 2>&1 | cut -d' ' -f2)
                print_success "pip3 found (version: $pip_version)"
            else
                print_warning "pip3 not found - will install"
                return 1
            fi
            return 0
        else
            print_warning "Python version $python_version is too old (required: $required_version+)"
            return 1
        fi
    elif command -v python &> /dev/null; then
        local python_version=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ "$python_version" == "3."* ]] && version_compare "$python_version" "$required_version"; then
            print_success "Python found (version: $python_version)"
            return 0
        else
            print_warning "Python version $python_version is incompatible (need Python 3.8+)"
            return 1
        fi
    else
        print_warning "Python not found (required: $required_version+)"
        return 1
    fi
}

# Node.js version checking
check_nodejs() {
    print_status "Checking Node.js installation..."
    local required_version="18.0"

    if command -v node &> /dev/null; then
        local node_version=$(node --version 2>&1 | sed 's/v//')
        if version_compare "$node_version" "$required_version"; then
            print_success "Node.js found (version: $node_version)"

            # Check npm
            if command -v npm &> /dev/null; then
                local npm_version=$(npm --version 2>&1)
                print_success "npm found (version: $npm_version)"
            else
                print_warning "npm not found - will install with Node.js"
                return 1
            fi
            return 0
        else
            print_warning "Node.js version $node_version is too old (required: $required_version+)"
            return 1
        fi
    else
        print_warning "Node.js not found (required: $required_version+)"
        return 1
    fi
}

# FFmpeg checking
check_ffmpeg() {
    print_status "Checking FFmpeg installation..."

    if command -v ffmpeg &> /dev/null; then
        local ffmpeg_version=$(ffmpeg -version 2>&1 | head -n1 | cut -d' ' -f3)
        print_success "FFmpeg found (version: $ffmpeg_version)"
        return 0
    else
        print_warning "FFmpeg not found (required for audio processing)"
        return 1
    fi
}

# Install package manager if needed
install_package_manager() {
    case "$PLATFORM" in
        "macOS")
            if ! command -v brew &> /dev/null; then
                print_status "Installing Homebrew package manager..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                print_success "Homebrew installed"
            fi
            ;;
        "Windows")
            if [[ "$PACKAGE_MANAGER" == "manual" ]]; then
                print_warning "No package manager found. Attempting to install Chocolatey..."
                powershell.exe -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
                PACKAGE_MANAGER="chocolatey"
            fi
            ;;
    esac
}

# Install Python with comprehensive error handling
install_python() {
    print_status "Installing Python 3.8+..."
    local max_retries=3
    local attempt=1

    while [ $attempt -le $max_retries ]; do
        print_status "Installation attempt $attempt of $max_retries..."

        case "$PACKAGE_MANAGER" in
            "brew")
                # Try Python 3.11 first, fallback to latest
                if brew install python@3.11 2>/dev/null || brew install python 2>/dev/null; then
                    break
                else
                    print_warning "Homebrew installation failed (attempt $attempt)"
                fi
                ;;
            "apt")
                # Update package list with error handling
                if sudo apt update 2>/dev/null && sudo apt install -y python3 python3-pip python3-venv 2>/dev/null; then
                    break
                else
                    print_warning "APT installation failed (attempt $attempt)"
                    # Try to fix broken packages
                    sudo apt --fix-broken install -y 2>/dev/null
                fi
                ;;
            "yum")
                if sudo yum install -y python3 python3-pip 2>/dev/null; then
                    break
                else
                    print_warning "YUM installation failed (attempt $attempt)"
                    # Try EPEL repository
                    sudo yum install -y epel-release 2>/dev/null
                fi
                ;;
            "pacman")
                if sudo pacman -S --noconfirm python python-pip 2>/dev/null; then
                    break
                else
                    print_warning "Pacman installation failed (attempt $attempt)"
                    # Update package database
                    sudo pacman -Sy 2>/dev/null
                fi
                ;;
            "chocolatey")
                if choco install python -y 2>/dev/null; then
                    break
                else
                    print_warning "Chocolatey installation failed (attempt $attempt)"
                fi
                ;;
            "winget")
                if winget install Python.Python.3.11 --silent 2>/dev/null; then
                    break
                else
                    print_warning "Winget installation failed (attempt $attempt)"
                fi
                ;;
            *)
                print_error "Cannot install Python automatically on this system"
                print_status "Please install Python 3.8+ manually from https://python.org"
                return 1
                ;;
        esac

        attempt=$((attempt + 1))
        if [ $attempt -le $max_retries ]; then
            print_status "Waiting 5 seconds before retry..."
            sleep 5
        fi
    done

    if [ $attempt -gt $max_retries ]; then
        print_error "Python installation failed after $max_retries attempts"
        print_status "Manual installation required:"
        print_status "  - Download from https://python.org"
        print_status "  - Or use your system's GUI package manager"
        return 1
    fi

    # Verify installation
    sleep 2
    if check_python; then
        print_success "Python installation completed and verified"
    else
        print_error "Python installation completed but verification failed"
        print_status "You may need to restart your terminal or add Python to PATH"
        return 1
    fi
}

# Install Node.js
install_nodejs() {
    print_status "Installing Node.js 18+..."

    case "$PACKAGE_MANAGER" in
        "brew")
            brew install node
            ;;
        "apt")
            # Install NodeSource repository for latest Node.js
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            sudo apt-get install -y nodejs
            ;;
        "yum")
            # Install NodeSource repository
            curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
            sudo yum install -y nodejs npm
            ;;
        "pacman")
            sudo pacman -S nodejs npm
            ;;
        "chocolatey")
            choco install nodejs -y
            ;;
        "winget")
            winget install OpenJS.NodeJS
            ;;
        *)
            print_error "Cannot install Node.js automatically on this system"
            print_status "Please install Node.js 18+ from https://nodejs.org"
            return 1
            ;;
    esac

    print_success "Node.js installation completed"
}

# Install FFmpeg
install_ffmpeg() {
    print_status "Installing FFmpeg..."

    case "$PACKAGE_MANAGER" in
        "brew")
            brew install ffmpeg
            ;;
        "apt")
            sudo apt update
            sudo apt install -y ffmpeg
            ;;
        "yum")
            # Enable EPEL for FFmpeg
            sudo yum install -y epel-release
            sudo yum install -y ffmpeg
            ;;
        "pacman")
            sudo pacman -S ffmpeg
            ;;
        "chocolatey")
            choco install ffmpeg -y
            ;;
        "winget")
            winget install Gyan.FFmpeg
            ;;
        *)
            print_error "Cannot install FFmpeg automatically on this system"
            print_status "Please install FFmpeg manually from https://ffmpeg.org"
            return 1
            ;;
    esac

    print_success "FFmpeg installation completed"
}

# General error handling utilities
handle_critical_error() {
    local error_message="$1"
    local recovery_suggestion="$2"

    print_error "$error_message"
    if [[ -n "$recovery_suggestion" ]]; then
        print_status "Recovery suggestion: $recovery_suggestion"
    fi

    print_status "Common troubleshooting steps:"
    print_status "  1. Check internet connection"
    print_status "  2. Verify system permissions"
    print_status "  3. Try running with elevated privileges (if safe)"
    print_status "  4. Check available disk space"

    return 1
}

# Enhanced Python virtual environment setup
setup_python_env() {
    print_status "Setting up Python virtual environment..."

    # Check available disk space (minimum 500MB)
    if command -v df &> /dev/null; then
        local available_space=$(df . | awk 'NR==2 {print $4}')
        if [[ "$available_space" -lt 512000 ]]; then
            handle_critical_error "Insufficient disk space" "Free up at least 500MB of disk space"
            return 1
        fi
    fi

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."

        # Try multiple Python commands
        if python3 -m venv venv 2>/dev/null; then
            print_success "Virtual environment created with python3"
        elif python -m venv venv 2>/dev/null; then
            print_success "Virtual environment created with python"
        else
            # Fallback: try virtualenv
            if command -v virtualenv &> /dev/null; then
                virtualenv venv || {
                    handle_critical_error "Failed to create virtual environment" "Install python3-venv or virtualenv package"
                    return 1
                }
                print_success "Virtual environment created with virtualenv"
            else
                handle_critical_error "Failed to create virtual environment" "Install python3-venv package"
                return 1
            fi
        fi
    else
        print_status "Virtual environment already exists"
    fi

    # Verify virtual environment structure
    if [[ ! -f "venv/bin/activate" ]] && [[ ! -f "venv/Scripts/activate" ]]; then
        print_error "Virtual environment appears corrupted"
        print_status "Recreating virtual environment..."
        rm -rf venv
        python3 -m venv venv || {
            handle_critical_error "Failed to recreate virtual environment" "Try manual Python installation"
            return 1
        }
    fi

    # Activate virtual environment (cross-platform)
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
    elif [[ -f "venv/Scripts/activate" ]]; then
        source venv/Scripts/activate
    else
        handle_critical_error "Cannot activate virtual environment" "Virtual environment activation script not found"
        return 1
    fi

    # Verify activation
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        handle_critical_error "Virtual environment activation failed" "Check Python installation"
        return 1
    fi

    print_status "Installing Python dependencies..."

    # Upgrade pip first
    python -m pip install --upgrade pip 2>/dev/null || {
        print_warning "Failed to upgrade pip, continuing with current version"
    }

    # Install requirements with retry logic
    local max_attempts=3
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        print_status "Installing dependencies (attempt $attempt/$max_attempts)..."

        if pip install -r requirements.txt 2>/dev/null; then
            break
        else
            print_warning "Dependencies installation failed (attempt $attempt)"

            if [ $attempt -eq $max_attempts ]; then
                print_error "Failed to install Python dependencies after $max_attempts attempts"
                print_status "Try manually: pip install -r requirements.txt"
                return 1
            fi

            # Clean pip cache and retry
            pip cache purge 2>/dev/null
            sleep 2
        fi

        attempt=$((attempt + 1))
    done

    # Verify critical packages are installed
    print_status "Verifying critical packages..."
    python -c "import discord; print('discord.py version:', discord.__version__)" 2>/dev/null || {
        print_error "Critical package 'discord.py' not properly installed"
        return 1
    }

    print_success "Python environment setup complete"
}

# Enhanced Node.js dependencies setup
setup_nodejs_env() {
    print_status "Installing Node.js dependencies..."

    # Verify package.json exists
    if [[ ! -f "package.json" ]]; then
        handle_critical_error "package.json not found" "Ensure you're in the correct project directory"
        return 1
    fi

    # Clean install with error handling
    local max_attempts=3
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        print_status "Installing Node.js dependencies (attempt $attempt/$max_attempts)..."

        # Clear npm cache on retry
        if [ $attempt -gt 1 ]; then
            print_status "Clearing npm cache..."
            npm cache clean --force 2>/dev/null

            # Remove node_modules and package-lock for clean install
            if [ -d "node_modules" ]; then
                print_status "Removing corrupted node_modules..."
                rm -rf node_modules
            fi
            if [ -f "package-lock.json" ]; then
                rm -f package-lock.json
            fi
        fi

        # Install with better error detection and timeout handling
        print_status "Installing packages (this may take several minutes)..."

        # Create a background process for npm install with timeout
        if command -v timeout &> /dev/null; then
            # Use timeout command if available (Linux/some Unix)
            timeout 600s npm install --verbose 2>&1 | tee npm_install.log
            install_result=${PIPESTATUS[0]}
        elif command -v gtimeout &> /dev/null; then
            # Use gtimeout on macOS (if GNU coreutils installed)
            gtimeout 600s npm install --verbose 2>&1 | tee npm_install.log
            install_result=${PIPESTATUS[0]}
        else
            # Fallback: regular npm install without timeout
            npm install --verbose 2>&1 | tee npm_install.log
            install_result=$?
        fi

        if [ $install_result -eq 0 ]; then
            print_success "npm install completed successfully"
            break
        else
            print_warning "npm install failed (attempt $attempt)"

            # Analyze error log for specific issues
            if [ -f "npm_install.log" ]; then
                if grep -q "ENOENT" npm_install.log; then
                    print_status "Detected missing files/directories issue"
                elif grep -q "EACCES" npm_install.log; then
                    print_status "Detected permissions issue - you may need to fix npm permissions"
                elif grep -q "network" npm_install.log; then
                    print_status "Detected network issue - check internet connection"
                elif grep -q "timeout" npm_install.log; then
                    print_status "Detected timeout issue - packages taking too long to download"
                fi
            fi

            if [ $attempt -eq $max_attempts ]; then
                print_error "Failed to install Node.js dependencies after $max_attempts attempts"
                print_status ""
                print_status "🔧 Manual troubleshooting steps:"
                print_status "  1. Check internet connection"
                print_status "  2. npm cache clean --force"
                print_status "  3. rm -rf node_modules package-lock.json"
                print_status "  4. npm install --verbose"
                print_status "  5. If permissions issues: npm config set prefix ~/.npm-global"

                # Show last few lines of error log
                if [ -f "npm_install.log" ]; then
                    print_status ""
                    print_status "📋 Last error details:"
                    tail -10 npm_install.log | sed 's/^/  /'
                fi

                return 1
            fi

            sleep 10  # Longer delay between retries
        fi

        attempt=$((attempt + 1))
    done

    # Verify critical packages are installed
    print_status "Verifying critical Node.js packages..."

    if [[ ! -d "node_modules/discord.js" ]]; then
        print_error "Critical package 'discord.js' not installed"
        return 1
    fi

    if [[ ! -d "node_modules/prism-media" ]]; then
        print_error "Critical package 'prism-media' not installed"
        return 1
    fi

    # Run security audit with graceful handling
    print_status "Running security audit..."
    if npm audit --audit-level=moderate 2>/dev/null; then
        print_success "No security issues found"
    else
        local audit_exit_code=$?
        if [ $audit_exit_code -eq 1 ]; then
            print_warning "Some npm packages have security warnings"
            print_status "Consider running 'npm audit fix' when convenient"
        else
            print_warning "Security audit could not be completed"
        fi
    fi

    # Test Node.js can load main modules
    print_status "Testing Node.js module loading..."
    node -e "const { Client } = require('discord.js'); console.log('Discord.js loaded successfully');" 2>/dev/null || {
        print_error "Node.js modules failed to load properly"
        return 1
    }

    print_success "Node.js environment setup complete"
}

# Create platform-specific background service
create_background_service() {
    print_status "Setting up background service for your platform..."

    case "$PLATFORM" in
        "macOS")
            print_success "macOS background service ready (using run_bot_forever.sh)"
            ;;
        "Linux")
            create_systemd_service
            ;;
        "Windows"*)
            create_windows_service
            ;;
        *)
            print_warning "Background service setup not available for this platform"
            print_status "You can still run the bot manually with ./run_hybrid.sh"
            ;;
    esac
}

create_systemd_service() {
    print_status "Creating comprehensive systemd service for Linux background operation..."

    # Enhanced systemd service with full error handling and monitoring
    cat > "discord-audio-bot.service" << EOF
[Unit]
Description=Discord Audio Archive Bot - Hybrid Python/Node.js Service
Documentation=https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME
After=network-online.target
Wants=network-online.target
StartLimitBurst=3
StartLimitIntervalSec=60

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$(pwd)

# Environment variables
Environment=BACKGROUND_MODE=true
Environment=NODE_ENV=production
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=$(pwd)/.env

# Main execution
ExecStart=/bin/bash $(pwd)/run_hybrid.sh
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/bash -c 'pkill -f "python.*hybrid_bot.py"; pkill -f "node.*voice_recorder.js"'

# Restart configuration
Restart=always
RestartSec=10
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
TimeoutStartSec=60

# Resource limits (optimized for background operation)
MemoryLimit=256M
MemoryAccounting=yes
CPUQuota=50%
CPUAccounting=yes
TasksMax=50

# Security hardening
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=$(pwd) $(pwd)/recordings $(pwd)/logs
PrivateTmp=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictRealtime=yes
RestrictNamespaces=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=discord-audio-bot

[Install]
WantedBy=multi-user.target
EOF

    # Create installation helper script
    cat > "install_systemd_service.sh" << EOF
#!/bin/bash
# Discord Audio Archive Bot - Systemd Service Installer

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "\${GREEN}[INFO]\${NC} \$1"; }
print_warning() { echo -e "\${YELLOW}[WARNING]\${NC} \$1"; }
print_error() { echo -e "\${RED}[ERROR]\${NC} \$1"; }

# Check if running as root
if [[ \$EUID -eq 0 ]]; then
    print_error "Do not run as root! Run as the user who will own the bot process."
    exit 1
fi

print_status "Installing Discord Audio Archive Bot systemd service..."

# Check if service file exists
if [[ ! -f "discord-audio-bot.service" ]]; then
    print_error "Service file 'discord-audio-bot.service' not found"
    print_status "Run the setup script first: ./setup_universal.sh"
    exit 1
fi

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    print_warning ".env configuration file not found"
    print_status "Make sure to create .env with your Discord bot settings"
fi

# Copy service file to systemd directory
print_status "Installing service file..."
sudo cp discord-audio-bot.service /etc/systemd/system/ || {
    print_error "Failed to install service file"
    exit 1
}

# Set proper permissions
sudo chmod 644 /etc/systemd/system/discord-audio-bot.service

# Reload systemd
print_status "Reloading systemd daemon..."
sudo systemctl daemon-reload || {
    print_error "Failed to reload systemd daemon"
    exit 1
}

# Enable service
print_status "Enabling Discord Audio Archive Bot service..."
sudo systemctl enable discord-audio-bot || {
    print_error "Failed to enable service"
    exit 1
}

print_status "✅ Systemd service installed successfully!"
echo
print_status "🚀 Available commands:"
echo "  Start:   sudo systemctl start discord-audio-bot"
echo "  Stop:    sudo systemctl stop discord-audio-bot"
echo "  Restart: sudo systemctl restart discord-audio-bot"
echo "  Status:  sudo systemctl status discord-audio-bot"
echo "  Logs:    sudo journalctl -u discord-audio-bot -f"
echo
print_status "🔧 The service is enabled and will start automatically on boot"
print_status "📊 Monitor resource usage: systemctl show discord-audio-bot"
EOF

    chmod +x install_systemd_service.sh

    # Create service management helper
    cat > "manage_service.sh" << EOF
#!/bin/bash
# Discord Audio Archive Bot - Service Management Helper

case "\$1" in
    start)
        echo "🚀 Starting Discord Audio Archive Bot..."
        sudo systemctl start discord-audio-bot
        echo "✅ Service started"
        ;;
    stop)
        echo "⏹️ Stopping Discord Audio Archive Bot..."
        sudo systemctl stop discord-audio-bot
        echo "✅ Service stopped"
        ;;
    restart)
        echo "🔄 Restarting Discord Audio Archive Bot..."
        sudo systemctl restart discord-audio-bot
        echo "✅ Service restarted"
        ;;
    status)
        echo "📊 Discord Audio Archive Bot Status:"
        sudo systemctl status discord-audio-bot --no-pager
        ;;
    logs)
        echo "📋 Discord Audio Archive Bot Logs (Press Ctrl+C to exit):"
        sudo journalctl -u discord-audio-bot -f --no-pager
        ;;
    install)
        echo "📦 Installing systemd service..."
        ./install_systemd_service.sh
        ;;
    uninstall)
        echo "🗑️ Uninstalling systemd service..."
        sudo systemctl stop discord-audio-bot 2>/dev/null || true
        sudo systemctl disable discord-audio-bot 2>/dev/null || true
        sudo rm -f /etc/systemd/system/discord-audio-bot.service
        sudo systemctl daemon-reload
        echo "✅ Service uninstalled"
        ;;
    *)
        echo "Discord Audio Archive Bot - Service Manager"
        echo "Usage: \$0 {start|stop|restart|status|logs|install|uninstall}"
        echo
        echo "Commands:"
        echo "  start     - Start the bot service"
        echo "  stop      - Stop the bot service"
        echo "  restart   - Restart the bot service"
        echo "  status    - Show service status"
        echo "  logs      - Show live logs"
        echo "  install   - Install systemd service"
        echo "  uninstall - Remove systemd service"
        exit 1
        ;;
esac
EOF

    chmod +x manage_service.sh

    print_success "Enhanced systemd service created with management tools!"
    echo
    print_status "📁 Created files:"
    print_status "  • discord-audio-bot.service - Systemd service definition"
    print_status "  • install_systemd_service.sh - Service installer"
    print_status "  • manage_service.sh - Service management helper"
    echo
    print_status "🚀 Quick start:"
    echo "  1. ./install_systemd_service.sh      # Install service"
    echo "  2. ./manage_service.sh start         # Start bot"
    echo "  3. ./manage_service.sh status        # Check status"
    echo "  4. ./manage_service.sh logs          # View logs"
}

create_windows_service() {
    print_status "Creating Windows service script..."

    # Create PowerShell service script
    cat > "install_windows_service.ps1" << 'EOF'
# Discord Audio Archive Bot - Windows Service Installer
# Run as Administrator

$serviceName = "DiscordAudioBot"
$serviceDisplayName = "Discord Audio Archive Bot"
$servicePath = "$(Get-Location)\run_bot_forever.bat"

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run as Administrator" -ForegroundColor Red
    exit 1
}

# Create the service
New-Service -Name $serviceName -BinaryPathName $servicePath -DisplayName $serviceDisplayName -StartupType Automatic

Write-Host "Windows service created successfully!" -ForegroundColor Green
Write-Host "Service name: $serviceName" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start: Start-Service $serviceName" -ForegroundColor Yellow
Write-Host "To stop:  Stop-Service $serviceName" -ForegroundColor Yellow
EOF

    print_success "Windows service installer created: install_windows_service.ps1"
    print_status "Run as Administrator in PowerShell to install the service"
}

# Configuration setup
setup_configuration() {
    print_status "Setting up configuration..."

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            chmod 600 .env
            print_success "Configuration file created from template"
            print_warning "Please edit .env with your Discord bot token and settings"
        else
            print_error ".env.example not found"
            return 1
        fi
    else
        print_success "Configuration file already exists"
    fi

    # Create recordings directory
    mkdir -p recordings
    print_success "Recordings directory ready"
}

# Main installation flow
main() {
    echo "🔍 PHASE 1: Platform Detection & Requirements Check"
    echo "================================================"
    detect_platform
    check_package_manager_versions

    # Check current installations
    python_ok=false
    nodejs_ok=false
    ffmpeg_ok=false

    check_python && python_ok=true
    check_nodejs && nodejs_ok=true
    check_ffmpeg && ffmpeg_ok=true

    echo
    echo "🔧 PHASE 2: Dependency Installation"
    echo "==================================="

    # Install package manager if needed
    install_package_manager

    # Install missing dependencies
    if [[ "$python_ok" == false ]]; then
        install_python
        # Re-check after installation
        check_python || {
            print_error "Python installation failed"
            exit 1
        }
    fi

    if [[ "$nodejs_ok" == false ]]; then
        install_nodejs
        # Re-check after installation
        check_nodejs || {
            print_error "Node.js installation failed"
            exit 1
        }
    fi

    if [[ "$ffmpeg_ok" == false ]]; then
        install_ffmpeg
        # Re-check after installation
        check_ffmpeg || {
            print_error "FFmpeg installation failed"
            exit 1
        }
    fi

    echo
    echo "📦 PHASE 3: Environment Setup"
    echo "============================="

    setup_python_env
    setup_nodejs_env
    setup_configuration

    echo
    echo "🚀 PHASE 4: Background Service Setup"
    echo "===================================="

    create_background_service

    echo
    echo "✅ SETUP COMPLETE!"
    echo "=================="
    print_success "Discord Audio Archive Bot is ready to use!"
    echo
    echo "🎯 Next Steps:"
    case "$PLATFORM" in
        "macOS")
            echo "   1. Edit .env with your Discord bot token"
            echo "   2. Run: ./run_bot_forever.sh"
            ;;
        "Linux")
            echo "   1. Edit .env with your Discord bot token"
            echo "   2. Install systemd service (see instructions above)"
            echo "   3. Or run manually: ./run_hybrid.sh"
            ;;
        "Windows"*)
            echo "   1. Edit .env with your Discord bot token"
            echo "   2. Install Windows service (see instructions above)"
            echo "   3. Or run manually: ./run_hybrid.sh"
            ;;
        *)
            echo "   1. Edit .env with your Discord bot token"
            echo "   2. Run: ./run_hybrid.sh"
            ;;
    esac
    echo
    print_success "🎵 Happy recording! Remember to get proper consent first."
}

# Security check - don't run as root/administrator
if [[ "$EUID" -eq 0 ]] && [[ "$PLATFORM" != "Windows"* ]]; then
    print_error "Do not run as root for security reasons!"
    exit 1
fi

# Run main installation
main "$@"
