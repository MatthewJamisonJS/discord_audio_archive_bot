#!/bin/bash

# Discord Audio Archive Bot - Background Service Manager
# Uses macOS best practices for minimal resource usage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="com.user.discord-audio-bot"
PLIST_FILE="$HOME/Library/LaunchAgents/${SERVICE_NAME}.plist"
PID_FILE="$BOT_DIR/bot.pid"

echo "🎵 Discord Audio Archive Bot - Background Service Setup"
echo "====================================================="
print_status "Setting up efficient background service with minimal resource usage..."

# Check if already running
check_service_status() {
    if launchctl list | grep -q "$SERVICE_NAME"; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Create optimized launchd service file
create_service_file() {
    print_status "Creating optimized macOS background service..."

    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Service Identity -->
    <key>Label</key>
    <string>${SERVICE_NAME}</string>

    <!-- Program Configuration -->
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${BOT_DIR}/background_runner.sh</string>
    </array>

    <!-- Working Directory -->
    <key>WorkingDirectory</key>
    <string>${BOT_DIR}</string>

    <!-- Auto-start and Keep Alive -->
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>

    <!-- Resource Optimization -->
    <key>ProcessType</key>
    <string>Background</string>
    <key>Nice</key>
    <integer>5</integer>

    <!-- Logging (Minimal) -->
    <key>StandardOutPath</key>
    <string>${BOT_DIR}/service.log</string>
    <key>StandardErrorPath</key>
    <string>${BOT_DIR}/service_error.log</string>

    <!-- Throttling for CPU efficiency -->
    <key>ThrottleInterval</key>
    <integer>10</integer>

    <!-- Environment Variables -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
        <key>NODE_ENV</key>
        <string>production</string>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
    </dict>

    <!-- Security -->
    <key>UserName</key>
    <string>$(whoami)</string>
</dict>
</plist>
EOF

    print_success "Service file created at: $PLIST_FILE"
}

# Create optimized background runner script
create_background_runner() {
    print_status "Creating resource-efficient background runner..."

    cat > "$BOT_DIR/background_runner.sh" << 'EOF'
#!/bin/bash

# Discord Audio Archive Bot - Optimized Background Runner
# Minimal resource usage with proper cleanup

BOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$BOT_DIR/bot.pid"
LOG_FILE="$BOT_DIR/background.log"

# Resource optimization
export NODE_OPTIONS="--max-old-space-size=128"  # Limit Node.js to 128MB
export PYTHONDONTWRITEBYTECODE=1                # No .pyc files
export PYTHONUNBUFFERED=1                      # Immediate output

# Function to log with timestamp
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Cleanup function
cleanup() {
    log_message "Cleaning up background processes..."

    # Kill child processes
    if [ -f "$PID_FILE" ]; then
        while read pid; do
            kill -TERM "$pid" 2>/dev/null || true
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi

    # Kill any remaining processes
    pkill -f "python.*hybrid_bot.py" 2>/dev/null || true
    pkill -f "node.*voice_recorder.js" 2>/dev/null || true

    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

cd "$BOT_DIR"

# Rotate logs to prevent disk space issues
if [ -f "$LOG_FILE" ] && [ $(wc -l < "$LOG_FILE") -gt 1000 ]; then
    tail -500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

log_message "Starting Discord Audio Archive Bot (Background Mode)"

# Start Python component with low priority and resource limits
(
    source venv/bin/activate 2>/dev/null || {
        log_message "ERROR: Virtual environment not found or broken"
        exit 1
    }

    # Verify Discord module is available
    python -c "import discord" 2>/dev/null || {
        log_message "ERROR: Discord module not found, attempting reinstall..."
        pip install -r requirements.txt || exit 1
    }

    ulimit -v 262144  # Limit virtual memory to 256MB
    nice -n 10 python hybrid_bot.py
) &
PYTHON_PID=$!
echo $PYTHON_PID >> "$PID_FILE"

# Give Python time to start
sleep 3

# Start Node.js component with resource limits
(
    ulimit -v 131072  # Limit virtual memory to 128MB
    nice -n 10 node voice_recorder.js
) &
NODE_PID=$!
echo $NODE_PID >> "$PID_FILE"

log_message "Started Python component (PID: $PYTHON_PID) and Node.js component (PID: $NODE_PID)"

# Monitor processes and restart if needed
while true do
    # Check if Python process is still running
    if ! kill -0 $PYTHON_PID 2>/dev/null; then
        log_message "Python component died, restarting..."
        (
            source venv/bin/activate 2>/dev/null || {
                log_message "ERROR: Virtual environment not available during restart"
                exit 1
            }

            # Verify dependencies are still available
            python -c "import discord" 2>/dev/null || {
                log_message "ERROR: Discord module missing during restart"
                exit 1
            }

            ulimit -v 262144
            nice -n 10 python hybrid_bot.py
        ) &
        PYTHON_PID=$!
        echo $PYTHON_PID >> "$PID_FILE"
    fi

    # Check if Node.js process is still running
    if ! kill -0 $NODE_PID 2>/dev/null; then
        log_message "Node.js component died, restarting..."
        (
            ulimit -v 131072
            nice -n 10 node voice_recorder.js
        ) &
        NODE_PID=$!
        echo $NODE_PID >> "$PID_FILE"
    fi

    # Sleep for 30 seconds before next check (low CPU usage)
    sleep 30
done
EOF

    chmod +x "$BOT_DIR/background_runner.sh"
    print_success "Background runner created with resource optimization"
}

# Ensure virtual environment exists and is working
ensure_venv() {
    print_status "Checking Python virtual environment..."

    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found. Creating it now..."
        python3 -m venv venv || {
            print_error "Failed to create virtual environment"
            exit 1
        }
    fi

    # Test if venv works and has required packages
    if ! source venv/bin/activate 2>/dev/null || ! python -c "import discord" 2>/dev/null; then
        print_warning "Virtual environment needs setup. Installing dependencies..."
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt || {
            print_error "Failed to install Python dependencies"
            exit 1
        }
    fi

    print_success "Python environment ready"
}

# Main execution
main() {
    # Ensure environment is ready first
    ensure_venv

    # Check if service is already running
    if check_service_status; then
        print_warning "Service is already running!"
        echo
        echo "Available commands:"
        echo "  ./run_bot_forever.sh stop     - Stop the service"
        echo "  ./run_bot_forever.sh restart  - Restart the service"
        echo "  ./run_bot_forever.sh status   - Check service status"
        echo "  ./run_bot_forever.sh logs     - View service logs"
        exit 0
    fi

    # Handle command line arguments
    case "${1:-start}" in
        "stop")
            print_status "Stopping background service..."
            launchctl unload "$PLIST_FILE" 2>/dev/null || true
            launchctl remove "$SERVICE_NAME" 2>/dev/null || true

            # Clean up any remaining processes
            pkill -f "python.*hybrid_bot.py" 2>/dev/null || true
            pkill -f "node.*voice_recorder.js" 2>/dev/null || true

            rm -f "$PID_FILE"
            print_success "Service stopped"
            exit 0
            ;;
        "restart")
            "$0" stop
            sleep 2
            "$0" start
            exit 0
            ;;
        "status")
            if check_service_status; then
                print_success "Service is running"
                echo "Logs: tail -f $BOT_DIR/background.log"
            else
                print_warning "Service is not running"
            fi
            exit 0
            ;;
        "logs")
            if [ -f "$BOT_DIR/background.log" ]; then
                tail -f "$BOT_DIR/background.log"
            else
                print_warning "No log file found"
            fi
            exit 0
            ;;
        "start")
            # Continue with setup
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Usage: $0 [start|stop|restart|status|logs]"
            exit 1
            ;;
    esac

    # Create LaunchAgents directory if it doesn't exist
    mkdir -p "$HOME/Library/LaunchAgents"

    # Create service files
    create_service_file
    create_background_runner

    # Load and start the service
    print_status "Loading background service..."
    launchctl load "$PLIST_FILE"

    # Wait a moment and check if it started
    sleep 3

    if check_service_status; then
        print_success "🎉 Success! Your Discord Audio Archive Bot is now running in the background!"
        echo
        echo "✨ What this means:"
        echo "   • The bot runs automatically even after you restart your computer"
        echo "   • It uses minimal CPU and RAM (optimized for background operation)"
        echo "   • You can close this Terminal window - the bot keeps working"
        echo "   • Logs are automatically rotated to save disk space"
        echo
        echo "📋 Useful commands:"
        echo "   ./run_bot_forever.sh status   - Check if it's running"
        echo "   ./run_bot_forever.sh logs     - View live activity"
        echo "   ./run_bot_forever.sh stop     - Stop the service"
        echo "   ./run_bot_forever.sh restart  - Restart if needed"
        echo
        print_success "Your bot is now watching for voice activity! 🎵"
    else
        print_error "Service failed to start. Check the logs:"
        echo "   tail -f $BOT_DIR/service_error.log"
        exit 1
    fi
}

main "$@"
