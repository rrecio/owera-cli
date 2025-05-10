# Testing Guide

This guide covers the testing infrastructure and practices for Owera CLI.

## Test Structure

The test suite is organized as follows:

```
tests/
├── agents/           # Agent-specific tests
├── integration/      # Integration tests
├── unit/            # Unit tests
└── conftest.py      # Shared test fixtures
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=owera

# Run specific test file
pytest tests/agents/test_ux_specialist.py

# Run tests with specific marker
pytest -m "integration"
```

### Test Categories

Tests are categorized using pytest markers:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Long-running tests

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
```

## Writing Tests

### Agent Tests

Agent tests should cover:

1. Initialization
2. Prompt generation
3. Response processing
4. Tool functionality
5. Error handling

Example:

```python
def test_ux_specialist_initialization(ux_specialist):
    """Test UX Specialist initialization."""
    assert ux_specialist.role == "UX Specialist"
    assert "user_flow" in ux_specialist.tools
```

### Integration Tests

Integration tests should verify:

1. Agent collaboration
2. End-to-end workflows
3. Project generation
4. File system operations

Example:

```python
def test_project_generation_workflow(app, client):
    """Test complete project generation workflow."""
    # Test steps
    pass
```

## Best Practices

1. **Test Isolation**
   - Each test should be independent
   - Use fixtures for setup and teardown
   - Clean up resources after tests

2. **Coverage**
   - Aim for high test coverage
   - Focus on critical paths
   - Test edge cases and error conditions

3. **Performance**
   - Keep tests fast
   - Use appropriate markers for slow tests
   - Mock external dependencies

4. **Maintenance**
   - Keep tests up to date
   - Document test purpose
   - Use meaningful test names

## Continuous Integration

Tests are automatically run on:

- Pull requests
- Merges to main branch
- Daily scheduled runs

## Debugging Tests

### Common Issues

1. **Test Failures**
   - Check test environment
   - Verify dependencies
   - Review test logs

2. **Slow Tests**
   - Use `pytest --durations=10`
   - Profile test execution
   - Optimize slow tests

### Debugging Tools

```bash
# Run tests with debugger
pytest --pdb

# Show test durations
pytest --durations=0

# Generate coverage report
pytest --cov=owera --cov-report=html
```

## Adding New Tests

1. Create test file in appropriate directory
2. Write test cases
3. Add necessary fixtures
4. Run tests locally
5. Submit pull request

## Test Documentation

- Document test purpose
- Explain complex test scenarios
- Keep test documentation up to date
- Include examples where helpful 