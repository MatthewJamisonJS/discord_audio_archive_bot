#!/bin/bash
# Verification script for DevOps setup
# Checks that all configuration files are properly installed

set -e

echo "==================================================================="
echo "Audio Archive Bot - DevOps Setup Verification"
echo "==================================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ERRORS=0
WARNINGS=0

# Function to check file exists
check_file() {
    local file=$1
    local description=$2

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} Found: $description"
        return 0
    else
        echo -e "${RED}✗${NC} Missing: $description"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Function to check command exists
check_command() {
    local cmd=$1
    local description=$2

    if command -v "$cmd" &> /dev/null; then
        local version=$($cmd --version 2>&1 | head -1)
        echo -e "${GREEN}✓${NC} Found: $description - $version"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} Missing: $description (optional but recommended)"
        WARNINGS=$((WARNINGS + 1))
        return 1
    fi
}

echo "1. Checking Configuration Files..."
echo "-------------------------------------------------------------------"
check_file ".github/dependabot.yml" "Dependabot configuration"
check_file ".pre-commit-config.yaml" "Pre-commit hooks configuration"
check_file "pyproject.toml" "Python project configuration"
check_file ".flake8" "Flake8 configuration"
echo ""

echo "2. Checking Documentation..."
echo "-------------------------------------------------------------------"
check_file "CONTRIBUTING.md" "Contribution guidelines"
check_file "DEVELOPMENT.md" "Development quick reference"
check_file "SETUP_SUMMARY.md" "Setup summary documentation"
echo ""

echo "3. Checking Python Environment..."
echo "-------------------------------------------------------------------"
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment activated: $VIRTUAL_ENV"
else
    echo -e "${YELLOW}⚠${NC} No virtual environment detected"
    echo "   Run: python3 -m venv venv && source venv/bin/activate"
    WARNINGS=$((WARNINGS + 1))
fi

check_command "python3" "Python 3"
check_command "pip" "pip package manager"
echo ""

echo "4. Checking Development Tools..."
echo "-------------------------------------------------------------------"
check_command "black" "Black code formatter"
check_command "isort" "isort import sorter"
check_command "flake8" "Flake8 linter"
check_command "bandit" "Bandit security scanner"
check_command "pre-commit" "Pre-commit framework"
echo ""

echo "5. Checking Pre-commit Installation..."
echo "-------------------------------------------------------------------"
if [ -f ".git/hooks/pre-commit" ]; then
    echo -e "${GREEN}✓${NC} Pre-commit hooks installed"
else
    echo -e "${YELLOW}⚠${NC} Pre-commit hooks not installed"
    echo "   Run: pre-commit install"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

echo "6. Checking Node.js Environment..."
echo "-------------------------------------------------------------------"
check_command "node" "Node.js runtime"
check_command "npm" "npm package manager"
check_file "package.json" "Node.js package configuration"
echo ""

echo "7. Configuration Validation..."
echo "-------------------------------------------------------------------"

# Validate YAML files
if command -v python3 &> /dev/null; then
    if python3 -c "import yaml" 2>/dev/null; then
        for file in .github/dependabot.yml .pre-commit-config.yaml; do
            if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} Valid YAML: $file"
            else
                echo -e "${RED}✗${NC} Invalid YAML: $file"
                ERRORS=$((ERRORS + 1))
            fi
        done
    else
        echo -e "${YELLOW}⚠${NC} PyYAML not installed, skipping YAML validation"
        WARNINGS=$((WARNINGS + 1))
    fi
fi

# Validate pyproject.toml
if command -v python3 &> /dev/null; then
    if python3 -c "import tomli" 2>/dev/null || python3 -c "import tomllib" 2>/dev/null; then
        if python3 -c "try:
    import tomllib
except ImportError:
    import tomli as tomllib
with open('pyproject.toml', 'rb') as f:
    tomllib.load(f)" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Valid TOML: pyproject.toml"
        else
            echo -e "${RED}✗${NC} Invalid TOML: pyproject.toml"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo -e "${YELLOW}⚠${NC} tomli/tomllib not installed, skipping TOML validation"
        WARNINGS=$((WARNINGS + 1))
    fi
fi
echo ""

echo "==================================================================="
echo "Verification Summary"
echo "==================================================================="
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Setup verification passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Install dev dependencies: pip install -e \".[dev]\""
    echo "2. Install pre-commit hooks: pre-commit install"
    echo "3. Run pre-commit on all files: pre-commit run --all-files"
    echo "4. Commit configuration files to git"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Setup verification failed with $ERRORS error(s)${NC}"
    echo ""
    echo "Please review the errors above and fix them before proceeding."
    echo ""
    exit 1
fi
