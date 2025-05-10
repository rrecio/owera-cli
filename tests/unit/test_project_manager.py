import pytest
from pathlib import Path
import yaml
from owera.models.project import Project
from owera.models.task import Task
from owera.models.feature import Feature

def test_project_initialization(mock_project):
    """Test project initialization with mock data."""
    project = Project(**mock_project)
    assert project.name == "TestApp"
    assert project.tech_stack["backend"] == "Python/Flask"
    assert project.tech_stack["frontend"] == "HTML/CSS"
    assert len(project.features) == 1
    assert len(project.tasks) == 1

def test_project_feature_management(mock_project):
    """Test adding and removing features."""
    project = Project(**mock_project)
    
    # Add new feature
    new_feature = Feature(
        name="product_list",
        description="Product listing page",
        status="todo"
    )
    project.add_feature(new_feature)
    assert len(project.features) == 2
    assert any(f.name == "product_list" for f in project.features)
    
    # Remove feature
    project.remove_feature("home_page")
    assert len(project.features) == 1
    assert not any(f.name == "home_page" for f in project.features)

def test_project_task_management(mock_project):
    """Test adding and removing tasks."""
    project = Project(**mock_project)
    
    # Add new task
    new_task = Task(
        name="Implement product list",
        description="Create the product listing page",
        status="todo",
        assigned_to="Developer"
    )
    project.add_task(new_task)
    assert len(project.tasks) == 2
    assert any(t.name == "Implement product list" for t in project.tasks)
    
    # Remove task
    project.remove_task("Implement home page")
    assert len(project.tasks) == 1
    assert not any(t.name == "Implement home page" for t in project.tasks)

def test_project_serialization(mock_project):
    """Test project serialization to and from YAML."""
    project = Project(**mock_project)
    
    # Serialize to YAML
    yaml_data = project.to_yaml()
    assert isinstance(yaml_data, str)
    
    # Deserialize from YAML
    loaded_data = yaml.safe_load(yaml_data)
    loaded_project = Project(**loaded_data)
    
    assert loaded_project.name == project.name
    assert loaded_project.tech_stack == project.tech_stack
    assert len(loaded_project.features) == len(project.features)
    assert len(loaded_project.tasks) == len(project.tasks)

def test_project_validation(mock_project):
    """Test project validation."""
    # Test with valid data
    project = Project(**mock_project)
    assert project.validate()
    
    # Test with invalid data
    invalid_project = mock_project.copy()
    invalid_project["name"] = ""  # Empty name is invalid
    project = Project(**invalid_project)
    assert not project.validate()

def test_project_status_tracking(mock_project):
    """Test project status tracking."""
    project = Project(**mock_project)
    
    # Initial status
    assert project.get_status() == "todo"
    
    # Update feature status
    project.features[0].status = "in_progress"
    assert project.get_status() == "in_progress"
    
    # Update task status
    project.tasks[0].status = "done"
    project.features[0].status = "done"
    assert project.get_status() == "done" 