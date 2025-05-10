"""Configuration manager for Owera CLI."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
import logging

class Config:
    """Configuration manager for Owera CLI."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_file = config_file or os.getenv("OWERA_CONFIG", "config/default.yaml")
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self, config_file: Optional[str] = None) -> None:
        """Load configuration from file."""
        if config_file:
            self.config_file = config_file
        
        try:
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            logging.warning(f"Config file not found: {self.config_file}")
            self.config = {}
        except yaml.YAMLError as e:
            logging.error(f"Error parsing config file: {e}")
            self.config = {}
    
    def save(self, config_file: Optional[str] = None) -> None:
        """Save configuration to file."""
        if config_file:
            self.config_file = config_file
        
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        except Exception as e:
            logging.error(f"Error saving config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def delete(self, key: str) -> None:
        """Delete configuration value."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                return
            config = config[k]
        
        if keys[-1] in config:
            del config[keys[-1]]
    
    def has(self, key: str) -> bool:
        """Check if configuration key exists."""
        return self.get(key) is not None
    
    def clear(self) -> None:
        """Clear all configuration."""
        self.config = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.config.copy()
    
    def update(self, config: Dict[str, Any]) -> None:
        """Update configuration with dictionary."""
        self.config.update(config)
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return str(self.config)
    
    def __repr__(self) -> str:
        """Representation of configuration."""
        return f"Config(config_file='{self.config_file}')"

config = Config() 