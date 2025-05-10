# Owera CLI API Documentation

## Table of Contents
1. [Models](#models)
2. [Agents](#agents)
3. [Utils](#utils)
4. [Generator](#generator)

## Models

### Project
```python
class Project:
    def __init__(self, name: str, tech_stack: Dict[str, str], features: List[Feature], tasks: List[Task])
    def add_feature(self, feature: Feature) -> None
    def remove_feature(self, name: str) -> None
    def add_task(self, task: Task) -> None
    def remove_task(self, name: str) -> None
    def validate(self) -> bool
    def get_status(self) -> str
    def to_yaml(self) -> str
```

### Feature
```python
class Feature:
    def __init__(self, name: str, description: str, status: str = "todo", constraints: List[str] = None)
    def validate(self) -> bool
    def to_dict(self) -> Dict[str, Any]
```

### Task
```python
class Task:
    def __init__(self, name: str, description: str, status: str = "todo", assigned_to: str = None)
    def validate(self) -> bool
    def to_dict(self) -> Dict[str, Any]
```

## Agents

### BaseAgent
```python
class BaseAgent:
    def __init__(self, config: Config)
    def perform_task(self, task: Task, project: Project) -> None
    def validate_task(self, task: Task) -> bool
```

### UISpecialist
```python
class UISpecialist(BaseAgent):
    def generate_templates(self, feature: Feature) -> List[str]
    def validate_design(self, feature: Feature) -> bool
```

### Developer
```python
class Developer(BaseAgent):
    def implement_feature(self, feature: Feature) -> None
    def write_tests(self, feature: Feature) -> None
```

### QASpecialist
```python
class QASpecialist(BaseAgent):
    def run_tests(self, feature: Feature) -> bool
    def validate_feature(self, feature: Feature) -> bool
```

### ProductOwner
```python
class ProductOwner(BaseAgent):
    def validate_specification(self, project: Project) -> bool
    def prioritize_features(self, features: List[Feature]) -> List[Feature]
```

## Utils

### DependencyManager
```python
class DependencyManager:
    def __init__(self, config_path: str = "config/default.yaml")
    def check_dependencies(self) -> List[Tuple[str, str, str]]
    def get_update_commands(self) -> List[str]
    def validate_environment(self) -> bool
    def update_dependencies(self, dry_run: bool = True) -> List[str]
```

### SpecParser
```python
class SpecParser:
    @staticmethod
    def parse_spec_string(spec: str) -> Dict[str, Any]
    @staticmethod
    def parse_spec_file(file_path: str) -> Dict[str, Any]
    @staticmethod
    def validate_spec(spec: Dict[str, Any]) -> bool
```

## Generator

### CodeGenerator
```python
class CodeGenerator:
    def __init__(self, project: Project)
    def generate(self, output_dir: str) -> None
    def _load_template(self, tech: str, template_name: str) -> str
    def _render_template(self, template: str, **kwargs) -> str
```

## Configuration

### Config
```python
class Config:
    def __init__(self, config_path: str = "config/default.yaml")
    def load(self) -> Dict[str, Any]
    def save(self, config: Dict[str, Any]) -> None
    def validate(self) -> bool
```

## Example Usage

### Creating a Project
```python
from owera.models import Project, Feature, Task
from owera.agents import UISpecialist, Developer, QASpecialist, ProductOwner
from owera.generator import CodeGenerator

# Create project
project = Project(
    name="MyApp",
    tech_stack={"backend": "Python/Flask", "frontend": "HTML/CSS"},
    features=[],
    tasks=[]
)

# Add feature
feature = Feature(
    name="home_page",
    description="Home page with welcome message",
    constraints=["responsive_design"]
)
project.add_feature(feature)

# Initialize agents
ui_specialist = UISpecialist()
developer = Developer()
qa_specialist = QASpecialist()
product_owner = ProductOwner()

# Generate code
generator = CodeGenerator(project)
generator.generate("output/my_app")
```

### Managing Dependencies
```python
from owera.utils import DependencyManager

# Initialize dependency manager
dep_manager = DependencyManager()

# Check dependencies
conflicts = dep_manager.check_dependencies()
if conflicts:
    print("Dependency conflicts detected:")
    for pkg, installed, required in conflicts:
        print(f"  - {pkg}: installed {installed}, required {required}")

# Update dependencies
commands = dep_manager.update_dependencies(dry_run=True)
for cmd in commands:
    print(f"Would run: {cmd}")
```

### Parsing Specifications
```python
from owera.utils import SpecParser

# Parse specification string
spec = """
project:
  name: MyApp
  tech_stack:
    backend: Python/Flask
    frontend: HTML/CSS
features:
  - name: home_page
    description: Home page with welcome message
"""

parsed_spec = SpecParser.parse_spec_string(spec)
if SpecParser.validate_spec(parsed_spec):
    print("Specification is valid")
``` 