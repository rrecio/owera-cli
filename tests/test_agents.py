import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from owera.agents.base import BaseAgent, AgentError, TimeoutError
from owera.agents.ui_specialist import UISpecialist
from owera.agents.developer import Developer
from owera.agents.qa_specialist import QASpecialist
from owera.agents.product_owner import ProductOwner
from owera.agents.project_manager import ProjectManager
from owera.models.base import Feature, Task, Project, Issue

class TestAgent(BaseAgent):
    """Test implementation of BaseAgent."""
    def __init__(self):
        super().__init__("TestAgent")

    def generate_prompt(self, task: Task, project: Project) -> str:
        return f"Test prompt for {task.description}"
    
    def process_response(self, response: str, task: Task, project: Project) -> None:
        task.status = "done"
    
    def extract_code(self, response: str) -> str:
        return response.replace("```", "").strip()

@pytest.fixture
def mock_project():
    """Create a mock project for testing."""
    return Project({
        "project": {
            "name": "TestProject",
            "tech_stack": {
                "backend": "Python/Flask",
                "frontend": "HTML/CSS"
            }
        },
        "features": [
            {
                "name": "test_feature",
                "description": "Test feature description",
                "constraints": ["responsive design"]
            }
        ]
    })

@pytest.fixture
def mock_task(mock_project):
    """Create a mock task for testing."""
    feature = mock_project.features[0]
    return Task("implement", feature, "Implement test feature")

def test_base_agent_initialization():
    """Test BaseAgent initialization."""
    agent = TestAgent()
    assert agent.role == "TestAgent"
    assert agent.logger.name == "owera.agent.testagent"

@patch('ollama.generate')
def test_base_agent_get_model_response(mock_generate):
    """Test model response generation."""
    agent = TestAgent()
    mock_generate.return_value = {"response": "Test response"}
    
    response = agent._get_model_response("Test prompt")
    assert response == "Test response"
    mock_generate.assert_called_once()

@patch('ollama.generate')
def test_base_agent_timeout(mock_generate):
    """Test timeout handling."""
    agent = TestAgent()
    mock_generate.side_effect = Exception("Request timed out")
    
    with pytest.raises(TimeoutError):
        agent._get_model_response("Test prompt")

def test_ui_specialist_prompt_generation(mock_task, mock_project):
    """Test UI Specialist prompt generation."""
    agent = UISpecialist()
    prompt = agent.generate_prompt(mock_task, mock_project)
    
    assert "HTML code" in prompt
    assert "responsive template" in prompt
    assert mock_task.feature.name in prompt
    assert mock_task.feature.description in prompt

def test_developer_prompt_generation(mock_task, mock_project):
    """Test Developer prompt generation."""
    agent = Developer()
    prompt = agent.generate_prompt(mock_task, mock_project)
    
    assert "Flask route" in prompt
    assert mock_task.feature.name in prompt
    assert mock_task.feature.description in prompt

def test_qa_specialist_response_processing(mock_task, mock_project):
    """Test QA Specialist response processing."""
    agent = QASpecialist()
    
    # Test passing response
    agent.process_response("No issues found", mock_task, mock_project)
    assert mock_task.feature.has_passed_tests is True
    assert len(mock_project.issues) == 0
    
    # Test failing response
    agent.process_response("Found security issues", mock_task, mock_project)
    assert len(mock_project.issues) == 1
    assert len(mock_project.tasks) == 1
    assert mock_project.tasks[0].type == "fix"

def test_product_owner_validation(mock_task, mock_project):
    """Test Product Owner validation."""
    agent = ProductOwner()
    
    # Test approval
    agent.process_response("Approve", mock_task, mock_project)
    assert mock_task.feature.is_approved is True
    assert mock_task.status == "done"
    
    # Test rejection
    mock_task.feature.is_approved = True  # Reset for testing
    agent.process_response("Needs more features", mock_task, mock_project)
    assert mock_task.feature.is_approved is False
    assert mock_task.status == "failed"
    assert len(mock_project.issues) == 1

def test_project_manager_task_planning(mock_project):
    """Test Project Manager task planning."""
    agent = ProjectManager()
    
    # Initial planning
    agent.plan(mock_project)
    assert len(mock_project.tasks) > 0
    
    # Test task assignment
    design_task = next(t for t in mock_project.tasks if t.type == "design")
    assert design_task.assigned_to == "UI Specialist"
    
    # Test task progression
    design_task.status = "done"
    mock_project.features[0].has_design = True
    agent.plan(mock_project)
    implement_task = next(t for t in mock_project.tasks if t.type == "implement")
    assert implement_task.assigned_to == "Developer"

def test_code_extraction():
    """Test code extraction from responses."""
    ui_agent = UISpecialist()
    dev_agent = Developer()
    
    # Test UI code extraction
    html_response = "```html\n<div>Test</div>\n```"
    extracted_html = ui_agent.extract_code(html_response)
    assert extracted_html == "<div>Test</div>"
    
    # Test Python code extraction
    python_response = "```python\n@app.route('/test')\ndef test():\n    return 'test'\n```"
    extracted_python = dev_agent.extract_code(python_response)
    assert "def test()" in extracted_python

def test_error_handling(mock_task, mock_project):
    """Test error handling in agents."""
    agent = TestAgent()
    
    with patch('ollama.generate') as mock_generate:
        mock_generate.side_effect = Exception("Test error")
        agent.perform_task(mock_task, mock_project)
    
    assert mock_task.status == "failed"
    assert len(mock_project.issues) == 1 