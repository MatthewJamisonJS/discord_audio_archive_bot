# Audio Archive Bot - Quick Start Guide

## Installation (Choose One Method)

### Method 1: Interactive Installer (Easiest)
```bash
./install_package.sh
```
Follow the prompts to choose development or production installation.

### Method 2: Development Mode (Recommended for Contributors)
```bash
pip3 install -e .
```

### Method 3: Development with All Tools
```bash
pip3 install -e ".[dev]"
```

### Method 4: Production Mode
```bash
pip3 install .
```

## Configuration

1. **Create your environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   DISCORD_TOKEN=your_discord_bot_token_here
   TARGET_USER_ID=user_id_to_monitor
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

## Running the Bot

### Recommended Method
```bash
audio_bot_run
```

### Alternative Methods
```bash
# Using Python module
python3 -m audio_archive_bot

# Traditional method (still works)
python3 hybrid_bot.py

# With Node.js recorder (automated)
./run_hybrid.sh
```

## Verify Installation

```bash
# Check package is installed
pip3 show audio-archive-bot

# Check version
python3 -c "import audio_archive_bot; print(audio_archive_bot.__version__)"

# Verify command exists
which audio_bot_run
```

## Next Steps

- Read **README.md** for detailed bot functionality
- See **PACKAGING_GUIDE.md** for advanced packaging topics
- Check **CONTRIBUTING.md** if you want to contribute
- Review **PACKAGE_SUMMARY.md** for complete packaging overview

## Need Help?

- Run `./install_package.sh` for interactive installation
- Check existing documentation files
- Review GitHub issues
- Open a new issue with your question

---

**Version**: 0.1.0
**Python**: >=3.8
**Node.js**: >=18
**License**: MIT
