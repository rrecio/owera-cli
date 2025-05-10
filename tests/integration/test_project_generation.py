import pytest
import os
import shutil
from pathlib import Path
import yaml
from owera.main import owera
from click.testing import CliRunner
from ..utils.test_helpers import cleanup_temp_files
from owera.generator import ProjectGenerator
from owera.models.base import Project, Feature

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary directory for project generation."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    yield project_dir
    shutil.rmtree(project_dir)

@pytest.fixture
def sample_project():
    """Create a sample project specification."""
    return Project(
        name="Test E-commerce",
        type="Web Application",
        target_users="Online shoppers",
        target_market="Retail consumers",
        business_goals=["Increase sales", "Improve user experience"],
        requirements=["Security", "Usability", "Accessibility"],
        budget=100000,
        timeline="6 months",
        features=[
            Feature(
                name="Product Search",
                description="Implement advanced product search with filters"
            ),
            Feature(
                name="Shopping Cart",
                description="Implement shopping cart functionality"
            )
        ]
    )

@pytest.fixture
def generator():
    """Create a project generator instance."""
    return ProjectGenerator()

def test_project_generation_with_dependencies(runner, temp_project_spec, temp_project_dir):
    """Test project generation with dependency checking."""
    result = runner.invoke(owera, [
        'generate',
        '--spec-file', temp_project_spec,
        '--output', temp_project_dir,
        '--check-deps'
    ])
    
    assert result.exit_code == 0
    assert "Project generated successfully" in result.output
    
    # Verify project structure
    project_path = Path(temp_project_dir)
    assert (project_path / "app.py").exists()
    assert (project_path / "models.py").exists()
    assert (project_path / "routes.py").exists()
    assert (project_path / "templates").exists()
    assert (project_path / "static").exists()
    assert (project_path / "tests").exists()

def test_project_generation_without_dependencies(runner, temp_project_spec, temp_project_dir):
    """Test project generation without dependency checking."""
    result = runner.invoke(owera, [
        'generate',
        '--spec-file', temp_project_spec,
        '--output', temp_project_dir,
        '--no-check-deps'
    ])
    
    assert result.exit_code == 0
    assert "Project generated successfully" in result.output

def test_project_generation_with_custom_tech_stack(runner, temp_project_dir):
    """Test project generation with custom tech stack."""
    custom_spec = {
        "project": {
            "name": "CustomApp",
            "tech_stack": {
                "backend": "Python/Django",
                "frontend": "React"
            }
        },
        "features": [
            {
                "name": "home_page",
                "description": "Home page with welcome message"
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(custom_spec, f)
        spec_path = f.name
    
    try:
        result = runner.invoke(owera, [
            'generate',
            '--spec-file', spec_path,
            '--output', temp_project_dir,
            '--no-check-deps'
        ])
        
        assert result.exit_code == 0
        assert "Project generated successfully" in result.output
        
        # Verify custom tech stack implementation
        project_path = Path(temp_project_dir)
        assert (project_path / "manage.py").exists()  # Django specific
        assert (project_path / "frontend" / "package.json").exists()  # React specific
        
    finally:
        cleanup_temp_files(spec_path)

def test_project_generation_with_invalid_spec(runner, temp_project_dir):
    """Test project generation with invalid specification."""
    invalid_spec = {
        "project": {
            "name": "InvalidApp"
            # Missing required fields
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(invalid_spec, f)
        spec_path = f.name
    
    try:
        result = runner.invoke(owera, [
            'generate',
            '--spec-file', spec_path,
            '--output', temp_project_dir
        ])
        
        assert result.exit_code != 0
        assert "Error" in result.output
        
    finally:
        cleanup_temp_files(spec_path)

def test_project_structure_generation(generator, temp_project_dir, sample_project):
    """Test the generation of project structure."""
    # Generate project structure
    generator.generate_structure(sample_project, temp_project_dir)
    
    # Verify directory structure
    assert (temp_project_dir / "app.py").exists()
    assert (temp_project_dir / "models.py").exists()
    assert (temp_project_dir / "routes.py").exists()
    assert (temp_project_dir / "templates").exists()
    assert (temp_project_dir / "static").exists()
    assert (temp_project_dir / "tests").exists()
    assert (temp_project_dir / "requirements.txt").exists()
    assert (temp_project_dir / "README.md").exists()

def test_feature_implementation(generator, temp_project_dir, sample_project):
    """Test the implementation of project features."""
    # Generate project structure
    generator.generate_structure(sample_project, temp_project_dir)
    
    # Implement features
    for feature in sample_project.features:
        generator.implement_feature(feature, temp_project_dir)
    
    # Verify feature implementation
    assert (temp_project_dir / "templates" / "product_search.html").exists()
    assert (temp_project_dir / "templates" / "shopping_cart.html").exists()
    assert (temp_project_dir / "static" / "css" / "product_search.css").exists()
    assert (temp_project_dir / "static" / "css" / "shopping_cart.css").exists()
    assert (temp_project_dir / "static" / "js" / "product_search.js").exists()
    assert (temp_project_dir / "static" / "js" / "shopping_cart.js").exists()

def test_dependency_management(generator, temp_project_dir, sample_project):
    """Test the generation of dependency management files."""
    # Generate project structure
    generator.generate_structure(sample_project, temp_project_dir)
    
    # Verify requirements.txt
    requirements_file = temp_project_dir / "requirements.txt"
    assert requirements_file.exists()
    
    with open(requirements_file) as f:
        requirements = f.read()
        assert "flask" in requirements.lower()
        assert "pytest" in requirements.lower()
        assert "sqlalchemy" in requirements.lower()

def test_test_generation(generator, temp_project_dir, sample_project):
    """Test the generation of test files."""
    # Generate project structure
    generator.generate_structure(sample_project, temp_project_dir)
    
    # Verify test files
    assert (temp_project_dir / "tests" / "test_product_search.py").exists()
    assert (temp_project_dir / "tests" / "test_shopping_cart.py").exists()
    assert (temp_project_dir / "tests" / "conftest.py").exists()

def test_documentation_generation(generator, temp_project_dir, sample_project):
    """Test the generation of documentation files."""
    # Generate project structure
    generator.generate_structure(sample_project, temp_project_dir)
    
    # Verify documentation files
    assert (temp_project_dir / "README.md").exists()
    assert (temp_project_dir / "docs" / "api.md").exists()
    assert (temp_project_dir / "docs" / "user_guide.md").exists()

def test_error_handling(generator, temp_project_dir, sample_project):
    """Test error handling during project generation."""
    # Create invalid project
    invalid_project = Project(
        name="Invalid Project",
        type="Invalid Type",
        features=[]
    )
    
    # Attempt to generate project
    with pytest.raises(ValueError):
        generator.generate_structure(invalid_project, temp_project_dir)

def test_end_to_end_generation(generator, temp_project_dir, sample_project):
    """Test the complete end-to-end project generation process."""
    # Generate complete project
    generator.generate_project(sample_project, temp_project_dir)
    
    # Verify project structure
    test_project_structure_generation(generator, temp_project_dir, sample_project)
    
    # Verify feature implementation
    test_feature_implementation(generator, temp_project_dir, sample_project)
    
    # Verify dependency management
    test_dependency_management(generator, temp_project_dir, sample_project)
    
    # Verify test generation
    test_test_generation(generator, temp_project_dir, sample_project)
    
    # Verify documentation generation
    test_documentation_generation(generator, temp_project_dir, sample_project)
    
    # Verify project can be run
    assert (temp_project_dir / "app.py").exists()
    with open(temp_project_dir / "app.py") as f:
        app_code = f.read()
        assert "if __name__ == '__main__':" in app_code
        assert "app.run" in app_code 