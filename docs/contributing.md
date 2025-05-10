# Contributing to Owera CLI

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Pull Requests](#pull-requests)
7. [Release Process](#release-process)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)
- Code editor (VS Code recommended)

### Repository Structure
```
owera-cli/
├── owera/              # Main package
│   ├── agents/         # AI agent implementations
│   ├── models/         # Data models
│   ├── utils/          # Utility functions
│   ├── generator/      # Code generation
│   └── main.py         # CLI entry point
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Example projects
└── scripts/            # Development scripts
```

## Development Setup

### Clone Repository
```bash
git clone https://github.com/yourusername/owera-cli.git
cd owera-cli
```

### Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n owera python=3.8
conda activate owera
```

### Install Dependencies
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Configure Development Environment
1. Create `.env` file:
```bash
cp .env.example .env
```

2. Update configuration:
```yaml
# config/development.yaml
system:
  debug: true
  log_level: DEBUG

templates:
  auto_reload: true
```

## Code Style

### Python Style Guide
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- Keep functions small
- Use meaningful names

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

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/psf/black
    rev: 21.5b2
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.9.3
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
```

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
2. Follow AAA pattern
3. Test edge cases
4. Mock dependencies

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

### Test Coverage
- Maintain coverage above 80%
- Cover edge cases
- Test error conditions
- Document test cases

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
1. Update docstrings
2. Update README.md
3. Update user guide
4. Update API docs

## Pull Requests

### Branch Naming
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `refactor/` for refactoring

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Testing
- `chore:` Maintenance

### PR Process
1. Create feature branch
2. Make changes
3. Add tests
4. Update documentation
5. Create pull request
6. Address review comments
7. Merge when approved

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

## Code Review

### Review Checklist
1. Code style compliance
2. Test coverage
3. Documentation updates
4. Error handling
5. Performance considerations
6. Security implications

### Review Process
1. Automated checks
2. Peer review
3. Address comments
4. Final approval
5. Merge

## Development Workflow

### Feature Development
1. Create feature branch
2. Implement feature
3. Add tests
4. Update documentation
5. Create pull request

### Bug Fixes
1. Create fix branch
2. Reproduce issue
3. Implement fix
4. Add test case
5. Create pull request

### Documentation
1. Update docstrings
2. Update guides
3. Add examples
4. Update README

## Support

### Getting Help
- GitHub Issues
- Documentation
- Community chat
- Email support

### Reporting Issues
1. Check existing issues
2. Create new issue
3. Provide details
4. Include reproduction steps

## License

### Code License
- MIT License
- See LICENSE file

### Contribution License
- Contributor License Agreement
- Sign CLA before contributing 