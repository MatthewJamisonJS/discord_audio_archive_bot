# 🎙️ Discord Audio Archive Bot

![PyPI version](https://badge.fury.io/py/audio-archive-bot.svg)
![Python](https://img.shields.io/pypi/pyversions/audio-archive-bot)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![CI](https://github.com/MatthewJamisonJS/discord_audio_archive_bot/workflows/CI/badge.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Security](https://img.shields.io/badge/security-bandit-yellow.svg)

> **Preserve your Discord voice conversations with crystal-clear quality**

**Welcome! 👋** This intelligent bot automatically captures Discord voice conversations in professional-quality MP3 format. Perfect for preserving important meetings, memorable gaming sessions, or special moments with friends.

✨ **Set it up once, enjoy forever** — The bot quietly monitors Discord and handles everything automatically.

---

## 🚀 Quick Start (5 minutes!)

### What You Need
- Any computer (Windows, macOS, or Linux)
- Discord account
- Internet connection

### Option 0: Install via pip (Easiest) 🚀
```bash
# Install the package
pip3 install audio-archive-bot

# Run the bot
audio_bot_run
```
*(Installs everything automatically - Python package only)*

### Option 1: Universal Auto-Setup ⚡
```bash
curl -O https://raw.githubusercontent.com/MatthewJamisonJS/discord_audio_archive_bot/main/setup_universal.sh
chmod +x setup_universal.sh && ./setup_universal.sh
```
*(Detects your platform and installs everything automatically)*

### Option 2: Manual Setup 🔧
```bash
# 1. Download the project
git clone https://github.com/MatthewJamisonJS/discord_audio_archive_bot.git
cd discord-audio-archive-bot

# 2. Run setup script  
./setup_universal.sh
```
*(Installs Python, Node.js, FFmpeg, and all dependencies)*

### Option 3: Advanced Setup 🛠️
<details>
<summary>Click for manual installation steps</summary>

```bash
# Install dependencies manually
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install

# Configure your settings
cp .env.example .env
# Edit .env with your Discord bot token and settings

# Run in two terminals
python hybrid_bot.py        # Terminal 1: Event monitor
node voice_recorder.js      # Terminal 2: Voice processor
```
</details>

---

## 📋 Step-by-Step: What Happens When You Run It

### 1. **Initial Setup** 
- **Creates Discord bot connection** *(Uses your bot token to connect to Discord API)*
- **Monitors voice channel activity** *(Python component watches for voice state changes)*
- **Prepares audio processing pipeline** *(Node.js component initializes FFmpeg for recording)*

### 2. **Counter-Party Detection**
- **Watches for your counter-party** *(Monitors Discord events for specific user ID)*
- **Detects when they join ANY voice channel** *(Automatically scans all channels in your servers)*
- **Triggers recording sequence** *(Sends command from Python to Node.js via JSON file)*

### 3. **Automatic Recording**
- **Bot joins the voice channel** *(Connects using Discord's voice API)*
- **Starts capturing audio** *(Records at 48kHz stereo quality directly from Discord)*
- **Processes audio in real-time** *(Converts Opus codec to PCM then to MP3)*
- **Saves with smart filename** *(Format: `MM_DD_YYYY_HH-MM-SS_Username_UniqueID.mp3`)*

### 4. **Smart Management**
- **Follows user between channels** *(Automatically moves recording when counter-party switches channels)*
- **Stops when user leaves** *(Ends recording and finalizes MP3 file)*
- **Cleans up resources** *(Disconnects from voice, frees memory)*

### 5. **Optional Email Delivery**
- **Sends completed recording** *(Attaches MP3 to email with metadata)*
- **Includes recording details** *(Date, duration, username in email body)*
- **Falls back to local storage** *(Always saves locally even if email fails)*

---

## ⚙️ Configuration Guide

### Discord Bot Setup
1. **Go to [Discord Developer Portal](https://discord.com/developers/applications)**
2. **Create New Application** → Name it "Audio Archive Bot"
3. **Go to Bot section** → Click "Add Bot"
4. **Copy Token** → Paste into `.env` file as `DISCORD_TOKEN`
5. **Set Permissions** → Enable: Connect, Speak, Use Voice Activity *(Minimal permissions for security)*

### Counter-Party User Setup  
1. **Enable Developer Mode** *(Discord Settings → Advanced → Developer Mode)*
2. **Right-click counter-party user** → Copy ID
3. **Paste into `.env`** as `TARGET_USER_ID` *(Bot will only record this specific person)*

### Email Setup (Optional)
1. **Generate Gmail App Password** *(Not your regular password - use [App Passwords](https://myaccount.google.com/apppasswords))*
2. **Add to `.env`**:
   - `EMAIL_USER=your-email@gmail.com`
   - `EMAIL_PASS=your-app-password`
   - `EMAIL_RECIPIENT=where-to-send@email.com`

---

## 🎯 How Each Feature Works

### 🔍 **Smart Detection System**
The bot uses Discord's voice state events to monitor when your counter-party joins or leaves voice channels *(Python component listens to WebSocket events and processes them)*

### 🎙️ **High-Quality Recording**  
Audio is captured directly from Discord's voice gateway at 48kHz stereo, then processed through FFmpeg for optimal MP3 compression *(Node.js handles real-time audio streams with minimal latency)*

### 🔄 **Hybrid Architecture**
- **Python handles** Discord events, logic, and coordination *(Lightweight, efficient for monitoring)*
- **Node.js handles** voice connections and audio processing *(Optimized for real-time audio)*
- **JSON files enable** seamless communication between components *(Simple, reliable IPC mechanism)*

### 📁 **Intelligent File Management**
Files are automatically named with timestamps and usernames, stored locally first, then optionally emailed *(Ensures no recordings are lost)*

### 🛡️ **Security-First Design**
All credentials stay on your computer, no cloud services involved, minimal Discord permissions required *(Your data never leaves your control)*

---

## 🚀 Running Your Bot

### Quick Run (Recommended)
```bash
audio_bot_run
```
*(After pip installation)*

### Background Mode (Recommended)
```bash
# macOS/Linux
./run_bot_forever.sh
# Bot runs in background, survives restarts

# Windows
./run_bot_forever.bat
# Creates Windows service for background operation
```

### Manual Mode
```bash
# Run both components
./run_hybrid.sh
# Runs in foreground, shows all activity
```

### Service Mode (Linux)
```bash
# Install as system service
./install_systemd_service.sh

# Control the service
./manage_service.sh start|stop|restart|status|logs
```

---

## 💝 Responsible Use Guidelines

### 🤝 **Always Get Permission First**
This tool helps preserve meaningful conversations, but **consent is essential**:
- ✅ Ask everyone before recording
- ✅ Check your local laws (some require all-party consent)  
- ✅ Be transparent about recording
- ✅ Keep recordings secure and private
- ✅ Respect privacy and Discord's Terms of Service

*We built this to help communities preserve important moments — please use it responsibly and legally.* 💙

---

## 🔧 Troubleshooting

### Quick Health Check
```bash
python test_hybrid_system.py
# Runs 7 system tests to verify everything works
```

### Common Issues & Solutions

| Problem | Solution | How It Works |
|---------|----------|--------------|
| **"Bot not responding"** | Check Discord token in `.env` | *(Token authenticates bot with Discord API)* |
| **"No audio recorded"** | Verify bot has voice permissions | *(Needs Connect, Speak, Use Voice Activity permissions)* |
| **"Email not sending"** | Use Gmail App Password, not regular password | *(Gmail requires App Passwords for third-party apps)* |
| **"Python/Node.js not found"** | Run `./setup_universal.sh` again | *(Automatically installs missing dependencies)* |
| **"FFmpeg not working"** | Install FFmpeg: `brew install ffmpeg` (macOS) | *(Required for audio format conversion)* |
| **"Command not found: audio_bot_run"** | Install via pip: `pip3 install audio-archive-bot` | *(Creates console command in your PATH)* |

### Get Live Help
```bash
# View real-time logs
tail -f hybrid_bot.log              # Python component activity
tail -f background.log              # Background service logs  

# Check component status
python -c "from voice_manager_hybrid import HybridVoiceManager; print(HybridVoiceManager.get_status())"
```

---

## 🔬 Development Setup

Want to contribute or modify the bot? Here's how to set up a development environment:

```bash
# Clone the repository
git clone https://github.com/MatthewJamisonJS/discord_audio_archive_bot.git
cd audio-archive-bot

# Install in development mode with dev dependencies
pip3 install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
python test_hybrid_system.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 🌟 Contributing & Support

We'd love your help making this even better!

- **🐛 Found a bug?** → Use the Issues tab on this GitHub repository
- **💡 Have an idea?** → Submit a feature request via GitHub Issues
- **🔧 Want to contribute?** → See [CONTRIBUTING.md](CONTRIBUTING.md)
- **❓ Need help?** → Check the repository documentation and existing Issues

**⭐ Star this repo if it helped you!** It helps others find this project.

---

## 📊 System Requirements

| Component | Minimum | Recommended | Purpose |
|-----------|---------|-------------|---------|
| **Python** | 3.8+ | 3.11+ | *Event monitoring and coordination* |
| **Node.js** | 18+ | 20+ | *Voice processing and real-time audio* |
| **FFmpeg** | 4.0+ | Latest | *Audio format conversion and optimization* |
| **RAM** | 256MB | 512MB | *Audio buffering and processing* |
| **Storage** | 100MB + recordings | 1GB+ | *Application files and audio storage* |
| **Network** | Stable internet | Broadband | *Discord API connectivity* |

---

## 📝 License & Credits

**MIT License** — Use freely, modify as needed, share with friends!

**Special thanks to:**
- [Discord.js](https://discord.js.org/) & [Discord.py](https://discordpy.readthedocs.io/) communities
- [FFmpeg](https://ffmpeg.org/) for incredible audio processing  
- [Node.js](https://nodejs.org/) and [Python](https://python.org/) ecosystems
- Our amazing contributors and users 💙

---

<div align="center">

**Built with ❤️ for preserving precious moments**

*Start recording your Discord memories today!*

[🚀 Quick Start](#-quick-start-5-minutes) • [🔧 Troubleshooting](#-troubleshooting) • [🌟 Contributing](#-contributing--support)

</div>