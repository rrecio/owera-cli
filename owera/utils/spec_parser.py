import json
import re
import logging
import requests
import ollama
from typing import Dict, Any, List
from ..config import config

logger = logging.getLogger(__name__)

class ParsingError(Exception):
    """Raised when spec parsing fails."""
    pass

def parse_spec_string(spec_string: str) -> Dict[str, Any]:
    """Parse a specification string into a structured format."""
    logger.info("Parsing specification string")
    
    # Try JSON parsing first
    try:
        return _parse_json(spec_string)
    except (json.JSONDecodeError, KeyError, requests.exceptions.Timeout) as e:
        logger.error(f"JSON parsing failed: {str(e)}. Falling back to manual parsing.")
    
    # Fall back to manual parsing
    try:
        return _parse_manual(spec_string)
    except Exception as e:
        logger.error(f"Manual parsing failed: {str(e)}. Using default features.")
        return _get_default_spec()

def _parse_json(spec_string: str) -> Dict[str, Any]:
    """Parse specification using JSON format."""
    json_structure = (
        "{'project': {'name': 'AppName', 'tech_stack': {'backend': 'Python/Flask', 'frontend': 'HTML/CSS'}}, "
        "'features': [{'name': 'feature name', 'description': 'feature description', 'constraints': ['constraint1']}]}}"
    )
    
    prompt = (
        f"Parse this app description into JSON with the following structure: {json_structure} "
        f"Default to Python/Flask, HTML/CSS, SQLite, JWT auth if unspecified. Ensure valid JSON output with 'features' key. "
        f"If the description is unclear, include at least one feature (e.g., a home page). Description: {spec_string}"
    )
    
    logger.info("Sending request to Ollama for JSON parsing...")
    response = ollama.generate(
        model=config.MODEL_NAME,
        prompt=prompt,
        options={"timeout": config.TIMEOUT}
    )['response']
    
    logger.debug(f"Raw JSON parsing response: {response}")
    parsed = json.loads(response)
    
    # Validate and complete the parsed structure
    if "project" not in parsed:
        parsed["project"] = {}
    if "features" not in parsed or not parsed["features"]:
        parsed["features"] = [{"name": "home_page", "description": "A basic home page to display a welcome message"}]
    if "tech_stack" not in parsed["project"]:
        parsed["project"]["tech_stack"] = {"backend": "Python/Flask", "frontend": "HTML/CSS"}
    if "name" not in parsed["project"]:
        parsed["project"]["name"] = "SimpleApp"
    
    logger.info(f"Found {len(parsed['features'])} features to build.")
    return parsed

def _parse_manual(spec_string: str) -> Dict[str, Any]:
    """Parse specification using manual text analysis."""
    # Extract project name
    name_match = re.search(r"called\s+(\w+)", spec_string, re.IGNORECASE)
    project_name = name_match.group(1) if name_match else "SimpleApp"
    
    # Extract features and constraints
    feature_phrases = []
    constraints = []
    current_phrase = spec_string.lower()
    
    # Split on feature indicators
    split_points = [m.start() for m in re.finditer(r'(?:with a|and a|and)\s+', current_phrase)]
    split_points.append(len(current_phrase))
    
    start = 0
    for end in split_points:
        phrase = current_phrase[start:end].strip()
        if phrase:
            feature_phrases.append(phrase)
        start = end
    
    features = []
    for phrase in feature_phrases:
        # Skip project description
        if "build an" in phrase or "called" in phrase:
            continue
        
        # Extract constraints
        if "design" in phrase or "use a database" in phrase or "secure login" in phrase:
            constraints.append(phrase)
            continue
        
        # Clean up the phrase for feature extraction
        phrase = phrase.replace("with a", "").replace("and a", "").replace("and", "").strip()
        parts = phrase.split(" to ")
        
        if len(parts) >= 2:
            name = parts[0].strip()
            description = " to ".join(parts[1:]).strip()
        else:
            name = phrase.strip()
            description = f"Implement {name}"
        
        # Normalize feature name for Flask routes
        name = name.replace(" ", "_")
        features.append({
            "name": name,
            "description": description,
            "constraints": constraints
        })
    
    if not features:
        features = [{"name": "home_page", "description": "A basic home page to display a welcome message"}]
    
    parsed = {
        "project": {
            "name": project_name,
            "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"},
            "features": features
        }
    }
    
    logger.info(f"Manually parsed {len(features)} features: {features}")
    return parsed

def _get_default_spec() -> Dict[str, Any]:
    """Return a default specification."""
    return {
        "project": {
            "name": "SimpleApp",
            "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"},
            "features": [{"name": "home_page", "description": "A basic home page to display a welcome message"}]
        }
    } 