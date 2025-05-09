# Owera CLI (⚠️currently in alpha)

Owera CLI is an AI-powered web application development tool that turns your app ideas into working software. It uses a team of specialized AI agents to design, implement, test, and validate your web application features.

https://owera.ai

## Features

- **AI-Powered Development**: Uses multiple specialized AI agents to handle different aspects of development
- **Modern Tech Stack**: Built with Python/Flask, SQLAlchemy, and Tailwind CSS
- **Smart Code Generation**: Automatically generates clean, modular code with proper error handling
- **Project Management**: Tracks features, tasks, and issues throughout development
- **Quality Assurance**: Includes built-in testing and validation
- **Version Control**: Automatically initializes Git repository
- **Documentation**: Generates comprehensive documentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rrecio/owera-cli.git
cd owera-cli
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Basic Usage

```bash
owera --spec "Build a blog with a home page" --output my-blog
```

### Advanced Usage

```bash
# Using a specification file
owera --spec-file app-spec.txt --output my-app

# Enable debug mode
owera --spec "Build a todo app" --output my-todo --debug
```

### Specification Format

You can provide your app specification in two ways:

1. **Direct String**:
```bash
owera --spec "Build a course platform with user authentication and course listing"
```

2. **JSON File**:
```json
{
  "project": {
    "name": "CoursePlatform",
    "tech_stack": {
      "backend": "Python/Flask",
      "frontend": "HTML/CSS"
    }
  },
  "features": [
    {
      "name": "user_auth",
      "description": "User authentication system",
      "constraints": ["secure login"]
    },
    {
      "name": "course_list",
      "description": "List available courses",
      "constraints": ["responsive design"]
    }
  ]
}
```

#### Specification Details

The specification can include the following components:

1. **Project Information**:
   - `name`: The name of your application
   - `tech_stack`: Technology choices for backend and frontend

2. **Features**:
   - `name`: Feature identifier (used for routes and templates)
   - `description`: Detailed description of the feature
   - `constraints`: List of requirements and constraints

3. **Common Constraints**:
   - `secure login`: Adds authentication and authorization
   - `responsive design`: Ensures mobile-friendly UI
   - `use a database`: Implements data persistence
   - `real-time updates`: Adds WebSocket support
   - `file upload`: Enables file handling
   - `search functionality`: Implements search features
   - `pagination`: Adds paginated results
   - `sorting`: Enables data sorting
   - `filtering`: Implements data filtering
   - `export data`: Adds data export capabilities

#### Example Specifications

1. **Simple Blog**:
```json
{
  "project": {
    "name": "SimpleBlog",
    "tech_stack": {
      "backend": "Python/Flask",
      "frontend": "HTML/CSS"
    }
  },
  "features": [
    {
      "name": "home_page",
      "description": "Display recent blog posts",
      "constraints": ["responsive design", "pagination"]
    },
    {
      "name": "post_detail",
      "description": "Show full blog post with comments",
      "constraints": ["responsive design"]
    },
    {
      "name": "create_post",
      "description": "Create new blog posts",
      "constraints": ["secure login", "file upload"]
    }
  ]
}
```

2. **E-commerce Platform**:
```json
{
  "project": {
    "name": "ShopEasy",
    "tech_stack": {
      "backend": "Python/Flask",
      "frontend": "HTML/CSS"
    }
  },
  "features": [
    {
      "name": "product_catalog",
      "description": "Browse products with filters",
      "constraints": ["responsive design", "filtering", "sorting", "pagination"]
    },
    {
      "name": "shopping_cart",
      "description": "Manage shopping cart",
      "constraints": ["secure login", "real-time updates"]
    },
    {
      "name": "checkout",
      "description": "Process orders",
      "constraints": ["secure login", "use a database"]
    }
  ]
}
```

3. **Task Management**:
```json
{
  "project": {
    "name": "TaskMaster",
    "tech_stack": {
      "backend": "Python/Flask",
      "frontend": "HTML/CSS"
    }
  },
  "features": [
    {
      "name": "task_list",
      "description": "View and manage tasks",
      "constraints": ["responsive design", "sorting", "filtering"]
    },
    {
      "name": "create_task",
      "description": "Create new tasks",
      "constraints": ["secure login", "file upload"]
    },
    {
      "name": "task_analytics",
      "description": "View task statistics",
      "constraints": ["secure login", "export data"]
    }
  ]
}
```

#### Feature Types and Best Practices

1. **Common Feature Types**:
   - **Authentication**: User registration, login, and profile management
   - **Content Management**: Create, read, update, and delete operations
   - **Search and Filter**: Advanced search and filtering capabilities
   - **File Handling**: Upload, download, and manage files
   - **Analytics**: Data visualization and reporting
   - **Notifications**: Real-time updates and alerts
   - **API Integration**: Connect with external services
   - **Export/Import**: Data import and export functionality

2. **Naming Conventions**:
   - Use lowercase with underscores for feature names
   - Keep names descriptive but concise
   - Use consistent naming patterns across features
   - Examples: `user_profile`, `product_catalog`, `order_history`

3. **Constraint Best Practices**:
   - Be specific about requirements
   - Include security constraints when needed
   - Specify UI/UX requirements
   - Consider performance implications
   - Include data handling requirements

4. **Description Guidelines**:
   - Be clear and concise
   - Include main functionality
   - Specify user interactions
   - Mention any special requirements
   - Include expected outcomes

#### Advanced Configuration

You can customize the behavior of features using additional configuration:

```json
{
  "project": {
    "name": "AdvancedApp",
    "tech_stack": {
      "backend": "Python/Flask",
      "frontend": "HTML/CSS"
    },
    "config": {
      "auth": {
        "require_email_verification": true,
        "password_min_length": 8
      },
      "database": {
        "use_migrations": true,
        "backup_enabled": true
      },
      "security": {
        "rate_limiting": true,
        "cors_enabled": true
      }
    }
  },
  "features": [
    {
      "name": "user_management",
      "description": "Comprehensive user management system",
      "constraints": ["secure login", "use a database"],
      "config": {
        "roles": ["admin", "user", "guest"],
        "permissions": ["read", "write", "delete"]
      }
    }
  ]
}
```

## Project Structure

The generated application will have the following structure:

```
my-app/
├── src/
│   └── app.py           # Main application code
├── templates/           # HTML templates
├── docs/
│   └── README.md       # Project documentation
└── logs/
    └── development.log # Development history
```

## AI Agents

Owera uses several specialized AI agents:

1. **UI Specialist**: Generates responsive HTML templates using Tailwind CSS
2. **Developer**: Implements backend functionality with Flask
3. **QA Specialist**: Tests features and identifies issues
4. **Product Owner**: Validates features against specifications
5. **Project Manager**: Coordinates tasks and manages the development process

## Configuration

Configure Owera using environment variables:

```bash
export OWERA_SECRET_KEY="your-secret-key"
export OWERA_DATABASE_URI="sqlite:///database.db"
export OWERA_MODEL="qwen2.5-coder:7b"
export OWERA_TIMEOUT="60"
export OWERA_DEBUG="False"
export OWERA_LOG_LEVEL="INFO"
```

## Dependencies

- Python 3.8+
- Flask 3.0.2+
- Flask-SQLAlchemy 3.1.1+
- PyJWT 2.8.0+
- Python-dotenv 1.0.1+
- Requests 2.31.0+
- GitPython 3.1.42+
- Click 8.1.7+
- tqdm 4.66.2+
- Ollama 0.1.6+

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Specification Parsing Errors**:
   - Ensure JSON is properly formatted
   - Check for missing required fields
   - Verify feature names follow naming conventions
   - Validate constraint names

2. **Code Generation Issues**:
   - Check if all required dependencies are installed
   - Verify environment variables are set correctly
   - Ensure sufficient disk space for generated files
   - Check write permissions in output directory

3. **Template Generation Problems**:
   - Verify feature names match template names
   - Check for conflicting route names
   - Ensure proper template inheritance
   - Validate template syntax

4. **Database Issues**:
   - Check database connection string
   - Verify database permissions
   - Ensure models are properly defined
   - Check for migration conflicts

### Debug Mode

Enable debug mode for detailed logging:

```bash
export OWERA_DEBUG="True"
export OWERA_LOG_LEVEL="DEBUG"
owera --spec "..." --output my-app --debug
```

### Logging

Logs are stored in `logs/development.log` and include:
- Specification parsing details
- Code generation steps
- Agent activities
- Error messages and stack traces
- Performance metrics

## Support

For support, email info@owera.ai or open an issue in the GitHub repository. 
