# 🎙️ Discord Audio Archive Bot

**Automatically record Discord voice conversations in crystal-clear audio**

**Welcome! 👋** This friendly bot automatically records Discord voice conversations in high-quality MP3. Perfect for preserving important meetings or memorable moments with friends.

**✨ Simply set it up once:**
The bot watches for your target person, records with professional audio quality, and can email finished recordings.

---

## 🚀 Quick Start (Recommended)

**What you need:** A Mac computer and Discord account

1. **Download project** and open Terminal in the folder
2. **Run setup:**
   ```bash
   chmod +x setup.sh && ./setup.sh
   ```
3. **Follow prompts** to:
   - Create your Discord bot
   - Set your target person
   - Configure email (optional)
4. **Start permanently:**
   ```bash
   ./run_bot_forever.sh
   ```

**🎉 Done!** Bot runs quietly in background. Close Terminal - it keeps working!

<details>
<summary>🔧 Advanced Setup (For curious minds)</summary>

**Manual process:**
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install
cp .env.example .env  # Edit with your settings
python hybrid_bot.py  # In one terminal
node voice_recorder.js  # In another
```
</details>

---

## ✨ What You Get

### 🎯 Smart & Automatic
- Records when your target person joins *any* voice channel
- Starts instantly, stops automatically

### 🎧 Crystal-Clear Audio
- Professional 256kbps MP3 quality
- Noise-free recordings

### 📧 Easy Delivery
- Email notifications (optional)
- Organized filenames like ```12_25_2024_14-30-15_JohnDoe.mp3```

### 🛡️ Privacy First
- All data stays on your computer
- Secure by design

---

## 🤔 Quick Help

### "Where are recordings?"
- ```recordings/``` folder on your computer
- Email (if configured)

### "Is this secure?"
Absolutely! Your Discord tokens and passwords never leave your computer.

### "How do I know it's working?"
- Bot sends status messages in Discord
- Use ```!status``` command

---

## 🚨 Please Be Respectful

**🤝 Always get permission first:**
- Ask everyone before recording
- Check local laws (some require all-party consent)
- Be transparent about recording
- Keep recordings safe

*We built this to preserve meaningful conversations - please use it kindly and legally. 💝*

---

## 🔧 Troubleshooting

Most issues fixed by:
```bash
python test_hybrid_system.py
```

**Common fixes:**
- Run ```./setup.sh``` first
- Verify Discord token in ```.env```
- Enable Gmail [App Passwords](https://myaccount.google.com/apppasswords) for email

---

## 💕 Contribute

We'd love your help!
- Found a bug? → [Open issue](https://github.com/your-repo/issues)
- Have an idea? → Share in [Discussions](https://github.com/your-repo/discussions)
- Want to code? → See [Contributing Guide](CONTRIBUTING.md)

---

## 📝 License

**MIT License** - Use and modify freely!
*Special thanks to Discord.js, FFmpeg, and our amazing community.*

---

<div align="center">

*Built with ❤️ for the Discord community*
**Star this repo if it helped you!** ⭐

</div>
