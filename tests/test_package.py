"""
Package structure and import tests for audio_archive_bot.

This module tests:
- Package can be imported successfully
- Version information is correct
- All submodules are accessible
- No import errors occur
- Package structure integrity
"""

import sys
import importlib
import pytest
from pathlib import Path


def test_package_import():
    """
    Test that the audio_archive_bot package can be imported.

    This is a fundamental test to ensure the package is properly installed
    and structured.
    """
    try:
        import audio_archive_bot
        assert audio_archive_bot is not None
    except ImportError as e:
        pytest.fail(f"Failed to import audio_archive_bot package: {e}")


def test_package_version():
    """
    Test that the package version is correctly set to 0.1.0.

    The version should match the specification in pyproject.toml.
    """
    try:
        import audio_archive_bot
        assert hasattr(audio_archive_bot, '__version__')
        assert audio_archive_bot.__version__ == "0.1.0"
    except ImportError:
        pytest.skip("Package not installed, skipping version test")


def test_package_metadata():
    """
    Test that package metadata attributes exist.

    Checks for __author__, __license__, and __version__ attributes.
    """
    try:
        import audio_archive_bot
        assert hasattr(audio_archive_bot, '__version__')
        assert hasattr(audio_archive_bot, '__author__')
        assert hasattr(audio_archive_bot, '__license__')

        assert audio_archive_bot.__license__ == "MIT"
        assert audio_archive_bot.__author__ == "Audio Archive Bot Contributors"
    except ImportError:
        pytest.skip("Package not installed, skipping metadata test")


def test_hybrid_voice_manager_import():
    """
    Test that HybridVoiceManager can be imported from the package.

    This is the main public API of the package.
    """
    try:
        from audio_archive_bot import HybridVoiceManager
        assert HybridVoiceManager is not None
    except ImportError as e:
        pytest.fail(f"Failed to import HybridVoiceManager: {e}")


def test_hybrid_voice_manager_accessible():
    """
    Test that HybridVoiceManager is in __all__ exports.
    """
    try:
        import audio_archive_bot
        assert hasattr(audio_archive_bot, '__all__')
        assert 'HybridVoiceManager' in audio_archive_bot.__all__
    except ImportError:
        pytest.skip("Package not installed, skipping __all__ test")


def test_submodule_cli_import():
    """
    Test that the CLI module can be imported.
    """
    try:
        from audio_archive_bot import cli
        assert cli is not None
        assert hasattr(cli, 'main')
    except ImportError as e:
        pytest.fail(f"Failed to import CLI module: {e}")


def test_submodule_voice_manager_import():
    """
    Test that the voice_manager_hybrid module can be imported.
    """
    try:
        from audio_archive_bot import voice_manager_hybrid
        assert voice_manager_hybrid is not None
        assert hasattr(voice_manager_hybrid, 'HybridVoiceManager')
    except ImportError as e:
        pytest.fail(f"Failed to import voice_manager_hybrid module: {e}")


def test_submodule_hybrid_bot_import():
    """
    Test that the hybrid_bot module can be imported.

    Note: This test may fail if Discord credentials are required at import time.
    """
    try:
        # Set minimal environment to prevent errors
        import os
        os.environ.setdefault('DISCORD_TOKEN', 'test_token')
        os.environ.setdefault('TARGET_USER_ID', '123456789')

        from audio_archive_bot import hybrid_bot
        assert hybrid_bot is not None
    except ImportError as e:
        pytest.skip(f"Cannot import hybrid_bot module (may require credentials): {e}")
    except ValueError as e:
        pytest.skip(f"hybrid_bot requires environment configuration: {e}")


def test_no_syntax_errors_in_modules():
    """
    Test that all Python modules in the package have valid syntax.

    This test attempts to compile all .py files to check for syntax errors.
    """
    package_path = Path(__file__).parent.parent / "audio_archive_bot"

    if not package_path.exists():
        pytest.skip("Package directory not found")

    python_files = list(package_path.glob("*.py"))
    assert len(python_files) > 0, "No Python files found in package"

    errors = []
    for py_file in python_files:
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), py_file.name, 'exec')
        except SyntaxError as e:
            errors.append(f"{py_file.name}: {e}")

    assert len(errors) == 0, f"Syntax errors found:\n" + "\n".join(errors)


def test_package_structure():
    """
    Test that the expected package structure exists.

    Verifies that all expected modules are present in the package directory.
    """
    package_path = Path(__file__).parent.parent / "audio_archive_bot"

    if not package_path.exists():
        pytest.skip("Package directory not found")

    expected_files = [
        "__init__.py",
        "__main__.py",
        "cli.py",
        "voice_manager_hybrid.py",
        "hybrid_bot.py"
    ]

    missing_files = []
    for filename in expected_files:
        file_path = package_path / filename
        if not file_path.exists():
            missing_files.append(filename)

    assert len(missing_files) == 0, f"Missing files: {missing_files}"


def test_main_entry_point():
    """
    Test that the package can be run as a module (python -m audio_archive_bot).

    Verifies the __main__.py entry point exists and is properly configured.
    """
    try:
        from audio_archive_bot import __main__
        assert __main__ is not None
    except ImportError as e:
        pytest.fail(f"Failed to import __main__ module: {e}")


def test_hybrid_voice_manager_class_methods():
    """
    Test that HybridVoiceManager has the expected methods.

    Verifies the public API of the HybridVoiceManager class.
    """
    try:
        from audio_archive_bot import HybridVoiceManager

        expected_methods = [
            'send_command',
            'get_status',
            'start_recording',
            'stop_recording'
        ]

        for method_name in expected_methods:
            assert hasattr(HybridVoiceManager, method_name), \
                f"HybridVoiceManager missing method: {method_name}"
    except ImportError:
        pytest.skip("Cannot import HybridVoiceManager")


def test_hybrid_voice_manager_class_attributes():
    """
    Test that HybridVoiceManager has expected class attributes.

    Verifies constants like COMMANDS_FILE and STATUS_FILE.
    """
    try:
        from audio_archive_bot import HybridVoiceManager

        assert hasattr(HybridVoiceManager, 'COMMANDS_FILE')
        assert hasattr(HybridVoiceManager, 'STATUS_FILE')

        assert HybridVoiceManager.COMMANDS_FILE == 'voice_commands.json'
        assert HybridVoiceManager.STATUS_FILE == 'voice_status.json'
    except ImportError:
        pytest.skip("Cannot import HybridVoiceManager")


@pytest.mark.parametrize("module_name", [
    "audio_archive_bot",
    "audio_archive_bot.cli",
    "audio_archive_bot.voice_manager_hybrid",
])
def test_module_imports_without_errors(module_name):
    """
    Test that specific modules can be imported without errors.

    This parametrized test checks multiple module imports.

    Args:
        module_name: Name of the module to import
    """
    try:
        # Set up minimal environment
        import os
        os.environ.setdefault('DISCORD_TOKEN', 'test_token')
        os.environ.setdefault('TARGET_USER_ID', '123456789')

        importlib.import_module(module_name)
    except ImportError as e:
        pytest.fail(f"Failed to import {module_name}: {e}")
    except Exception as e:
        # Some modules may require full Discord setup
        pytest.skip(f"Module {module_name} requires full setup: {e}")


def test_package_does_not_import_discord_at_package_level():
    """
    Test that importing the package doesn't immediately require Discord.

    The package should be importable even if discord.py is not installed,
    as long as we don't try to use the bot functionality.
    """
    try:
        # This should work without Discord being available
        import audio_archive_bot
        assert audio_archive_bot.__version__ is not None
    except ImportError as e:
        if "discord" in str(e).lower():
            pytest.fail("Package imports Discord at package level, should be lazy")
        raise
