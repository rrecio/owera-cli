import pytest
from owera.agents import (
    UISpecialist, UXSpecialist, Developer, QASpecialist,
    ProductOwner, Stakeholder
)
from owera.models.base import Task, Project, Feature

@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project(
        name="E-commerce Platform",
        type="Web Application",
        target_users="Online shoppers",
        target_market="Retail consumers",
        business_goals=["Increase sales", "Improve user experience"],
        requirements=["Security", "Usability", "Accessibility"],
        budget=100000,
        timeline="6 months"
    )

@pytest.fixture
def sample_feature():
    """Create a sample feature for testing."""
    return Feature(
        name="Product Search",
        description="Implement advanced product search with filters"
    )

@pytest.fixture
def agents():
    """Create all agent instances."""
    return {
        "ui": UISpecialist(),
        "ux": UXSpecialist(),
        "dev": Developer(),
        "qa": QASpecialist(),
        "po": ProductOwner(),
        "stakeholder": Stakeholder()
    }

def test_planning_phase(agents, sample_project, sample_feature):
    """Test the planning phase collaboration between agents."""
    # Product Owner creates initial task
    po_task = Task(
        description="Define product search requirements",
        feature=sample_feature
    )
    agents["po"].perform_task(po_task, sample_project)
    
    # Stakeholder validates business value
    stakeholder_task = Task(
        description="Validate business value of product search",
        feature=sample_feature
    )
    agents["stakeholder"].perform_task(stakeholder_task, sample_project)
    
    # Verify collaboration results
    assert hasattr(sample_feature, "requirements")
    assert hasattr(sample_feature, "business_validation")
    assert sample_feature.status == "planned"

def test_design_phase(agents, sample_project, sample_feature):
    """Test the design phase collaboration between agents."""
    # UI Specialist creates design
    ui_task = Task(
        description="Design product search interface",
        feature=sample_feature
    )
    agents["ui"].perform_task(ui_task, sample_project)
    
    # UX Specialist optimizes experience
    ux_task = Task(
        description="Optimize product search user experience",
        feature=sample_feature
    )
    agents["ux"].perform_task(ux_task, sample_project)
    
    # Product Owner reviews design
    po_task = Task(
        description="Review product search design",
        feature=sample_feature
    )
    agents["po"].perform_task(po_task, sample_project)
    
    # Verify collaboration results
    assert hasattr(sample_feature, "design")
    assert hasattr(sample_feature, "ux_improvements")
    assert sample_feature.status == "designed"

def test_development_phase(agents, sample_project, sample_feature):
    """Test the development phase collaboration between agents."""
    # Developer implements feature
    dev_task = Task(
        description="Implement product search functionality",
        feature=sample_feature
    )
    agents["dev"].perform_task(dev_task, sample_project)
    
    # QA Specialist tests implementation
    qa_task = Task(
        description="Test product search implementation",
        feature=sample_feature
    )
    agents["qa"].perform_task(qa_task, sample_project)
    
    # Verify collaboration results
    assert hasattr(sample_feature, "implementation")
    assert hasattr(sample_feature, "test_results")
    assert sample_feature.status == "implemented"

def test_review_phase(agents, sample_project, sample_feature):
    """Test the review phase collaboration between agents."""
    # QA Specialist verifies quality
    qa_task = Task(
        description="Verify product search quality",
        feature=sample_feature
    )
    agents["qa"].perform_task(qa_task, sample_project)
    
    # Stakeholder evaluates business impact
    stakeholder_task = Task(
        description="Evaluate product search business impact",
        feature=sample_feature
    )
    agents["stakeholder"].perform_task(stakeholder_task, sample_project)
    
    # Product Owner approves feature
    po_task = Task(
        description="Approve product search feature",
        feature=sample_feature
    )
    agents["po"].perform_task(po_task, sample_project)
    
    # Verify collaboration results
    assert hasattr(sample_feature, "quality_metrics")
    assert hasattr(sample_feature, "business_impact")
    assert sample_feature.status == "approved"

def test_end_to_end_workflow(agents, sample_project, sample_feature):
    """Test the complete end-to-end workflow."""
    # Planning Phase
    test_planning_phase(agents, sample_project, sample_feature)
    
    # Design Phase
    test_design_phase(agents, sample_project, sample_feature)
    
    # Development Phase
    test_development_phase(agents, sample_project, sample_feature)
    
    # Review Phase
    test_review_phase(agents, sample_project, sample_feature)
    
    # Verify final state
    assert sample_feature.status == "approved"
    assert all(hasattr(sample_feature, attr) for attr in [
        "requirements",
        "business_validation",
        "design",
        "ux_improvements",
        "implementation",
        "test_results",
        "quality_metrics",
        "business_impact"
    ])

def test_error_handling(agents, sample_project, sample_feature):
    """Test error handling in agent collaboration."""
    # Simulate error in development phase
    sample_feature.status = "error"
    
    # Developer attempts to fix
    dev_task = Task(
        description="Fix product search implementation",
        feature=sample_feature
    )
    agents["dev"].perform_task(dev_task, sample_project)
    
    # QA verifies fix
    qa_task = Task(
        description="Verify product search fix",
        feature=sample_feature
    )
    agents["qa"].perform_task(qa_task, sample_project)
    
    # Verify error handling
    assert sample_feature.status != "error"
    assert hasattr(sample_feature, "error_history")
    assert len(sample_feature.error_history) > 0 