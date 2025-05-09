import re
from typing import Optional, List
from .base import BaseAgent, AgentError
from ..models.base import Task, Project, Feature

class Developer(BaseAgent):
    """Agent responsible for implementing backend functionality."""
    
    def __init__(self):
        """Initialize the Developer agent."""
        super().__init__("Developer")
        self.feature: Optional[Feature] = None
    
    def generate_prompt(self, task: Task, project: Project) -> str:
        """Generate a prompt for backend implementation."""
        tech_stack = project.specs["project"]["tech_stack"]
        constraints = ", ".join(task.feature.constraints) if task.feature.constraints else "clean, modular code"
        self.feature = task.feature
        
        if task.type == "implement":
            design = project.designs.get(task.feature.name, "")
            template_name = task.feature.name.replace("_", "")  # Remove underscores for template name
            return (
                f"Generate a Flask route for the feature '{task.feature.name}' in {tech_stack['backend']}. "
                f"Return only the Python code, without explanations, comments, or imports "
                f"(assume Flask, render_template, request, redirect, url_for, session, jsonify, SQLAlchemy, and db are imported). "
                f"The models (User, Course, Enrollment) are already defined in the file, so do NOT add any import statements for them. "
                f"Define the route function as 'def {task.feature.name}():' to match the feature name. "
                f"Use the route path '@app.route('/{task.feature.name}')'. "
                f"Render the template '{template_name}.html'. "
                f"If the feature involves displaying items (e.g., courses), query the database using Course.query.all() "
                f"and pass the results to the template as 'items'. "
                f"If authentication is required, use the @login_required decorator without parentheses. "
                f"Description: {task.feature.description}. Design: {design}. Constraints: {constraints}. "
                f"Include necessary logic (e.g., database queries, authentication) as specified in the description."
            )
        elif task.type == "fix":
            code = "\n".join(project.code["backend"])
            return (
                f"Fix the issue in the Flask route for '{task.feature.name}': {task.description}. "
                f"Current code: {code}. Provide only the corrected Python code without explanations or comments."
            )
        else:
            raise AgentError(f"Unknown task type: {task.type}")
    
    def process_response(self, response: str, task: Task, project: Project) -> None:
        """Process the generated backend code."""
        if task.type == "implement":
            project.code["backend"].append(response)
        elif task.type == "fix":
            project.code["backend"] = [response]
        task.feature.has_implementation = True
    
    def extract_code(self, response: str) -> str:
        """Extract Python code from the model's response."""
        # Try to find code blocks first
        code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        
        # Look for Python code patterns
        lines = response.split('\n')
        code_lines: List[str] = []
        in_code = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Start capturing code if we see a route, function definition, or other Python constructs
            if (line.startswith(('@app.route', 'def ', 'from ', 'import ', 'if __name__')) or 
                in_code):
                code_lines.append(line)
                in_code = True
            # Continue capturing if we see Flask patterns or Python constructs
            elif in_code and (
                line.startswith(('#', 'return', 'if ', 'for ', 'while ', 'try ', 'except ', 
                               'with ', 'class ', '@login_required')) or
                any(line.startswith(prefix) for prefix in ('items =', 'courses =', 'user =', 
                                                         'enrollment =')) or
                line.endswith(':')
            ):
                code_lines.append(line)
            # Stop capturing if we hit a non-code line after starting
            elif in_code and not (
                line.startswith(('#', 'return', 'if ', 'for ', 'while ', 'try ', 'except ', 
                               'with ', 'class ', '@login_required')) or
                line.endswith(':')
            ):
                break
        
        if code_lines:
            return '\n'.join(code_lines).strip()
        
        # Generate a fallback route
        self.logger.warning(f"No valid Python code found in response: {response}")
        return self._generate_fallback_route()
    
    def _generate_fallback_route(self) -> str:
        """Generate a fallback route when no valid Python code is found."""
        auth_required = any("secure login" in constraint.lower() 
                          for constraint in self.feature.constraints)
        decorator = "@login_required" if auth_required else ""
        
        return f"""@app.route('/{self.feature.name}')
{decorator}
def {self.feature.name}():
    items = Course.query.all() if 'course' in '{self.feature.name}' else []
    return render_template('{self.feature.name}.html', items=items)""" 