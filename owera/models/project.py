"""Project model for Owera CLI."""

from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import os

from .base import BaseModel
from .feature import Feature
from .task import Task

class Project(BaseModel):
    """Project model representing a generated application."""
    
    def __init__(
        self,
        name: str,
        tech_stack: Dict[str, str],
        features: Optional[List[Feature]] = None,
        tasks: Optional[List[Task]] = None,
        status: str = "initialized"
    ):
        """Initialize project with given attributes."""
        super().__init__(
            name=name,
            tech_stack=tech_stack,
            features=features or [],
            tasks=tasks or [],
            status=status
        )
    
    def add_feature(self, feature: Feature) -> None:
        """Add a feature to the project."""
        if not isinstance(feature, Feature):
            feature = Feature(**feature)
        self.features.append(feature)
    
    def remove_feature(self, name: str) -> None:
        """Remove a feature from the project."""
        self.features = [f for f in self.features if f.name != name]
    
    def get_feature(self, name: str) -> Feature:
        """Get a feature by name."""
        for feature in self.features:
            if feature.name == name:
                return feature
        raise ValueError(f"Feature {name} not found")
    
    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        if not isinstance(task, Task):
            task = Task(**task)
        self.tasks.append(task)
    
    def remove_task(self, name: str) -> None:
        """Remove a task from the project."""
        self.tasks = [t for t in self.tasks if t.name != name]
    
    def get_task(self, name: str) -> Task:
        """Get a task by name."""
        for task in self.tasks:
            if task.name == name:
                return task
        raise ValueError(f"Task {name} not found")
    
    def validate(self) -> bool:
        """Validate project data."""
        if not self.name:
            raise ValueError("Project must have a name")
        
        if not self.tech_stack:
            raise ValueError("Project must have a tech stack")
        
        if not isinstance(self.tech_stack, dict):
            raise ValueError("Tech stack must be a dictionary")
        
        if "backend" not in self.tech_stack:
            raise ValueError("Tech stack must include backend")
        
        if "frontend" not in self.tech_stack:
            raise ValueError("Tech stack must include frontend")
        
        for feature in self.features:
            if not isinstance(feature, Feature):
                raise ValueError(f"Invalid feature: {feature}")
            feature.validate()
        
        for task in self.tasks:
            if not isinstance(task, Task):
                raise ValueError(f"Invalid task: {task}")
            task.validate()
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary."""
        return {
            "name": self.name,
            "tech_stack": self.tech_stack,
            "features": [f.to_dict() for f in self.features],
            "tasks": [t.to_dict() for t in self.tasks],
            "status": self.status
        }
    
    @classmethod
    def load(cls, project_dir: Optional[str] = None) -> 'Project':
        """Load project from directory."""
        if project_dir is None:
            project_dir = os.getcwd()
        
        project_file = Path(project_dir) / "project.json"
        if not project_file.exists():
            raise ValueError(f"Project file not found: {project_file}")
        
        with open(project_file, 'r') as f:
            data = json.load(f)
        
        # Convert feature and task dictionaries to objects
        if "features" in data:
            data["features"] = [Feature(**f) for f in data["features"]]
        if "tasks" in data:
            data["tasks"] = [Task(**t) for t in data["tasks"]]
        
        return cls(**data)
    
    def save(self, project_dir: Optional[str] = None) -> None:
        """Save project to directory."""
        if project_dir is None:
            project_dir = os.getcwd()
        
        project_file = Path(project_dir) / "project.json"
        # Ensure parent directory exists
        project_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(project_file, 'w') as f:
            f.write(self.to_json()) 