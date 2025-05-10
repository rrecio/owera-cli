from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from pathlib import Path

@dataclass
class Feature:
    """Represents a feature in the project."""
    name: str
    description: str
    status: str = "planned"
    requirements: List[str] = field(default_factory=list)
    design: Optional[Dict[str, Any]] = None
    ux_improvements: List[str] = field(default_factory=list)
    implementation: Optional[Dict[str, Any]] = None
    test_results: Optional[Dict[str, Any]] = None
    quality_metrics: Optional[Dict[str, Any]] = None
    business_impact: Optional[Dict[str, Any]] = None
    error_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Issue:
    """Represents an issue in a feature."""
    description: str
    feature: Feature
    is_resolved: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

@dataclass
class Task:
    """Represents a task in the project."""
    description: str
    feature: Feature
    status: str = "planned"
    assigned_to: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

@dataclass
class User:
    """Represents a user in the system."""
    id: int
    email: str
    password: str
    role: str
    created_at: datetime = field(default_factory=datetime.now)
    
    def set_password(self, password: str) -> None:
        """Set the user's password with hashing."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)

@dataclass
class Course:
    """Represents a course in the system."""
    id: int
    title: str
    subject: str
    description: str
    instructor_id: int
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Enrollment:
    """Represents a course enrollment."""
    id: int
    user_id: int
    course_id: int
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Project:
    """Represents a project."""
    name: str
    type: str
    target_users: str
    target_market: str
    business_goals: List[str]
    requirements: List[str]
    budget: float
    timeline: str
    features: List[Feature] = field(default_factory=list)
    status: str = "planned"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    progress: Optional[Dict[str, Any]] = None

@dataclass
class SprintPlan:
    """Represents a sprint plan."""
    tasks: List[Task]
    start_date: datetime
    end_date: datetime
    status: str = "planned"
    velocity: float = 0.0
    burndown: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class Progress:
    """Represents project progress."""
    completed_tasks: List[Task]
    remaining_tasks: List[Task]
    completion_percentage: float
    burndown_data: List[Dict[str, Any]] = field(default_factory=list)
    velocity: float = 0.0

@dataclass
class SprintReview:
    """Represents a sprint review."""
    completed_features: List[Feature]
    remaining_features: List[Feature]
    velocity: float
    retrospective: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    improvements: List[str] = field(default_factory=list)

class BaseModel:
    """Base model class for all models."""
    
    def __init__(self, **kwargs):
        """Initialize model with given attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
    
    def to_json(self) -> str:
        """Convert model to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def save(self, file_path: Optional[str] = None) -> None:
        """Save model to file."""
        if file_path is None:
            file_path = f"{self.__class__.__name__.lower()}.json"
        
        with open(file_path, 'w') as f:
            f.write(self.to_json())
    
    @classmethod
    def load(cls, file_path: str) -> 'BaseModel':
        """Load model from file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate model data."""
        return True
    
    def __str__(self) -> str:
        """String representation of model."""
        return f"{self.__class__.__name__}({self.to_dict()})"
    
    def __repr__(self) -> str:
        """Representation of model."""
        return self.__str__() 