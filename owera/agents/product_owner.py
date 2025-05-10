"""Product owner agent for Owera CLI."""

from typing import Dict, Any, Optional
from ..models import Project, Feature, Task
from ..config import Config
from .base import BaseAgent

class ProductOwner(BaseAgent):
    """Product owner agent for generating documentation."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize product owner."""
        super().__init__(config)
        self.role = "Product Owner"
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for the AI model."""
        return f"""As a Product Owner, please help with the following task:
Task: {task.description}
Feature: {task.feature.name if task.feature else 'N/A'}
Project: {project.name}

Please provide documentation and specifications that clearly define the feature requirements.
Focus on user stories, acceptance criteria, and business value."""

    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the response from the AI model."""
        # For product owner tasks, we'll store the generated documentation
        if "doc" in task.description.lower() or "spec" in task.description.lower():
            feature_name = task.feature.name if task.feature else "unknown"
            project.documentation[feature_name] = response
        else:
            self.logger.warning(f"Unhandled product owner task type: {task.description}")

    def extract_code(self, response: str) -> str:
        """Extract code from the model's response."""
        # For product owner, we don't typically extract code
        # but we'll return the response as is for consistency
        return response.strip()

    def generate_documentation(self, feature: Feature, output_dir: str) -> None:
        """Generate documentation for a feature."""
        # Generate markdown documentation
        doc = self._generate_markdown(feature)
        doc_file = f"{feature.name.lower().replace(' ', '_')}.md"
        
        with open(f"{output_dir}/docs/{doc_file}", "w") as f:
            f.write(doc)
    
    def _generate_markdown(self, feature: Feature) -> str:
        """Generate markdown documentation for a feature."""
        doc = f"""# {feature.name}

## Description
{feature.description}

## Status
Current status: {feature.status}

## Priority
Priority level: {feature.priority}/5

## Constraints
"""
        
        if feature.constraints:
            for constraint in feature.constraints:
                doc += f"- {constraint}\n"
        else:
            doc += "No specific constraints defined.\n"
        
        doc += """
## Implementation Details
- Backend: Flask
- Frontend: HTML/CSS
- Database: SQLite

## Testing
Run the following command to test this feature:
```bash
pytest tests/test_{feature.name.lower().replace(' ', '_')}.py
```

## API Endpoints
- GET /{feature.name.lower().replace(' ', '_')} - View feature page

## Dependencies
- Flask
- Flask-SQLAlchemy
- pytest (for testing)
"""
        
        return doc 