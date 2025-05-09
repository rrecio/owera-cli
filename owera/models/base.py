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
    _status: str = field(default="todo")
    assigned_to: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    VALID_STATUSES = ["todo", "in_progress", "done", "failed"]

    @property
    def status(self) -> str:
        """Get the task status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Set the task status with validation."""
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}. Must be one of {self.VALID_STATUSES}")
        self._status = value
        if value == "done":
            self.completed_at = datetime.now()

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
    """Represents a project in the system."""
    name: str
    tech_stack: Dict[str, str]
    features: List['Feature'] = field(default_factory=list)
    tasks: List['Task'] = field(default_factory=list)
    issues: List['Issue'] = field(default_factory=list)
    code: Dict[str, List[str]] = field(default_factory=lambda: {"backend": [], "frontend": []})
    designs: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    specs: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        """Initialize project from dictionary if needed."""
        if data is None:
            data = {
                "project": {
                    "name": "SimpleApp",
                    "tech_stack": {
                        "backend": "Python/Flask",
                        "frontend": "HTML/CSS"
                    }
                },
                "features": []
            }
        
        self.specs = data
        project_data = data["project"]
        self.name = project_data["name"]
        self.tech_stack = project_data.get("tech_stack", {
            "backend": "Python/Flask",
            "frontend": "HTML/CSS"
        })
        self.features = [
            Feature(
                name=f["name"],
                description=f["description"],
                constraints=f.get("constraints", [])
            )
            for f in data["features"]
        ]
        self.tasks = []
        self.issues = []
        self.code = {"backend": [], "frontend": []}
        self.designs = {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now() 