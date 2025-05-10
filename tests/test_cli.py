import pytest
from unittest.mock import patch, mock_open, MagicMock
from click.testing import CliRunner
from click import UsageError
from owera.main import owera
from owera.models.base import Project, Feature, Task
from owera.agents import UISpecialist, Developer, QASpecialist, ProductOwner, ProjectManager
from owera.config import Config
import subprocess
import os
from owera.cli import app

@pytest.fixture
def mock_config():
    """Create a mock config."""
    config = MagicMock(spec=Config)
    config.MAX_ITERATIONS = 10
    return config

@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()

class MockProject:
    """Mock project class for testing."""
    def __init__(self, name=None, tech_stack=None, features=None, tasks=None, code=None):
        self.name = name
        self.tech_stack = tech_stack
        self.features = features
        self.tasks = tasks
        self.code = code

    def validate(self):
        """Validate the project structure."""
        if not hasattr(self, 'name') or not self.name:
            raise ValueError("Project must have a name")
        if not hasattr(self, 'tech_stack') or not self.tech_stack:
            raise ValueError("Project must have a tech stack")
        if not hasattr(self, 'features') or self.features is None:
            raise ValueError("Project must have features")
        if not hasattr(self, 'tasks') or self.tasks is None:
            self.tasks = []

@pytest.fixture
def mock_project():
    """Create a mock project for testing."""
    return MockProject(
        name="TestApp",
        tech_stack={
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        },
        features=[
            MagicMock(
                name="home_page",
                description="Home page with welcome message",
                constraints=["responsive design"]
            )
        ],
        tasks=[],
        code={
            "backend": ["from flask import Flask\napp = Flask(__name__)\n"],
            "frontend": ["<html><body>Welcome</body></html>"]
        }
    )

@pytest.fixture
def mock_invalid_project_no_name():
    """Create a mock project with no name."""
    return MockProject(
        name=None,
        tech_stack={"backend": "Python/Flask"},
        features=[],
        tasks=[]
    )

@pytest.fixture
def mock_invalid_project_no_tech_stack():
    """Create a mock project with no tech stack."""
    return MockProject(
        name="TestApp",
        tech_stack=None,
        features=[],
        tasks=[]
    )

@pytest.fixture
def mock_invalid_project_no_features():
    """Create a mock project with no features."""
    return MockProject(
        name="TestApp",
        tech_stack={"backend": "Python/Flask"},
        features=None,
        tasks=[]
    )

@pytest.fixture
def mock_agents():
    ui_specialist = MagicMock()
    developer = MagicMock()
    qa_specialist = MagicMock()
    product_owner = MagicMock()
    project_manager = MagicMock()
    
    ui_specialist.perform_task.return_value = None
    developer.perform_task.return_value = None
    qa_specialist.perform_task.return_value = None
    product_owner.perform_task.return_value = None
    project_manager.plan.return_value = None
    
    return ui_specialist, developer, qa_specialist, product_owner, project_manager

def test_owera_command_with_spec(runner, mock_project, mock_config, mock_agents):
    """Test the owera command with a specification."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec], catch_exceptions=False)
        assert result.exit_code == 0

def test_owera_command_with_spec_file(runner, mock_project, mock_config, mock_agents):
    """Test the owera command with a specification file."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    mock_spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('builtins.open', mock_open(read_data=mock_spec)), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec-file', 'spec.json'], catch_exceptions=False)
        assert result.exit_code == 0

def test_owera_command_with_debug(runner, mock_project, mock_config, mock_agents):
    """Test the owera command with debug mode."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec, '--debug'], catch_exceptions=False)
        assert result.exit_code == 0

def test_agent_initialization(runner, mock_project, mock_config, mock_agents):
    """Test agent initialization."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec], catch_exceptions=False)
        assert result.exit_code == 0

def test_output_generation(runner, mock_project, mock_config, mock_agents):
    """Test output generation."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec, '--output', 'test_output'], catch_exceptions=False)
        assert result.exit_code == 0

def test_logging_setup(runner, mock_project, mock_config, mock_agents):
    """Test logging setup."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec], catch_exceptions=False)
        assert result.exit_code == 0

def test_progress_tracking(runner, mock_project, mock_config, mock_agents):
    """Test progress tracking in the main application."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('tqdm.tqdm') as mock_tqdm, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec], catch_exceptions=False)
        assert result.exit_code == 0

def test_generated_app_tests(runner, mock_project, mock_config, mock_agents):
    """Test that generated app tests are created and run."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    spec = '{"project": {"name": "TestApp", "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"}}, "features": [{"name": "home_page", "description": "Home page with welcome message", "constraints": ["responsive design"]}]}'
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', spec], catch_exceptions=False)
        assert result.exit_code == 0

def test_missing_features_error(runner, mock_config, mock_invalid_project_no_features):
    """Test error handling when project has no features."""
    with patch('owera.main.parse_spec_string', return_value=mock_invalid_project_no_features), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Project must have features" in result.output

def test_missing_name_error(runner, mock_config, mock_invalid_project_no_name):
    """Test error handling when project has no name."""
    with patch('owera.main.parse_spec_string', return_value=mock_invalid_project_no_name), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Project must have a name" in result.output

def test_missing_tech_stack_error(runner, mock_config, mock_invalid_project_no_tech_stack):
    """Test error handling when project has no tech stack."""
    with patch('owera.main.parse_spec_string', return_value=mock_invalid_project_no_tech_stack), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Project must have a tech stack" in result.output

def test_agent_initialization_error(runner, mock_project, mock_config):
    """Test error handling when agent initialization fails."""
    with patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.main.initialize_agents', side_effect=ValueError("Failed to initialize agents")), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Failed to initialize agents" in result.output

def test_development_loop_error(runner, mock_project, mock_config, mock_agents):
    """Test error handling when development loop fails."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    project_manager.plan.side_effect = Exception("Development loop error")
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Failed during development loop" in result.output

def test_output_generation_error(runner, mock_project, mock_config, mock_agents):
    """Test error handling when output generation fails."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output', side_effect=Exception("Output generation error")), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Tests failed" in result.output

def test_test_execution_error(runner, mock_project, mock_config, mock_agents):
    """Test error handling when test execution fails."""
    ui_specialist, developer, qa_specialist, product_owner, project_manager = mock_agents
    
    with patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.main.parse_spec_string', return_value=mock_project), \
         patch('owera.utils.code_generator.generate_output'), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, "pytest", "Test failures", "Error details")):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Error: Tests failed" in result.output

def test_tasks_initialization(runner, mock_config, mock_agents):
    """Test that tasks are properly initialized when None."""
    project = MockProject(
        name="TestApp",
        tech_stack={"backend": "Python/Flask"},
        features=[MagicMock(name="home_page", description="desc", constraints=[])],
        tasks=None,
        code={"backend": [], "frontend": []}
    )
    
    with patch('owera.main.parse_spec_string', return_value=project), \
         patch('owera.main.initialize_agents', return_value=mock_agents), \
         patch('owera.utils.code_generator.generate_output') as mock_gen, \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = MagicMock(stdout="All tests passed", stderr="")
        
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        if result.exit_code != 0:
            print('CLI Output:', result.output)
        assert result.exit_code == 0
        assert project.tasks == []

def test_parse_spec_string_returns_dict_error(runner, mock_config):
    """Test error if parse_spec_string returns a dict instead of a Project instance."""
    with patch('owera.main.parse_spec_string', return_value={"name": "TestApp"}), \
         patch('owera.main.setup_logging') as mock_setup, \
         patch('owera.main.config', mock_config):
        result = runner.invoke(owera, ['--spec', '{}'], catch_exceptions=False)
        assert result.exit_code == 1
        assert "Project must be a Project instance, not a dict" in result.output

@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    project = Project(
        name="test-project",
        tech_stack={
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        }
    )
    
    # Add feature
    feature = Feature(
        name="test-feature",
        description="A test feature",
        constraints=["secure", "responsive"]
    )
    project.add_feature(feature)
    
    # Add task
    task = Task(
        name="test-task",
        description="A test task",
        status="todo",
        assigned_to="developer"
    )
    project.add_task(task)
    
    return project

def test_create_project(runner, tmp_path):
    """Test creating a new project."""
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--backend", "Python/Flask",
            "--frontend", "HTML/CSS"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    assert result.exit_code == 0
    assert "Project test-project created successfully" in result.stdout
    
    # Check project structure
    project_dir = os.path.join(tmp_path, "test-project")
    assert os.path.exists(project_dir)
    assert os.path.exists(os.path.join(project_dir, "app.py"))
    assert os.path.exists(os.path.join(project_dir, "models.py"))
    assert os.path.exists(os.path.join(project_dir, "routes.py"))
    assert os.path.exists(os.path.join(project_dir, "templates"))
    assert os.path.exists(os.path.join(project_dir, "static"))
    assert os.path.exists(os.path.join(project_dir, "tests"))

def test_add_feature(runner, tmp_path, sample_project):
    """Test adding a feature to a project."""
    # Create project first
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--backend", "Python/Flask",
            "--frontend", "HTML/CSS"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    # Add feature
    result = runner.invoke(
        app,
        [
            "add-feature",
            "test-project",
            "test-feature",
            "--description", "A test feature",
            "--constraints", "secure", "responsive"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    assert result.exit_code == 0
    assert "Feature test-feature added to project test-project" in result.stdout
    
    # Check feature structure
    project_dir = os.path.join(tmp_path, "test-project")
    feature_dir = os.path.join(project_dir, "features", "test-feature")
    assert os.path.exists(feature_dir)
    assert os.path.exists(os.path.join(feature_dir, "routes.py"))
    assert os.path.exists(os.path.join(feature_dir, "models.py"))
    assert os.path.exists(os.path.join(feature_dir, "templates"))
    assert os.path.exists(os.path.join(feature_dir, "static"))

def test_add_task(runner, tmp_path, sample_project):
    """Test adding a task to a project."""
    # Create project first
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--backend", "Python/Flask",
            "--frontend", "HTML/CSS"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    # Add task
    result = runner.invoke(
        app,
        [
            "add-task",
            "test-project",
            "test-task",
            "--description", "A test task",
            "--status", "todo",
            "--assigned-to", "developer"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    assert result.exit_code == 0
    assert "Task test-task added to project test-project" in result.stdout
    
    # Check task structure
    project_dir = os.path.join(tmp_path, "test-project")
    task_dir = os.path.join(project_dir, "tasks", "test-task")
    assert os.path.exists(task_dir)
    assert os.path.exists(os.path.join(task_dir, "routes.py"))
    assert os.path.exists(os.path.join(task_dir, "models.py"))
    assert os.path.exists(os.path.join(task_dir, "templates"))
    assert os.path.exists(os.path.join(task_dir, "static"))

def test_list_projects(runner, tmp_path, sample_project):
    """Test listing projects."""
    # Create project first
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--backend", "Python/Flask",
            "--frontend", "HTML/CSS"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    # List projects
    result = runner.invoke(
        app,
        ["list"],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    assert result.exit_code == 0
    assert "test-project" in result.stdout

def test_show_project(runner, tmp_path, sample_project):
    """Test showing project details."""
    # Create project first
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--backend", "Python/Flask",
            "--frontend", "HTML/CSS"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    # Show project
    result = runner.invoke(
        app,
        ["show", "test-project"],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    assert result.exit_code == 0
    assert "test-project" in result.stdout
    assert "Python/Flask" in result.stdout
    assert "HTML/CSS" in result.stdout

def test_delete_project(runner, tmp_path, sample_project):
    """Test deleting a project."""
    # Create project first
    result = runner.invoke(
        app,
        [
            "create",
            "test-project",
            "--backend", "Python/Flask",
            "--frontend", "HTML/CSS"
        ],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    # Delete project
    result = runner.invoke(
        app,
        ["delete", "test-project"],
        env={"OWERA_PROJECTS_DIR": str(tmp_path)}
    )
    
    assert result.exit_code == 0
    assert "Project test-project deleted successfully" in result.stdout
    
    # Check project is deleted
    project_dir = os.path.join(tmp_path, "test-project")
    assert not os.path.exists(project_dir) 