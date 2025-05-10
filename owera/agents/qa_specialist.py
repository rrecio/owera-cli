"""QA specialist agent for Owera CLI."""

from typing import Dict, Any, Optional
from ..models import Project, Feature, Task
from ..config import Config
from .base import BaseAgent

class QASpecialist(BaseAgent):
    """QA specialist agent for generating test code."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize QA specialist."""
        super().__init__(config)
        self.role = "QA Specialist"
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for the AI model."""
        return f"""As a QA Specialist, please help with the following task:
Task: {task.description}
Feature: {task.feature.name if task.feature else 'N/A'}
Project: {project.name}

Please provide test cases that verify the functionality and quality of the feature.
Focus on writing comprehensive tests that cover edge cases and error conditions."""

    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the response from the AI model."""
        # For QA tasks, we'll store the generated test code
        if "test" in task.description.lower():
            feature_name = task.feature.name if task.feature else "unknown"
            project.test_code[feature_name] = response
        else:
            self.logger.warning(f"Unhandled QA task type: {task.description}")

    def extract_code(self, response: str) -> str:
        """Extract code from the model's response."""
        # Look for Python code blocks in the response
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            return response[start:end].strip()
        return response.strip()

    def generate_tests(self, feature: Feature, output_dir: str) -> None:
        """Generate test files for a feature."""
        # Generate test file
        test_code = self._generate_test_code(feature)
        test_file = f"test_{feature.name.lower().replace(' ', '_')}.py"
        
        with open(f"{output_dir}/tests/{test_file}", "w") as f:
            f.write(test_code)
    
    def _generate_test_code(self, feature: Feature) -> str:
        """Generate test code for a feature."""
        test_name = feature.name.replace(" ", "")
        route_name = feature.name.lower().replace(" ", "_")
        
        code = f"""import pytest
from flask import url_for

def test_{route_name}_route(client):
    response = client.get(url_for('{route_name}'))
    assert response.status_code == 200
    assert b'{feature.name}' in response.data

def test_{route_name}_content(client):
    response = client.get(url_for('{route_name}'))
    assert b'{feature.description}' in response.data"""
        
        # Add tests for constraints
        if feature.constraints:
            code += "\n\ndef test_{route_name}_constraints(client):"
            code += "\n    response = client.get(url_for('{route_name}'))"
            for constraint in feature.constraints:
                code += f"\n    assert b'{constraint}' in response.data"
        
        return code 