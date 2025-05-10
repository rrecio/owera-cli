"""Specification parser for Owera CLI."""

import os
from typing import Dict, Any, Optional
import yaml
import json
import logging
import re
from owera.config import Config

config = Config()
logger = logging.getLogger(__name__)

class ParsingError(Exception):
    """Raised when parsing fails."""
    pass

class SpecParser:
    """Parser for project specification files."""
    
    @staticmethod
    def parse_spec_file(file_path: str) -> Dict[str, Any]:
        """Parse a project specification file.
        
        Args:
            file_path: Path to specification file
            
        Returns:
            Dictionary containing parsed specification
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Specification file not found: {file_path}")
        
        _, ext = os.path.splitext(file_path)
        
        try:
            with open(file_path, 'r') as f:
                if ext.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(f)
                elif ext.lower() == '.json':
                    return json.load(f)
                else:
                    raise ValueError(f"Unsupported file format: {ext}")
        
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing specification file: {e}")
    
    @staticmethod
    def validate_spec(spec: Dict[str, Any]) -> bool:
        """Validate a project specification.
        
        Args:
            spec: Project specification dictionary
            
        Returns:
            True if specification is valid
        """
        required_fields = ['project']
        for field in required_fields:
            if field not in spec:
                raise ValueError(f"Missing required field: {field}")
        
        project = spec['project']
        required_project_fields = ['name', 'tech_stack']
        for field in required_project_fields:
            if field not in project:
                raise ValueError(f"Missing required project field: {field}")
        
        tech_stack = project['tech_stack']
        required_tech_fields = ['backend', 'frontend']
        for field in required_tech_fields:
            if field not in tech_stack:
                raise ValueError(f"Missing required tech stack field: {field}")
        
        # Validate features if present
        if 'features' in spec:
            for feature in spec['features']:
                required_feature_fields = ['name', 'description']
                for field in required_feature_fields:
                    if field not in feature:
                        raise ValueError(f"Missing required feature field: {field}")
        
        # Validate tasks if present
        if 'tasks' in spec:
            for task in spec['tasks']:
                required_task_fields = ['name', 'description']
                for field in required_task_fields:
                    if field not in task:
                        raise ValueError(f"Missing required task field: {field}")
        
        return True
    
    @staticmethod
    def write_spec_file(spec: Dict[str, Any], file_path: str) -> None:
        """Write a project specification to file.
        
        Args:
            spec: Project specification dictionary
            file_path: Path to write specification file
        """
        _, ext = os.path.splitext(file_path)
        
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                if ext.lower() in ['.yaml', '.yml']:
                    yaml.dump(spec, f, default_flow_style=False)
                elif ext.lower() == '.json':
                    json.dump(spec, f, indent=2)
                else:
                    raise ValueError(f"Unsupported file format: {ext}")
        
        except Exception as e:
            raise ValueError(f"Error writing specification file: {e}")
    
    @staticmethod
    def merge_specs(specs: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple project specifications.
        
        Args:
            specs: List of project specification dictionaries
            
        Returns:
            Merged specification dictionary
        """
        if not specs:
            raise ValueError("No specifications to merge")
        
        merged = specs[0].copy()
        
        for spec in specs[1:]:
            # Merge project
            if 'project' in spec:
                merged['project'].update(spec['project'])
            
            # Merge features
            if 'features' in spec:
                if 'features' not in merged:
                    merged['features'] = []
                merged['features'].extend(spec['features'])
            
            # Merge tasks
            if 'tasks' in spec:
                if 'tasks' not in merged:
                    merged['tasks'] = []
                merged['tasks'].extend(spec['tasks'])
        
        return merged

def parse_spec_string(spec_string: str) -> Dict[str, Any]:
    """Parse a specification string into a structured format."""
    try:
        # First try to parse as JSON
        return json.loads(spec_string)
    except json.JSONDecodeError:
        # If not valid JSON, try manual parsing
        try:
            return _parse_manual(spec_string)
        except Exception as e:
            logger.error(f"Failed to parse specification: {e}")
            raise ParsingError(f"Failed to parse specification: {e}")

def _parse_manual(spec_string: str) -> Dict[str, Any]:
    """Parse specification using manual parsing."""
    # Extract project name
    project_name = "SimpleApp"
    name_match = re.search(r"build\s+(?:a\s+)?(\w+)", spec_string.lower())
    if name_match:
        project_name = name_match.group(1).title()

    # Extract features
    features = []
    feature_matches = re.findall(r"(?:with|and)\s+(?:a\s+)?(\w+(?:\s+\w+)*)\s+(?:page|feature)", spec_string.lower())
    
    if not feature_matches:
        features.append({
            "name": "home_page",
            "description": "Home page with welcome message",
            "constraints": []
        })
    else:
        for match in feature_matches:
            name = match.replace(" ", "_").lower()
            features.append({
                "name": name,
                "description": f"{match.title()} page",
                "constraints": []
            })

        # Add home page if not already included
        if not any(f["name"] == "home_page" for f in features):
            features.append({
                "name": "home_page",
                "description": "Home page with welcome message",
                "constraints": []
            })

    return {
        "project": {
            "name": project_name,
            "tech_stack": {
                "backend": "Python/Flask",
                "frontend": "HTML/CSS"
            }
        },
        "features": features
    }

def _get_default_spec() -> Dict[str, Any]:
    """Get default specification."""
    return {
        "project": {
            "name": "SimpleApp",
            "tech_stack": {
                "backend": "Python/Flask",
                "frontend": "HTML/CSS"
            }
        },
        "features": [
            {
                "name": "home_page",
                "description": "Home page with welcome message",
                "constraints": []
            }
        ]
    } 