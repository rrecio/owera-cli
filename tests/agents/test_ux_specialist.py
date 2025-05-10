import pytest
from owera.agents.ux_specialist import UXSpecialist
from owera.models.base import Task, Project, Feature

@pytest.fixture
def ux_specialist():
    """Create a UX Specialist agent instance."""
    return UXSpecialist()

@pytest.fixture
def sample_feature():
    """Create a sample feature for testing."""
    return Feature(
        name="User Authentication",
        description="Implement secure user authentication system"
    )

@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project(
        name="Test Project",
        type="Web Application",
        target_users="General users",
        requirements=["Security", "Usability", "Accessibility"]
    )

@pytest.fixture
def sample_task(sample_feature):
    """Create a sample task for testing."""
    return Task(
        description="Analyze UX for authentication system",
        feature=sample_feature
    )

def test_ux_specialist_initialization(ux_specialist):
    """Test UX Specialist initialization."""
    assert ux_specialist.role == "UX Specialist"
    assert "user_flow" in ux_specialist.tools
    assert "accessibility_check" in ux_specialist.tools
    assert "usability_test" in ux_specialist.tools
    assert "user_journey" in ux_specialist.tools

def test_generate_prompt(ux_specialist, sample_task, sample_project):
    """Test prompt generation."""
    prompt = ux_specialist.generate_prompt(sample_task, sample_project)
    assert "User Authentication" in prompt
    assert "Web Application" in prompt
    assert "General users" in prompt
    assert "Security" in prompt
    assert "Usability" in prompt
    assert "Accessibility" in prompt

def test_create_user_flow(ux_specialist, sample_feature):
    """Test user flow creation."""
    flow = ux_specialist.create_user_flow(sample_feature)
    assert isinstance(flow, dict)
    assert "nodes" in flow
    assert "edges" in flow
    assert "recommendations" in flow

def test_check_accessibility(ux_specialist, sample_feature):
    """Test accessibility checking."""
    recommendations = ux_specialist.check_accessibility(sample_feature)
    assert isinstance(recommendations, list)

def test_perform_usability_test(ux_specialist, sample_feature):
    """Test usability testing."""
    results = ux_specialist.perform_usability_test(sample_feature)
    assert isinstance(results, dict)
    assert "issues" in results
    assert "recommendations" in results

def test_create_user_journey(ux_specialist, sample_feature):
    """Test user journey creation."""
    journey = ux_specialist.create_user_journey(sample_feature)
    assert isinstance(journey, dict)
    assert "stages" in journey
    assert "touchpoints" in journey
    assert "emotions" in journey

def test_process_response(ux_specialist, sample_task, sample_project):
    """Test response processing."""
    response = """
    User Flow Analysis:
    - Login page
    - Registration page
    - Password reset
    
    Accessibility Recommendations:
    - Add ARIA labels
    - Ensure keyboard navigation
    
    Usability Improvements:
    - Simplify form layout
    - Add clear error messages
    
    User Journey:
    - Entry point
    - Authentication steps
    - Success/failure paths
    """
    
    ux_specialist.process_response(response, sample_task, sample_project)
    assert hasattr(sample_task.feature, "ux_improvements")
    assert isinstance(sample_task.feature.ux_improvements, list)

def test_extract_code(ux_specialist):
    """Test code extraction."""
    response = "Some UX analysis without code"
    code = ux_specialist.extract_code(response)
    assert code == "" 