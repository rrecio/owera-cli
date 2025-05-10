import os
import tempfile
import yaml
from pathlib import Path
from typing import Dict, Any

def create_temp_project_spec(name: str = "TestApp", tech_stack: Dict[str, str] = None) -> str:
    """Create a temporary project specification file."""
    if tech_stack is None:
        tech_stack = {
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        }
    
    spec = {
        "project": {
            "name": name,
            "tech_stack": tech_stack
        },
        "features": [
            {
                "name": "home_page",
                "description": "Home page with welcome message"
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(spec, f)
        return f.name

def create_temp_config(config_data: Dict[str, Any] = None) -> str:
    """Create a temporary configuration file."""
    if config_data is None:
        config_data = {
            "dependencies": {
                "flask": "2.3.3",
                "werkzeug": "2.3.7",
                "pytest": "7.4.3"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        return f.name

def create_temp_project_structure(base_path: str) -> None:
    """Create a temporary project structure for testing."""
    paths = [
        "app.py",
        "models.py",
        "routes.py",
        "templates/home.html",
        "templates/productlist.html",
        "static/css/style.css",
        "static/js/main.js",
        "tests/__init__.py",
        "tests/test_app.py"
    ]
    
    for path in paths:
        full_path = os.path.join(base_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(f"# Test file: {path}\n")

def cleanup_temp_files(*file_paths: str) -> None:
    """Clean up temporary files created during testing."""
    for path in file_paths:
        try:
            os.unlink(path)
        except OSError:
            pass

def create_mock_project() -> Dict[str, Any]:
    """Create a mock project object for testing."""
    return {
        "name": "TestApp",
        "tech_stack": {
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        },
        "features": [
            {
                "name": "home_page",
                "description": "Home page with welcome message",
                "status": "todo"
            }
        ],
        "tasks": [
            {
                "name": "Implement home page",
                "description": "Create the home page with welcome message",
                "status": "todo",
                "assigned_to": "Developer"
            }
        ]
    } 