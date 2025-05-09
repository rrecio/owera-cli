import pytest
import os
import tempfile
import logging
from owera.models.base import Project, Feature, Task, Issue
from owera.config import Config

@pytest.fixture(scope="session")
def test_config():
    """Create a test configuration."""
    return Config(
        OPENAI_API_KEY="test_key",
        DEBUG=True,
        LOG_LEVEL="DEBUG",
        MAX_ITERATIONS=10,
        TIMEOUT=5
    )

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test output."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project({
        "project": {
            "name": "TestApp",
            "tech_stack": {
                "backend": "Python/Flask",
                "frontend": "HTML/CSS"
            }
        },
        "features": [
            {
                "name": "home_page",
                "description": "Home page with welcome message",
                "constraints": ["responsive design"]
            },
            {
                "name": "about_page",
                "description": "About page with team information",
                "constraints": []
            }
        ]
    })

@pytest.fixture
def sample_feature():
    """Create a sample feature for testing."""
    return Feature(
        name="test_feature",
        description="Test feature description",
        constraints=["test constraint"]
    )

@pytest.fixture
def sample_task(sample_feature):
    """Create a sample task for testing."""
    return Task(
        feature=sample_feature,
        description="Test task description",
        status="pending"
    )

@pytest.fixture
def sample_issue(sample_feature):
    """Create a sample issue for testing."""
    return Issue(
        feature=sample_feature,
        description="Test issue description",
        severity="low"
    )

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("MAX_ITERATIONS", "10")
    monkeypatch.setenv("TIMEOUT", "5")

@pytest.fixture(autouse=True)
def mock_logging(monkeypatch):
    """Mock logging for testing."""
    class MockLogger:
        def __init__(self, name=None):
            self.name = name or "root"
        
        def debug(self, *args, **kwargs): pass
        def info(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass
        def error(self, *args, **kwargs): pass
        def critical(self, *args, **kwargs): pass
        def addHandler(self, *args, **kwargs): pass
        def removeHandler(self, *args, **kwargs): pass
        def setLevel(self, *args, **kwargs): pass
    
    monkeypatch.setattr(logging, "getLogger", MockLogger)
    monkeypatch.setattr(logging, "basicConfig", lambda **kwargs: None)

@pytest.fixture(autouse=True)
def mock_ollama(monkeypatch):
    """Mock Ollama API calls for testing."""
    def mock_generate(*args, **kwargs):
        return "Mocked response"
    
    monkeypatch.setattr("ollama.generate", mock_generate) 