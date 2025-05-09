from typing import Optional
from .base import BaseAgent
from ..models.base import Task, Project, Feature, Issue

class QASpecialist(BaseAgent):
    """Agent responsible for testing and quality assurance."""
    
    def __init__(self):
        """Initialize the QA Specialist agent."""
        super().__init__("QA Specialist")
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for testing a feature."""
        code = "\n".join(project.code["backend"])
        design = project.designs.get(task.feature.name, "")
        return (
            f"Test the feature '{task.feature.name}'. "
            f"Code: {code}. Design: {design}. "
            f"Description: {task.feature.description}. "
            f"Provide only a brief result: 'No issues' or list specific issues. "
            f"Focus on:\n"
            f"1. Functionality: Does it work as described?\n"
            f"2. Security: Are there any security vulnerabilities?\n"
            f"3. Performance: Are there any obvious performance issues?\n"
            f"4. User Experience: Is the interface intuitive and responsive?"
        )
    
    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the testing results."""
        if "no issues" in response.lower() or "passes" in response.lower():
            task.feature.has_passed_tests = True
            self.logger.info(f"Feature '{task.feature.name}' passed QA testing")
        else:
            issue = Issue(response, task.feature)
            project.issues.append(issue)
            self.logger.warning(f"Found issues in feature '{task.feature.name}': {response}")
            
            # Create a fix task
            fix_task = Task("fix", task.feature, f"Fix: {response}")
            fix_task.assigned_to = "Developer"
            project.tasks.append(fix_task)
    
    def extract_code(self, response: str) -> str:
        """QA Specialist doesn't need to extract code."""
        return response 