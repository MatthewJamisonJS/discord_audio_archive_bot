# Contributing to Discord Audio Archive Bot

Thank you for your interest in contributing to the Discord Audio Archive Bot! This project is designed with security and privacy at its core, so all contributions must adhere to strict security guidelines.

## 🛡️ Security-First Development

### Before You Start
- **Review**: Read our [SECURITY.md](SECURITY.md) policy thoroughly
- **Understand**: This bot handles sensitive voice recordings and credentials
- **Compliance**: Ensure familiarity with privacy laws (GDPR, CCPA, etc.)
- **Consent**: Never test with real user data without explicit consent

### Security Requirements
All contributions must:
- ✅ Never expose credentials in code, logs, or error messages
- ✅ Validate all inputs and sanitize outputs
- ✅ Follow principle of least privilege
- ✅ Include comprehensive error handling
- ✅ Pass security review before merging

## 🚀 Getting Started

### Development Environment Setup
```bash
# Fork and clone the repository
git clone https://github.com/MatthewJamisonJS/discord_audio_archive_bot.git
cd discord-audio-archive-bot

# Create development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install development dependencies (includes pre-commit, black, flake8, etc.)
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# (Optional) Run pre-commit on all files to verify setup
pre-commit run --all-files

# Run diagnostics
python troubleshoot.py

# Run integration tests
python test_integration.py
```

### Development Prerequisites
- **macOS** (primary support platform)
- **Python 3.8+**
- **FFmpeg** installed via Homebrew
- **Test Discord server** (for safe testing)
- **Gmail test account** with App Password

## 🛠️ Code Quality Tools

This project uses automated code quality tools to maintain consistency and catch issues early.

### Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality. The hooks include:

**Python Tools:**
- **Black**: Automatic code formatting (100 character line length)
- **isort**: Import sorting (compatible with Black)
- **Flake8**: Code linting for style and logical errors
- **Bandit**: Security vulnerability scanning

**General File Checks:**
- Trailing whitespace removal
- End-of-file newline enforcement
- YAML/JSON syntax validation
- Merge conflict detection
- Large file prevention (>500KB)
- Private key detection
- Dependency security scanning

### Using Pre-commit Hooks

```bash
# Install hooks (one-time setup)
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run bandit --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Bypass hooks (use sparingly!)
git commit --no-verify -m "Emergency fix"
```

### Code Style Configuration

The project uses these settings for consistency:
- **Line length**: 100 characters (Black and Flake8)
- **Python version**: 3.8+ compatible
- **Import style**: Black-compatible isort
- **Security**: Bandit in light mode to avoid false positives

All configuration is in:
- `/Users/wwjd_._/Code/audio_archive_bot/.pre-commit-config.yaml` - Pre-commit hook configuration
- `/Users/wwjd_._/Code/audio_archive_bot/pyproject.toml` - Black, isort, and Bandit settings
- `/Users/wwjd_._/Code/audio_archive_bot/.flake8` - Flake8 configuration

### Automated Dependency Updates

**Dependabot** monitors dependencies and creates automated pull requests:

- **Python (pip)**: Weekly checks for `requirements.txt` updates
- **Node.js (npm)**: Weekly checks for `package.json` updates
- **GitHub Actions**: Weekly checks for workflow updates
- **Schedule**: Mondays at 9:00 AM
- **PR Limit**: Maximum 5 open PRs per ecosystem

Configuration: `/Users/wwjd_._/Code/audio_archive_bot/.github/dependabot.yml`

## 📋 Contribution Types

### 🐛 Bug Reports
**Use GitHub Issues with the `bug` label**

Include:
- **Environment**: OS, Python version, dependency versions
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Logs**: Relevant log entries (sanitize any credentials!)
- **Impact**: Security implications if applicable

**Security bugs**: Follow responsible disclosure in [SECURITY.md](SECURITY.md)

### ✨ Feature Requests
**Use GitHub Discussions or Issues with `enhancement` label**

Include:
- **Use case**: Why is this needed?
- **Proposed solution**: How should it work?
- **Security implications**: Any privacy/security considerations
- **Alternatives considered**: Other approaches evaluated
- **Implementation complexity**: Rough effort estimate

### 🔧 Code Contributions

#### Pull Request Process
1. **Fork** the repository
2. **Branch** from `main`: `git checkout -b feature/your-feature-name`
3. **Develop** following our guidelines below
4. **Test** thoroughly with integration tests
5. **Document** any user-facing changes
6. **Security review** your own code first
7. **Submit** pull request with detailed description

#### Code Guidelines

**Python Code Style**
```python
# Follow existing patterns in bot.py
# Use type hints where appropriate
# Comprehensive error handling
# Descriptive variable names
# Security-first approach

def secure_function(user_input: str) -> bool:
    """
    Example function with proper security practices.
    
    Args:
        user_input: Validated input from user
        
    Returns:
        bool: Success status
        
    Raises:
        ValueError: For invalid input (sanitized message)
    """
    try:
        # Validate input
        if not isinstance(user_input, str) or len(user_input) == 0:
            raise ValueError("Invalid input provided")
            
        # Process safely
        result = process_input_safely(user_input)
        logger.info("Operation completed successfully")
        return True
        
    except Exception as e:
        # Log error without exposing sensitive data
        logger.error(f"Operation failed: {type(e).__name__}")
        return False
```

**Security Patterns**
```python
# ✅ Good: Environment variable usage
discord_token = os.getenv('DISCORD_TOKEN')
if not discord_token:
    logger.error("Missing required environment variable: DISCORD_TOKEN")
    raise ValueError("Missing required environment variable")

# ❌ Bad: Hardcoded credentials
discord_token = "MTIzNDU2Nzg5MA.GhIjKl.MnOpQrStUvWxYz"

# ✅ Good: Input validation
def validate_user_id(user_id: str) -> int:
    try:
        uid = int(user_id)
        if uid <= 0:
            raise ValueError("User ID must be positive")
        return uid
    except ValueError:
        logger.warning("Invalid user ID provided")
        raise

# ✅ Good: Error sanitization
except Exception as e:
    logger.error(f"Database operation failed: {type(e).__name__}")
    return {"error": "Operation failed", "details": None}
```

**Testing Requirements**
All code changes must include:
```python
# Update test_integration.py with new test cases
def test_your_feature(self):
    """Test the new feature with comprehensive scenarios."""
    # Test normal operation
    assert your_feature_works()
    
    # Test error conditions
    with pytest.raises(ExpectedError):
        your_feature_with_bad_input()
    
    # Test security boundaries
    assert not your_feature_leaks_credentials()
```

## 📚 Documentation

### Documentation Updates Required For
- New configuration options
- New commands or features
- Security-related changes
- Installation/setup changes
- Breaking changes

### Documentation Style
- **Clear and concise** language
- **Security warnings** where appropriate
- **Code examples** for complex features
- **Troubleshooting** for common issues
- **Links to relevant resources**

## 🔍 Review Process

### Automated Checks
All PRs must pass:
- ✅ Pre-commit hooks (Black, isort, Flake8, Bandit)
- ✅ Integration test suite
- ✅ Code style validation (100 char line length)
- ✅ Security linting (Bandit security scanner)
- ✅ YAML/JSON validation
- ✅ No trailing whitespace or merge conflicts

### Manual Review Focus Areas
- **Security implications** of changes
- **Privacy considerations** for new features
- **Error handling** completeness
- **Code maintainability** and clarity
- **Documentation** accuracy and completeness

### Review Timeline
- **Initial response**: Within 3 days
- **Full review**: Within 1 week
- **Security reviews**: May require additional time
- **Minor fixes**: Fast-tracked after approval

## 🚨 Security Review Checklist

Before submitting any PR, verify:

- [ ] No credentials or tokens in code
- [ ] All user inputs validated and sanitized
- [ ] Error messages don't leak sensitive information
- [ ] New dependencies are from trusted sources
- [ ] File permissions are restrictive where needed
- [ ] Network communications use encryption
- [ ] Logging doesn't expose credentials or personal data
- [ ] New features follow principle of least privilege

## 🎯 Priority Areas for Contribution

### High Priority
- **Security enhancements**: Additional safeguards
- **Error handling**: More robust error recovery
- **Performance optimization**: Memory usage, processing speed
- **Cross-platform support**: Windows, Linux compatibility
- **Documentation**: Setup guides, troubleshooting

### Medium Priority
- **Feature additions**: Multi-user support, cloud storage
- **User interface**: Web dashboard, better commands
- **Integration**: Webhooks, APIs, third-party services
- **Monitoring**: Health checks, metrics, alerting

### Low Priority
- **Code cleanup**: Refactoring, optimization
- **Testing**: Additional test coverage
- **Developer experience**: Better tooling, automation

## 🏷️ Issue and PR Labels

### Type Labels
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `security` - Security-related issues
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers

### Priority Labels
- `priority:high` - Critical issues
- `priority:medium` - Important improvements
- `priority:low` - Nice to have

### Status Labels
- `needs-review` - Ready for review
- `needs-work` - Changes requested
- `security-review` - Requires security review

## 📞 Getting Help

### Community Resources
- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **README.md**: Setup and usage documentation
- **SECURITY.md**: Security policies and reporting

### Maintainer Contact
For security-sensitive discussions or maintainer-only topics:
- **Email**: [maintainer-email@domain.com]
- **Security issues**: Follow responsible disclosure process
- **General questions**: Use GitHub Discussions first

## 🙏 Recognition

Contributors will be recognized in:
- **CHANGELOG.md**: Feature contributions
- **README.md**: Significant contributions
- **GitHub contributors**: All merged PRs
- **Release notes**: Notable improvements

## 📜 Legal

By contributing, you agree that:
- Your contributions will be licensed under the MIT License
- You have the right to submit the contributions
- You understand the security and privacy implications
- You will follow responsible disclosure for security issues

---

**Thank you for helping make Discord voice recording safer and more reliable!** 🎵🔒

*This project values security, privacy, and user consent above all else.*