#!/usr/bin/env python3
"""
Hybrid Voice Manager - IPC Interface to Node.js Voice Recorder
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger('AudioArchiveBot')

class HybridVoiceManager:
    """
    Manages voice recording via Node.js IPC communication.
    """
    
    COMMANDS_FILE = 'voice_commands.json'
    STATUS_FILE = 'voice_status.json'
    
    @staticmethod
    def send_command(action: str, **kwargs):
        """Send command to Node.js voice recorder via JSON file."""
        try:
            command = {
                'action': action,
                'timestamp': datetime.now().isoformat(),
                **kwargs
            }
            
            with open(HybridVoiceManager.COMMANDS_FILE, 'w') as f:
                json.dump(command, f, indent=2)
            
            logger.info(f"🚀 Sent IPC command: {action}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send IPC command {action}: {e}")
            return False
    
    @staticmethod
    def get_status():
        """Get current status from Node.js voice recorder."""
        try:
            if not os.path.exists(HybridVoiceManager.STATUS_FILE):
                return None
            
            with open(HybridVoiceManager.STATUS_FILE, 'r') as f:
                status = json.load(f)
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to read IPC status: {e}")
            return None
    
    @staticmethod
    async def start_recording(guild_id: int, channel, target_user_id: int) -> bool:
        """Request Node.js component to start voice recording."""
        try:
            logger.info(f"🎙️ Starting hybrid voice recording - Guild: {guild_id}, Channel: {channel.name}")
            
            success = HybridVoiceManager.send_command(
                'start_recording',
                guildId=str(guild_id),
                channelId=str(channel.id),
                targetUserId=str(target_user_id)
            )
            
            if success:
                logger.info(f"✅ Recording command sent to Node.js component")
                return True
            else:
                logger.error("❌ Failed to send recording command")
                return False
                
        except Exception as e:
            logger.error(f"Error in hybrid start_recording: {e}")
            return False
    
    @staticmethod
    async def stop_recording(guild_id: int) -> bool:
        """Request Node.js component to stop voice recording."""
        try:
            logger.info(f"🛑 Stopping hybrid voice recording - Guild: {guild_id}")
            
            success = HybridVoiceManager.send_command(
                'stop_recording',
                guildId=str(guild_id)
            )
            
            if success:
                logger.info(f"✅ Stop command sent to Node.js component")
                return True
            else:
                logger.error("❌ Failed to send stop command")
                return False
                
        except Exception as e:
            logger.error(f"Error in hybrid stop_recording: {e}")
            return False