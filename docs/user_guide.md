# Owera CLI User Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Project Generation](#project-generation)
4. [Feature Management](#feature-management)
5. [Task Management](#task-management)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Basic Installation
```bash
# Install from PyPI
pip install owera-cli

# Install with development dependencies
pip install "owera-cli[dev]"
```

### Development Installation
```bash
# Clone repository
git clone https://github.com/yourusername/owera-cli.git
cd owera-cli

# Install in editable mode
pip install -e ".[dev]"
```

## Quick Start

### Create a New Project
```bash
# Create a new project
owera create my_project

# Create with specific tech stack
owera create my_project --backend python/flask --frontend html/css
```

### Project Structure
```
my_project/
├── app.py              # Main application file
├── models.py           # Data models
├── routes.py           # Route definitions
├── templates/          # HTML templates
├── static/             # Static files
└── tests/              # Test files
```

## Project Generation

### Basic Generation
```bash
# Generate project from specification
owera generate --spec project.yaml

# Generate with custom output directory
owera generate --spec project.yaml --output custom_dir
```

### Specification Format
```yaml
project:
  name: MyApp
  tech_stack:
    backend: Python/Flask
    frontend: HTML/CSS
features:
  - name: home_page
    description: Home page with welcome message
  - name: user_auth
    description: User authentication system
tasks:
  - name: setup_database
    description: Set up SQLite database
  - name: create_templates
    description: Create HTML templates
```

## Feature Management

### Adding Features
```bash
# Add a new feature
owera feature add home_page "Home page with welcome message"

# Add feature with constraints
owera feature add user_auth "User authentication" --constraints "secure" "responsive"
```

### Managing Features
```bash
# List all features
owera feature list

# Update feature
owera feature update home_page --description "Updated home page"

# Remove feature
owera feature remove home_page
```

## Task Management

### Creating Tasks
```bash
# Create a new task
owera task create setup_database "Set up SQLite database"

# Create task with assignee
owera task create create_templates "Create HTML templates" --assignee developer
```

### Task Operations
```bash
# List all tasks
owera task list

# Update task status
owera task update setup_database --status completed

# Remove task
owera task remove setup_database
```

## Configuration

### Configuration File
```yaml
# config.yaml
defaults:
  backend: Python/Flask
  frontend: HTML/CSS
  output_dir: ./output

templates:
  backend: templates/python/flask
  frontend: templates/html/css

logging:
  level: INFO
  file: owera.log
```

### Environment Variables
```bash
# Set configuration file location
export OWERA_CONFIG=/path/to/config.yaml

# Set log level
export OWERA_LOG_LEVEL=DEBUG
```

## Troubleshooting

### Common Issues

#### Project Generation Fails
```bash
# Check specification file
owera validate --spec project.yaml

# Check dependencies
owera check-deps

# Enable debug logging
owera generate --spec project.yaml --log-level DEBUG
```

#### Feature Addition Fails
```bash
# Validate feature specification
owera feature validate home_page

# Check project status
owera status

# View detailed logs
tail -f owera.log
```

### Debug Mode
```bash
# Enable debug mode
owera --debug generate --spec project.yaml

# Show detailed output
owera --verbose feature list
```

### Getting Help
```bash
# Show general help
owera --help

# Show command help
owera generate --help

# Show version
owera --version
```

## Best Practices

### Project Organization
1. Use meaningful project names
2. Keep specifications in version control
3. Document custom templates
4. Regular project validation

### Feature Development
1. Start with clear requirements
2. Use consistent naming
3. Document constraints
4. Regular feature validation

### Task Management
1. Break down large tasks
2. Set clear deadlines
3. Regular status updates
4. Document dependencies

## Examples

### Complete Project Generation
```bash
# Create specification
cat > project.yaml << EOF
project:
  name: MyApp
  tech_stack:
    backend: Python/Flask
    frontend: HTML/CSS
features:
  - name: home_page
    description: Home page with welcome message
  - name: user_auth
    description: User authentication system
tasks:
  - name: setup_database
    description: Set up SQLite database
EOF

# Generate project
owera generate --spec project.yaml

# Add feature
owera feature add contact_form "Contact form with validation"

# Create task
owera task create implement_form "Implement contact form" --assignee developer
```

### Custom Template Usage
```bash
# Create custom template
mkdir -p templates/custom
cp template.html templates/custom/

# Use custom template
owera generate --spec project.yaml --template-dir templates/custom
```

### Project Validation
```bash
# Validate entire project
owera validate --project my_project

# Validate specific feature
owera validate --feature user_auth

# Validate with custom rules
owera validate --rules custom_rules.yaml
``` 