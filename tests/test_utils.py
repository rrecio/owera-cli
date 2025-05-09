import pytest
import json
import os
from unittest.mock import patch, mock_open
from owera.utils.spec_parser import parse_spec_string, ParsingError
from owera.utils.code_generator import generate_output, CodeGenerationError
from owera.models.base import Project

def test_spec_parser_json():
    """Test JSON specification parsing."""
    spec = {
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
    
    result = parse_spec_string(json.dumps(spec))
    assert result["project"]["name"] == "TestApp"
    assert len(result["features"]) == 1
    assert result["features"][0]["name"] == "home_page"

def test_spec_parser_string():
    """Test string specification parsing."""
    spec = "Build a blog with a home page and about page"
    result = parse_spec_string(spec)
    
    assert "project" in result
    assert "features" in result
    assert len(result["features"]) >= 2
    assert any(f["name"] == "home_page" for f in result["features"])
    assert any(f["name"] == "about_page" for f in result["features"])

def test_spec_parser_invalid_json():
    """Test invalid JSON handling."""
    with pytest.raises(ParsingError):
        parse_spec_string("{invalid json}")

def test_spec_parser_default():
    """Test default specification generation."""
    result = parse_spec_string("")
    assert result["project"]["name"] == "SimpleApp"
    assert len(result["features"]) == 1
    assert result["features"][0]["name"] == "home_page"

@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
def test_code_generator(mock_file, mock_makedirs):
    """Test code generation."""
    project = Project({
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
                "description": "Home page",
                "constraints": []
            }
        ]
    })
    
    project.code = {
        "backend": ["@app.route('/home')\ndef home():\n    return render_template('home.html')"]
    }
    project.designs = {
        "home_page": "<div>Home Page</div>"
    }
    
    generate_output(project, "test_output")
    
    # Verify directory creation
    mock_makedirs.assert_any_call("test_output")
    mock_makedirs.assert_any_call("test_output/src")
    mock_makedirs.assert_any_call("test_output/templates")
    mock_makedirs.assert_any_call("test_output/docs")
    mock_makedirs.assert_any_call("test_output/logs")
    
    # Verify file writing
    assert mock_file.call_count > 0

def test_code_generator_error():
    """Test code generation error handling."""
    project = Project({
        "project": {"name": "TestApp"},
        "features": []
    })
    
    with pytest.raises(CodeGenerationError):
        generate_output(project, "/invalid/path")

@patch('git.Repo')
def test_git_setup(mock_repo):
    """Test Git repository setup."""
    project = Project({
        "project": {"name": "TestApp"},
        "features": []
    })
    
    generate_output(project, "test_output")
    mock_repo.init.assert_called_once_with("test_output")

def test_template_generation():
    """Test HTML template generation."""
    project = Project({
        "project": {"name": "TestApp"},
        "features": []
    })
    
    project.designs = {
        "test_page": "<div>Test Page</div>"
    }
    
    with patch('builtins.open', new_callable=mock_open) as mock_file:
        generate_output(project, "test_output")
        mock_file.assert_any_call("test_output/templates/test_page.html", "w")

def test_documentation_generation():
    """Test documentation generation."""
    project = Project({
        "project": {"name": "TestApp"},
        "features": [
            {
                "name": "feature1",
                "description": "Test feature 1"
            }
        ]
    })
    
    with patch('builtins.open', new_callable=mock_open) as mock_file:
        generate_output(project, "test_output")
        mock_file.assert_any_call("test_output/docs/README.md", "w")
        
        # Verify README content
        write_calls = [call[0][0] for call in mock_file.mock_calls if call[0][0] == "test_output/docs/README.md"]
        assert any("TestApp" in call for call in write_calls)
        assert any("feature1" in call for call in write_calls) 