"""Project generation module for Owera CLI."""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape

from owera.models.base import Project, Feature
from owera.utils.template_loader import load_templates
from owera.utils.code_formatter import format_code

class ProjectGenerator:
    """Handles project generation and code creation."""
    
    def __init__(self):
        """Initialize the project generator."""
        self.templates = load_templates()
        self.env = Environment(
            loader=FileSystemLoader(self.templates),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def generate_project(self, project: Project, output_dir: Path) -> None:
        """Generate a complete project.
        
        Args:
            project: The project specification.
            output_dir: Directory to generate the project in.
            
        Raises:
            ValueError: If the project is invalid or output directory exists.
        """
        if not project.features:
            raise ValueError("Project must have at least one feature")
        
        if output_dir.exists():
            raise ValueError(f"Output directory {output_dir} already exists")
        
        # Create project structure
        self.generate_structure(project, output_dir)
        
        # Implement features
        for feature in project.features:
            self.implement_feature(feature, output_dir)
        
        # Generate tests
        self.generate_tests(project, output_dir)
        
        # Generate documentation
        self.generate_documentation(project, output_dir)
    
    def generate_structure(self, project: Project, output_dir: Path) -> None:
        """Generate the basic project structure.
        
        Args:
            project: The project specification.
            output_dir: Directory to generate the project in.
        """
        # Create main directories
        directories = [
            output_dir,
            output_dir / "templates",
            output_dir / "static" / "css",
            output_dir / "static" / "js",
            output_dir / "tests",
            output_dir / "docs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Generate main application files
        self._generate_app_file(project, output_dir)
        self._generate_models_file(project, output_dir)
        self._generate_routes_file(project, output_dir)
        self._generate_requirements_file(project, output_dir)
        self._generate_readme_file(project, output_dir)
    
    def implement_feature(self, feature: Feature, output_dir: Path) -> None:
        """Implement a specific feature.
        
        Args:
            feature: The feature to implement.
            output_dir: Directory containing the project.
        """
        # Generate template
        template_path = output_dir / "templates" / f"{feature.name.lower()}.html"
        template = self.env.get_template("feature_template.html")
        template_content = template.render(feature=feature)
        template_path.write_text(format_code(template_content, "html"))
        
        # Generate CSS
        css_path = output_dir / "static" / "css" / f"{feature.name.lower()}.css"
        css_template = self.env.get_template("feature_style.css")
        css_content = css_template.render(feature=feature)
        css_path.write_text(format_code(css_content, "css"))
        
        # Generate JavaScript
        js_path = output_dir / "static" / "js" / f"{feature.name.lower()}.js"
        js_template = self.env.get_template("feature_script.js")
        js_content = js_template.render(feature=feature)
        js_path.write_text(format_code(js_content, "javascript"))
        
        # Update routes
        self._update_routes_file(feature, output_dir)
    
    def generate_tests(self, project: Project, output_dir: Path) -> None:
        """Generate test files for the project.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        # Generate test configuration
        conftest_path = output_dir / "tests" / "conftest.py"
        conftest_template = self.env.get_template("conftest.py")
        conftest_content = conftest_template.render(project=project)
        conftest_path.write_text(format_code(conftest_content, "python"))
        
        # Generate feature tests
        for feature in project.features:
            test_path = output_dir / "tests" / f"test_{feature.name.lower()}.py"
            test_template = self.env.get_template("feature_test.py")
            test_content = test_template.render(feature=feature)
            test_path.write_text(format_code(test_content, "python"))
    
    def generate_documentation(self, project: Project, output_dir: Path) -> None:
        """Generate documentation for the project.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        # Generate API documentation
        api_path = output_dir / "docs" / "api.md"
        api_template = self.env.get_template("api_docs.md")
        api_content = api_template.render(project=project)
        api_path.write_text(api_content)
        
        # Generate user guide
        guide_path = output_dir / "docs" / "user_guide.md"
        guide_template = self.env.get_template("user_guide.md")
        guide_content = guide_template.render(project=project)
        guide_path.write_text(guide_content)
    
    def _generate_app_file(self, project: Project, output_dir: Path) -> None:
        """Generate the main application file.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        app_path = output_dir / "app.py"
        app_template = self.env.get_template("app.py")
        app_content = app_template.render(project=project)
        app_path.write_text(format_code(app_content, "python"))
    
    def _generate_models_file(self, project: Project, output_dir: Path) -> None:
        """Generate the models file.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        models_path = output_dir / "models.py"
        models_template = self.env.get_template("models.py")
        models_content = models_template.render(project=project)
        models_path.write_text(format_code(models_content, "python"))
    
    def _generate_routes_file(self, project: Project, output_dir: Path) -> None:
        """Generate the routes file.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        routes_path = output_dir / "routes.py"
        routes_template = self.env.get_template("routes.py")
        routes_content = routes_template.render(project=project)
        routes_path.write_text(format_code(routes_content, "python"))
    
    def _generate_requirements_file(self, project: Project, output_dir: Path) -> None:
        """Generate the requirements file.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        requirements_path = output_dir / "requirements.txt"
        requirements_template = self.env.get_template("requirements.txt")
        requirements_content = requirements_template.render(project=project)
        requirements_path.write_text(requirements_content)
    
    def _generate_readme_file(self, project: Project, output_dir: Path) -> None:
        """Generate the README file.
        
        Args:
            project: The project specification.
            output_dir: Directory containing the project.
        """
        readme_path = output_dir / "README.md"
        readme_template = self.env.get_template("README.md")
        readme_content = readme_template.render(project=project)
        readme_path.write_text(readme_content)
    
    def _update_routes_file(self, feature: Feature, output_dir: Path) -> None:
        """Update the routes file with new feature routes.
        
        Args:
            feature: The feature to add routes for.
            output_dir: Directory containing the project.
        """
        routes_path = output_dir / "routes.py"
        routes_template = self.env.get_template("feature_routes.py")
        routes_content = routes_template.render(feature=feature)
        
        # Append new routes to existing file
        with open(routes_path, "a") as f:
            f.write("\n" + routes_content) 