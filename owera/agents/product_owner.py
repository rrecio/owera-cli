from typing import Optional
from .base import BaseAgent
from ..models.base import Task, Project, Feature, Issue

class ProductOwner(BaseAgent):
    """Agent responsible for validating features against specifications."""
    
    def __init__(self):
        """Initialize the Product Owner agent."""
        super().__init__("Product Owner")
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for feature validation."""
        code = "\n".join(project.code["backend"])
        design = project.designs.get(task.feature.name, "")
        return (
            f"Verify if '{task.feature.name}' meets the specification. "
            f"Code: {code}. Design: {design}. "
            f"Description: {task.feature.description}. "
            f"Provide only 'Approve' or list specific discrepancies. "
            f"Focus on:\n"
            f"1. Requirements: Does it fulfill all specified requirements?\n"
            f"2. Constraints: Are all constraints satisfied?\n"
            f"3. User Value: Does it provide the intended value to users?\n"
            f"4. Integration: Does it work well with other features?"
        )
    
    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the validation results."""
        if "approve" in response.lower():
            task.feature.is_approved = True
            self.logger.info(f"Feature '{task.feature.name}' approved by Product Owner")
        else:
            issue = Issue(response, task.feature)
            project.issues.append(issue)
            self.logger.warning(f"Feature '{task.feature.name}' needs revision: {response}")
            
            # Create a fix task
            fix_task = Task("fix", task.feature, f"Fix: {response}")
            fix_task.assigned_to = "Developer"
            project.tasks.append(fix_task)
    
    def extract_code(self, response: str) -> str:
        """Product Owner doesn't need to extract code."""
        return response 