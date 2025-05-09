from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class Feature:
    """Represents a feature in the project."""
    name: str
    description: str
    constraints: List[str] = field(default_factory=list)
    has_design: bool = False
    has_implementation: bool = False
    has_passed_tests: bool = False
    is_approved: bool = False
    issues: List['Issue'] = field(default_factory=list)

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
    type: str
    feature: Feature
    description: str
    status: str = "todo"
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

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