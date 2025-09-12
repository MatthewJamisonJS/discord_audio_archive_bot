#!/bin/bash

# Discord Audio Archive Bot - Hybrid Runner
# =========================================
# This script runs both Python and Node.js components simultaneously

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

echo "🎵 Discord Audio Archive Bot - Hybrid Mode"
echo "========================================="
echo

# Check if we're in the correct directory
if [ ! -f "hybrid_bot.py" ] || [ ! -f "voice_recorder.js" ]; then
    print_error "Required files not found. Please run this script from the audio_archive_bot directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check Node.js and npm
print_status "Checking Node.js environment..."
if ! command -v node &> /dev/null; then
    print_error "Node.js not found. Please install Node.js"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm not found. Please install npm"
    exit 1
fi

node_version=$(node --version)
print_success "Node.js version: $node_version"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
fi

# Check FFmpeg
print_status "Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    print_error "FFmpeg not found. Please install FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    exit 1
fi

ffmpeg_version=$(ffmpeg -version | head -n1 | cut -d' ' -f3)
print_success "FFmpeg version: $ffmpeg_version"

# Activate virtual environment
print_status "Activating Python virtual environment..."
source venv/bin/activate

# Verify virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

print_success "Virtual environment activated: $VIRTUAL_ENV"

# Check Python dependencies
print_status "Checking Python dependencies..."
if python -c "import discord; print(f'Discord version: {discord.__version__}')" 2>/dev/null; then
    discord_version=$(python -c "import discord; print(discord.__version__)")
    print_success "Discord module found (version $discord_version)"
else
    print_error "Discord module not found. Installing..."
    pip install -r requirements.txt
fi

# Check if .env file exists and has content
print_status "Checking configuration..."
if [ ! -f ".env" ]; then
    print_error ".env file not found"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning "Created .env from template. Please edit with your credentials:"
        print_status "Required: DISCORD_TOKEN, TARGET_USER_ID"
        print_status "Optional: EMAIL_USER, EMAIL_PASS, EMAIL_RECIPIENT"
        echo
        read -p "Continue with default values? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Edit .env file and run this script again."
            exit 1
        fi
    else
        print_error ".env.example not found. Please check your installation."
        exit 1
    fi
fi

# Create recordings directory
print_status "Creating recordings directory..."
mkdir -p recordings

# Function to handle cleanup
cleanup() {
    print_status "Shutting down..."
    if [ ! -z "$PYTHON_PID" ]; then
        kill $PYTHON_PID 2>/dev/null || true
    fi
    if [ ! -z "$NODE_PID" ]; then
        kill $NODE_PID 2>/dev/null || true
    fi
    # Clean up any remaining processes
    pkill -f "python.*hybrid_bot.py" 2>/dev/null || true
    pkill -f "node.*voice_recorder.js" 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo
print_success "🚀 Starting Hybrid Discord Bot..."
echo "=====================================0"
print_status "Python component: Event monitoring and logic"
print_status "Node.js component: Voice recording and processing"
print_status "Press Ctrl+C to stop both components"
echo

# Start Node.js voice recorder in background
print_status "Starting Node.js voice recorder..."
node voice_recorder.js &
NODE_PID=$!

# Give Node.js time to start
sleep 2

# Start Python event monitor
print_status "Starting Python event monitor..."
python hybrid_bot.py &
PYTHON_PID=$!

# Wait for both processes
wait $PYTHON_PID $NODE_PID
