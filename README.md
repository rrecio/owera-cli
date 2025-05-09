# Owera CLI

Owera CLI is an AI-powered web application development tool that turns your app ideas into working software. It uses a team of specialized AI agents to design, implement, test, and validate your web application features.

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

## Support

For support, email info@owera.ai or open an issue in the GitHub repository. 