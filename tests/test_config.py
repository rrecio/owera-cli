import os
import pytest
from owera.config import Config

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