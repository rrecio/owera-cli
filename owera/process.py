"""Process automation module for Owera CLI."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from owera.models.base import Project, Feature, Task, SprintPlan, Progress, SprintReview
from owera.agents.base import BaseAgent

class ProcessManager:
    """Manages the Agile development process automation."""
    
    def __init__(self):
        """Initialize the process manager."""
        self.sprint_duration = timedelta(days=14)  # 2-week sprints
    
    def plan_sprint(self, project: Project) -> SprintPlan:
        """Create a sprint plan for the project.
        
        Args:
            project: The project to plan the sprint for.
            
        Returns:
            A SprintPlan object containing the planned tasks.
            
        Raises:
            ValueError: If the project is invalid or has no features.
        """
        if not project.features:
            raise ValueError("Project must have at least one feature")
        
        # Create tasks for each feature
        tasks = []
        for feature in project.features:
            # Planning tasks
            tasks.append(Task(
                description=f"Define requirements for {feature.name}",
                feature=feature,
                status="planned"
            ))
            
            # Design tasks
            tasks.append(Task(
                description=f"Design {feature.name} interface",
                feature=feature,
                status="planned"
            ))
            tasks.append(Task(
                description=f"Optimize {feature.name} user experience",
                feature=feature,
                status="planned"
            ))
            
            # Development tasks
            tasks.append(Task(
                description=f"Implement {feature.name} functionality",
                feature=feature,
                status="planned"
            ))
            
            # Testing tasks
            tasks.append(Task(
                description=f"Test {feature.name} implementation",
                feature=feature,
                status="planned"
            ))
        
        # Create sprint plan
        return SprintPlan(
            tasks=tasks,
            start_date=datetime.now(),
            end_date=datetime.now() + self.sprint_duration
        )
    
    def assign_tasks(self, tasks: List[Task], agents: Dict[str, BaseAgent]) -> Dict[Task, BaseAgent]:
        """Assign tasks to appropriate agents.
        
        Args:
            tasks: List of tasks to assign.
            agents: Dictionary of available agents.
            
        Returns:
            Dictionary mapping tasks to assigned agents.
            
        Raises:
            ValueError: If there are no tasks or agents.
        """
        if not tasks:
            raise ValueError("No tasks to assign")
        if not agents:
            raise ValueError("No agents available")
        
        assignments = {}
        for task in tasks:
            # Determine appropriate agent based on task description
            if "requirements" in task.description.lower():
                agent = agents["po"]
            elif "design" in task.description.lower():
                agent = agents["ui"]
            elif "optimize" in task.description.lower():
                agent = agents["ux"]
            elif "implement" in task.description.lower():
                agent = agents["dev"]
            elif "test" in task.description.lower():
                agent = agents["qa"]
            else:
                agent = agents["dev"]  # Default to developer
            
            assignments[task] = agent
        
        return assignments
    
    def track_progress(self, sprint_plan: SprintPlan, assignments: Dict[Task, BaseAgent]) -> Progress:
        """Track the progress of the sprint.
        
        Args:
            sprint_plan: The current sprint plan.
            assignments: Dictionary of task assignments.
            
        Returns:
            A Progress object containing progress information.
            
        Raises:
            ValueError: If the sprint plan is invalid.
        """
        if not sprint_plan.tasks:
            raise ValueError("Sprint plan has no tasks")
        
        completed_tasks = [task for task in sprint_plan.tasks if task.status == "completed"]
        remaining_tasks = [task for task in sprint_plan.tasks if task.status != "completed"]
        
        completion_percentage = (len(completed_tasks) / len(sprint_plan.tasks)) * 100
        
        return Progress(
            completed_tasks=completed_tasks,
            remaining_tasks=remaining_tasks,
            completion_percentage=completion_percentage
        )
    
    def review_sprint(self, sprint_plan: SprintPlan, assignments: Dict[Task, BaseAgent]) -> SprintReview:
        """Review the completed sprint.
        
        Args:
            sprint_plan: The completed sprint plan.
            assignments: Dictionary of task assignments.
            
        Returns:
            A SprintReview object containing sprint review information.
        """
        # Get completed and remaining features
        completed_features = set()
        remaining_features = set()
        
        for task in sprint_plan.tasks:
            if task.status == "completed":
                completed_features.add(task.feature)
            else:
                remaining_features.add(task.feature)
        
        # Calculate velocity (completed tasks per day)
        days_elapsed = (datetime.now() - sprint_plan.start_date).days
        velocity = len([t for t in sprint_plan.tasks if t.status == "completed"]) / max(days_elapsed, 1)
        
        # Generate retrospective
        retrospective = self._generate_retrospective(sprint_plan, assignments)
        
        return SprintReview(
            completed_features=list(completed_features),
            remaining_features=list(remaining_features),
            velocity=velocity,
            retrospective=retrospective
        )
    
    def execute_tasks_concurrently(self, assignments: Dict[Task, BaseAgent], project: Project) -> List[Task]:
        """Execute tasks concurrently using thread pool.
        
        Args:
            assignments: Dictionary of task assignments.
            project: The project being worked on.
            
        Returns:
            List of completed tasks.
        """
        results = []
        with ThreadPoolExecutor() as executor:
            # Submit tasks to thread pool
            future_to_task = {
                executor.submit(agent.perform_task, task, project): task
                for task, agent in assignments.items()
            }
            
            # Process completed tasks
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    task.status = "error"
                    task.error = str(e)
                    results.append(task)
        
        return results
    
    def _generate_retrospective(self, sprint_plan: SprintPlan, assignments: Dict[Task, BaseAgent]) -> str:
        """Generate sprint retrospective.
        
        Args:
            sprint_plan: The completed sprint plan.
            assignments: Dictionary of task assignments.
            
        Returns:
            A string containing the sprint retrospective.
        """
        # Calculate metrics
        total_tasks = len(sprint_plan.tasks)
        completed_tasks = len([t for t in sprint_plan.tasks if t.status == "completed"])
        error_tasks = len([t for t in sprint_plan.tasks if t.status == "error"])
        
        # Generate retrospective
        retrospective = f"Sprint Retrospective:\n"
        retrospective += f"- Total Tasks: {total_tasks}\n"
        retrospective += f"- Completed Tasks: {completed_tasks}\n"
        retrospective += f"- Error Tasks: {error_tasks}\n"
        
        if error_tasks > 0:
            retrospective += "\nAreas for Improvement:\n"
            for task in sprint_plan.tasks:
                if task.status == "error":
                    retrospective += f"- {task.description}: {task.error}\n"
        
        return retrospective 