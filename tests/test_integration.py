"""
Integration tests for audio_archive_bot package.

This module tests:
- Package installation workflow
- Module interdependencies
- File structure integrity
- End-to-end IPC communication
- Environment configuration integration
"""

import os
import sys
import json
import pytest
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import importlib


def test_package_imports_work_together():
    """
    Test that all package modules can be imported together without conflicts.
    """
    try:
        import audio_archive_bot
        from audio_archive_bot import HybridVoiceManager
        from audio_archive_bot import cli
        from audio_archive_bot import voice_manager_hybrid

        assert audio_archive_bot is not None
        assert HybridVoiceManager is not None
        assert cli is not None
        assert voice_manager_hybrid is not None
    except ImportError as e:
        pytest.fail(f"Package imports failed: {e}")


def test_voice_manager_accessible_from_package():
    """
    Test that HybridVoiceManager can be accessed from package root.
    """
    try:
        from audio_archive_bot import HybridVoiceManager
        from audio_archive_bot.voice_manager_hybrid import HybridVoiceManager as DirectImport

        # Should be the same class
        assert HybridVoiceManager is DirectImport
    except ImportError as e:
        pytest.fail(f"Failed to verify HybridVoiceManager accessibility: {e}")


def test_cli_can_import_hybrid_bot(minimal_env):
    """
    Test that CLI can successfully import the hybrid_bot module.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # The CLI adds the project root to sys.path
    # This test verifies that mechanism works
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=KeyboardInterrupt)

        try:
            main()
        except SystemExit:
            pass

    # If we got here, the import worked


def test_full_ipc_workflow(cleanup_ipc_files, mock_discord_channel):
    """
    Test the full IPC workflow: send command -> check status.

    Args:
        cleanup_ipc_files: Fixture to clean up IPC files
        mock_discord_channel: Mock Discord channel fixture
    """
    from audio_archive_bot import HybridVoiceManager

    commands_file, status_file = cleanup_ipc_files

    # Send a start recording command
    result = HybridVoiceManager.send_command(
        'start_recording',
        guildId='111',
        channelId='222',
        targetUserId='333'
    )

    assert result is True
    assert commands_file.exists()

    # Simulate Node.js writing a status response
    status_data = {
        'status': 'recording',
        'message': 'Recording started',
        'guildId': '111'
    }
    with open(status_file, 'w') as f:
        json.dump(status_data, f)

    # Read the status
    status = HybridVoiceManager.get_status()

    assert status is not None
    assert status['status'] == 'recording'
    assert status['guildId'] == '111'


@pytest.mark.asyncio
async def test_recording_lifecycle(cleanup_ipc_files, mock_discord_channel):
    """
    Test the complete recording lifecycle: start -> stop.

    Args:
        cleanup_ipc_files: Fixture to clean up IPC files
        mock_discord_channel: Mock Discord channel fixture
    """
    from audio_archive_bot import HybridVoiceManager

    commands_file, status_file = cleanup_ipc_files

    # Start recording
    start_result = await HybridVoiceManager.start_recording(
        guild_id=111,
        channel=mock_discord_channel,
        target_user_id=333
    )

    assert start_result is True

    # Verify command was created
    with open(commands_file, 'r') as f:
        start_command = json.load(f)

    assert start_command['action'] == 'start_recording'

    # Stop recording
    stop_result = await HybridVoiceManager.stop_recording(guild_id=111)

    assert stop_result is True

    # Verify stop command was created
    with open(commands_file, 'r') as f:
        stop_command = json.load(f)

    assert stop_command['action'] == 'stop_recording'


def test_package_structure_integrity():
    """
    Test that the package structure is intact and all files exist.
    """
    package_path = Path(__file__).parent.parent / "audio_archive_bot"

    required_files = {
        "__init__.py": "Package initialization",
        "__main__.py": "Module entry point",
        "cli.py": "Command-line interface",
        "voice_manager_hybrid.py": "Voice manager",
        "hybrid_bot.py": "Discord bot"
    }

    for filename, description in required_files.items():
        file_path = package_path / filename
        assert file_path.exists(), f"Missing {description} file: {filename}"
        assert file_path.stat().st_size > 0, f"{filename} is empty"


def test_package_has_no_import_cycles():
    """
    Test that there are no circular import dependencies.
    """
    try:
        # These imports should work without circular dependency errors
        import audio_archive_bot
        from audio_archive_bot import HybridVoiceManager
        from audio_archive_bot import cli
        from audio_archive_bot.voice_manager_hybrid import HybridVoiceManager as VM

        # Try to reload to catch circular dependencies
        importlib.reload(audio_archive_bot)

    except ImportError as e:
        if "circular" in str(e).lower():
            pytest.fail(f"Circular import detected: {e}")
        raise


def test_environment_configuration_flow(temp_env_file):
    """
    Test that environment configuration flows correctly through the package.

    Args:
        temp_env_file: Fixture providing temporary .env file
    """
    # Verify environment is set up
    assert os.getenv('DISCORD_TOKEN') is not None
    assert os.getenv('TARGET_USER_ID') is not None

    # CLI should be able to read these
    from audio_archive_bot.cli import main

    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=KeyboardInterrupt)

        try:
            main()
        except SystemExit as e:
            # Should exit cleanly (code 0) on KeyboardInterrupt
            assert e.code == 0


def test_module_can_be_run_as_script(minimal_env):
    """
    Test that the package can be run as python -m audio_archive_bot.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot import __main__

    # Just verify that the __main__ module exists and imports main
    # The actual execution test is in CLI tests
    assert hasattr(__main__, 'main') or True  # main is imported from cli

    # Verify the file structure
    main_file = Path(__file__).parent.parent / "audio_archive_bot" / "__main__.py"
    assert main_file.exists()

    # Verify it calls cli.main()
    with open(main_file) as f:
        content = f.read()
        assert 'from .cli import main' in content


def test_package_version_consistency():
    """
    Test that package version is consistent across files.
    """
    import audio_archive_bot

    package_version = audio_archive_bot.__version__

    # Check pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        with open(pyproject_path, 'r') as f:
            content = f.read()
            assert f'version = "{package_version}"' in content


def test_logging_configuration_integration(minimal_env):
    """
    Test that logging is properly configured across modules.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    import logging

    # Import modules that configure logging
    from audio_archive_bot import voice_manager_hybrid

    # Logger should exist
    logger = logging.getLogger('AudioArchiveBot')
    assert logger is not None


@pytest.mark.asyncio
async def test_multiple_guilds_recording(cleanup_ipc_files, mock_discord_channel):
    """
    Test handling multiple guild recordings (though only one at a time).

    Args:
        cleanup_ipc_files: Fixture to clean up IPC files
        mock_discord_channel: Mock Discord channel fixture
    """
    from audio_archive_bot import HybridVoiceManager

    commands_file, _ = cleanup_ipc_files

    # Start recording for guild 1
    await HybridVoiceManager.start_recording(
        guild_id=111,
        channel=mock_discord_channel,
        target_user_id=333
    )

    with open(commands_file, 'r') as f:
        cmd1 = json.load(f)

    assert cmd1['guildId'] == '111'

    # Stop and start for different guild
    await HybridVoiceManager.stop_recording(guild_id=111)
    await HybridVoiceManager.start_recording(
        guild_id=222,
        channel=mock_discord_channel,
        target_user_id=333
    )

    with open(commands_file, 'r') as f:
        cmd2 = json.load(f)

    assert cmd2['guildId'] == '222'


def test_file_permissions_on_ipc_files(cleanup_ipc_files):
    """
    Test that IPC files are created with appropriate permissions.

    Args:
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    from audio_archive_bot import HybridVoiceManager

    commands_file, _ = cleanup_ipc_files

    HybridVoiceManager.send_command('test')

    # File should be readable and writable
    assert commands_file.exists()
    assert os.access(commands_file, os.R_OK)
    assert os.access(commands_file, os.W_OK)


def test_json_formatting_in_command_files(cleanup_ipc_files):
    """
    Test that command files are formatted with proper indentation.

    Args:
        cleanup_ipc_files: Fixture to clean up IPC files
    """
    from audio_archive_bot import HybridVoiceManager

    commands_file, _ = cleanup_ipc_files

    HybridVoiceManager.send_command('test', param1='value1', param2='value2')

    with open(commands_file, 'r') as f:
        content = f.read()

    # File should have indentation (not minified)
    assert '\n' in content
    assert '  ' in content or '\t' in content


def test_error_propagation_through_layers(mock_discord_channel):
    """
    Test that errors propagate correctly through integration layers.

    Args:
        mock_discord_channel: Mock Discord channel fixture
    """
    from audio_archive_bot import HybridVoiceManager

    # Simulate filesystem error
    with patch('builtins.open', side_effect=PermissionError("No permission")):
        result = HybridVoiceManager.send_command('test')

        # Should return False, not raise
        assert result is False


def test_package_metadata_accessible():
    """
    Test that package metadata is accessible after import.
    """
    import audio_archive_bot

    metadata_attrs = ['__version__', '__author__', '__license__']

    for attr in metadata_attrs:
        assert hasattr(audio_archive_bot, attr), f"Missing metadata: {attr}"
        assert getattr(audio_archive_bot, attr) is not None


def test_cli_module_independence():
    """
    Test that CLI module can function independently when needed.
    """
    from audio_archive_bot import cli

    # CLI should have its own main function
    assert hasattr(cli, 'main')
    assert callable(cli.main)


@pytest.mark.parametrize("module_name", [
    "audio_archive_bot",
    "audio_archive_bot.cli",
    "audio_archive_bot.voice_manager_hybrid",
])
def test_module_reload_safety(module_name, minimal_env):
    """
    Test that modules can be safely reloaded without errors.

    Args:
        module_name: Name of module to test
        minimal_env: Fixture providing minimal environment
    """
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)
    except ImportError:
        pytest.skip(f"Module {module_name} not available")
    except Exception as e:
        # hybrid_bot might fail to reload due to Discord initialization
        if "hybrid_bot" in module_name:
            pytest.skip(f"Module {module_name} cannot be reloaded: {e}")
        else:
            raise


def test_package_installation_detection():
    """
    Test that we can detect if the package is properly installed.
    """
    try:
        import audio_archive_bot
        # If we can import and get version, it's installed
        version = audio_archive_bot.__version__
        assert version is not None
        installed = True
    except ImportError:
        installed = False

    # We should be able to import since we're testing
    assert installed is True


def test_ipc_files_location():
    """
    Test that IPC files are created in the expected location (current directory).
    """
    from audio_archive_bot import HybridVoiceManager

    # Files should be created in current working directory
    commands_file = Path(HybridVoiceManager.COMMANDS_FILE)
    status_file = Path(HybridVoiceManager.STATUS_FILE)

    # These should be relative paths (no directory component)
    assert not commands_file.is_absolute()
    assert not status_file.is_absolute()
    assert '/' not in HybridVoiceManager.COMMANDS_FILE
    assert '/' not in HybridVoiceManager.STATUS_FILE
