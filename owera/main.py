import click
import os
import git
import logging
import json
from datetime import datetime
from tqdm import tqdm
import sys
from typing import Dict, Any, Optional

from .config import config
from .models.base import Project, Feature, Task, Issue
from .agents.ui_specialist import UISpecialist
from .agents.developer import Developer
from .agents.qa_specialist import QASpecialist
from .agents.product_owner import ProductOwner
from .agents.project_manager import ProjectManager
from .utils.spec_parser import parse_spec_string
from .utils.code_generator import generate_output

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s: %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('development.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

@click.command()
@click.option('--spec', default=None, help='Describe your app (e.g., "Build a blog with a home page")')
@click.option('--spec-file', type=click.Path(exists=True), default=None, help='Text file with app description')
@click.option('--output', required=True, help='Folder name for your app')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def owera(spec: Optional[str], spec_file: Optional[str], output: str, debug: bool) -> None:
    """Owera: Turns your app ideas into working software."""
    if spec and spec_file:
        raise click.UsageError("Use either --spec or --spec-file, not both.")
    if not spec and not spec_file:
        raise click.UsageError("Provide --spec or --spec-file.")
    
    if debug:
        config.DEBUG = True
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("Starting Owera to build your app")
    
    # Get specification
    spec_string = spec
    if spec_file:
        with open(spec_file, "r") as f:
            spec_string = f.read().strip()
    
    # Parse specification and create project
    specs = parse_spec_string(spec_string)
    project = Project(specs)
    
    # Initialize agents
    agents = {
        "UI Specialist": UISpecialist(),
        "Developer": Developer(),
        "QA Specialist": QASpecialist(),
        "Product Owner": ProductOwner(),
        "Project Manager": ProjectManager()
    }
    
    # Main development loop
    iteration = 0
    max_iterations = 100
    with tqdm(total=len(project.features) * 4, desc="Building Your App", unit="step") as pbar:
        while not project.is_complete() and iteration < max_iterations:
            iteration += 1
            logger.debug(f"Iteration {iteration}: {len(project.tasks)} tasks to process")
            
            # Plan tasks
            agents["Project Manager"].plan(project)
            
            # Process tasks
            tasks_to_process = [task for task in project.tasks if task.status == "todo"]
            for task in tasks_to_process:
                task.status = "in_progress"
                agents[task.assigned_to].perform_task(task, project)
                pbar.update(1)
            
            if not tasks_to_process:
                logger.warning("No tasks to process, but project not complete. Possible deadlock.")
                break
        
        if iteration >= max_iterations:
            logger.error("Reached maximum iterations. Possible infinite loop detected.")
    
    # Generate output
    try:
        generate_output(project, output)
        logger.info("\n=== Your App is Ready! ===")
        logger.info(f"App Folder: {output}")
        logger.info("What's Inside:")
        logger.info(f"- src/app.py: The main app code to run your website.")
        logger.info(f"- templates/: Designed pages for your app's features.")
        logger.info(f"- docs/README.md: Instructions to start your app.")
        logger.info(f"- logs/development.log: A record of how your app was built.")
        logger.info("Next Steps: Check the README.md for how to run your app!")
    except Exception as e:
        logger.error(f"Failed to generate output: {str(e)}")
        raise

if __name__ == "__main__":
    owera() 