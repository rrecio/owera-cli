"""Tests for the ProjectGenerator."""

import os
import pytest
from owera.generator import ProjectGenerator
from owera.models import Project, Feature, Task

@pytest.fixture
def project_generator(tmp_path):
    """Create a ProjectGenerator instance for testing."""
    return ProjectGenerator(str(tmp_path))

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

def test_project_generator_creation(project_generator):
    """Test creating a new ProjectGenerator."""
    assert os.path.exists(project_generator.output_dir)
    assert project_generator.template_dir is not None

def test_project_generator_generate_project(project_generator, sample_project):
    """Test generating a project."""
    # Generate project
    project_generator.generate_project(sample_project)
    
    # Check project structure
    project_dir = os.path.join(project_generator.output_dir, sample_project.name)
    assert os.path.exists(project_dir)
    assert os.path.exists(os.path.join(project_dir, "app.py"))
    assert os.path.exists(os.path.join(project_dir, "models.py"))
    assert os.path.exists(os.path.join(project_dir, "routes.py"))
    assert os.path.exists(os.path.join(project_dir, "templates"))
    assert os.path.exists(os.path.join(project_dir, "static"))
    assert os.path.exists(os.path.join(project_dir, "tests"))

def test_project_generator_generate_feature(project_generator, sample_project):
    """Test generating a feature."""
    # Generate feature
    feature = sample_project.features[0]
    project_generator.generate_feature(sample_project, feature)
    
    # Check feature structure
    project_dir = os.path.join(project_generator.output_dir, sample_project.name)
    feature_dir = os.path.join(project_dir, "features", feature.name)
    assert os.path.exists(feature_dir)
    assert os.path.exists(os.path.join(feature_dir, "routes.py"))
    assert os.path.exists(os.path.join(feature_dir, "models.py"))
    assert os.path.exists(os.path.join(feature_dir, "templates"))
    assert os.path.exists(os.path.join(feature_dir, "static"))

def test_project_generator_generate_task(project_generator, sample_project):
    """Test generating a task."""
    # Generate task
    task = sample_project.tasks[0]
    project_generator.generate_task(sample_project, task)
    
    # Check task structure
    project_dir = os.path.join(project_generator.output_dir, sample_project.name)
    task_dir = os.path.join(project_dir, "tasks", task.name)
    assert os.path.exists(task_dir)
    assert os.path.exists(os.path.join(task_dir, "routes.py"))
    assert os.path.exists(os.path.join(task_dir, "models.py"))
    assert os.path.exists(os.path.join(task_dir, "templates"))
    assert os.path.exists(os.path.join(task_dir, "static"))

def test_project_generator_generate_all(project_generator, sample_project):
    """Test generating all project components."""
    # Generate all
    project_generator.generate_all(sample_project)
    
    # Check project structure
    project_dir = os.path.join(project_generator.output_dir, sample_project.name)
    assert os.path.exists(project_dir)
    assert os.path.exists(os.path.join(project_dir, "app.py"))
    assert os.path.exists(os.path.join(project_dir, "models.py"))
    assert os.path.exists(os.path.join(project_dir, "routes.py"))
    assert os.path.exists(os.path.join(project_dir, "templates"))
    assert os.path.exists(os.path.join(project_dir, "static"))
    assert os.path.exists(os.path.join(project_dir, "tests"))
    
    # Check feature structure
    feature = sample_project.features[0]
    feature_dir = os.path.join(project_dir, "features", feature.name)
    assert os.path.exists(feature_dir)
    assert os.path.exists(os.path.join(feature_dir, "routes.py"))
    assert os.path.exists(os.path.join(feature_dir, "models.py"))
    assert os.path.exists(os.path.join(feature_dir, "templates"))
    assert os.path.exists(os.path.join(feature_dir, "static"))
    
    # Check task structure
    task = sample_project.tasks[0]
    task_dir = os.path.join(project_dir, "tasks", task.name)
    assert os.path.exists(task_dir)
    assert os.path.exists(os.path.join(task_dir, "routes.py"))
    assert os.path.exists(os.path.join(task_dir, "models.py"))
    assert os.path.exists(os.path.join(task_dir, "templates"))
    assert os.path.exists(os.path.join(task_dir, "static")) 