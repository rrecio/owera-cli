import os
from typing import Dict, Any

class Config:
    """Configuration class for Owera."""
    def __init__(self, **kwargs):
        """Initialize configuration."""
        self.SECRET_KEY = kwargs.get('SECRET_KEY') or os.getenv('OWERA_SECRET_KEY', 'your-secret-key')
        self.DATABASE_URI = kwargs.get('DATABASE_URI') or os.getenv('OWERA_DATABASE_URI', 'sqlite:///database.db')
        self.MODEL_NAME = kwargs.get('MODEL_NAME') or os.getenv('OWERA_MODEL', 'qwen2.5-coder:7b')
        self.DEBUG = kwargs.get('DEBUG') or os.getenv('OWERA_DEBUG', 'false').lower() == 'true'
        self.LOG_LEVEL = kwargs.get('LOG_LEVEL') or os.getenv('OWERA_LOG_LEVEL', 'INFO')
        self.MAX_ITERATIONS = int(kwargs.get('MAX_ITERATIONS') or os.getenv('OWERA_MAX_ITERATIONS', '10'))
        
        try:
            self.TIMEOUT = int(kwargs.get('TIMEOUT') or os.getenv('OWERA_TIMEOUT', '60'))
        except ValueError:
            raise ValueError("TIMEOUT must be a valid integer")

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create configuration from dictionary."""
        return cls(**config_dict)

config = Config() 