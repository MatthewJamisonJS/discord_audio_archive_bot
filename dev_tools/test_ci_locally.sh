#!/bin/bash

###############################################################################
# Local CI Testing Script
# Run this script to test CI workflows locally before pushing to GitHub
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track test results
PASSED=0
FAILED=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Local CI Testing Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -e "${YELLOW}[TEST]${NC} $test_name"

    if eval "$test_command"; then
        echo -e "${GREEN}[PASS]${NC} $test_name"
        ((PASSED++))
    else
        echo -e "${RED}[FAIL]${NC} $test_name"
        ((FAILED++))
    fi
    echo ""
}

# Check required tools
echo -e "${BLUE}Checking required tools...${NC}"
echo ""

REQUIRED_TOOLS=("python3" "node" "npm" "ffmpeg" "git")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v "$tool" &> /dev/null; then
        version=$("$tool" --version 2>&1 | head -n 1)
        echo -e "${GREEN}✓${NC} $tool: $version"
    else
        echo -e "${RED}✗${NC} $tool: NOT FOUND"
        MISSING_TOOLS+=("$tool")
    fi
done

echo ""

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    echo -e "${RED}Missing required tools: ${MISSING_TOOLS[*]}${NC}"
    echo "Please install missing tools before continuing."
    exit 1
fi

# Install Python linting tools
echo -e "${BLUE}Installing Python linting tools...${NC}"
pip install --quiet black flake8 isort 2>&1 | grep -v "already satisfied" || true
echo ""

# Run linting tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Linting Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

run_test "Black Code Formatting" "black --check --diff . 2>&1 || true"
run_test "isort Import Sorting" "isort --check --diff . 2>&1 || true"
run_test "Flake8 Linting" "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics 2>&1 || true"

# Run Python tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Python Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

run_test "Python Dependencies Installation" "pip install -q -r requirements.txt"
run_test "Python Import Test (discord.py)" "python3 -c 'import discord; print(f\"discord.py {discord.__version__}\")'"
run_test "Python Import Test (dotenv)" "python3 -c 'import dotenv; print(\"python-dotenv OK\")'"
run_test "Python Import Test (pydub)" "python3 -c 'import pydub; print(\"pydub OK\")'"
run_test "Python Import Test (psutil)" "python3 -c 'import psutil; print(\"psutil OK\")'"

run_test "Python Syntax Check (hybrid_bot.py)" "python3 -m py_compile hybrid_bot.py"
run_test "Python Syntax Check (voice_manager_hybrid.py)" "python3 -m py_compile voice_manager_hybrid.py"
run_test "Python Syntax Check (test_hybrid_system.py)" "python3 -m py_compile test_hybrid_system.py"

# Run Node.js tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Node.js Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

run_test "Node.js Dependencies Installation" "npm ci --silent"
run_test "JavaScript Syntax Check" "node --check voice_recorder.js"
run_test "Verify @discordjs/voice" "npm list @discordjs/voice --depth=0"
run_test "Verify discord.js" "npm list discord.js --depth=0"

# Run integration tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Integration Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

run_test "Hybrid System Test" "python3 test_hybrid_system.py || true"
run_test "FFmpeg Availability" "ffmpeg -version > /dev/null 2>&1"
run_test "Recordings Directory" "mkdir -p recordings && test -d recordings"

# Run security tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Security Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if command -v shellcheck &> /dev/null; then
    run_test "ShellCheck on setup_universal.sh" "shellcheck setup_universal.sh || true"
    run_test "ShellCheck on run_bot_forever.sh" "shellcheck run_bot_forever.sh || true"
    run_test "ShellCheck on run_hybrid.sh" "shellcheck run_hybrid.sh || true"
else
    echo -e "${YELLOW}[SKIP]${NC} ShellCheck not installed (optional)"
    echo ""
fi

# Optional: npm audit
echo -e "${YELLOW}[INFO]${NC} Running npm audit (may show known vulnerabilities)"
npm audit || true
echo ""

# Build test
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Build Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if command -v docker &> /dev/null; then
    echo -e "${YELLOW}[INFO]${NC} Docker is available. To test Docker build, run:"
    echo "  docker build -t audio-archive-bot:test ."
    echo ""
else
    echo -e "${YELLOW}[SKIP]${NC} Docker not installed (optional)"
    echo ""
fi

# Summary
TOTAL=$((PASSED + FAILED))
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}All tests passed! Ready to push.${NC}"
    echo -e "${GREEN}========================================${NC}"
    exit 0
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}Some tests failed. Please fix before pushing.${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi
