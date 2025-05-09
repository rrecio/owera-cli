from typing import List, Optional
from datetime import datetime
from .base import BaseAgent
from ..models.base import Task, Project, Feature

class ProjectManager(BaseAgent):
    """Agent responsible for project planning and task coordination."""
    
    def __init__(self):
        """Initialize the Project Manager agent."""
        super().__init__("Project Manager")
    
    def plan(self, project: Project) -> None:
        """Plan tasks for all features in the project."""
        self.logger.info("Planning tasks for features")
        
        for feature in project.features:
            self._plan_feature_tasks(feature, project)
        
        self.logger.info(f"Planned {len(project.tasks)} tasks")
    
    def _plan_feature_tasks(self, feature: Feature, project: Project) -> None:
        """Plan tasks for a single feature."""
        # Design task
        if not feature.has_design and not self._has_task(feature, "design", project.tasks):
            task = Task("design", feature, f"Design {feature.name}")
            task.assigned_to = "UI Specialist"
            project.tasks.append(task)
            self.logger.debug(f"Assigned design task for feature: {feature.name}")
        
        # Implementation task
        elif feature.has_design and not feature.has_implementation and not self._has_task(feature, "implement", project.tasks):
            task = Task("implement", feature, f"Implement {feature.name}")
            task.assigned_to = "Developer"
            project.tasks.append(task)
            self.logger.debug(f"Assigned implement task for feature: {feature.name}")
        
        # Testing task
        elif feature.has_implementation and not feature.has_passed_tests and not self._has_task(feature, "test", project.tasks):
            task = Task("test", feature, f"Test {feature.name}")
            task.assigned_to = "QA Specialist"
            project.tasks.append(task)
            self.logger.debug(f"Assigned test task for feature: {feature.name}")
        
        # Review task
        elif feature.has_passed_tests and not feature.is_approved and not self._has_task(feature, "review", project.tasks):
            task = Task("review", feature, f"Review {feature.name}")
            task.assigned_to = "Product Owner"
            project.tasks.append(task)
            self.logger.debug(f"Assigned review task for feature: {feature.name}")
    
    def _has_task(self, feature: Feature, task_type: str, tasks: List[Task]) -> bool:
        """Check if a feature already has a specific type of task."""
        return any(t.feature == feature and t.type == task_type for t in tasks)
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Project Manager doesn't need to generate prompts."""
        return ""
    
    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Project Manager doesn't need to process responses."""
        pass
    
    def extract_code(self, response: str) -> str:
        """Project Manager doesn't need to extract code."""
        return response 