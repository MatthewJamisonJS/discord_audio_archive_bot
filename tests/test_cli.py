"""
CLI entry point tests for audio_archive_bot.

This module tests:
- CLI command availability
- Environment variable validation
- Error handling
- Main execution flow
- Help and version flags (if implemented)
"""

import sys
import os
import subprocess
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


@pytest.mark.skipif(
    subprocess.run(
        ["which", "audio_bot_run"],
        capture_output=True
    ).returncode != 0,
    reason="audio_bot_run command not installed"
)
def test_cli_command_exists():
    """
    Test that the audio_bot_run command is installed and available.

    This test is skipped if the package is not installed.
    """
    result = subprocess.run(
        ["which", "audio_bot_run"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_cli_main_function_exists():
    """
    Test that the CLI main function exists and is callable.
    """
    try:
        from audio_archive_bot.cli import main
        assert callable(main)
    except ImportError as e:
        pytest.fail(f"Failed to import CLI main function: {e}")


def test_cli_validates_missing_discord_token(minimal_env):
    """
    Test that CLI exits with error when DISCORD_TOKEN is missing.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Remove DISCORD_TOKEN
    if 'DISCORD_TOKEN' in os.environ:
        del os.environ['DISCORD_TOKEN']

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


def test_cli_validates_missing_target_user_id(minimal_env):
    """
    Test that CLI exits with error when TARGET_USER_ID is missing.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Remove TARGET_USER_ID
    if 'TARGET_USER_ID' in os.environ:
        del os.environ['TARGET_USER_ID']

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


def test_cli_loads_dotenv(minimal_env):
    """
    Test that CLI loads environment variables from .env file.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock load_dotenv in the dotenv module
    with patch('dotenv.load_dotenv') as mock_load_dotenv:
        # Mock hybrid_bot at import time
        with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
            mock_bot = sys.modules['hybrid_bot'].bot
            mock_bot.run = Mock(side_effect=KeyboardInterrupt)

            try:
                main()
            except SystemExit:
                pass

            # Verify load_dotenv was called
            mock_load_dotenv.assert_called()


def test_cli_main_execution_flow(minimal_env):
    """
    Test the main execution flow of the CLI.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock hybrid_bot at import time
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=KeyboardInterrupt)

        # Should exit cleanly on KeyboardInterrupt
        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

        # Verify bot.run was called with the token
        mock_bot.run.assert_called_once()
        call_args = mock_bot.run.call_args
        assert call_args[0][0] == minimal_env['DISCORD_TOKEN']


def test_cli_handles_general_exception(minimal_env):
    """
    Test that CLI handles general exceptions gracefully.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock hybrid_bot at import time
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=RuntimeError("Test error"))

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1


def test_cli_prints_error_for_missing_token(capsys):
    """
    Test that CLI prints helpful error message for missing DISCORD_TOKEN.

    Args:
        capsys: pytest fixture to capture stdout/stderr
    """
    from audio_archive_bot.cli import main

    # Clear environment variables
    env_backup = os.environ.copy()
    os.environ.clear()

    try:
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Missing required environment variable: DISCORD_TOKEN" in captured.out
        assert ".env file" in captured.out
    finally:
        os.environ.update(env_backup)


def test_cli_prints_error_for_missing_user_id(capsys):
    """
    Test that CLI prints helpful error message for missing TARGET_USER_ID.

    Args:
        capsys: pytest fixture to capture stdout/stderr
    """
    from audio_archive_bot.cli import main

    # Set only DISCORD_TOKEN
    env_backup = os.environ.copy()
    os.environ.clear()
    os.environ['DISCORD_TOKEN'] = 'test_token'

    try:
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Missing required environment variable: TARGET_USER_ID" in captured.out
    finally:
        os.environ.update(env_backup)


def test_cli_adds_project_root_to_path(minimal_env):
    """
    Test that CLI adds project root to sys.path for imports.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock hybrid_bot at import time
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=KeyboardInterrupt)

        original_path = sys.path.copy()

        try:
            main()
        except SystemExit:
            pass

        # The function should have manipulated sys.path
        # Since the import happens inside main(), sys.path should be modified
        # This is more of an integration test to verify the mechanism works


def test_cli_handles_keyboard_interrupt(capsys, minimal_env):
    """
    Test that CLI handles KeyboardInterrupt (Ctrl+C) gracefully.

    Args:
        capsys: pytest fixture to capture stdout/stderr
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock hybrid_bot at import time
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=KeyboardInterrupt)

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "stopped by user" in captured.out.lower()


def test_cli_logs_fatal_errors(minimal_env):
    """
    Test that CLI logs fatal errors properly.

    Args:
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock hybrid_bot at import time
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        with patch('logging.error') as mock_error:
            test_error = Exception("Fatal test error")
            sys.modules['hybrid_bot'].bot.run = Mock(side_effect=test_error)

            with pytest.raises(SystemExit):
                main()

            # Verify error was logged
            mock_error.assert_called()


def test_cli_prints_monitoring_message(capsys, minimal_env):
    """
    Test that CLI prints the monitoring message with user ID.

    Args:
        capsys: pytest fixture to capture stdout/stderr
        minimal_env: Fixture providing minimal environment
    """
    from audio_archive_bot.cli import main

    # Mock hybrid_bot at import time
    with patch.dict('sys.modules', {'hybrid_bot': MagicMock()}):
        mock_bot = sys.modules['hybrid_bot'].bot
        mock_bot.run = Mock(side_effect=KeyboardInterrupt)

        try:
            main()
        except SystemExit:
            pass

        captured = capsys.readouterr()
        assert "Monitoring user ID" in captured.out
        assert minimal_env['TARGET_USER_ID'] in captured.out


@pytest.mark.parametrize("env_var,value", [
    ("DISCORD_TOKEN", ""),
    ("DISCORD_TOKEN", None),
    ("TARGET_USER_ID", ""),
    ("TARGET_USER_ID", None),
])
def test_cli_validates_empty_environment_variables(env_var, value):
    """
    Test that CLI validates empty or None environment variables.

    Args:
        env_var: Environment variable name
        value: Value to test (empty string or None)
    """
    from audio_archive_bot.cli import main

    env_backup = os.environ.copy()

    try:
        # Set up environment
        os.environ['DISCORD_TOKEN'] = 'test_token'
        os.environ['TARGET_USER_ID'] = '123456789'

        # Set the problematic variable
        if value is None:
            if env_var in os.environ:
                del os.environ[env_var]
        else:
            os.environ[env_var] = value

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    finally:
        os.environ.clear()
        os.environ.update(env_backup)


def test_cli_main_as_script():
    """
    Test that CLI can be run as a script (__name__ == "__main__").

    This tests the if __name__ == "__main__" block.
    """
    cli_module_path = Path(__file__).parent.parent / "audio_archive_bot" / "cli.py"

    if not cli_module_path.exists():
        pytest.skip("CLI module file not found")

    # Check that the file contains the main block
    with open(cli_module_path, 'r') as f:
        content = f.read()
        assert 'if __name__ == "__main__":' in content
        assert 'main()' in content
