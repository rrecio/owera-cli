"""Developer agent for Owera CLI."""

from typing import Dict, Any, Optional
from ..models import Project, Feature, Task
from ..config import Config
from .base import BaseAgent

class Developer(BaseAgent):
    """Developer agent for generating backend code."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize developer."""
        super().__init__(config)
        self.role = "Developer"
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for the AI model."""
        return f"""As a Developer, please help with the following task:
Task: {task.description}
Feature: {task.feature.name if task.feature else 'N/A'}
Project: {project.name}
Tech Stack: {project.tech_stack}

Please provide Python code that implements the requested functionality.
Focus on writing clean, maintainable, and well-documented code."""

    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the response from the AI model."""
        # For development tasks, we'll store the generated code
        if "app" in task.description.lower():
            project.app_code = response
        elif "model" in task.description.lower():
            project.models_code = response
        elif "route" in task.description.lower():
            project.routes_code = response
        else:
            self.logger.warning(f"Unhandled development task type: {task.description}")

    def extract_code(self, response: str) -> str:
        """Extract code from the model's response."""
        # Look for Python code blocks in the response
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            return response[start:end].strip()
        return response.strip()

    def generate_flask_app(self, project: Project) -> str:
        """Generate Flask application code."""
        code = f"""from flask import Flask, render_template
from .models import db
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)"""
        return code
    
    def generate_models(self, project: Project) -> str:
        """Generate database models."""
        code = """from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()"""
        
        # Add models for each feature
        for feature in project.features:
            model_name = feature.name.replace(" ", "")
            code += f"""

class {model_name}(BaseModel):
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<{model_name} {{self.name}}>'"""
        
        return code
    
    def generate_routes(self, project: Project) -> str:
        """Generate route handlers."""
        code = """from flask import render_template, redirect, url_for, flash, request
from .models import db

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}"""
        
        # Add routes for each feature
        for feature in project.features:
            route_name = feature.name.lower().replace(" ", "_")
            code += f"""

    @app.route('/{route_name}')
    def {route_name}():
        return render_template('{route_name}.html')"""
        
        return code
    
    def generate_requirements(self, project: Project) -> str:
        """Generate requirements.txt file."""
        requirements = [
            "flask==3.0.0",
            "flask-sqlalchemy==3.1.1",
            "python-dotenv==1.0.0",
            "pytest==7.4.3",
            "pytest-flask==1.3.0"
        ]
        
        # Add feature-specific requirements
        if any("api" in f.name.lower() for f in project.features):
            requirements.append("flask-restful==0.3.10")
        
        if any("auth" in f.name.lower() for f in project.features):
            requirements.append("flask-login==0.6.3")
            requirements.append("flask-wtf==1.2.1")
        
        return "\n".join(requirements) 