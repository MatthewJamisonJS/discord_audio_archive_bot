# Audio Archive Bot Test Suite

Comprehensive pytest test suite for the audio_archive_bot package.

## Overview

This test suite provides **80 test cases** covering all aspects of the audio_archive_bot package, including unit tests, integration tests, and CLI tests. The tests are designed to run in CI/CD environments and do not require actual Discord credentials.

## Test Files

### 1. `conftest.py` - Pytest Configuration and Fixtures

Central configuration file providing shared fixtures and test utilities:

**Fixtures:**
- `temp_env_file` - Creates temporary .env files for testing
- `minimal_env` - Sets up minimal required environment variables
- `cleanup_ipc_files` - Cleans up IPC command/status files
- `mock_discord_member` - Mock Discord member objects
- `mock_discord_channel` - Mock Discord voice channel objects
- `mock_voice_state` - Mock Discord voice state objects
- `sample_command_data` - Sample IPC command data
- `sample_status_data` - Sample IPC status data
- `mock_discord_bot` - Mock Discord bot instance
- `mock_discord_context` - Mock Discord command context
- `reset_logging` - Auto-reset logging between tests

### 2. `test_package.py` - Package Structure Tests (16 tests)

Tests fundamental package structure and imports:

**Test Coverage:**
- Package import verification
- Version validation (0.1.0)
- Package metadata (__author__, __license__)
- HybridVoiceManager accessibility
- Submodule imports (cli, voice_manager_hybrid, hybrid_bot)
- Syntax validation for all .py files
- Package structure integrity
- Entry point validation (__main__.py)
- Public API verification
- Import cycle detection

### 3. `test_cli.py` - CLI Entry Point Tests (18 tests)

Tests command-line interface functionality:

**Test Coverage:**
- CLI command installation detection
- Environment variable validation
- Missing DISCORD_TOKEN handling
- Missing TARGET_USER_ID handling
- Empty/None environment variable handling
- load_dotenv() invocation
- Main execution flow
- KeyboardInterrupt (Ctrl+C) handling
- General exception handling
- Error logging
- User feedback messages
- sys.path manipulation
- Script execution (__name__ == "__main__")

### 4. `test_voice_manager.py` - HybridVoiceManager Unit Tests (27 tests)

Tests the core voice manager functionality:

**Test Coverage:**
- Class existence and structure
- Class constants (COMMANDS_FILE, STATUS_FILE)
- IPC command file creation
- JSON format validation
- Timestamp inclusion
- Multiple parameter handling
- File write error handling
- Command file overwriting
- Status file reading
- Missing status file handling
- Invalid JSON handling
- File read error handling
- Async start_recording() functionality
- ID-to-string conversion
- Async stop_recording() functionality
- Error propagation
- Logging verification
- Parametrized action testing
- JSON validity verification
- Concurrent command handling

### 5. `test_integration.py` - Integration Tests (19 tests)

Tests module interdependencies and end-to-end workflows:

**Test Coverage:**
- Package-wide import compatibility
- HybridVoiceManager accessibility from package root
- CLI → hybrid_bot import chain
- Full IPC workflow (send command → receive status)
- Recording lifecycle (start → stop)
- Package structure integrity
- Circular import detection
- Environment configuration flow
- Module execution as script
- Version consistency across files
- Logging configuration integration
- Multi-guild recording scenarios
- File permissions verification
- JSON formatting validation
- Error propagation through layers
- Package metadata accessibility
- Module independence
- Module reload safety
- Package installation detection
- IPC file location validation

## Running Tests

### Run All Tests

```bash
# From project root
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=audio_archive_bot --cov-report=term-missing
```

### Run Specific Test Files

```bash
pytest tests/test_package.py
pytest tests/test_cli.py
pytest tests/test_voice_manager.py
pytest tests/test_integration.py
```

### Run Specific Test Cases

```bash
# Run a single test
pytest tests/test_package.py::test_package_version

# Run tests matching a pattern
pytest tests/ -k "voice_manager"

# Run parametrized tests
pytest tests/test_cli.py::test_cli_validates_empty_environment_variables
```

### Run with Different Verbosity

```bash
# Quiet mode
pytest tests/ -q

# Verbose mode
pytest tests/ -v

# Very verbose (show individual test output)
pytest tests/ -vv
```

## Test Coverage

Current test coverage statistics:

```
Module                               Coverage
--------------------------------------------
audio_archive_bot/__init__.py           50%
audio_archive_bot/__main__.py          100%
audio_archive_bot/cli.py               100%
audio_archive_bot/voice_manager.py      89%
--------------------------------------------
Total Package Coverage:                 38%
```

**Note:** The hybrid_bot.py module has lower coverage (37%) because it requires a running Discord bot for full testing. The module is tested through integration tests with mocked Discord components.

## CI/CD Integration

These tests are designed to run in CI/CD environments:

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        run: |
          pytest tests/ --cov=audio_archive_bot --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Test Strategy

### Test-Driven Development (TDD)
- Tests written to verify expected behavior
- Red-Green-Refactor cycle encouraged
- Tests serve as living documentation

### Behavior-Driven Testing
- Tests describe behavior, not implementation
- Descriptive test names (e.g., `test_cli_validates_missing_discord_token`)
- Comprehensive docstrings

### Mocking Strategy
- External dependencies (Discord, filesystem) are mocked
- No actual Discord credentials required
- Tests are fast and isolated
- Mock fixtures provided in conftest.py

### Error Handling Testing
- Both success and failure paths tested
- Edge cases covered (empty strings, None values, etc.)
- Error propagation verified

## Test Data

### Sample IPC Command
```json
{
  "action": "start_recording",
  "timestamp": "2025-10-17T12:00:00",
  "guildId": "111111111",
  "channelId": "222222222",
  "targetUserId": "123456789"
}
```

### Sample IPC Status
```json
{
  "status": "recording",
  "message": "Recording in progress",
  "timestamp": "2025-10-17T12:00:00",
  "guildId": "111111111"
}
```

## Adding New Tests

### 1. Create Test Function

```python
def test_new_feature():
    """Test description."""
    # Arrange
    expected = "value"

    # Act
    result = function_under_test()

    # Assert
    assert result == expected
```

### 2. Use Fixtures

```python
def test_with_fixture(minimal_env, cleanup_ipc_files):
    """Test using fixtures."""
    # Environment is set up automatically
    # IPC files will be cleaned up automatically
    pass
```

### 3. Add Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("value1", "result1"),
    ("value2", "result2"),
])
def test_multiple_cases(input, expected):
    """Test multiple cases."""
    assert process(input) == expected
```

### 4. Add Async Tests

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async functionality."""
    result = await async_function()
    assert result is not None
```

## Troubleshooting

### Test Failures

**Problem:** `ModuleNotFoundError: No module named 'audio_archive_bot'`
**Solution:** Install the package in development mode: `pip install -e .`

**Problem:** `AssertionError` in environment variable tests
**Solution:** Check that fixtures are properly cleaning up environment

**Problem:** IPC file conflicts between tests
**Solution:** Use the `cleanup_ipc_files` fixture

### Running Tests

**Problem:** Tests run slowly
**Solution:** Run in parallel: `pytest tests/ -n auto` (requires pytest-xdist)

**Problem:** Coverage not calculated
**Solution:** Ensure pytest-cov is installed: `pip install pytest-cov`

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Use fixtures to ensure cleanup
3. **Descriptive Names**: Test names should describe what they test
4. **Documentation**: Add docstrings to all tests
5. **Assertions**: Use specific assertions with clear messages
6. **Mocking**: Mock external dependencies
7. **Coverage**: Aim for high coverage, but prioritize critical paths
8. **Performance**: Keep tests fast (< 1 second per test)

## Continuous Improvement

### Adding Coverage

To identify areas needing more tests:

```bash
# Generate HTML coverage report
pytest tests/ --cov=audio_archive_bot --cov-report=html

# Open htmlcov/index.html in browser
open htmlcov/index.html
```

### Test Quality Metrics

- **Total Tests:** 80
- **Pass Rate:** 98.8% (79 passed, 1 skipped)
- **Async Tests:** 8
- **Parametrized Tests:** 7
- **Average Test Runtime:** <0.02 seconds per test
- **Total Suite Runtime:** ~1.5 seconds

## Contributing

When contributing new features:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Add test documentation
5. Update this README if needed

## License

Tests are part of the audio_archive_bot project and follow the same MIT license.
