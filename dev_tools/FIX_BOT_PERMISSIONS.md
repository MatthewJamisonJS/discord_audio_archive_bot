# 🔧 Discord Bot Permissions Fix Guide

Your Discord bot is missing critical permissions required for voice recording functionality. This guide will help you fix the permission issues.

## 🚨 Current Issue

**Your bot permissions integer:** `1125899941448832`

**Missing Required Permissions:**
- ❌ **SPEAK** - Required for voice activity detection
- ❌ **READ_MESSAGE_HISTORY** - Required for command processing

**Currently Granted:**
- ✅ **CONNECT** - Can join voice channels
- ✅ **USE_VAD** (Use Voice Activity) - Can detect voice activity
- ✅ **VIEW_CHANNEL** - Can see channels
- ⚪ **SEND_MESSAGES** - Can send messages (optional)
- ⚪ **VIEW_AUDIT_LOG** - Can view audit logs (unnecessary)

## 🎯 Required Minimal Permissions

**Minimal permission integer needed:** `36766720`

**Required permissions for audio recording bot:**
1. **VIEW_CHANNEL** (Read Messages) - See voice channels
2. **CONNECT** - Join voice channels
3. **SPEAK** - Required for voice recording functionality
4. **USE_VAD** (Use Voice Activity) - Detect when users are speaking
5. **READ_MESSAGE_HISTORY** - Process bot commands

## 🔧 How to Fix Bot Permissions

### Method 1: Re-invite Bot with Correct Permissions

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Select your bot application

2. **Navigate to OAuth2 → URL Generator**
   - **Scopes:** Check `bot`
   - **Bot Permissions:** Select ONLY these:
     - ✅ **View Channels** (under General)
     - ✅ **Connect** (under Voice)
     - ✅ **Speak** (under Voice)
     - ✅ **Use Voice Activity** (under Voice)
     - ✅ **Read Message History** (under Text)

3. **Generate New Invite URL**
   - Copy the generated URL
   - The permission integer should be: `36766720`

4. **Re-invite Your Bot**
   - Use the new URL to invite bot to your server
   - This will update the bot's permissions

### Method 2: Manually Update Permissions in Discord Server

1. **Go to Your Discord Server**
   - Right-click server name → **Server Settings**

2. **Navigate to Roles**
   - Find your bot's role (usually has the same name as the bot)
   - Click on the bot's role

3. **Update Voice Permissions**
   - Scroll to **Voice Permissions** section
   - Enable these permissions:
     - ✅ **Connect**
     - ✅ **Speak**
     - ✅ **Use Voice Activity**

4. **Update Text Permissions**
   - Scroll to **Text Permissions** section
   - Enable:
     - ✅ **View Channels**
     - ✅ **Read Message History**

5. **Save Changes**
   - Click **Save Changes** at the bottom

## 🛡️ Security Best Practices

### ✅ What Your Bot SHOULD Have
```
Minimal Required Permissions (36766720):
- VIEW_CHANNEL (1024)
- CONNECT (1048576) 
- SPEAK (2097152)
- USE_VAD (33554432)
- READ_MESSAGE_HISTORY (65536)
```

### ❌ What Your Bot Should NOT Have
```
Dangerous Permissions to Avoid:
- ADMINISTRATOR (8)
- MANAGE_GUILD (32)
- MANAGE_ROLES (268435456)
- MANAGE_CHANNELS (16)
- BAN_MEMBERS (4)
- KICK_MEMBERS (2)
```

## 🔍 Verify Permissions Are Fixed

### Test with Permission Decoder
```bash
cd audio_archive_bot
python decode_permissions.py [new_permission_integer]
```

**Expected output should show:**
```
REQUIRED PERMISSIONS FOR AUDIO BOT:
----------------------------------------
VIEW_CHANNEL              ✅ GRANTED
CONNECT                   ✅ GRANTED
SPEAK                     ✅ GRANTED
USE_VAD                   ✅ GRANTED
READ_MESSAGE_HISTORY      ✅ GRANTED
```

### Test Bot Functionality
```bash
# Run bot with proper permissions
python bot.py

# In Discord, test commands:
!bot_info
!recording_status
```

## 🚀 Quick Fix URL Generator

Replace `YOUR_CLIENT_ID` with your bot's actual Client ID:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=36766720&scope=bot
```

**Where to find Client ID:**
- Discord Developer Portal → Your Application → General Information → Application ID

## 📞 Still Having Issues?

### Common Problems

**❌ "Bot not responding to commands"**
- Ensure READ_MESSAGE_HISTORY permission is granted
- Check bot is online and has internet connection

**❌ "Bot joins channel but no recording"**
- Verify SPEAK and USE_VAD permissions
- Check target user has microphone enabled

**❌ "Permission denied when joining voice"**
- Confirm CONNECT permission is granted
- Ensure voice channel isn't user-limited

### Debug Commands
```bash
# Check system requirements
python troubleshoot.py

# Test full integration
python test_integration.py

# Decode your current permissions
python decode_permissions.py YOUR_PERMISSION_INTEGER
```

## ✅ Final Verification

Once permissions are fixed, your bot should:

1. ✅ Join voice channels automatically when target user connects
2. ✅ Start recording immediately upon joining
3. ✅ Respond to admin commands like `!bot_info`
4. ✅ Process and email recordings when target user disconnects
5. ✅ Show proper permission analysis with decoder script

---

**🔒 Security Reminder:** Only grant the minimum permissions needed. Your bot handles sensitive voice data - keep permissions minimal for security!