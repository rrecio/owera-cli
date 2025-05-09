from typing import Optional
from owera.agents.base import BaseAgent
from owera.models.base import Task, Project, Issue

class ProductOwner(BaseAgent):
    """Product Owner agent responsible for validating features."""
    def __init__(self):
        super().__init__("Product Owner")

    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for feature validation."""
        return (
            f"As a Product Owner, validate if the feature '{task.feature.name}' meets the requirements:\n"
            f"Description: {task.feature.description}\n"
            f"Constraints: {', '.join(task.feature.constraints)}\n\n"
            f"Please respond with either 'Approve' or provide specific reasons for rejection."
        )

    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the validation response."""
        if "approve" in response.lower():
            task.feature.is_approved = True
            task.status = "done"
        else:
            task.feature.is_approved = False
            task.status = "failed"
            project.issues.append(Issue(
                description=f"Feature validation failed: {response}",
                feature=task.feature
            ))

    def extract_code(self, response: str) -> str:
        """Extract code from response (not used for Product Owner)."""
        return "" 