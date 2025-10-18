# Development Quick Reference

This document provides quick reference for common development tasks.

## Initial Setup

```bash
# 1. Clone and setup environment
git clone <repository-url>
cd audio_archive_bot
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"
npm install

# 3. Setup pre-commit hooks
pre-commit install

# 4. Verify setup
pre-commit run --all-files
```

## Daily Development Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Pull latest changes
git pull origin main

# 3. Create feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes
# ... edit files ...

# 5. Run pre-commit checks manually (optional)
pre-commit run --all-files

# 6. Commit (pre-commit runs automatically)
git add .
git commit -m "feat: your commit message"

# 7. Push changes
git push origin feature/your-feature-name
```

## Pre-commit Commands

```bash
# Install hooks (one-time)
pre-commit install

# Run all hooks on all files
pre-commit run --all-files

# Run all hooks on staged files only
pre-commit run

# Run specific hook
pre-commit run black
pre-commit run flake8
pre-commit run isort
pre-commit run bandit

# Update to latest versions
pre-commit autoupdate

# Skip hooks (emergency only)
git commit --no-verify -m "message"
```

## Code Quality Tools

### Black (Code Formatter)
```bash
# Format all Python files
black .

# Check what would be formatted
black --check .

# Format specific file
black bot.py
```

### isort (Import Sorter)
```bash
# Sort all imports
isort .

# Check without modifying
isort --check-only .

# Sort specific file
isort bot.py
```

### Flake8 (Linter)
```bash
# Lint all Python files
flake8 .

# Lint specific file
flake8 bot.py

# Show statistics
flake8 --statistics .
```

### Bandit (Security Scanner)
```bash
# Scan all files
bandit -r .

# Scan with config
bandit -r . -c pyproject.toml

# Scan specific file
bandit bot.py
```

## Testing

```bash
# Run integration tests
python test_integration.py

# Run diagnostics
python troubleshoot.py

# Check for dependency vulnerabilities
safety check -r requirements.txt
```

## Dependency Management

### Python Dependencies
```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Check for updates
pip list --outdated

# Install dev dependencies
pip install -e ".[dev]"
```

### Node.js Dependencies
```bash
# Install new package
npm install package-name

# Update all packages
npm update

# Check for vulnerabilities
npm audit
npm audit fix
```

### Dependabot
- Automatically creates PRs for updates weekly (Mondays)
- Check `.github/dependabot.yml` for configuration
- Review and merge Dependabot PRs regularly

## Configuration Files

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Pre-commit hook configuration |
| `pyproject.toml` | Python project config (Black, isort, Bandit) |
| `.flake8` | Flake8 linter configuration |
| `.github/dependabot.yml` | Automated dependency updates |
| `requirements.txt` | Python production dependencies |
| `package.json` | Node.js dependencies |

## Code Style Standards

- **Line length**: 100 characters
- **Python version**: 3.8+
- **Formatter**: Black (automatic)
- **Import style**: isort with Black profile
- **Linting**: Flake8 (compatible with Black)
- **Security**: Bandit scanning enabled

## Common Issues

### Pre-commit Hook Failures

**Black formatting issues:**
```bash
# Let Black fix automatically
black .
git add .
git commit -m "style: apply black formatting"
```

**Import sorting issues:**
```bash
# Let isort fix automatically
isort .
git add .
git commit -m "style: sort imports"
```

**Flake8 errors:**
```bash
# View errors
flake8 .

# Fix manually based on error messages
# Then commit changes
```

**Bandit security warnings:**
```bash
# Review warnings carefully
bandit -r .

# Fix security issues
# Add # nosec comment only if false positive
```

### Pre-commit Installation Issues

```bash
# Reinstall pre-commit
pip install --upgrade pre-commit
pre-commit clean
pre-commit install

# Clear cache
pre-commit clean
pre-commit run --all-files
```

### Dependency Conflicts

```bash
# Create fresh virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"
```

## Git Workflow

### Commit Message Format

```
<type>: <description>

[optional body]
[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `deps`: Dependency updates
- `ci`: CI/CD changes
- `security`: Security fixes

**Examples:**
```bash
git commit -m "feat: add multi-channel recording support"
git commit -m "fix: resolve audio corruption in long recordings"
git commit -m "docs: update installation instructions"
git commit -m "security: fix token exposure in error logs"
```

### Branch Naming

```
feature/description
fix/description
docs/description
refactor/description
```

**Examples:**
- `feature/multi-channel-recording`
- `fix/audio-corruption`
- `docs/update-readme`
- `refactor/audio-processing`

## Security Checklist

Before every commit, verify:

- [ ] No credentials in code (use environment variables)
- [ ] No tokens in logs or error messages
- [ ] All user inputs are validated
- [ ] Error messages don't leak sensitive data
- [ ] File permissions are restrictive
- [ ] Dependencies are up to date
- [ ] Bandit security scan passes
- [ ] No private keys or secrets committed

## Resources

- **Contributing Guide**: `CONTRIBUTING.md`
- **Security Policy**: `SECURITY.md`
- **README**: `README.md`
- **Pre-commit Docs**: https://pre-commit.com/
- **Black Docs**: https://black.readthedocs.io/
- **Flake8 Docs**: https://flake8.pycqa.org/
- **Bandit Docs**: https://bandit.readthedocs.io/

## Getting Help

1. Check this development guide
2. Review `CONTRIBUTING.md`
3. Search existing GitHub Issues
4. Ask in GitHub Discussions
5. Contact maintainers (security issues only)

---

**Remember**: Security first, code quality always, test thoroughly.
