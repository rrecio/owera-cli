import pytest
from datetime import datetime
from owera.models.base import Feature, Issue, Task, User, Course, Enrollment

def test_feature_creation():
    """Test Feature creation and default values."""
    feature = Feature(
        name="test_feature",
        description="Test feature description"
    )
    assert feature.name == "test_feature"
    assert feature.description == "Test feature description"
    assert feature.constraints == []
    assert feature.has_design is False
    assert feature.has_implementation is False
    assert feature.has_passed_tests is False
    assert feature.is_approved is False
    assert feature.issues == []

def test_issue_creation():
    """Test Issue creation and timestamps."""
    feature = Feature("test_feature", "Test description")
    issue = Issue("Test issue", feature)
    
    assert issue.description == "Test issue"
    assert issue.feature == feature
    assert issue.is_resolved is False
    assert isinstance(issue.created_at, datetime)
    assert issue.resolved_at is None

def test_task_creation():
    """Test Task creation and status management."""
    feature = Feature("test_feature", "Test description")
    task = Task("implement", feature, "Implement test feature")
    
    assert task.type == "implement"
    assert task.feature == feature
    assert task.description == "Implement test feature"
    assert task.status == "todo"
    assert task.assigned_to is None
    assert isinstance(task.created_at, datetime)
    assert task.completed_at is None

def test_user_password_management():
    """Test User password hashing and verification."""
    user = User(
        id=1,
        email="test@example.com",
        password="password123",
        role="user"
    )
    
    # Test password hashing
    user.set_password("newpassword")
    assert user.password != "newpassword"
    
    # Test password verification
    assert user.check_password("newpassword") is True
    assert user.check_password("wrongpassword") is False

def test_course_creation():
    """Test Course creation and relationships."""
    course = Course(
        id=1,
        title="Test Course",
        subject="Computer Science",
        description="Test course description",
        instructor_id=1
    )
    
    assert course.title == "Test Course"
    assert course.subject == "Computer Science"
    assert course.description == "Test course description"
    assert course.instructor_id == 1
    assert isinstance(course.created_at, datetime)

def test_enrollment_creation():
    """Test Enrollment creation and progress tracking."""
    enrollment = Enrollment(
        id=1,
        user_id=1,
        course_id=1,
        progress=0.5
    )
    
    assert enrollment.user_id == 1
    assert enrollment.course_id == 1
    assert enrollment.progress == 0.5
    assert isinstance(enrollment.created_at, datetime)
    assert isinstance(enrollment.updated_at, datetime)

def test_feature_with_constraints():
    """Test Feature with constraints."""
    feature = Feature(
        name="secure_feature",
        description="Secure feature description",
        constraints=["secure login", "use a database"]
    )
    
    assert len(feature.constraints) == 2
    assert "secure login" in feature.constraints
    assert "use a database" in feature.constraints

def test_task_status_transitions():
    """Test Task status transitions."""
    feature = Feature("test_feature", "Test description")
    task = Task("implement", feature, "Implement test feature")
    
    # Test status transitions
    assert task.status == "todo"
    task.status = "in_progress"
    assert task.status == "in_progress"
    task.status = "done"
    assert task.status == "done"
    
    # Test invalid status
    with pytest.raises(ValueError):
        task.status = "invalid_status" 