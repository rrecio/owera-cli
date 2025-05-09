import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Config:
    """Configuration settings for Owera CLI."""
    SECRET_KEY: str = os.getenv('OWERA_SECRET_KEY', 'your-secret-key')
    DATABASE_URI: str = os.getenv('OWERA_DATABASE_URI', 'sqlite:///database.db')
    MODEL_NAME: str = os.getenv('OWERA_MODEL', 'qwen2.5-coder:7b')
    TIMEOUT: int = int(os.getenv('OWERA_TIMEOUT', '60'))
    DEBUG: bool = os.getenv('OWERA_DEBUG', 'False').lower() == 'true'
    LOG_LEVEL: str = os.getenv('OWERA_LOG_LEVEL', 'INFO')
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create a Config instance from a dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})

config = Config() 