"""UI specialist agent for Owera CLI."""

from typing import Dict, Any, Optional
from ..models import Project, Feature, Task
from ..config import Config
from .base import BaseAgent

class UISpecialist(BaseAgent):
    """UI specialist agent for generating frontend code."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize UI specialist."""
        super().__init__(config)
        self.role = "UI Specialist"
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for the AI model."""
        return f"""As a UI Specialist, please help with the following task:
Task: {task.description}
Feature: {task.feature.name if task.feature else 'N/A'}
Project: {project.name}

Please provide HTML/CSS code that implements the requested UI changes.
Focus on creating a clean, modern, and responsive design."""

    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the response from the AI model."""
        # For UI tasks, we'll store the generated templates and styles
        if "template" in task.description.lower():
            project.templates[task.name] = response
        elif "style" in task.description.lower() or "css" in task.description.lower():
            project.styles[task.name] = response
        else:
            self.logger.warning(f"Unhandled UI task type: {task.description}")

    def extract_code(self, response: str) -> str:
        """Extract code from the model's response."""
        # Look for code blocks in the response
        if "```html" in response:
            start = response.find("```html") + 7
            end = response.find("```", start)
            return response[start:end].strip()
        elif "```css" in response:
            start = response.find("```css") + 6
            end = response.find("```", start)
            return response[start:end].strip()
        return response.strip()
    
    def generate_base_template(self, project: Project) -> str:
        """Generate base HTML template."""
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project.name}</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="{{{{ url_for('index') }}}}">Home</a></li>
                {{% for feature in features %}}
                <li><a href="{{{{ url_for(feature.name.lower()) }}}}">{{{{ feature.name }}}}</a></li>
                {{% endfor %}}
            </ul>
        </nav>
    </header>
    
    <main>
        {{% block content %}}{{% endblock %}}
    </main>
    
    <footer>
        <p>&copy; 2024 {project.name}. All rights reserved.</p>
    </footer>
</body>
</html>"""
        return template
    
    def generate_feature_template(self, feature: Feature) -> str:
        """Generate HTML template for a feature."""
        template = f"""{{% extends "base.html" %}}

{{% block content %}}
<div class="feature">
    <h1>{feature.name}</h1>
    <p>{feature.description}</p>
    
    {{% if feature.constraints %}}
    <div class="constraints">
        <h2>Constraints</h2>
        <ul>
            {{% for constraint in feature.constraints %}}
            <li>{{{{ constraint }}}}</li>
            {{% endfor %}}
        </ul>
    </div>
    {{% endif %}}
</div>
{{% endblock %}}"""
        return template
    
    def generate_static_files(self, project: Project) -> Dict[str, str]:
        """Generate static files (CSS, JS, etc.)."""
        return {
            "css/style.css": """/* Main styles */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

header {
    background-color: #333;
    color: white;
    padding: 1rem;
}

nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
}

nav ul li {
    margin-right: 1rem;
}

nav ul li a {
    color: white;
    text-decoration: none;
}

main {
    padding: 2rem;
}

footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    position: fixed;
    bottom: 0;
    width: 100%;
}

.feature {
    max-width: 800px;
    margin: 0 auto;
}

.constraints {
    margin-top: 2rem;
    padding: 1rem;
    background-color: #f4f4f4;
    border-radius: 5px;
}"""
        } 