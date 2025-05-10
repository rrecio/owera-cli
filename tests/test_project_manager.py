"""Tests for the ProjectManager."""

import os
import pytest
from owera.models import Project, Feature, Task, ProjectManager

@pytest.fixture
def project_manager(tmp_path):
    """Create a ProjectManager instance for testing."""
    return ProjectManager(str(tmp_path))

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

def test_project_manager_creation(project_manager):
    """Test creating a new ProjectManager."""
    assert os.path.exists(project_manager.projects_dir)
    assert project_manager.projects == {}

def test_project_manager_add_project(project_manager, sample_project):
    """Test adding a project."""
    project_manager.add_project(sample_project)
    
    assert sample_project.name in project_manager.projects
    assert project_manager.projects[sample_project.name] == sample_project
    
    # Test adding duplicate project
    with pytest.raises(ValueError, match="Project test-project already exists"):
        project_manager.add_project(sample_project)

def test_project_manager_get_project(project_manager, sample_project):
    """Test getting a project."""
    project_manager.add_project(sample_project)
    
    # Get existing project
    assert project_manager.get_project("test-project") == sample_project
    
    # Get non-existent project
    with pytest.raises(ValueError, match="Project non-existent not found"):
        project_manager.get_project("non-existent")

def test_project_manager_remove_project(project_manager, sample_project):
    """Test removing a project."""
    project_manager.add_project(sample_project)
    
    # Remove existing project
    project_manager.remove_project("test-project")
    assert "test-project" not in project_manager.projects
    
    # Remove non-existent project
    with pytest.raises(ValueError, match="Project non-existent not found"):
        project_manager.remove_project("non-existent")

def test_project_manager_list_projects(project_manager, sample_project):
    """Test listing projects."""
    project_manager.add_project(sample_project)
    
    projects = project_manager.list_projects()
    assert len(projects) == 1
    assert projects[0] == sample_project

def test_project_manager_save_load_project(project_manager, sample_project):
    """Test saving and loading a project."""
    # Save project
    project_manager.add_project(sample_project)
    project_manager.save_project("test-project")
    
    # Clear projects
    project_manager.projects = {}
    
    # Load project
    project_manager.load_project("test-project")
    
    loaded_project = project_manager.get_project("test-project")
    assert loaded_project.name == sample_project.name
    assert loaded_project.tech_stack == sample_project.tech_stack
    assert len(loaded_project.features) == len(sample_project.features)
    assert len(loaded_project.tasks) == len(sample_project.tasks)
    assert loaded_project.status == sample_project.status

def test_project_manager_load_all_projects(project_manager, sample_project):
    """Test loading all projects."""
    # Save project
    project_manager.add_project(sample_project)
    project_manager.save_project("test-project")
    
    # Clear projects
    project_manager.projects = {}
    
    # Load all projects
    project_manager.load_all_projects()
    
    assert "test-project" in project_manager.projects
    loaded_project = project_manager.get_project("test-project")
    assert loaded_project.name == sample_project.name
    assert loaded_project.tech_stack == sample_project.tech_stack
    assert len(loaded_project.features) == len(sample_project.features)
    assert len(loaded_project.tasks) == len(sample_project.tasks)
    assert loaded_project.status == sample_project.status 