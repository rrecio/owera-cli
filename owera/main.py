"""Owera CLI main entry point."""

import os
import sys
from typing import Optional

import click
import typer
from rich.console import Console
from rich.logging import RichHandler

from owera.config import Config
from owera.models import Project
from owera.agents import UISpecialist, Developer, QASpecialist, ProductOwner
from owera.generator import CodeGenerator
from owera.utils import DependencyManager, SpecParser

# Initialize Typer app
app = typer.Typer(
    name="owera",
    help="A powerful command-line tool for generating and managing web applications using AI agents",
    add_completion=False,
)

# Initialize console
console = Console()

# Initialize configuration
config = Config()

def setup_logging():
    """Set up logging configuration."""
    import logging
    logging.basicConfig(
        level=config.get("logging.level", "INFO"),
        format=config.get("logging.format", "%(message)s"),
        handlers=[RichHandler(rich_tracebacks=True)]
    )

@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    config_file: Optional[str] = typer.Option(None, "--config", help="Path to config file"),
):
    """Owera CLI main entry point."""
    if debug:
        config.set("system.debug", True)
        config.set("system.log_level", "DEBUG")
    
    if config_file:
        config.load(config_file)
    
    setup_logging()

@app.command()
def create(
    name: str = typer.Argument(..., help="Project name"),
    backend: str = typer.Option(None, "--backend", help="Backend framework"),
    frontend: str = typer.Option(None, "--frontend", help="Frontend framework"),
):
    """Create a new project."""
    try:
        # Create project
        project = Project(
            name=name,
            tech_stack={
                "backend": backend or config.get("project.default_backend"),
                "frontend": frontend or config.get("project.default_frontend"),
            }
        )
        
        # Initialize agents
        ui_specialist = UISpecialist(config)
        developer = Developer(config)
        qa_specialist = QASpecialist(config)
        product_owner = ProductOwner(config)
        
        # Generate project
        generator = CodeGenerator(project)
        generator.generate(config.get("project.output_dir"))
        
        console.print(f"[green]Project {name} created successfully![/green]")
    
    except Exception as e:
        console.print(f"[red]Error creating project: {str(e)}[/red]")
        sys.exit(1)

@app.command()
def generate(
    spec: str = typer.Argument(..., help="Path to project specification file"),
    output: Optional[str] = typer.Option(None, "--output", help="Output directory"),
):
    """Generate a project from specification."""
    try:
        # Parse specification
        spec_data = SpecParser.parse_spec_file(spec)
        
        # Create project
        project = Project(
            name=spec_data["project"]["name"],
            tech_stack=spec_data["project"]["tech_stack"]
        )
        
        # Add features
        for feature_data in spec_data.get("features", []):
            project.add_feature(feature_data)
        
        # Add tasks
        for task_data in spec_data.get("tasks", []):
            project.add_task(task_data)
        
        # Generate project
        generator = CodeGenerator(project)
        generator.generate(output or config.get("project.output_dir"))
        
        console.print(f"[green]Project generated successfully![/green]")
    
    except Exception as e:
        console.print(f"[red]Error generating project: {str(e)}[/red]")
        sys.exit(1)

@app.command()
def feature(
    action: str = typer.Argument(..., help="Action to perform (add/list/update/remove)"),
    name: Optional[str] = typer.Argument(None, help="Feature name"),
    description: Optional[str] = typer.Option(None, "--description", help="Feature description"),
    constraints: Optional[list[str]] = typer.Option(None, "--constraints", help="Feature constraints"),
):
    """Manage project features."""
    try:
        if action == "add":
            if not name or not description:
                raise ValueError("Name and description are required")
            
            # Add feature
            project = Project.load()
            project.add_feature({
                "name": name,
                "description": description,
                "constraints": constraints or []
            })
            project.save()
            
            console.print(f"[green]Feature {name} added successfully![/green]")
        
        elif action == "list":
            # List features
            project = Project.load()
            for feature in project.features:
                console.print(f"[blue]{feature.name}[/blue]: {feature.description}")
        
        elif action == "update":
            if not name:
                raise ValueError("Feature name is required")
            
            # Update feature
            project = Project.load()
            feature = project.get_feature(name)
            if description:
                feature.description = description
            if constraints:
                feature.constraints = constraints
            project.save()
            
            console.print(f"[green]Feature {name} updated successfully![/green]")
        
        elif action == "remove":
            if not name:
                raise ValueError("Feature name is required")
            
            # Remove feature
            project = Project.load()
            project.remove_feature(name)
            project.save()
            
            console.print(f"[green]Feature {name} removed successfully![/green]")
        
        else:
            raise ValueError(f"Unknown action: {action}")
    
    except Exception as e:
        console.print(f"[red]Error managing features: {str(e)}[/red]")
        sys.exit(1)

@app.command()
def task(
    action: str = typer.Argument(..., help="Action to perform (create/list/update/remove)"),
    name: Optional[str] = typer.Argument(None, help="Task name"),
    description: Optional[str] = typer.Option(None, "--description", help="Task description"),
    status: Optional[str] = typer.Option(None, "--status", help="Task status"),
    assignee: Optional[str] = typer.Option(None, "--assignee", help="Task assignee"),
):
    """Manage project tasks."""
    try:
        if action == "create":
            if not name or not description:
                raise ValueError("Name and description are required")
            
            # Create task
            project = Project.load()
            project.add_task({
                "name": name,
                "description": description,
                "status": status or config.get("tasks.default_status"),
                "assigned_to": assignee
            })
            project.save()
            
            console.print(f"[green]Task {name} created successfully![/green]")
        
        elif action == "list":
            # List tasks
            project = Project.load()
            for task in project.tasks:
                console.print(f"[blue]{task.name}[/blue]: {task.description}")
        
        elif action == "update":
            if not name:
                raise ValueError("Task name is required")
            
            # Update task
            project = Project.load()
            task = project.get_task(name)
            if description:
                task.description = description
            if status:
                task.status = status
            if assignee:
                task.assigned_to = assignee
            project.save()
            
            console.print(f"[green]Task {name} updated successfully![/green]")
        
        elif action == "remove":
            if not name:
                raise ValueError("Task name is required")
            
            # Remove task
            project = Project.load()
            project.remove_task(name)
            project.save()
            
            console.print(f"[green]Task {name} removed successfully![/green]")
        
        else:
            raise ValueError(f"Unknown action: {action}")
    
    except Exception as e:
        console.print(f"[red]Error managing tasks: {str(e)}[/red]")
        sys.exit(1)

@app.command()
def check_deps():
    """Check project dependencies."""
    try:
        dep_manager = DependencyManager()
        conflicts = dep_manager.check_dependencies()
        
        if conflicts:
            console.print("[yellow]Dependency conflicts detected:[/yellow]")
            for pkg, installed, required in conflicts:
                console.print(f"  - {pkg}: installed {installed}, required {required}")
        else:
            console.print("[green]All dependencies are up to date![/green]")
    
    except Exception as e:
        console.print(f"[red]Error checking dependencies: {str(e)}[/red]")
        sys.exit(1)

@app.command()
def update_deps(
    dry_run: bool = typer.Option(True, "--no-dry-run", help="Actually update dependencies"),
):
    """Update project dependencies."""
    try:
        dep_manager = DependencyManager()
        commands = dep_manager.update_dependencies(dry_run)
        
        if dry_run:
            console.print("[yellow]Would run the following commands:[/yellow]")
        else:
            console.print("[green]Running the following commands:[/green]")
        
        for cmd in commands:
            console.print(f"  - {cmd}")
    
    except Exception as e:
        console.print(f"[red]Error updating dependencies: {str(e)}[/red]")
        sys.exit(1)

@app.command()
def validate(
    spec: Optional[str] = typer.Option(None, "--spec", help="Path to project specification file"),
    project: Optional[str] = typer.Option(None, "--project", help="Project directory"),
):
    """Validate project or specification."""
    try:
        if spec:
            # Validate specification
            spec_data = SpecParser.parse_spec_file(spec)
            if SpecParser.validate_spec(spec_data):
                console.print("[green]Specification is valid![/green]")
            else:
                console.print("[red]Specification is invalid![/red]")
                sys.exit(1)
        
        elif project:
            # Validate project
            project = Project.load(project)
            if project.validate():
                console.print("[green]Project is valid![/green]")
            else:
                console.print("[red]Project is invalid![/red]")
                sys.exit(1)
        
        else:
            raise ValueError("Either --spec or --project must be specified")
    
    except Exception as e:
        console.print(f"[red]Error validating: {str(e)}[/red]")
        sys.exit(1)

# Export the Typer app as the main function
owera = app

if __name__ == "__main__":
    app() 