"""Code formatting utility for Owera CLI."""

import subprocess
from typing import Optional

def format_code(code: str, language: str) -> str:
    """Format code using appropriate formatter.
    
    Args:
        code: The code to format.
        language: The programming language of the code.
        
    Returns:
        Formatted code.
    """
    if language == "python":
        return _format_python(code)
    elif language == "javascript":
        return _format_javascript(code)
    elif language == "css":
        return _format_css(code)
    elif language == "html":
        return _format_html(code)
    else:
        return code

def _format_python(code: str) -> str:
    """Format Python code using black.
    
    Args:
        code: The Python code to format.
        
    Returns:
        Formatted Python code.
    """
    try:
        result = subprocess.run(
            ["black", "-"],
            input=code.encode(),
            capture_output=True,
            check=True
        )
        return result.stdout.decode()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return code

def _format_javascript(code: str) -> str:
    """Format JavaScript code using prettier.
    
    Args:
        code: The JavaScript code to format.
        
    Returns:
        Formatted JavaScript code.
    """
    try:
        result = subprocess.run(
            ["prettier", "--parser", "babel"],
            input=code.encode(),
            capture_output=True,
            check=True
        )
        return result.stdout.decode()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return code

def _format_css(code: str) -> str:
    """Format CSS code using prettier.
    
    Args:
        code: The CSS code to format.
        
    Returns:
        Formatted CSS code.
    """
    try:
        result = subprocess.run(
            ["prettier", "--parser", "css"],
            input=code.encode(),
            capture_output=True,
            check=True
        )
        return result.stdout.decode()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return code

def _format_html(code: str) -> str:
    """Format HTML code using prettier.
    
    Args:
        code: The HTML code to format.
        
    Returns:
        Formatted HTML code.
    """
    try:
        result = subprocess.run(
            ["prettier", "--parser", "html"],
            input=code.encode(),
            capture_output=True,
            check=True
        )
        return result.stdout.decode()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return code 