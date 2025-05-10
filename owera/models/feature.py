"""Feature model for Owera CLI."""

from typing import Dict, List, Optional, Any
from .base import BaseModel

class Feature(BaseModel):
    """Feature model representing a project feature."""
    
    def __init__(
        self,
        name: str,
        description: str,
        constraints: Optional[List[str]] = None,
        status: str = "planned",
        priority: int = 1
    ):
        """Initialize feature with given attributes."""
        super().__init__(
            name=name,
            description=description,
            constraints=constraints or [],
            status=status,
            priority=priority
        )
    
    def validate(self) -> bool:
        """Validate feature data."""
        if not self.name:
            raise ValueError("Feature must have a name")
        
        if not self.description:
            raise ValueError("Feature must have a description")
        
        if not isinstance(self.constraints, list):
            raise ValueError("Constraints must be a list")
        
        if not isinstance(self.priority, int):
            raise ValueError("Priority must be an integer")
        
        if self.priority < 1 or self.priority > 5:
            raise ValueError("Priority must be between 1 and 5")
        
        valid_statuses = ["planned", "in_progress", "completed", "blocked"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert feature to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "constraints": self.constraints,
            "status": self.status,
            "priority": self.priority
        } 