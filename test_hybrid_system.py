#!/usr/bin/env python3
"""
Hybrid System Test - Validates the audio archive bot components
"""

import os
import sys
import json
import time
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('SystemTest')

def run_test(name, test_func):
    """Run a single test and return result"""
    logger.info(f"🧪 Testing: {name}")
    try:
        result = test_func()
        if result:
            logger.info(f"✅ PASSED: {name}")
            return True
        else:
            logger.error(f"❌ FAILED: {name}")
            return False
    except Exception as e:
        logger.error(f"❌ ERROR in {name}: {e}")
        return False

def test_python_environment():
    """Test Python virtual environment and dependencies"""
    try:
        import discord
        import asyncio
        from dotenv import load_dotenv
        from voice_manager_hybrid import HybridVoiceManager

        logger.info(f"   Discord version: {discord.__version__}")
        return True
    except ImportError as e:
        logger.error(f"   Missing Python dependency: {e}")
        return False

def test_node_environment():
    """Test Node.js and required packages"""
    try:
        # Check node and npm
        node_result = subprocess.run(['node', '--version'],
                                   capture_output=True, text=True, timeout=5)
        if node_result.returncode != 0:
            return False

        logger.info(f"   Node.js version: {node_result.stdout.strip()}")

        # Check package.json dependencies
        if not os.path.exists('package.json'):
            logger.error("   package.json not found")
            return False

        if not os.path.exists('node_modules'):
            logger.error("   node_modules not found - run 'npm install'")
            return False

        return True
    except Exception as e:
        logger.error(f"   Node.js check failed: {e}")
        return False

def test_ffmpeg():
    """Test FFmpeg installation and functionality"""
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return False

        version_line = result.stdout.split('\n')[0]
        logger.info(f"   {version_line}")

        # Test basic FFmpeg conversion capability
        test_cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'testsrc=duration=1:size=320x240:rate=1',
                   '-f', 'null', '-', '-loglevel', 'error']
        test_result = subprocess.run(test_cmd, capture_output=True, timeout=10)

        return test_result.returncode == 0

    except Exception as e:
        logger.error(f"   FFmpeg test failed: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    required_files = [
        'hybrid_bot.py',
        'voice_recorder.js',
        'voice_manager_hybrid.py',
        'package.json',
        'requirements.txt',
        '.env.example'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        logger.error(f"   Missing files: {missing_files}")
        return False

    logger.info(f"   All {len(required_files)} required files present")
    return True

def test_ipc_system():
    """Test JSON-based IPC communication"""
    try:
        from voice_manager_hybrid import HybridVoiceManager

        # Test command sending
        test_command = {
            'action': 'test_command',
            'guildId': '123456789',
            'channelId': '987654321',
            'targetUserId': '555666777'
        }

        # Clean up any existing files
        for file in [HybridVoiceManager.COMMANDS_FILE, HybridVoiceManager.STATUS_FILE]:
            if os.path.exists(file):
                os.remove(file)

        # Test sending command
        success = HybridVoiceManager.send_command(**test_command)
        if not success:
            return False

        # Verify command file was created
        if not os.path.exists(HybridVoiceManager.COMMANDS_FILE):
            logger.error("   Command file not created")
            return False

        # Read and verify command
        with open(HybridVoiceManager.COMMANDS_FILE, 'r') as f:
            saved_command = json.load(f)

        if saved_command['action'] != 'test_command':
            logger.error("   Command not saved correctly")
            return False

        # Clean up
        os.remove(HybridVoiceManager.COMMANDS_FILE)

        logger.info("   IPC command system working")
        return True

    except Exception as e:
        logger.error(f"   IPC test failed: {e}")
        return False

def test_recordings_directory():
    """Test recordings directory setup"""
    recordings_dir = Path("recordings")

    if not recordings_dir.exists():
        try:
            recordings_dir.mkdir(parents=True)
            logger.info("   Created recordings directory")
        except Exception as e:
            logger.error(f"   Failed to create recordings directory: {e}")
            return False

    # Test write permissions
    try:
        test_file = recordings_dir / "test_file.tmp"
        test_file.write_text("test")
        test_file.unlink()
        logger.info("   Recordings directory writable")
        return True
    except Exception as e:
        logger.error(f"   Recordings directory not writable: {e}")
        return False

def test_env_config():
    """Test environment configuration setup"""
    if not os.path.exists('.env.example'):
        logger.error("   .env.example template missing")
        return False

    # Check if .env exists
    has_env = os.path.exists('.env')
    logger.info(f"   .env file exists: {has_env}")

    if has_env:
        # Load and check for placeholder values
        from dotenv import load_dotenv
        load_dotenv()

        required_vars = ['DISCORD_TOKEN', 'TARGET_USER_ID']
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            logger.warning(f"   Missing environment variables: {missing_vars}")
            logger.info("   This is expected for testing - configure .env for production")
        else:
            logger.info("   All required environment variables present")

    return True

def main():
    """Run all system tests"""
    logger.info("🔍 Starting Hybrid System Tests")
    logger.info("=" * 50)

    tests = [
        ("Python Environment Setup", test_python_environment),
        ("Node.js Environment Setup", test_node_environment),
        ("FFmpeg Availability", test_ffmpeg),
        ("File Structure", test_file_structure),
        ("IPC Communication System", test_ipc_system),
        ("Recordings Directory", test_recordings_directory),
        ("Environment Configuration", test_env_config)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
        else:
            failed += 1
        print()  # Add spacing between tests

    # Print summary
    total = passed + failed
    logger.info("=" * 50)
    logger.info("📊 TEST SUMMARY")
    logger.info(f"   Total tests: {total}")
    logger.info(f"   Passed: {passed}")
    logger.info(f"   Failed: {failed}")

    if failed == 0:
        logger.info("🎉 ALL TESTS PASSED - System ready for deployment!")
        return True
    else:
        logger.error("❌ Some tests failed - check configuration and dependencies")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
