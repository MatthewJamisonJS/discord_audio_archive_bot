#!/usr/bin/env python3
"""
Hybrid Discord Bot - Python for events, Node.js for voice recording
Optimized for background operation with minimal resource usage
"""

import discord
from discord.ext import commands
import os
import asyncio
import logging
import gc
from datetime import datetime
from dotenv import load_dotenv
from voice_manager_hybrid import HybridVoiceManager

# Load environment variables
load_dotenv()

# Configure logging with background mode detection
BACKGROUND_MODE = os.getenv('BACKGROUND_MODE', 'false').lower() == 'true'

if BACKGROUND_MODE:
    # Minimal logging for background operation
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('hybrid_bot.log')]
    )
else:
    # Full logging for interactive mode
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hybrid_bot.log'),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger('HybridBot')

# Memory optimization
gc.set_threshold(700, 10, 10)  # Aggressive garbage collection

# Configuration with validation
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_USER_ID_STR = os.getenv('TARGET_USER_ID')

if not DISCORD_TOKEN:
    logger.error("❌ Missing required environment variable: DISCORD_TOKEN")
    raise ValueError("Missing required configuration: DISCORD_TOKEN")

if not TARGET_USER_ID_STR:
    logger.error("❌ Missing required environment variable: TARGET_USER_ID")
    raise ValueError("Missing required configuration: TARGET_USER_ID")

try:
    TARGET_USER_ID = int(TARGET_USER_ID_STR)
except ValueError:
    logger.error("❌ TARGET_USER_ID must be a valid integer")
    raise ValueError("Invalid TARGET_USER_ID format")

# Optional email configuration validation
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

if EMAIL_USER and EMAIL_PASS and EMAIL_RECIPIENT:
    logger.info("✅ Email configuration detected - recordings will be emailed")
else:
    logger.warning("⚠️ Email configuration incomplete - recordings will be saved locally only")

# Bot setup with optimization
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
# Disable unnecessary intents for efficiency
intents.presences = False
intents.typing = False
intents.integrations = False
intents.webhooks = False

bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    heartbeat_timeout=60.0,  # Longer heartbeat for efficiency
    guild_ready_timeout=10.0,  # Faster guild ready timeout
)

# Tracking
recording_sessions = {}

# Background task for periodic cleanup
async def background_maintenance():
    """Periodic maintenance for background operation"""
    while True:
        try:
            # Force garbage collection every 10 minutes
            gc.collect()

            # Clean up old recording sessions (older than 24 hours)
            current_time = datetime.now()
            old_sessions = [
                k for k, v in recording_sessions.items()
                if hasattr(v, 'start_time') and
                (current_time - v.start_time).total_seconds() > 86400
            ]
            for session_id in old_sessions:
                recording_sessions.pop(session_id, None)

            if old_sessions and not BACKGROUND_MODE:
                logger.info(f"Cleaned up {len(old_sessions)} old recording sessions")

        except Exception as e:
            if not BACKGROUND_MODE:
                logger.error(f"Background maintenance error: {e}")

        # Wait 10 minutes before next cleanup
        await asyncio.sleep(600)

@bot.event
async def on_ready():
    """Bot startup event."""
    logger.info(f"🤖 Hybrid Bot logged in as {bot.user}")
    logger.info(f"🎯 Target User ID: {TARGET_USER_ID}")
    logger.info(f"📡 Connected to {len(bot.guilds)} guilds")

    # Check Node.js status
    status = HybridVoiceManager.get_status()
    if status:
        logger.info(f"🎙️ Node.js Voice Recorder Status: {status['status']}")
    else:
        logger.warning("⚠️ No status from Node.js voice recorder - ensure voice_recorder.js is running")

    logger.info("🔄 Monitoring voice state changes...")

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state changes."""
    if member.id != TARGET_USER_ID:
        return

    guild_id = member.guild.id
    username = member.display_name or member.name

    # User joined voice channel
    if before.channel is None and after.channel is not None:
        logger.info(f"🎯 TARGET USER JOINED: {username} in {after.channel.name} (Guild: {member.guild.name})")

        # Start recording via Node.js
        success = await HybridVoiceManager.start_recording(
            guild_id=guild_id,
            channel=after.channel,
            target_user_id=TARGET_USER_ID
        )

        if success:
            logger.info("✅ Recording request sent to Node.js component")

            # Wait a moment and check status
            await asyncio.sleep(2)
            status = HybridVoiceManager.get_status()
            if status and 'status' in status:
                logger.info(f"🎙️ Node.js Response: {status['status']} - {status.get('message', '')}")
        else:
            logger.error("❌ Failed to send recording request")

    # User left voice channel
    elif before.channel is not None and after.channel is None:
        logger.info(f"🎯 TARGET USER LEFT: {username} from {before.channel.name} (Guild: {member.guild.name})")

        # Stop recording via Node.js
        success = await HybridVoiceManager.stop_recording(guild_id)

        if success:
            logger.info("✅ Stop request sent to Node.js component")

            # Wait for Node.js to process the stop command and disconnect
            await asyncio.sleep(5)
            status = HybridVoiceManager.get_status()
            if status and 'status' in status:
                logger.info(f"🎙️ Final Status: {status['status']} - {status.get('message', '')}")
                if status.get('status') in ['stopped', 'ready']:
                    logger.info("✅ Bot successfully disconnected from voice channel")
                else:
                    logger.warning(f"⚠️ Bot may still be connected - Status: {status.get('status')}")
        else:
            logger.error("❌ Failed to send stop request")

    # User switched channels
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        logger.info(f"🔄 TARGET USER MOVED: {username} from {before.channel.name} to {after.channel.name}")

        # Stop current recording
        await HybridVoiceManager.stop_recording(guild_id)
        await asyncio.sleep(1)

        # Start new recording in new channel
        success = await HybridVoiceManager.start_recording(
            guild_id=guild_id,
            channel=after.channel,
            target_user_id=TARGET_USER_ID
        )

        if success:
            logger.info("✅ Recording moved to new channel")
        else:
            logger.error("❌ Failed to restart recording in new channel")

@bot.command(name='status')
async def check_status(ctx):
    """Check Node.js voice recorder status."""
    status = HybridVoiceManager.get_status()
    if status:
        await ctx.send(f"📊 Node.js Status: {status['status']} - {status['message']}")
    else:
        await ctx.send("❌ No status available from Node.js component")

@bot.command(name='test_recording')
@commands.has_permissions(administrator=True)
async def test_recording(ctx):
    """Test voice recording functionality."""
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        success = await HybridVoiceManager.start_recording(
            guild_id=ctx.guild.id,
            channel=channel,
            target_user_id=ctx.author.id
        )

        if success:
            await ctx.send("✅ Test recording started!")
            await asyncio.sleep(5)
            await HybridVoiceManager.stop_recording(ctx.guild.id)
            await ctx.send("⏹️ Test recording stopped!")
        else:
            await ctx.send("❌ Failed to start test recording")
    else:
        await ctx.send("You must be in a voice channel to test recording")

if __name__ == "__main__":
    logger.info("🚀 Starting Hybrid Discord Bot...")
    bot.run(DISCORD_TOKEN)
