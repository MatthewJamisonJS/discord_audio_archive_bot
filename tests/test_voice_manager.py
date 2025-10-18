"""
Unit tests for HybridVoiceManager class.

This module tests:
- IPC command file creation
- Command format validation
- Status file reading
- File cleanup
- Recording start/stop functionality
- Error handling
"""

import os
import json
import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


@pytest.fixture
def voice_manager_class():
    """Import and return the HybridVoiceManager class."""
    from audio_archive_bot.voice_manager_hybrid import HybridVoiceManager
    return HybridVoiceManager


def test_voice_manager_class_exists(voice_manager_class):
    """
    Test that HybridVoiceManager class exists and is importable.
    """
    assert voice_manager_class is not None


def test_voice_manager_has_required_constants(voice_manager_class):
    """
    Test that HybridVoiceManager has required class constants.
    """
    assert hasattr(voice_manager_class, 'COMMANDS_FILE')
    assert hasattr(voice_manager_class, 'STATUS_FILE')
    assert voice_manager_class.COMMANDS_FILE == 'voice_commands.json'
    assert voice_manager_class.STATUS_FILE == 'voice_status.json'


def test_send_command_creates_json_file(voice_manager_class, cleanup_ipc_files):
    """
    Test that send_command creates a JSON file with the correct format.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    result = voice_manager_class.send_command('test_action', testParam='value')

    assert result is True
    assert commands_file.exists()

    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert data['action'] == 'test_action'
    assert data['testParam'] == 'value'
    assert 'timestamp' in data


def test_send_command_includes_timestamp(voice_manager_class, cleanup_ipc_files):
    """
    Test that send_command includes a timestamp in ISO format.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    voice_manager_class.send_command('test_action')

    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert 'timestamp' in data
    # Verify timestamp is in ISO format
    timestamp = datetime.fromisoformat(data['timestamp'])
    assert isinstance(timestamp, datetime)


def test_send_command_with_multiple_parameters(voice_manager_class, cleanup_ipc_files):
    """
    Test send_command with multiple keyword arguments.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    voice_manager_class.send_command(
        'start_recording',
        guildId='111',
        channelId='222',
        targetUserId='333'
    )

    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert data['action'] == 'start_recording'
    assert data['guildId'] == '111'
    assert data['channelId'] == '222'
    assert data['targetUserId'] == '333'


def test_send_command_handles_file_error(voice_manager_class, cleanup_ipc_files):
    """
    Test that send_command handles file write errors gracefully.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    with patch('builtins.open', side_effect=IOError("Test error")):
        result = voice_manager_class.send_command('test_action')

        assert result is False


def test_send_command_overwrites_previous_command(voice_manager_class, cleanup_ipc_files):
    """
    Test that send_command overwrites the previous command file.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    # Send first command
    voice_manager_class.send_command('action1')

    with open(commands_file, 'r') as f:
        data1 = json.load(f)

    # Send second command
    voice_manager_class.send_command('action2')

    with open(commands_file, 'r') as f:
        data2 = json.load(f)

    assert data1['action'] == 'action1'
    assert data2['action'] == 'action2'


def test_get_status_returns_none_when_file_missing(voice_manager_class, cleanup_ipc_files):
    """
    Test that get_status returns None when status file doesn't exist.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    _, status_file = cleanup_ipc_files

    # Ensure file doesn't exist
    if status_file.exists():
        status_file.unlink()

    result = voice_manager_class.get_status()

    assert result is None


def test_get_status_reads_json_file(voice_manager_class, cleanup_ipc_files, sample_status_data):
    """
    Test that get_status correctly reads the JSON status file.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
        sample_status_data: Sample status data fixture
    """
    _, status_file = cleanup_ipc_files

    # Create status file
    with open(status_file, 'w') as f:
        json.dump(sample_status_data, f)

    result = voice_manager_class.get_status()

    assert result is not None
    assert result['status'] == sample_status_data['status']
    assert result['message'] == sample_status_data['message']


def test_get_status_handles_invalid_json(voice_manager_class, cleanup_ipc_files):
    """
    Test that get_status handles invalid JSON gracefully.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    _, status_file = cleanup_ipc_files

    # Create invalid JSON file
    with open(status_file, 'w') as f:
        f.write("invalid json {{{")

    result = voice_manager_class.get_status()

    assert result is None


def test_get_status_handles_read_error(voice_manager_class, cleanup_ipc_files):
    """
    Test that get_status handles file read errors gracefully.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', side_effect=IOError("Test error")):
            result = voice_manager_class.get_status()

            assert result is None


@pytest.mark.asyncio
async def test_start_recording_creates_command(voice_manager_class, cleanup_ipc_files,
                                                mock_discord_channel):
    """
    Test that start_recording creates the correct command file.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
        mock_discord_channel: Mock Discord channel fixture
    """
    commands_file, _ = cleanup_ipc_files

    guild_id = 111111111
    target_user_id = 123456789

    result = await voice_manager_class.start_recording(
        guild_id=guild_id,
        channel=mock_discord_channel,
        target_user_id=target_user_id
    )

    assert result is True
    assert commands_file.exists()

    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert data['action'] == 'start_recording'
    assert data['guildId'] == str(guild_id)
    assert data['channelId'] == str(mock_discord_channel.id)
    assert data['targetUserId'] == str(target_user_id)


@pytest.mark.asyncio
async def test_start_recording_converts_ids_to_strings(voice_manager_class, cleanup_ipc_files,
                                                        mock_discord_channel):
    """
    Test that start_recording converts IDs to strings for JSON compatibility.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
        mock_discord_channel: Mock Discord channel fixture
    """
    commands_file, _ = cleanup_ipc_files

    await voice_manager_class.start_recording(
        guild_id=111111111,
        channel=mock_discord_channel,
        target_user_id=123456789
    )

    with open(commands_file, 'r') as f:
        data = json.load(f)

    # All IDs should be strings
    assert isinstance(data['guildId'], str)
    assert isinstance(data['channelId'], str)
    assert isinstance(data['targetUserId'], str)


@pytest.mark.asyncio
async def test_start_recording_handles_errors(voice_manager_class, mock_discord_channel):
    """
    Test that start_recording handles errors gracefully.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        mock_discord_channel: Mock Discord channel fixture
    """
    with patch.object(voice_manager_class, 'send_command', return_value=False):
        result = await voice_manager_class.start_recording(
            guild_id=111,
            channel=mock_discord_channel,
            target_user_id=123
        )

        assert result is False


@pytest.mark.asyncio
async def test_stop_recording_creates_command(voice_manager_class, cleanup_ipc_files):
    """
    Test that stop_recording creates the correct command file.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    guild_id = 111111111

    result = await voice_manager_class.stop_recording(guild_id=guild_id)

    assert result is True
    assert commands_file.exists()

    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert data['action'] == 'stop_recording'
    assert data['guildId'] == str(guild_id)


@pytest.mark.asyncio
async def test_stop_recording_handles_errors(voice_manager_class):
    """
    Test that stop_recording handles errors gracefully.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
    """
    with patch.object(voice_manager_class, 'send_command', return_value=False):
        result = await voice_manager_class.stop_recording(guild_id=111)

        assert result is False


@pytest.mark.asyncio
async def test_start_recording_logs_info(voice_manager_class, cleanup_ipc_files,
                                         mock_discord_channel):
    """
    Test that start_recording logs appropriate info messages.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
        mock_discord_channel: Mock Discord channel fixture
    """
    with patch('audio_archive_bot.voice_manager_hybrid.logger') as mock_logger:
        await voice_manager_class.start_recording(
            guild_id=111,
            channel=mock_discord_channel,
            target_user_id=123
        )

        # Verify logging calls were made
        assert mock_logger.info.called


@pytest.mark.asyncio
async def test_stop_recording_logs_info(voice_manager_class, cleanup_ipc_files):
    """
    Test that stop_recording logs appropriate info messages.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    with patch('audio_archive_bot.voice_manager_hybrid.logger') as mock_logger:
        await voice_manager_class.stop_recording(guild_id=111)

        # Verify logging calls were made
        assert mock_logger.info.called


@pytest.mark.parametrize("action,kwargs", [
    ("start_recording", {"guildId": "111", "channelId": "222", "targetUserId": "333"}),
    ("stop_recording", {"guildId": "111"}),
    ("custom_action", {"param1": "value1", "param2": "value2"}),
])
def test_send_command_with_various_actions(voice_manager_class, cleanup_ipc_files,
                                           action, kwargs):
    """
    Test send_command with various action types and parameters.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
        action: Action string to test
        kwargs: Keyword arguments to pass
    """
    commands_file, _ = cleanup_ipc_files

    voice_manager_class.send_command(action, **kwargs)

    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert data['action'] == action
    for key, value in kwargs.items():
        assert data[key] == value


def test_commands_file_is_valid_json(voice_manager_class, cleanup_ipc_files):
    """
    Test that the created commands file is always valid JSON.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    # Test with various data types
    voice_manager_class.send_command(
        'test',
        string_param="test",
        int_param=123,
        bool_param=True,
        list_param=[1, 2, 3],
        dict_param={"key": "value"}
    )

    # Should be able to parse without errors
    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_concurrent_command_sends(voice_manager_class, cleanup_ipc_files):
    """
    Test that concurrent send_command calls don't corrupt the file.

    Args:
        voice_manager_class: HybridVoiceManager class fixture
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    commands_file, _ = cleanup_ipc_files

    # Send multiple commands concurrently
    tasks = [
        asyncio.create_task(
            asyncio.to_thread(
                voice_manager_class.send_command,
                f'action_{i}'
            )
        )
        for i in range(5)
    ]

    await asyncio.gather(*tasks)

    # File should still be valid JSON
    with open(commands_file, 'r') as f:
        data = json.load(f)

    assert isinstance(data, dict)
    assert 'action' in data
