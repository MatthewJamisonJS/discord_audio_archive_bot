# Audio Archive Bot - Modern Python Packaging Guide

This project now uses modern Python packaging standards (PEP 621) with `pyproject.toml`.

## Package Structure

```
audio_archive_bot/
├── audio_archive_bot/          # Main Python package
│   ├── __init__.py            # Package initialization and exports
│   ├── __main__.py            # Entry point for `python -m audio_archive_bot`
│   ├── cli.py                 # CLI entry point
│   ├── hybrid_bot.py          # Main bot implementation
│   └── voice_manager_hybrid.py # Voice management IPC interface
├── pyproject.toml             # Modern packaging configuration (PEP 621)
├── MANIFEST.in                # Additional files to include in distribution
├── setup.py                   # Legacy setup for backward compatibility
├── requirements.txt           # Development reference (deprecated)
├── voice_recorder.js          # Node.js voice recording component
├── package.json               # Node.js dependencies
└── [root-level files]         # Original files (kept for backward compatibility)
```

## Installation

### Development Installation (Recommended)

Install in editable mode for active development:

```bash
# From the project root directory
pip3 install -e .

# Or with development dependencies
pip3 install -e ".[dev]"
```

### Production Installation

Install as a regular package:

```bash
pip3 install .

# Or from a git repository
pip3 install git+https://github.com/MatthewJamisonJS/discord_audio_archive_bot.git
```

### Verify Installation

```bash
# Check that the package is installed
pip3 show audio-archive-bot

# Check the command is available
which audio_bot_run

# Check the version
python3 -c "import audio_archive_bot; print(audio_archive_bot.__version__)"
```

## Running the Bot

### Method 1: Using the CLI Command (Recommended)

After installation, you can run the bot using the `audio_bot_run` command:

```bash
audio_bot_run
```

This is the modern, user-friendly way to start the bot.

### Method 2: Using Python Module

Run the bot as a Python module:

```bash
python3 -m audio_archive_bot
```

### Method 3: Traditional Method (Backward Compatible)

The original methods still work:

```bash
# Direct execution
python3 hybrid_bot.py

# Using the shell script
./run_hybrid.sh

# Background mode
./run_bot_forever.sh
```

## Configuration

Before running the bot, ensure you have configured your environment:

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```bash
   DISCORD_TOKEN=your_bot_token_here
   TARGET_USER_ID=user_id_to_monitor
   # Optional email configuration
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASS=your-app-password
   EMAIL_RECIPIENT=where-to-send@email.com
   ```

## Development

### Installing Development Dependencies

```bash
# Install with all development tools
pip3 install -e ".[dev]"
```

This includes:
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `bandit` - Security analysis
- `pytest` - Testing framework
- `pre-commit` - Git hooks

### Code Quality Tools

```bash
# Format code with Black
black audio_archive_bot/

# Sort imports with isort
isort audio_archive_bot/

# Lint with flake8
flake8 audio_archive_bot/

# Security check with bandit
bandit -r audio_archive_bot/

# Run all checks
black --check audio_archive_bot/ && \
isort --check audio_archive_bot/ && \
flake8 audio_archive_bot/ && \
bandit -r audio_archive_bot/
```

### Testing

```bash
# Run tests (when available)
pytest

# With coverage
pytest --cov=audio_archive_bot --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Pre-commit Hooks

Set up pre-commit hooks for automatic code quality checks:

```bash
pre-commit install
pre-commit run --all-files
```

## Building Distribution Packages

### Source Distribution

```bash
python3 -m build --sdist
```

### Wheel Distribution

```bash
python3 -m build --wheel
```

### Both

```bash
pip3 install build
python3 -m build
```

The built packages will be in the `dist/` directory.

## Publishing to PyPI

### Test PyPI (Recommended First)

```bash
# Install twine
pip3 install twine

# Upload to Test PyPI
python3 -m twine upload --repository testpypi dist/*

# Test installation
pip3 install --index-url https://test.pypi.org/simple/ audio-archive-bot
```

### Production PyPI

```bash
# Upload to PyPI
python3 -m twine upload dist/*

# Install from PyPI
pip3 install audio-archive-bot
```

## Uninstallation

```bash
pip3 uninstall audio-archive-bot
```

## Package Information

### Metadata

- **Name**: audio-archive-bot
- **Version**: 0.1.0
- **License**: MIT
- **Python**: >=3.8

### Dependencies

**Required**:
- discord.py[voice] >= 2.6.3
- python-dotenv >= 1.0.0
- pydub >= 0.25.1
- psutil >= 5.9.0

**Development** (optional):
- black >= 24.10.0
- isort >= 5.13.2
- flake8 >= 7.1.1
- bandit >= 1.7.10
- pytest >= 8.0.0
- pre-commit >= 4.0.0

### Entry Points

The package provides the following console commands:

- `audio_bot_run` - Main CLI entry point to start the bot

## Troubleshooting

### Import Errors

If you get import errors, ensure the package is installed:

```bash
pip3 install -e .
```

### Command Not Found

If `audio_bot_run` is not found, ensure your Python scripts directory is in PATH:

```bash
# Check where pip installs scripts
python3 -m site --user-base

# Add to PATH (macOS/Linux)
export PATH="$PATH:$(python3 -m site --user-base)/bin"

# Or use the full path
$(python3 -m site --user-base)/bin/audio_bot_run
```

### Missing Dependencies

Reinstall with dependencies:

```bash
pip3 uninstall audio-archive-bot
pip3 install -e ".[dev]"
```

## Migration from Old Setup

If you were using the old setup, here's how to migrate:

### Before (Old Method)

```bash
pip3 install -r requirements.txt
python3 hybrid_bot.py
```

### After (New Method)

```bash
pip3 install -e .
audio_bot_run
```

The old method still works for backward compatibility!

## Node.js Integration

The bot requires Node.js for voice recording. After Python package installation:

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Run the Node.js voice recorder (in a separate terminal):
   ```bash
   node voice_recorder.js
   ```

3. Or use the hybrid shell script:
   ```bash
   ./run_hybrid.sh
   ```

## Additional Resources

- **PEP 621**: https://peps.python.org/pep-0621/
- **Packaging Tutorial**: https://packaging.python.org/tutorials/packaging-projects/
- **pyproject.toml Guide**: https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
