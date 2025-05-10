"""Template loading utility for Owera CLI."""

import os
from pathlib import Path
from typing import Dict, List

def load_templates() -> Path:
    """Load project templates.
    
    Returns:
        Path to the templates directory.
        
    Raises:
        FileNotFoundError: If templates directory is not found.
    """
    # Get the package directory
    package_dir = Path(__file__).parent.parent
    
    # Look for templates in the package
    templates_dir = package_dir / "templates"
    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found at {templates_dir}")
    
    return templates_dir 