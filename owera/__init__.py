"""
Owera CLI - A powerful command-line tool for generating and managing web applications.
"""

__version__ = "0.1.0"
__author__ = "Owera Team"
__email__ = "team@owera.ai"

from .config import Config
from .models import Project, Feature, Task
from .agents import UISpecialist, Developer, QASpecialist, ProductOwner
from .generator import CodeGenerator
from .utils import DependencyManager, SpecParser

__all__ = [
    'Config',
    'Project',
    'Feature',
    'Task',
    'UISpecialist',
    'Developer',
    'QASpecialist',
    'ProductOwner',
    'CodeGenerator',
    'DependencyManager',
    'SpecParser'
] 