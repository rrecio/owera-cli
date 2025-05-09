import pytest
from unittest.mock import patch, mock_open
from click.testing import CliRunner
from owera.main import owera
from owera.models.base import Project
from owera.agents import UISpecialist, Developer, QASpecialist, ProductOwner, ProjectManager

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_project():
    return {
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
            }
        ]
    }

def test_owera_command_with_spec(runner, mock_project):
    """Test the owera command with a specification."""
    with patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'):
        
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}'])
        assert result.exit_code == 0
        assert "Starting project generation" in result.output

def test_owera_command_with_spec_file(runner, mock_project):
    """Test the owera command with a specification file."""
    mock_spec = '{"project": {"name": "TestApp"}}'
    with patch('builtins.open', mock_open(read_data=mock_spec)), \
         patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'):
        
        result = runner.invoke(owera, ['--spec-file', 'spec.json'])
        assert result.exit_code == 0
        assert "Starting project generation" in result.output

def test_owera_command_with_invalid_spec(runner):
    """Test the owera command with an invalid specification."""
    result = runner.invoke(owera, ['--spec', 'invalid json'])
    assert result.exit_code != 0
    assert "Error" in result.output

def test_owera_command_with_debug(runner, mock_project):
    """Test the owera command with debug mode."""
    with patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'):
        
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}', '--debug'])
        assert result.exit_code == 0
        assert "Debug mode enabled" in result.output

@patch('owera.agents.UISpecialist')
@patch('owera.agents.Developer')
@patch('owera.agents.QASpecialist')
@patch('owera.agents.ProductOwner')
@patch('owera.agents.ProjectManager')
def test_agent_initialization(mock_pm, mock_po, mock_qa, mock_dev, mock_ui, runner, mock_project):
    """Test agent initialization."""
    with patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'):
        
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}'])
        assert result.exit_code == 0
        
        # Verify all agents were initialized
        mock_ui.assert_called_once()
        mock_dev.assert_called_once()
        mock_qa.assert_called_once()
        mock_po.assert_called_once()
        mock_pm.assert_called_once()

def test_output_generation(runner, mock_project):
    """Test output generation."""
    with patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen:
        
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}', '--output', 'test_output'])
        assert result.exit_code == 0
        mock_gen.assert_called_once()

def test_error_handling(runner):
    """Test error handling in the main application."""
    with patch('owera.utils.spec_parser.parse_spec_string', side_effect=Exception("Test error")):
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}'])
        assert result.exit_code != 0
        assert "Error" in result.output

def test_logging_setup(runner, mock_project):
    """Test logging setup."""
    with patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'), \
         patch('logging.basicConfig') as mock_logging:
        
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}'])
        assert result.exit_code == 0
        mock_logging.assert_called_once()

def test_progress_tracking(runner, mock_project):
    """Test progress tracking in the main application."""
    with patch('owera.utils.spec_parser.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'), \
         patch('tqdm.tqdm') as mock_tqdm:
        
        result = runner.invoke(owera, ['--spec', '{"project": {"name": "TestApp"}}'])
        assert result.exit_code == 0
        mock_tqdm.assert_called() 