import json
import re
import logging
from typing import Dict, Any
from owera.config import Config

config = Config()
logger = logging.getLogger(__name__)

class ParsingError(Exception):
    """Raised when parsing fails."""
    pass

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