"""Tests for the Project model."""

import pytest
from owera.models import Project, Feature, Task

def test_project_creation():
    """Test creating a new project."""
    project = Project(
        name="test-project",
        tech_stack={
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        }
    )
    
    assert project.name == "test-project"
    assert project.tech_stack["backend"] == "Python/Flask"
    assert project.tech_stack["frontend"] == "HTML/CSS"
    assert project.features == []
    assert project.tasks == []
    assert project.status == "initialized"

def test_project_validation():
    """Test project validation."""
    # Test missing name
    with pytest.raises(ValueError, match="Project must have a name"):
        Project(name="", tech_stack={"backend": "Python/Flask", "frontend": "HTML/CSS"})
    
    # Test missing tech stack
    with pytest.raises(ValueError, match="Project must have a tech stack"):
        Project(name="test-project", tech_stack={})
    
    # Test missing backend
    with pytest.raises(ValueError, match="Tech stack must include backend"):
        Project(name="test-project", tech_stack={"frontend": "HTML/CSS"})
    
    # Test missing frontend
    with pytest.raises(ValueError, match="Tech stack must include frontend"):
        Project(name="test-project", tech_stack={"backend": "Python/Flask"})

def test_project_features():
    """Test managing project features."""
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
    
    assert len(project.features) == 1
    assert project.features[0].name == "test-feature"
    
    # Get feature
    assert project.get_feature("test-feature") == feature
    
    # Remove feature
    project.remove_feature("test-feature")
    assert len(project.features) == 0
    
    # Get non-existent feature
    with pytest.raises(ValueError, match="Feature test-feature not found"):
        project.get_feature("test-feature")

def test_project_tasks():
    """Test managing project tasks."""
    project = Project(
        name="test-project",
        tech_stack={
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        }
    )
    
    # Add task
    task = Task(
        name="test-task",
        description="A test task",
        status="todo",
        assigned_to="developer"
    )
    project.add_task(task)
    
    assert len(project.tasks) == 1
    assert project.tasks[0].name == "test-task"
    
    # Get task
    assert project.get_task("test-task") == task
    
    # Remove task
    project.remove_task("test-task")
    assert len(project.tasks) == 0
    
    # Get non-existent task
    with pytest.raises(ValueError, match="Task test-task not found"):
        project.get_task("test-task")

def test_project_serialization(tmp_path):
    """Test project serialization."""
    project = Project(
        name="test-project",
        tech_stack={
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        }
    )
    
    # Add feature and task
    feature = Feature(
        name="test-feature",
        description="A test feature",
        constraints=["secure", "responsive"]
    )
    project.add_feature(feature)
    
    task = Task(
        name="test-task",
        description="A test task",
        status="todo",
        assigned_to="developer"
    )
    project.add_task(task)
    
    # Save project
    project_file = tmp_path / "project.json"
    project.save(str(project_file))
    
    # Load project
    loaded_project = Project.load(str(project_file))
    
    assert loaded_project.name == project.name
    assert loaded_project.tech_stack == project.tech_stack
    assert len(loaded_project.features) == len(project.features)
    assert len(loaded_project.tasks) == len(project.tasks)
    assert loaded_project.status == project.status 