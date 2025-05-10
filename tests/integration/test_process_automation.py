import pytest
from owera.process import ProcessManager
from owera.models.base import Project, Feature, Task
from owera.agents import (
    UISpecialist, UXSpecialist, Developer, QASpecialist,
    ProductOwner, Stakeholder
)

@pytest.fixture
def process_manager():
    """Create a process manager instance."""
    return ProcessManager()

@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project(
        name="Test E-commerce",
        type="Web Application",
        target_users="Online shoppers",
        target_market="Retail consumers",
        business_goals=["Increase sales", "Improve user experience"],
        requirements=["Security", "Usability", "Accessibility"],
        budget=100000,
        timeline="6 months",
        features=[
            Feature(
                name="Product Search",
                description="Implement advanced product search with filters"
            ),
            Feature(
                name="Shopping Cart",
                description="Implement shopping cart functionality"
            )
        ]
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

def test_sprint_planning(process_manager, sample_project, agents):
    """Test sprint planning process."""
    # Create sprint plan
    sprint_plan = process_manager.plan_sprint(sample_project)
    
    # Verify sprint plan
    assert sprint_plan is not None
    assert len(sprint_plan.tasks) > 0
    assert all(isinstance(task, Task) for task in sprint_plan.tasks)
    assert sprint_plan.start_date is not None
    assert sprint_plan.end_date is not None

def test_task_assignment(process_manager, sample_project, agents):
    """Test task assignment process."""
    # Create sprint plan
    sprint_plan = process_manager.plan_sprint(sample_project)
    
    # Assign tasks to agents
    assignments = process_manager.assign_tasks(sprint_plan.tasks, agents)
    
    # Verify task assignments
    assert len(assignments) == len(sprint_plan.tasks)
    assert all(agent in agents.values() for agent in assignments.values())
    assert all(isinstance(task, Task) for task in assignments.keys())

def test_progress_tracking(process_manager, sample_project, agents):
    """Test progress tracking process."""
    # Create sprint plan
    sprint_plan = process_manager.plan_sprint(sample_project)
    
    # Assign tasks
    assignments = process_manager.assign_tasks(sprint_plan.tasks, agents)
    
    # Track progress
    progress = process_manager.track_progress(sprint_plan, assignments)
    
    # Verify progress tracking
    assert progress is not None
    assert hasattr(progress, "completed_tasks")
    assert hasattr(progress, "remaining_tasks")
    assert hasattr(progress, "completion_percentage")
    assert 0 <= progress.completion_percentage <= 100

def test_sprint_review(process_manager, sample_project, agents):
    """Test sprint review process."""
    # Create sprint plan
    sprint_plan = process_manager.plan_sprint(sample_project)
    
    # Assign tasks
    assignments = process_manager.assign_tasks(sprint_plan.tasks, agents)
    
    # Complete sprint
    for task, agent in assignments.items():
        agent.perform_task(task, sample_project)
    
    # Review sprint
    review = process_manager.review_sprint(sprint_plan, assignments)
    
    # Verify sprint review
    assert review is not None
    assert hasattr(review, "completed_features")
    assert hasattr(review, "remaining_features")
    assert hasattr(review, "velocity")
    assert hasattr(review, "retrospective")

def test_error_handling(process_manager, sample_project, agents):
    """Test error handling in process automation."""
    # Create invalid sprint plan
    invalid_plan = process_manager.plan_sprint(sample_project)
    invalid_plan.tasks = []
    
    # Attempt to assign tasks
    with pytest.raises(ValueError):
        process_manager.assign_tasks(invalid_plan.tasks, agents)
    
    # Attempt to track progress
    with pytest.raises(ValueError):
        process_manager.track_progress(invalid_plan, {})

def test_end_to_end_process(process_manager, sample_project, agents):
    """Test the complete end-to-end process automation."""
    # Plan sprint
    sprint_plan = process_manager.plan_sprint(sample_project)
    
    # Assign tasks
    assignments = process_manager.assign_tasks(sprint_plan.tasks, agents)
    
    # Track progress
    progress = process_manager.track_progress(sprint_plan, assignments)
    
    # Complete tasks
    for task, agent in assignments.items():
        agent.perform_task(task, sample_project)
    
    # Review sprint
    review = process_manager.review_sprint(sprint_plan, assignments)
    
    # Verify end-to-end process
    assert sprint_plan is not None
    assert len(assignments) > 0
    assert progress.completion_percentage == 100
    assert len(review.completed_features) == len(sample_project.features)
    assert len(review.remaining_features) == 0

def test_concurrent_task_execution(process_manager, sample_project, agents):
    """Test concurrent task execution."""
    # Create sprint plan
    sprint_plan = process_manager.plan_sprint(sample_project)
    
    # Assign tasks
    assignments = process_manager.assign_tasks(sprint_plan.tasks, agents)
    
    # Execute tasks concurrently
    results = process_manager.execute_tasks_concurrently(assignments, sample_project)
    
    # Verify concurrent execution
    assert len(results) == len(assignments)
    assert all(result is not None for result in results)
    assert all(hasattr(result, "status") for result in results)
    assert all(result.status == "completed" for result in results) 