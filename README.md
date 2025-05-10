# Owera CLI

Owera CLI is an AI-powered web application development tool that automates the creation of custom software projects. It takes a YAML specification file as input and generates a complete, production-ready web application.

## Features

- 🚀 Automated project generation from YAML specifications
- 🤖 AI-powered development with specialized agents
- 🎨 Multiple tech stack support (Flask, Django, React, etc.)
- 📦 Dependency management and version control
- 🧪 Comprehensive testing infrastructure
- 📝 Detailed documentation generation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/owera-cli.git
cd owera-cli

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Quick Start

1. Create a project specification file (e.g., `project.yaml`):
```yaml
project:
  name: MyApp
  tech_stack:
    backend: Python/Flask
    frontend: HTML/CSS
features:
  - name: home_page
    description: Home page with welcome message
```

2. Generate your project:
```bash
owera generate --spec-file project.yaml --output my_app
```

3. Run the generated application:
```bash
cd my_app
python app.py
```

## Project Structure

```
owera-cli/
├── owera/              # Main package
│   ├── agents/         # AI agent implementations
│   ├── models/         # Data models
│   ├── utils/          # Utility functions
│   ├── generator/      # Code generation
│   └── main.py         # CLI entry point
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Example projects
```

## Documentation

- [User Guide](docs/user_guide.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)
- [Testing Guide](docs/testing.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the AI capabilities
- Flask and Django communities for their excellent frameworks
- All contributors who have helped shape this project
