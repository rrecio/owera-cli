"""Dependency manager for Owera CLI."""

import os
import subprocess
from typing import List, Tuple, Dict, Optional
import pkg_resources
import logging

class DependencyManager:
    """Dependency manager for handling project dependencies."""
    
    def __init__(self, requirements_file: Optional[str] = None):
        """Initialize dependency manager."""
        self.requirements_file = requirements_file or "requirements.txt"
    
    def check_dependencies(self) -> List[Tuple[str, str, str]]:
        """Check for dependency conflicts.
        
        Returns:
            List of tuples containing (package_name, installed_version, required_version)
        """
        conflicts = []
        
        try:
            with open(self.requirements_file, 'r') as f:
                requirements = f.readlines()
            
            for req in requirements:
                req = req.strip()
                if not req or req.startswith('#'):
                    continue
                
                try:
                    pkg_resources.require(req)
                except pkg_resources.VersionConflict as e:
                    conflicts.append((
                        e.req.name,
                        e.dist.version,
                        str(e.req.specifier)
                    ))
                except pkg_resources.DistributionNotFound:
                    conflicts.append((
                        req.split('==')[0],
                        "not installed",
                        req
                    ))
        
        except FileNotFoundError:
            logging.warning(f"Requirements file not found: {self.requirements_file}")
        
        return conflicts
    
    def update_dependencies(self, dry_run: bool = True) -> List[str]:
        """Update project dependencies.
        
        Args:
            dry_run: If True, only return commands that would be run
            
        Returns:
            List of commands that would be run
        """
        commands = []
        
        try:
            with open(self.requirements_file, 'r') as f:
                requirements = f.readlines()
            
            for req in requirements:
                req = req.strip()
                if not req or req.startswith('#'):
                    continue
                
                package = req.split('==')[0]
                cmd = f"pip install --upgrade {req}"
                commands.append(cmd)
                
                if not dry_run:
                    try:
                        subprocess.run(cmd.split(), check=True)
                    except subprocess.CalledProcessError as e:
                        logging.error(f"Error updating {package}: {e}")
        
        except FileNotFoundError:
            logging.warning(f"Requirements file not found: {self.requirements_file}")
        
        return commands
    
    def install_dependencies(self, dry_run: bool = True) -> List[str]:
        """Install project dependencies.
        
        Args:
            dry_run: If True, only return commands that would be run
            
        Returns:
            List of commands that would be run
        """
        commands = []
        
        try:
            cmd = f"pip install -r {self.requirements_file}"
            commands.append(cmd)
            
            if not dry_run:
                try:
                    subprocess.run(cmd.split(), check=True)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error installing dependencies: {e}")
        
        except FileNotFoundError:
            logging.warning(f"Requirements file not found: {self.requirements_file}")
        
        return commands
    
    def add_dependency(self, package: str, version: Optional[str] = None) -> None:
        """Add a new dependency to requirements.txt.
        
        Args:
            package: Package name
            version: Optional version specifier
        """
        try:
            with open(self.requirements_file, 'a') as f:
                if version:
                    f.write(f"{package}=={version}\n")
                else:
                    f.write(f"{package}\n")
        
        except FileNotFoundError:
            logging.warning(f"Requirements file not found: {self.requirements_file}")
            with open(self.requirements_file, 'w') as f:
                if version:
                    f.write(f"{package}=={version}\n")
                else:
                    f.write(f"{package}\n")
    
    def remove_dependency(self, package: str) -> None:
        """Remove a dependency from requirements.txt.
        
        Args:
            package: Package name
        """
        try:
            with open(self.requirements_file, 'r') as f:
                requirements = f.readlines()
            
            with open(self.requirements_file, 'w') as f:
                for req in requirements:
                    if not req.startswith(package):
                        f.write(req)
        
        except FileNotFoundError:
            logging.warning(f"Requirements file not found: {self.requirements_file}")
    
    def get_installed_dependencies(self) -> Dict[str, str]:
        """Get currently installed dependencies.
        
        Returns:
            Dictionary mapping package names to versions
        """
        return {
            pkg.key: pkg.version
            for pkg in pkg_resources.working_set
        } 