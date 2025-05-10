"""Code generator for Owera CLI."""

import os
from typing import Dict, Any, Optional
import logging
from pathlib import Path
import shutil

from ..models import Project
from ..agents import UISpecialist, Developer, QASpecialist, ProductOwner

class CodeGenerator:
    """Code generator for creating project files."""
    
    def __init__(self, project: Project):
        """Initialize code generator."""
        self.project = project
        self.ui_specialist = UISpecialist()
        self.developer = Developer()
        self.qa_specialist = QASpecialist()
        self.product_owner = ProductOwner()
    
    def generate(self, output_dir: str) -> None:
        """Generate project files.
        
        Args:
            output_dir: Directory to generate files in
        """
        try:
            # Create project directory
            project_dir = os.path.join(output_dir, self.project.name)
            os.makedirs(project_dir, exist_ok=True)
            
            # Generate project structure
            self._generate_project_structure(project_dir)
            
            # Generate backend code
            self._generate_backend(project_dir)
            
            # Generate frontend code
            self._generate_frontend(project_dir)
            
            # Generate tests
            self._generate_tests(project_dir)
            
            # Generate documentation
            self._generate_documentation(project_dir)
            
            # Save project configuration
            self.project.save(os.path.join(project_dir, "project.json"))
            
            logging.info(f"Project generated successfully in {project_dir}")
        
        except Exception as e:
            logging.error(f"Error generating project: {e}")
            raise
    
    def _generate_project_structure(self, project_dir: str) -> None:
        """Generate project directory structure."""
        # Create subdirectories
        directories = [
            "src",
            "tests",
            "docs",
            "static",
            "templates",
            "config"
        ]
        
        for directory in directories:
            os.makedirs(os.path.join(project_dir, directory), exist_ok=True)
            
        # Create static subdirectories
        static_subdirs = ["css", "js", "images"]
        for subdir in static_subdirs:
            os.makedirs(os.path.join(project_dir, "static", subdir), exist_ok=True)
    
    def _generate_backend(self, project_dir: str) -> None:
        """Generate backend code."""
        backend = self.project.tech_stack["backend"]
        
        if backend == "Python/Flask":
            self._generate_flask_backend(project_dir)
        else:
            raise ValueError(f"Unsupported backend: {backend}")
    
    def _generate_frontend(self, project_dir: str) -> None:
        """Generate frontend code."""
        frontend = self.project.tech_stack["frontend"]
        
        if frontend == "HTML/CSS":
            self._generate_html_frontend(project_dir)
        else:
            raise ValueError(f"Unsupported frontend: {frontend}")
    
    def _generate_tests(self, project_dir: str) -> None:
        """Generate test files."""
        # Generate test files for each feature
        for feature in self.project.features:
            self.qa_specialist.generate_tests(feature, project_dir)
    
    def _generate_documentation(self, project_dir: str) -> None:
        """Generate documentation."""
        # Generate documentation for each feature
        for feature in self.project.features:
            self.product_owner.generate_documentation(feature, project_dir)
    
    def _generate_flask_backend(self, project_dir: str) -> None:
        """Generate Flask backend code."""
        # Generate app.py
        app_code = self.developer.generate_flask_app(self.project)
        with open(os.path.join(project_dir, "src", "app.py"), "w") as f:
            f.write(app_code)
        
        # Generate models.py
        models_code = self.developer.generate_models(self.project)
        with open(os.path.join(project_dir, "src", "models.py"), "w") as f:
            f.write(models_code)
        
        # Generate routes.py
        routes_code = self.developer.generate_routes(self.project)
        with open(os.path.join(project_dir, "src", "routes.py"), "w") as f:
            f.write(routes_code)
        
        # Generate requirements.txt
        requirements = self.developer.generate_requirements(self.project)
        with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
            f.write(requirements)
    
    def _generate_html_frontend(self, project_dir: str) -> None:
        """Generate HTML frontend code."""
        # Generate base template
        base_template = self.ui_specialist.generate_base_template(self.project)
        with open(os.path.join(project_dir, "templates", "base.html"), "w") as f:
            f.write(base_template)
        
        # Generate feature templates
        for feature in self.project.features:
            template = self.ui_specialist.generate_feature_template(feature)
            template_name = f"{feature.name.lower()}.html"
            with open(os.path.join(project_dir, "templates", template_name), "w") as f:
                f.write(template)
        
        # Generate static files
        static_files = self.ui_specialist.generate_static_files(self.project)
        for filename, content in static_files.items():
            # Ensure the directory exists before writing the file
            file_path = os.path.join(project_dir, "static", filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content) 