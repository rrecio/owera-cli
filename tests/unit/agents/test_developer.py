import pytest
from owera.agents.core.developer import DeveloperAgent

def test_developer_initialization(base_agent):
    """Test developer agent initialization."""
    developer = DeveloperAgent(base_agent.config)
    assert developer.name == "developer"
    assert developer.enabled is True

def test_developer_task_execution(base_agent):
    """Test developer agent task execution."""
    developer = DeveloperAgent(base_agent.config)
    task = {
        "name": "test_task",
        "description": "Test task description",
        "type": "implementation"
    }
    result = developer.execute_task(task)
    assert result is not None
    assert "status" in result
    assert result["status"] == "completed" 