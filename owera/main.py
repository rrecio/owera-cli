import os
import logging
import click
from tqdm import tqdm
from owera.utils.spec_parser import parse_spec_string
from owera.utils.code_generator import generate_output
from owera.models.base import Project
from owera.agents import (
    UISpecialist,
    Developer,
    QASpecialist,
    ProductOwner,
    ProjectManager
)
from owera.config import Config

config = Config()

def setup_logging(debug: bool) -> None:
    """Set up logging configuration."""
    log_level = "DEBUG" if debug else config.LOG_LEVEL
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler("logs/development.log"),
            logging.StreamHandler()
        ]
    )

@click.command()
@click.option("--spec", help="App specification as a JSON string")
@click.option("--spec-file", help="Path to app specification file")
@click.option("--output", default="output", help="Output folder name")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def owera(spec: str, spec_file: str, output: str, debug: bool) -> None:
    """Build a web application from a specification."""
    # Set up logging
    setup_logging(debug)
    logger = logging.getLogger(__name__)
    
    try:
        # Get specification
        if not spec and not spec_file:
            raise click.UsageError("Either --spec or --spec-file must be provided")
        
        if spec_file:
            with open(spec_file) as f:
                spec = f.read()
        
        # Parse specification
        spec_data = parse_spec_string(spec)
        project = Project(spec_data)

        # Initialize agents
        ui_specialist = UISpecialist()
        developer = Developer()
        qa_specialist = QASpecialist()
        product_owner = ProductOwner()
        project_manager = ProjectManager()

        # Main development loop
        max_iterations = config.MAX_ITERATIONS
        with tqdm(total=max_iterations, desc="Building app") as pbar:
            for i in range(max_iterations):
                # Plan tasks
                project_manager.plan(project)
                if not project.tasks:
                    logger.info("No more tasks to process")
                    break

                # Process tasks
                for task in project.tasks:
                    if task.status != "todo":
                        continue

                    agent = {
                        "UI Specialist": ui_specialist,
                        "Developer": developer,
                        "QA Specialist": qa_specialist,
                        "Product Owner": product_owner
                    }.get(task.assigned_to)

                    if agent:
                        agent.perform_task(task, project)

                pbar.update(1)
                if i == max_iterations - 1:
                    logger.warning("Reached maximum iterations")

        # Generate output
        generate_output(project, output)
        logger.info(f"App generated successfully in {output}/")

    except Exception as e:
        logger.error(f"Failed to build app: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == "__main__":
    owera() 