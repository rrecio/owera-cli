# Owera CLI Development Guide

## Table of Contents
1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Release Process](#release-process)

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv, conda, etc.)
- Code editor (VS Code recommended)

### Setup Steps
1. Clone the repository:
```bash
git clone https://github.com/yourusername/owera-cli.git
cd owera-cli
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Project Structure

```
owera-cli/
├── owera/              # Main package
│   ├── agents/         # AI agent implementations
│   │   ├── base.py     # Base agent class
│   │   ├── ui.py       # UI specialist
│   │   ├── dev.py      # Developer
│   │   ├── qa.py       # QA specialist
│   │   └── po.py       # Product owner
│   ├── models/         # Data models
│   │   ├── base.py     # Base model class
│   │   ├── project.py  # Project model
│   │   ├── feature.py  # Feature model
│   │   └── task.py     # Task model
│   ├── utils/          # Utility functions
│   │   ├── dep.py      # Dependency management
│   │   └── spec.py     # Specification parsing
│   ├── generator/      # Code generation
│   │   ├── base.py     # Base generator
│   │   └── templates/  # Code templates
│   └── main.py         # CLI entry point
├── tests/              # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── utils/         # Test utilities
├── docs/              # Documentation
├── examples/          # Example projects
└── scripts/           # Development scripts
```

## Code Style

### Python Style Guide
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions
- Keep functions small and focused
- Use meaningful variable names

### Example
```python
from typing import List, Dict, Any

def process_feature(feature: Dict[str, Any]) -> bool:
    """Process a feature specification.
    
    Args:
        feature: Feature specification dictionary
        
    Returns:
        bool: True if processing was successful
        
    Raises:
        ValueError: If feature specification is invalid
    """
    if not _validate_feature(feature):
        raise ValueError("Invalid feature specification")
    
    return _process_feature_impl(feature)
```

### Git Workflow
1. Create feature branch:
```bash
git checkout -b feature/your-feature
```

2. Make changes and commit:
```bash
git add .
git commit -m "feat: add new feature"
```

3. Push changes:
```bash
git push origin feature/your-feature
```

4. Create pull request

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Testing
- `chore:` Maintenance

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_feature.py

# Run with coverage
pytest --cov=owera

# Run with verbose output
pytest -v
```

### Writing Tests
1. Use pytest fixtures
2. Follow AAA pattern (Arrange, Act, Assert)
3. Test edge cases
4. Mock external dependencies

Example:
```python
import pytest
from owera.models import Feature

def test_feature_validation():
    # Arrange
    feature = Feature(
        name="test_feature",
        description="Test feature"
    )
    
    # Act
    is_valid = feature.validate()
    
    # Assert
    assert is_valid
```

## Documentation

### Docstring Format
Use Google style docstrings:
```python
def function_name(param1: str, param2: int) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: Description of when this exception is raised
    """
```

### Documentation Updates
1. Update docstrings when changing code
2. Update README.md for major changes
3. Update user guide for new features
4. Update API docs for interface changes

## Release Process

### Versioning
Follow semantic versioning:
- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

### Release Steps
1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create release branch
4. Run tests and checks
5. Create release tag
6. Build and publish package

### Package Building
```bash
# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

## Contributing

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit pull request

### Code Review
- All PRs require review
- Address review comments
- Keep PRs focused and small
- Update documentation

### Continuous Integration
- All tests must pass
- Code coverage must be maintained
- Style checks must pass
- Documentation must be up to date 