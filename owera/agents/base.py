from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging
import requests
import ollama
from datetime import datetime
from ..models.base import Task, Project, Feature, Issue
from ..config import config

class OweraError(Exception):
    """Base exception for Owera CLI."""
    pass

class AgentError(OweraError):
    """Base class for agent-related errors."""
    pass

class TimeoutError(AgentError):
    """Raised when an agent operation times out."""
    pass

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, role: str):
        """Initialize the agent with a role."""
        self.role = role
        self.logger = logging.getLogger(f"owera.agent.{role.lower()}")
    
    def perform_task(self, task: Task, project: Project) -> None:
        """Perform a task using the agent's capabilities."""
        try:
            self.logger.info(f"Starting task: {task.description}")
            prompt = self.generate_prompt(task, project)
            self.logger.debug(f"Generated prompt: {prompt}")
            
            response = self._get_model_response(prompt)
            self.logger.debug(f"Model response: {response}")
            
            if self.role in ["UI Specialist", "Developer"]:
                code = self.extract_code(response)
                self.logger.debug(f"Extracted code: {code}")
                if self.role == "Developer":
                    code = self._post_process_code(code)
                self.process_response(code, task, project)
            else:
                self.process_response(response, task, project)
            
            task.status = "done"
            task.completed_at = datetime.now()
            self.logger.info(f"Completed task: {task.description}")
            
        except TimeoutError as e:
            self.logger.error(f"Task timed out: {task.description}")
            task.status = "failed"
            project.issues.append(Issue(
                description=f"{self.role} timed out: {str(e)}",
                feature=task.feature
            ))
            raise
            
        except Exception as e:
            self.logger.error(f"Task failed: {str(e)}")
            task.status = "failed"
            project.issues.append(Issue(
                description=f"{self.role} failed: {str(e)}",
                feature=task.feature
            ))
            raise AgentError(f"{self.role} encountered an error: {str(e)}")
    
    def _get_model_response(self, prompt: str) -> str:
        """Get response from the AI model."""
        try:
            response = ollama.generate(
                model=config.MODEL_NAME,
                prompt=prompt,
                options={"timeout": config.TIMEOUT}
            )
            return response.get("response", "")
        except Exception as e:
            self.logger.error(f"Error getting model response: {e}")
            raise TimeoutError("Request timed out") from e
    
    def _post_process_code(self, code: str) -> str:
        """Post-process generated code."""
        code = self.fix_decorator_usage(code)
        code = self.remove_unnecessary_imports(code)
        return code.strip()
    
    def fix_decorator_usage(self, code: str) -> str:
        """Fix incorrect usage of decorators."""
        lines = code.split('\n')
        fixed_lines = []
        for line in lines:
            if "@login_required()" in line:
                line = line.replace("@login_required()", "@login_required")
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)
    
    def remove_unnecessary_imports(self, code: str) -> str:
        """Remove unnecessary import statements."""
        lines = code.split('\n')
        fixed_lines = []
        for line in lines:
            if line.startswith("from models import"):
                self.logger.info(f"Removing unnecessary import: {line}")
                continue
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)
    
    @abstractmethod
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for the AI model."""
        pass
    
    @abstractmethod
    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the response from the AI model."""
        pass
    
    @abstractmethod
    def extract_code(self, response: str) -> str:
        """Extract code from the model's response."""
        pass 