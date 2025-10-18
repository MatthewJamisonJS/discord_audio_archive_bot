"""
Pytest configuration and shared fixtures for audio_archive_bot tests.

This module provides:
- Environment configuration fixtures
- File cleanup fixtures
- Mock Discord objects
- Test data fixtures
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest

# Add the project root to the path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_env_file(tmp_path):
    """
    Create a temporary .env file for testing.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Yields:
        Path: Path to the temporary .env file

    Example:
        >>> def test_env(temp_env_file):
        ...     with open(temp_env_file) as f:
        ...         content = f.read()
    """
    env_file = tmp_path / ".env"
    env_content = """
DISCORD_TOKEN=test_token_12345
TARGET_USER_ID=123456789
EMAIL_USER=test@example.com
EMAIL_PASS=test_password
EMAIL_RECIPIENT=recipient@example.com
BACKGROUND_MODE=false
"""
    env_file.write_text(env_content.strip())

    # Set environment variables for the test
    original_env = os.environ.copy()
    os.environ.update({
        'DISCORD_TOKEN': 'test_token_12345',
        'TARGET_USER_ID': '123456789',
        'EMAIL_USER': 'test@example.com',
        'EMAIL_PASS': 'test_password',
        'EMAIL_RECIPIENT': 'recipient@example.com',
        'BACKGROUND_MODE': 'false'
    })

    yield env_file

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def minimal_env():
    """
    Set up minimal required environment variables.

    Yields:
        dict: Dictionary of environment variables set

    Example:
        >>> def test_minimal_config(minimal_env):
        ...     assert os.getenv('DISCORD_TOKEN') is not None
    """
    original_env = os.environ.copy()

    test_env = {
        'DISCORD_TOKEN': 'test_token_minimal',
        'TARGET_USER_ID': '987654321'
    }
    os.environ.update(test_env)

    yield test_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def cleanup_ipc_files():
    """
    Clean up IPC command and status files before and after tests.

    This fixture ensures that voice_commands.json and voice_status.json
    files are removed before and after each test to prevent interference.

    Yields:
        tuple: Paths to (commands_file, status_file)
    """
    commands_file = Path('voice_commands.json')
    status_file = Path('voice_status.json')

    # Clean up before test
    if commands_file.exists():
        commands_file.unlink()
    if status_file.exists():
        status_file.unlink()

    yield (commands_file, status_file)

    # Clean up after test
    if commands_file.exists():
        commands_file.unlink()
    if status_file.exists():
        status_file.unlink()


@pytest.fixture
def mock_discord_member():
    """
    Create a mock Discord member object.

    Returns:
        Mock: A mock Discord member with standard attributes

    Example:
        >>> def test_member(mock_discord_member):
        ...     assert mock_discord_member.id == 123456789
    """
    member = Mock()
    member.id = 123456789
    member.name = "TestUser"
    member.display_name = "Test User"
    member.guild = Mock()
    member.guild.id = 111111111
    member.guild.name = "Test Guild"
    return member


@pytest.fixture
def mock_discord_channel():
    """
    Create a mock Discord voice channel object.

    Returns:
        Mock: A mock Discord voice channel

    Example:
        >>> def test_channel(mock_discord_channel):
        ...     assert mock_discord_channel.name == "Test Voice"
    """
    channel = Mock()
    channel.id = 222222222
    channel.name = "Test Voice"
    channel.guild = Mock()
    channel.guild.id = 111111111
    return channel


@pytest.fixture
def mock_voice_state():
    """
    Create a mock Discord voice state object.

    Returns:
        Mock: A mock Discord voice state
    """
    voice_state = Mock()
    voice_state.channel = None
    voice_state.self_mute = False
    voice_state.self_deaf = False
    return voice_state


@pytest.fixture
def sample_command_data():
    """
    Provide sample IPC command data for testing.

    Returns:
        dict: Sample command dictionary

    Example:
        >>> def test_command(sample_command_data):
        ...     assert sample_command_data['action'] == 'start_recording'
    """
    return {
        'action': 'start_recording',
        'timestamp': '2025-10-17T12:00:00',
        'guildId': '111111111',
        'channelId': '222222222',
        'targetUserId': '123456789'
    }


@pytest.fixture
def sample_status_data():
    """
    Provide sample IPC status data for testing.

    Returns:
        dict: Sample status dictionary
    """
    return {
        'status': 'recording',
        'message': 'Recording in progress',
        'timestamp': '2025-10-17T12:00:00',
        'guildId': '111111111'
    }


@pytest.fixture
def mock_status_file(tmp_path, sample_status_data):
    """
    Create a temporary status file with sample data.

    Args:
        tmp_path: pytest's temporary directory
        sample_status_data: Sample status data fixture

    Returns:
        Path: Path to the temporary status file
    """
    status_file = tmp_path / "voice_status.json"
    with open(status_file, 'w') as f:
        json.dump(sample_status_data, f)
    return status_file


@pytest.fixture
def mock_discord_bot():
    """
    Create a mock Discord bot instance.

    Returns:
        Mock: A mock Discord bot with common attributes
    """
    bot = MagicMock()
    bot.user = Mock()
    bot.user.name = "TestBot"
    bot.user.id = 999999999
    bot.guilds = []
    return bot


@pytest.fixture
def mock_discord_context(mock_discord_member, mock_discord_channel):
    """
    Create a mock Discord command context.

    Args:
        mock_discord_member: Mock member fixture
        mock_discord_channel: Mock channel fixture

    Returns:
        Mock: A mock Discord context object
    """
    ctx = Mock()
    ctx.author = mock_discord_member
    ctx.guild = mock_discord_member.guild
    ctx.channel = Mock()
    ctx.channel.id = 333333333
    ctx.send = Mock()

    # Mock voice state
    ctx.author.voice = Mock()
    ctx.author.voice.channel = mock_discord_channel

    return ctx


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Reset logging configuration between tests.

    This auto-use fixture ensures that logging state doesn't leak between tests.
    """
    import logging

    # Store original handlers
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers[:]
    original_level = root_logger.level

    yield

    # Restore original state
    root_logger.handlers = original_handlers
    root_logger.level = original_level


# Test data constants
TEST_DISCORD_TOKEN = "test_token_12345"
TEST_TARGET_USER_ID = "123456789"
TEST_GUILD_ID = "111111111"
TEST_CHANNEL_ID = "222222222"
