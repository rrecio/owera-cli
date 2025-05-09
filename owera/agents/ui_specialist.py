import re
from typing import Optional
from .base import BaseAgent
from ..models.base import Task, Project, Feature

class UISpecialist(BaseAgent):
    """Agent responsible for generating UI templates."""
    
    def __init__(self):
        """Initialize the UI Specialist agent."""
        super().__init__("UI Specialist")
        self.feature: Optional[Feature] = None
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for UI template generation."""
        constraints = ", ".join(task.feature.constraints) if task.feature.constraints else "responsive, modern design"
        self.feature = task.feature
        return (
            f"Provide only the HTML code for a responsive template for '{task.feature.name}' "
            f"using Tailwind CSS via CDN. Do not include explanations or comments, just the raw HTML code. "
            f"Description: {task.feature.description}. Constraints: {constraints}."
        )
    
    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the generated UI template."""
        project.designs[task.feature.name] = response
        task.feature.has_design = True
    
    def extract_code(self, response: str) -> str:
        """Extract HTML code from the model's response."""
        # Try to find code blocks first
        html_blocks = re.findall(r'```html\n(.*?)\n```', response, re.DOTALL)
        if html_blocks:
            return html_blocks[0].strip()
        
        # Check if the entire response is HTML
        if response.strip().startswith('<!DOCTYPE html>') or response.strip().startswith('<html'):
            return response.strip()
        
        # Look for HTML-like content
        lines = response.split('\n')
        html_lines = [line for line in lines if line.strip().startswith(('<', '!DOCTYPE'))]
        if html_lines:
            return '\n'.join(html_lines).strip()
        
        # Generate a fallback template
        self.logger.warning(f"No HTML found in response: {response}")
        return self._generate_fallback_template()
    
    def _generate_fallback_template(self) -> str:
        """Generate a fallback template when no valid HTML is found."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.feature.name.title()}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-12">
        <h2 class="text-3xl font-bold mb-6 text-center">{self.feature.name.title()}</h2>
        <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-lg">
            <p class="text-gray-600">{self.feature.description}</p>
        </div>
    </div>
</body>
</html>""" 