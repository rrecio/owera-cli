# Owera CLI Development Guide

## Dependency Management

### Version Compatibility
- Flask 2.3.3 is required for compatibility with pytest-flask 1.2.0
- Werkzeug 2.3.7 is required for compatibility with Flask 2.3.3
- Use `importlib.metadata` instead of `pkg_resources` for modern Python dependency management

### Core Dependencies
```python
CORE_DEPENDENCIES = {
    'flask': '==2.3.3',
    'flask-sqlalchemy': '==3.1.1',
    'flask-login': '==0.6.3',
    'pyjwt': '==2.8.0',
    'python-dotenv': '==1.0.1',
    'requests': '==2.31.0',
    'gitpython': '==3.1.42',
    'click': '==8.1.7',
    'tqdm': '==4.66.2',
    'ollama': '==0.1.6'
}
```

### Development Dependencies
```python
DEV_DEPENDENCIES = {
    'pytest': '==7.4.3',
    'pytest-cov': '==4.1.0',
    'pytest-flask': '==1.2.0',
    'pytest-env': '==1.1.3'
}
```

### Sub-dependencies
```python
SUB_DEPENDENCIES = {
    'Werkzeug': '==2.3.7',
    'Jinja2': '==3.1.2',
    'SQLAlchemy': '==2.0.23',
    'MarkupSafe': '==2.1.3',
    'typing-extensions': '==4.8.0'
}
```

## Testing Configuration

### Flask Test Setup
```python
import pytest
from app import app as flask_app
from app import db

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with authentication."""
    with client.session_transaction() as session:
        session['user_id'] = 1
    return client
```

## Common Issues and Solutions

### 1. Flask Compatibility
- Problem: `ImportError: cannot import name '_request_ctx_stack' from 'flask'`
- Solution: Use Flask 2.3.3 with pytest-flask 1.2.0

### 2. Dependency Management
- Problem: Version conflicts between installed and required packages
- Solution: Use exact version pinning with `==` and maintain compatibility between related packages

### 3. Testing Setup
- Problem: Test configuration issues with Flask app context
- Solution: Use Flask's built-in testing utilities and proper fixture setup

## Best Practices

1. **Dependency Management**
   - Use exact version pinning for core dependencies
   - Keep development dependencies separate
   - Document sub-dependencies explicitly
   - Use `importlib.metadata` for modern Python dependency management

2. **Testing**
   - Use in-memory SQLite database for tests
   - Properly handle database creation and cleanup
   - Use session transactions for authentication testing
   - Keep test fixtures modular and reusable

3. **Error Handling**
   - Log dependency conflicts
   - Provide clear error messages
   - Handle database operations safely in tests

## Project Structure

```
├── owera/ # Main package directory
│ ├── agents/ # AI agent implementations
│ │ ├── base.py # Base agent class
│ │ ├── developer.py # Developer agent
│ │ ├── ui_specialist.py # UI specialist agent
│ │ ├── product_owner.py # Product owner agent
│ │ ├── project_manager.py # Project manager agent
│ │ └── qa_specialist.py # QA specialist agent
│ ├── models/ # Data models
│ │ └── base.py # Base model classes
│ ├── utils/ # Utility functions
│ │ ├── code_generator.py # Code generation utilities
│ │ └── spec_parser.py # Specification parsing utilities
│ ├── main.py # Main CLI entry point
│ ├── config.py # Configuration management
│ └── init.py # Package initialization
├── tests/ # Test suite
├── logs/ # Log files
├── requirements.txt # Project dependencies
├── setup.py # Package setup configuration
├── pytest.ini # Pytest configuration
└── README.md # Project documentation
```

## Future Improvements

1. **Dependency Management**
   - Implement automatic dependency updates
   - Add version conflict resolution strategies
   - Create dependency groups for different environments

2. **Testing**
   - Add more test fixtures for common scenarios
   - Implement integration tests
   - Add performance testing capabilities

3. **Documentation**
   - Add API documentation
   - Create user guides
   - Document deployment procedures

### Key Components

1. **Agents (`owera/agents/`)**
   - Each agent is responsible for a specific aspect of development
   - Agents inherit from `base.py` and implement specialized logic
   - Agents work together to generate complete applications

2. **Models (`owera/models/`)**
   - Contains data models and business logic
   - `base.py` defines core model classes used throughout the application

3. **Utils (`owera/utils/`)**
   - `code_generator.py`: Handles code generation and project setup
   - `spec_parser.py`: Parses project specifications from various formats

4. **Configuration**
   - `config.py`: Manages application configuration
   - `pytest.ini`: Configures test settings
   - `setup.py`: Defines package metadata and dependencies

5. **Generated Projects**
   - Projects are generated in their own directories (e.g., `shopeasy/`, `my-blog/`)
   - Each generated project follows a standard structure:
     ```
     project_name/
     ├── src/           # Source code
     ├── tests/         # Test files
     ├── templates/     # HTML templates
     ├── static/        # Static assets
     └── docs/          # Documentation
     ```

### Best Practices

1. **Code Organization**
   - Keep agent logic separate and focused
   - Use utility functions for common operations
   - Maintain clear separation of concerns

2. **Testing**
   - Place tests in the `tests/` directory
   - Use pytest fixtures for common test setup
   - Maintain test coverage reports

3. **Documentation**
   - Keep README.md up to date
   - Document agent responsibilities
   - Include usage examples

4. **Configuration**
   - Use environment variables for sensitive data
   - Keep configuration in dedicated files
   - Document configuration options

