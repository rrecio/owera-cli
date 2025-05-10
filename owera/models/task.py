"""Task model for Owera CLI."""

from typing import Dict, List, Optional, Any
from .base import BaseModel

class Task(BaseModel):
    """Task model representing a project task."""
    
    def __init__(
        self,
        name: str,
        description: str,
        status: str = "todo",
        assigned_to: Optional[str] = None,
        priority: int = 1,
        dependencies: Optional[List[str]] = None
    ):
        """Initialize task with given attributes."""
        super().__init__(
            name=name,
            description=description,
            status=status,
            assigned_to=assigned_to,
            priority=priority,
            dependencies=dependencies or []
        )
    
    def validate(self) -> bool:
        """Validate task data."""
        if not self.name:
            raise ValueError("Task must have a name")
        
        if not self.description:
            raise ValueError("Task must have a description")
        
        if not isinstance(self.dependencies, list):
            raise ValueError("Dependencies must be a list")
        
        if not isinstance(self.priority, int):
            raise ValueError("Priority must be an integer")
        
        if self.priority < 1 or self.priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        
        valid_statuses = ["todo", "in_progress", "completed", "blocked"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "priority": self.priority,
            "dependencies": self.dependencies
        } 