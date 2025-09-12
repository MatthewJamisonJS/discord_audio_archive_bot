# 🎙️ Discord Audio Archive Bot

> **Automatically record and save Discord voice conversations with crystal-clear audio quality**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-22.16+-green.svg)](https://nodejs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-First-red.svg)](SECURITY.md)

**Welcome! 👋** This friendly bot helps you automatically record Discord voice conversations and save them as high-quality MP3 files. Perfect for preserving important conversations, meetings, or memorable moments with friends.

**✨ What makes this special:** The bot watches for a specific person to join any voice channel, automatically starts recording with professional audio quality, and can even email you the results when done.

---

## 🚀 Two Ways to Get Started

**Choose your adventure based on your comfort level:**

---

### 🌟 **"I Just Want It to Work" (Recommended for Most People)**

**What you need:** A Mac computer, 10 minutes, and a Discord account

**Step 1:** Download this project to your computer  
**Step 2:** Open Terminal, go to the project folder, and run:
```bash
chmod +x setup.sh && ./setup.sh
```

**Step 3:** Follow the friendly prompts to:
- Create your Discord bot (we'll guide you!)  
- Set up your target person
- Configure email (optional)

**Step 4:** Start your bot **once** and let it run forever:
```bash
./run_bot_forever.sh
```

**🎉 Done!** Your bot will now run in the background, automatically starting recordings and restarting itself if needed. You can close Terminal - it keeps working!

---

### 🔧 **"I Want to Understand How It Works" (For Curious Minds)**

<details>
<summary>Click here for detailed technical setup</summary>

**What's happening under the hood:**
- **Hybrid Architecture**: Python handles Discord events, Node.js handles voice recording
- **Auto-restart**: Uses system services to keep running even after computer restarts
- **IPC Communication**: Components talk via JSON files for reliability
- **Professional Audio**: FFmpeg processing with Opus decoding for crystal-clear recordings

**Manual Setup Process:**
1. **Environment Setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   npm install
   ```

2. **Configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run Components:**
   ```bash
   # Terminal 1: Python event handler
   python hybrid_bot.py
   
   # Terminal 2: Node.js voice recorder  
   node voice_recorder.js
   ```

**System Integration Options:**
- **Background Service**: Runs automatically on startup
- **Manual Control**: Start/stop as needed
- **Development Mode**: See all logs and debug info

</details>

---

### 🤔 **Not Sure Which Path to Choose?**

**Go with the "Just Want It to Work" option!** It's designed to be foolproof and handles all the technical stuff automatically. You can always explore the technical details later if you're curious.

### 🔧 **Technical Note: Why No `venv/` Folder?**

<details>
<summary>Click if you're wondering about Python dependencies</summary>

You might notice there's no `venv/` folder in this repository. That's intentional and follows Python best practices:

- **The `venv/` folder contains platform-specific files** that only work on the computer where they were created
- **Including it would make this repo huge** (200-500MB) and broken on other systems
- **Our scripts automatically create and manage it** - you don't need to worry about it!

When you run `./run_bot_forever.sh`, it will:
1. ✅ Create the `venv/` folder if missing
2. ✅ Install all Python dependencies automatically  
3. ✅ Fix any dependency issues
4. ✅ Handle everything transparently

**Bottom line:** Just run the bot - it handles all the Python environment stuff for you! 🐍✨

</details>

---

## ✨ What This Bot Does For You

### 🎯 **Smart & Automatic**
- **Watches your target person** - No need to manually start/stop recording
- **Works across all voice channels** - Follows them wherever they go
- **Starts instantly** - Begins recording the moment they join
- **Stops automatically** - Ends when they leave, no wasted time

### 🎧 **Amazing Audio Quality**  
- **Crystal clear recordings** - Professional 256kbps MP3 quality
- **No background noise** - Advanced audio processing removes static
- **Perfect synchronization** - Never miss a word
- **Long recordings supported** - Up to 4 hours of continuous audio

### 📧 **Convenient Delivery**
- **Email notifications** - Get recordings sent directly to your inbox
- **Organized filenames** - Easy to find with dates and usernames
- **Secure transfer** - Your recordings are safely delivered
- **Local backup** - Also saved on your computer

### 🛡️ **Built with Care**
- **Your privacy matters** - All credentials stay on your computer
- **Secure by design** - No data stored on external servers
- **Easy to control** - Simple commands to check status or test
- **Reliable operation** - Designed to work without constant babysitting

### 🎮 **Simple Commands**
Once running, you can use these commands in Discord:
- `!status` - Check if everything is working
- `!test_recording` - Quick test to make sure audio works

---

## 🤔 Common Questions

### "How do I know it's working?"
After starting the bot with `./run_hybrid.sh`, you'll see friendly status messages. The bot will tell you when it connects to Discord and when it starts/stops recording.

### "Where do my recordings go?"
- **On your computer**: Look in the `recordings/` folder
- **Via email**: If configured, they'll be sent to your Gmail inbox automatically
- **File names**: Easy to read like `12_25_2024_14-30-15_JohnDoe_abc123.mp3`

### "Can I record multiple people?"
Currently, the bot focuses on one person at a time. This keeps things simple and reliable!

### "What if something goes wrong?"
The bot is designed to be very reliable, but if you need help:
- Check the console messages for friendly error explanations
- Use `!status` in Discord to see what's happening
- Look at the troubleshooting section below

### "Is this secure?"
Absolutely! Your Discord tokens and email passwords never leave your computer. Everything runs locally and securely.

---

## 🚨 Important: Please Be Respectful

**🤝 Always Get Permission First**

Before using this bot, please remember:
- **Ask everyone** if it's okay to record them - it's just good manners!
- **Check your local laws** - some places require everyone's permission to record
- **Be transparent** - let people know when recording is happening
- **Keep recordings safe** - treat them with the same care you'd want for your own conversations
- **Follow Discord's rules** - make sure you're using Discord responsibly

**We built this tool to help preserve important conversations, but please always use it kindly and legally.** 💝

---

## 🔧 If Something Isn't Working

Don't worry! Most issues are easy to fix. Here are the most common ones:

### 🟡 **"The bot isn't starting"**
- Make sure you ran `./setup.sh` first
- Check that your `.env` file has your Discord token
- Try running `python test_hybrid_system.py` to check everything

### 🟡 **"No recording is happening"**
- Make sure your target person is actually in a voice channel
- Check if the bot has permission to join voice channels
- Use `!status` in Discord to see what's happening

### 🟡 **"I'm getting weird error messages"**
- Most error messages are actually helpful! Read them carefully
- Common fixes:
  - Make sure FFmpeg is installed: `brew install ffmpeg`
  - Check your Discord token is correct
  - Make sure your target user ID is right (it should be all numbers)

### 🟡 **"Email isn't working"**
- You need to use a Gmail "App Password" (not your regular password)
- Visit [Gmail App Passwords](https://myaccount.google.com/apppasswords) to create one
- Double-check your email settings in the `.env` file

### 💡 **Still stuck?**
Run this helpful command to check everything:
```bash
python test_hybrid_system.py
```

This will tell you exactly what might be wrong and how to fix it!

---

## 💕 Want to Help Make This Better?

We'd love your help making this bot even more friendly and reliable! Here's how you can contribute:

### 🐛 **Found a Bug?**
- Please open an issue on GitHub with a friendly description
- Include what you were trying to do and what happened instead
- We'll help you fix it quickly!

### ✨ **Have an Idea?**
- Share your thoughts on new features or improvements  
- We especially love ideas that make the bot easier to use
- All suggestions are welcome!

### 🛠️ **Want to Code?**
If you're technically inclined:
- Check out our [Contributing Guide](CONTRIBUTING.md) for details
- The codebase is designed to be friendly to newcomers
- We're happy to help you get started!

---

## 📝 License & Credits

**License:** MIT (feel free to use and modify!)

**Special Thanks:**
- The Discord.js team for excellent voice handling
- The Discord.py community for event management inspiration  
- FFmpeg for amazing audio processing
- Everyone who tests and improves this bot

---

## 🎉 You're All Set!

Congratulations! You now have a powerful, friendly Discord audio recording bot that works reliably and securely. 

**Remember:**
- Always be respectful and get permission before recording
- The bot will automatically handle everything once it's running
- Check back here if you need help with anything

**Happy recording! 🎵✨**

---

<div align="center">

*Built with ❤️ for the Discord community*

**Star this repo if it helped you!** ⭐

</div>