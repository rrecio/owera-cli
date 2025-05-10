import pytest
from pathlib import Path
import tempfile
from owera.generator.code_generator import CodeGenerator
from owera.models.project import Project

def test_code_generator_initialization(mock_project):
    """Test code generator initialization."""
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    assert generator.project == project

def test_template_loading(mock_project):
    """Test loading of code templates."""
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    
    # Test loading Flask template
    template = generator._load_template("flask", "app.py")
    assert template is not None
    assert "from flask import Flask" in template
    
    # Test loading React template
    template = generator._load_template("react", "App.js")
    assert template is not None
    assert "import React" in template

def test_code_generation(mock_project, temp_project_dir):
    """Test code generation for a project."""
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    
    # Generate code
    generator.generate(temp_project_dir)
    
    # Verify generated files
    project_path = Path(temp_project_dir)
    assert (project_path / "app.py").exists()
    assert (project_path / "models.py").exists()
    assert (project_path / "routes.py").exists()
    assert (project_path / "templates" / "home.html").exists()
    assert (project_path / "static" / "css" / "style.css").exists()
    assert (project_path / "static" / "js" / "main.js").exists()

def test_custom_tech_stack_generation(mock_project, temp_project_dir):
    """Test code generation with custom tech stack."""
    # Modify project to use Django and React
    mock_project["tech_stack"] = {
        "backend": "Python/Django",
        "frontend": "React"
    }
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    
    # Generate code
    generator.generate(temp_project_dir)
    
    # Verify generated files
    project_path = Path(temp_project_dir)
    assert (project_path / "manage.py").exists()
    assert (project_path / "frontend" / "package.json").exists()
    assert (project_path / "frontend" / "src" / "App.js").exists()

def test_feature_specific_generation(mock_project, temp_project_dir):
    """Test code generation for specific features."""
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    
    # Add a new feature
    from owera.models.feature import Feature
    new_feature = Feature(
        name="product_list",
        description="Product listing page",
        status="todo"
    )
    project.add_feature(new_feature)
    
    # Generate code
    generator.generate(temp_project_dir)
    
    # Verify feature-specific files
    project_path = Path(temp_project_dir)
    assert (project_path / "templates" / "productlist.html").exists()
    assert (project_path / "static" / "js" / "productlist.js").exists()

def test_error_handling(mock_project, temp_project_dir):
    """Test error handling during code generation."""
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    
    # Test with invalid template
    with pytest.raises(ValueError):
        generator._load_template("invalid", "template.py")
    
    # Test with invalid output directory
    with pytest.raises(OSError):
        generator.generate("/invalid/path")

def test_template_rendering(mock_project):
    """Test template rendering with different variables."""
    project = Project(**mock_project)
    generator = CodeGenerator(project)
    
    # Test rendering with project variables
    template = generator._load_template("flask", "app.py")
    rendered = generator._render_template(template, project=project)
    
    assert project.name in rendered
    assert "Flask" in rendered
    assert "app = Flask(__name__)" in rendered 