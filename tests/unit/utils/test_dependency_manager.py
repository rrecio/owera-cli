import pytest
from unittest.mock import patch, MagicMock
from owera.utils.dependency_manager import DependencyManager

@pytest.fixture
def mock_config():
    return {
        "dependencies": {
            "flask": "2.3.3",
            "werkzeug": "2.3.7",
            "pytest": "7.4.3"
        }
    }

@pytest.fixture
def mock_installed_packages():
    return {
        "flask": "2.3.3",
        "werkzeug": "2.3.7",
        "pytest": "7.4.0"
    }

def test_dependency_manager_initialization(mock_config):
    """Test dependency manager initialization."""
    with patch("yaml.safe_load", return_value=mock_config):
        manager = DependencyManager()
        assert manager.required_versions == mock_config["dependencies"]

def test_check_dependencies(mock_config, mock_installed_packages):
    """Test dependency conflict checking."""
    with patch("yaml.safe_load", return_value=mock_config), \
         patch("pkg_resources.working_set", return_value=[
             MagicMock(key=k, version=v) for k, v in mock_installed_packages.items()
         ]):
        manager = DependencyManager()
        conflicts = manager.check_dependencies()
        assert len(conflicts) == 1
        assert conflicts[0][0] == "pytest"
        assert conflicts[0][1] == "7.4.0"
        assert conflicts[0][2] == "7.4.3"

def test_get_update_commands(mock_config, mock_installed_packages):
    """Test update command generation."""
    with patch("yaml.safe_load", return_value=mock_config), \
         patch("pkg_resources.working_set", return_value=[
             MagicMock(key=k, version=v) for k, v in mock_installed_packages.items()
         ]):
        manager = DependencyManager()
        commands = manager.get_update_commands()
        assert len(commands) == 1
        assert commands[0] == "pip install pytest==7.4.3"

def test_validate_environment(mock_config, mock_installed_packages):
    """Test environment validation."""
    with patch("yaml.safe_load", return_value=mock_config), \
         patch("pkg_resources.working_set", return_value=[
             MagicMock(key=k, version=v) for k, v in mock_installed_packages.items()
         ]):
        manager = DependencyManager()
        assert not manager.validate_environment()

def test_update_dependencies_dry_run(mock_config, mock_installed_packages):
    """Test dependency update in dry run mode."""
    with patch("yaml.safe_load", return_value=mock_config), \
         patch("pkg_resources.working_set", return_value=[
             MagicMock(key=k, version=v) for k, v in mock_installed_packages.items()
         ]):
        manager = DependencyManager()
        commands = manager.update_dependencies(dry_run=True)
        assert len(commands) == 1
        assert commands[0] == "pip install pytest==7.4.3" 