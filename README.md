# 🎙️ Discord Audio Archive Bot

>> **Preserve your**Preserve your Discord voice conversations withwith crystal-clear qualityquality**

**Welcome! 👋** This intelligent, intelligent bot automatically capturescaptures Discord voice conversations in professionalprofessional-quality MP3 format. Perfect for preserving important meetings, memorable gaming sessions, or specialspecial moments with friends.

✨ **Set**Set it up once, enjoy forever, enjoy forever** —  — The bot quietly quietly monitors Discord and handleshandles everythingeverything automaticallyautomatically.

---

## 🚀 Quick Start (3 minutes!5 minutes!)

### What You Need
- AnyAny computer with internet +(Windows, macOS, or Linux)
- Discord account
- Internet connection

### Option 1: Super Easy Setup
### Option 1: Universal Auto-Setup ⚡
```bash
curl -O https://raw.githubusercontent.com/[YOUR-USERNAME]/discord-audio-archive-bot/main/setup_universal.sh
chmod +x setup_universal.sh && ./setup_universal.sh
```
*(Detects your platform and installs everything automatically)*

### Option 2: Manual Setup 🔧
```bash
# 1. Download the project
git clone https://github.com/[YOUR-USERNAME]/discord-audio-archive-bot.git
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
 -O https://raw.githubusercontent.com/your-username/discord-audio-archive-bot/main/setup_universal.sh
chmod +x setup_universal.sh && ./setup_universal.sh
# Configure your settings

 .envDiscord bot token and 

# Run in two terminals        Terminal1:Event monitor      Terminal2: Voice processor
```

### Option 2: Traditional Setup  
1. **Download** → `git clone https://github.com/your-username/discord-audio-archive-bot.git`
2. **Setup** → `cd discord-audio-archive-bot && ./setup_universal.sh`  
3. **Configure** → Edit `.env` with your Discord bot token
4. **Run** → `./run_bot_forever.sh` (runs in background permanently)

**🎉 Done!** Your bot now intelligently monitors Discord and creates perfect recordings.

---

## 📋 Step-by-Step: What Happens When  This SpecialRun It

### 1. **Intelligent**Initial Setup** 
- Automatically detects**Creates Discord bot connection** *(Uses your bot token to connect to Discord API)*
- **Monitors voice channel activity** *(Python component watches for voice state changes)*
- **Prepares recording audio processing when they leave
- Zero manual intervention requiredpipeline** *(Node.js component initializes FFmpeg for recording)*

### 2. ****TargetDetection****Watches Audiofor Quality**  
- Records at Discord's native 48kHz stereoyour target person** *(Monitors Discord events for specific user ID)*
- Converts**Detects to optimized 256kbps MP3
- Crystal-clear audio that preserves every wordwhen they join ANY voice channel** *(Automatically scans all channels in your servers)*
- **Triggers recording sequence** *(Sends command from Python to Node.js via JSON file)*

### 3. **Seamless**Automatic Recording****
- Optional email**Bot joins the voice channel** *Connects using Discord's voice API*
- Smart**Starts filenamecapturing format:audio** `*(Records at 48kHz stereo quality directly from Discord)*
- **Processes audio in real-time** *(Converts Opus codec to PCM then to MP3)*
- **Saves with smart filename** *(Format: `MM_DD_YYYY_HH-MM-SS_Username_UniqueID.mp3`
- Local storage backup for reliability`)*

### 4. ****Smart-Management** Design**
- **Follows user between channels** *(Automatically moves recording when target switches channels)*
- No**Stops cloudwhen storage or third-party services
- You control everything

### 🌍 **Cross-Platform**
- **macOS**: Full support with background services
- **Linux**: Systemd integration  
- **Windows**: Service installation available
- **All platforms**: Manual mode always worksuser leaves** *(Ends recording and finalizes MP3 file)*
- **Cleans up resources** *(Disconnects from voice, frees memory)*

### 5. **Optional Email Delivery**
- **Sends completed recording** *(Attaches MP3 to email with metadata)*
- **Includes recording details** *(Date, duration, username in email body)*
- **Falls back to local storage** *(Always saves locally even if email fails)*
⚙️ConfigurationGuide###DiscordBotSetup1. **Go to [Discord Developer Portal](https://discord.com/developers/applications)**2. **Create New Application** → Name it "Audio Archive Bot"
3. **Go to secure and privateBot section** → Click "Add Bot"
4. **Copy Token** → Paste into `.env` file as `DISCORD_TOKEN`
5. **Set Permissions** → Enable: Connect, Speak, Use Voice Activity *(Minimal permissions for security)*

### Target User Setup  
1. **Enable Developer Mode** *(Discord Settings → Advanced → Developer Mode)*
2. **Right-click target user** → Copy ID
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
The bot uses Discord's voice state events to monitor when your target person joins or leaves voice channels *(Python component listens to WebSocket events and processes them)*

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

## 🔧 Need Help?

###### QuickQuick FixesHealthCheck
```bash
# Test everything is working
python test_hybrid_system.py
# Runs 7 system tests to verify everything works
```

### ### Common Issues & Solutions

| Problem | Solution | How It Works |
|---------|----------|--------------|
| **"Bot not responding"** | Check Discord token in `.env` | *(Token authenticates bot with Discord API)* |
| **"No audio recorded"** | Verify bot has voice permissions | *(Needs Connect, Speak, Use Voice Activity permissions)* |
| **"Email not sending"** | Use Gmail App Password, not regular password | *(Gmail requires App Passwords for third-party apps)* |
| **"Python/Node.js not found"** | Run `./setup_universal.sh` again | *(Automatically installs missing dependencies)* |
| **"FFmpeg not working"** | Install FFmpeg: `brew install ffmpeg` (macOS) | *(Required for audio format conversion)* |

### Get Live Help
```bash
# View real-time logs
tail -f hybrid_bot.log              # Python component activity
tail -f background.log              # Background service logs  

# Check component status
python -c "from voice_manager_hybrid import HybridVoiceManager; print(HybridVoiceManager.get_status())"
```

---

## 🌟🌟 Join Our CommunityJoin Our Community

We'd love your help making this even better!

- **🐛 Found a bug?** → [Report it](https://github.com/[YOUR-USERNAME]/discord-audio-archive-bot/issues)
- **💡 Have an idea?** → [Share it](https://github.com/[YOUR-USERNAME]/discord-audio-archive-bot/discussions)  
- **🔧 Want to contribute?** → See [CONTRIBUTING.md](CONTRIBUTING.md)
- **❓ Need help?** → Check [Documentation](https://github.com/[YOUR-USERNAME]/discord-audio-archive-bot/wiki)

**⭐ Star this repo if it helped you!** It helps others find this project.

---

## 📊 System Requirements & Credits

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

****Built with ❤️ for preservingpreserving preciousprecious momentsmoments**

*Start recording your Discord memories today!*

[📖 Documentation](https://github.com/[YOUR-USERNAME]/discord-audio-archive-bot/wiki) • [🚀 Quick Start](#-quick-start-5-minutes) • [💬 Community](https://github.com/[YOUR-USERNAME]/discord-audio-archive-bot/discussions)

</div>