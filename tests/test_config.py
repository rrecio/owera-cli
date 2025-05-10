"""Tests for the Config class."""

import os
import pytest
from owera.config import Config

@pytest.fixture
def config(tmp_path):
    """Create a Config instance for testing."""
    return Config(str(tmp_path))

def test_config_creation(config):
    """Test creating a new Config instance."""
    assert os.path.exists(config.config_dir)
    assert os.path.exists(config.config_file)
    assert config.projects_dir is not None
    assert config.template_dir is not None

def test_config_load(config):
    """Test loading configuration."""
    # Load configuration
    config.load()
    
    assert config.projects_dir is not None
    assert config.template_dir is not None

def test_config_save(config):
    """Test saving configuration."""
    # Set configuration
    config.projects_dir = "/tmp/projects"
    config.template_dir = "/tmp/templates"
    
    # Save configuration
    config.save()
    
    # Load configuration
    config.load()
    
    assert config.projects_dir == "/tmp/projects"
    assert config.template_dir == "/tmp/templates"

def test_config_get_set(config):
    """Test getting and setting configuration values."""
    # Set configuration
    config.set("test_key", "test_value")
    
    # Get configuration
    assert config.get("test_key") == "test_value"
    
    # Get non-existent configuration
    assert config.get("non_existent") is None
    
    # Get non-existent configuration with default
    assert config.get("non_existent", "default") == "default"

def test_config_environment_variables(config):
    """Test environment variables."""
    # Set environment variables
    os.environ["OWERA_PROJECTS_DIR"] = "/tmp/projects"
    os.environ["OWERA_TEMPLATE_DIR"] = "/tmp/templates"
    
    # Load configuration
    config.load()
    
    assert config.projects_dir == "/tmp/projects"
    assert config.template_dir == "/tmp/templates"
    
    # Clear environment variables
    del os.environ["OWERA_PROJECTS_DIR"]
    del os.environ["OWERA_TEMPLATE_DIR"]

def test_config_default_values():
    """Test default configuration values."""
    config = Config()
    assert config.SECRET_KEY == 'your-secret-key'
    assert config.DATABASE_URI == 'sqlite:///database.db'
    assert config.MODEL_NAME == 'qwen2.5-coder:7b'
    assert config.TIMEOUT == 60
    assert config.DEBUG is False
    assert config.LOG_LEVEL == 'INFO'

def test_config_from_env(monkeypatch):
    """Test configuration from environment variables."""
    monkeypatch.setenv('OWERA_SECRET_KEY', 'test-secret')
    monkeypatch.setenv('OWERA_DATABASE_URI', 'sqlite:///test.db')
    monkeypatch.setenv('OWERA_MODEL', 'test-model')
    monkeypatch.setenv('OWERA_TIMEOUT', '30')
    monkeypatch.setenv('OWERA_DEBUG', 'true')
    monkeypatch.setenv('OWERA_LOG_LEVEL', 'DEBUG')
    
    config = Config()
    assert config.SECRET_KEY == 'test-secret'
    assert config.DATABASE_URI == 'sqlite:///test.db'
    assert config.MODEL_NAME == 'test-model'
    assert config.TIMEOUT == 30
    assert config.DEBUG is True
    assert config.LOG_LEVEL == 'DEBUG'

def test_config_from_dict():
    """Test configuration from dictionary."""
    config_dict = {
        'SECRET_KEY': 'dict-secret',
        'DATABASE_URI': 'sqlite:///dict.db',
        'MODEL_NAME': 'dict-model',
        'TIMEOUT': 45,
        'DEBUG': True,
        'LOG_LEVEL': 'WARNING'
    }
    
    config = Config.from_dict(config_dict)
    assert config.SECRET_KEY == 'dict-secret'
    assert config.DATABASE_URI == 'sqlite:///dict.db'
    assert config.MODEL_NAME == 'dict-model'
    assert config.TIMEOUT == 45
    assert config.DEBUG is True
    assert config.LOG_LEVEL == 'WARNING'

def test_config_invalid_timeout(monkeypatch):
    """Test invalid timeout value."""
    monkeypatch.setenv('OWERA_TIMEOUT', 'invalid')
    with pytest.raises(ValueError):
        Config() 