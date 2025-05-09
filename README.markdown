# Owera CLI: Automated Web App Builder

## Overview
Owera CLI is a command-line tool that automates the process of building web applications by turning your app ideas into working software. It uses a team of specialized AI agents (Project Manager, UI Specialist, Developer, QA Specialist, and Product Owner) to handle design, implementation, testing, and review. Owera CLI leverages Flask for the backend, Tailwind CSS for the frontend, SQLite for the database, and JWT for authentication.

Owera CLI was developed to streamline web app creation, making it accessible for users to generate functional prototypes quickly. This project was built as part of a collaborative development process, addressing challenges like route generation, template rendering, and authentication.

## Features
- **Automated Development**: Converts app descriptions into fully functional Flask web applications.
- **Multi-Agent Workflow**: Utilizes AI agents for planning, UI design, development, QA testing, and product review.
- **Responsive UI**: Generates frontend templates using Tailwind CSS.
- **Backend with Flask**: Creates routes, handles database interactions, and implements JWT-based authentication.
- **Database Support**: Uses SQLite with SQLAlchemy for data persistence.
- **Git Integration**: Initializes a Git repository with an initial commit for version control.

## Prerequisites
Before using Owera CLI, ensure you have the following installed:
- Python 3.6+
- pip (Python package manager)
- Git
- Ollama (for running the AI models)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/owera-cli.git
   cd owera-cli
   ```
2. Install the required Python packages:
   ```bash
   pip install flask flask-sqlalchemy pyjwt click tqdm gitpython requests
   ```
3. Install and set up Ollama:
   - Follow the instructions at [Ollama's official site](https://ollama.ai/) to install Ollama.
   - Pull the required model:
     ```bash
     ollama pull qwen2.5-coder:7b
     ```

## Usage
Owera CLI takes an app description as input and generates a complete Flask web application.

### Command Syntax
```bash
python owera.py --spec "your app description" --output output_folder_name
```
Alternatively, you can provide a spec file:
```bash
python owera.py --spec-file path/to/spec.txt --output output_folder_name
```

### Example
To build an online course platform:
```bash
python owera.py --spec "Build an online course platform called LearnEasy with a course list to browse by subject, an enrollment page for users to join courses after signing in, a progress tracker to show course completion, and a teacher dashboard to manage courses. Use a database to store data, secure login for users and teachers, and a clean, modern design." --output learneasy_app
```

### Running the Generated App
1. Navigate to the generated app folder:
   ```bash
   cd learneasy_app
   ```
2. Install the app’s dependencies (as specified in the generated `README.md`):
   ```bash
   pip install flask flask-sqlalchemy pyjwt
   ```
3. Run the app:
   ```bash
   python src/app.py
   ```
4. Open your browser and visit `http://localhost:5000`.

## Project Structure
The generated app folder (`output_folder_name`) contains the following structure:
- **src/**: Contains the main Flask app code (`app.py`).
- **templates/**: Stores HTML templates for the app’s UI (e.g., `login.html`, `course_list.html`).
- **docs/**: Includes a `README.md` with setup instructions for the generated app.
- **logs/**: Contains `development.log`, a record of the app-building process.
- **database.db**: SQLite database file (created when the app runs).

## How It Works
Owera CLI uses a multi-agent system to build the app:
1. **Project Manager**: Plans tasks (design, implement, test, review) for each feature.
2. **UI Specialist**: Designs responsive HTML templates using Tailwind CSS.
3. **Developer**: Implements Flask routes, integrating database queries and authentication.
4. **QA Specialist**: Tests the implementation for issues and requests fixes if needed.
5. **Product Owner**: Reviews the feature against the specification and approves or requests fixes.

The process repeats iteratively until all features are implemented, tested, and approved.

## Contributing
Contributions to Owera CLI are welcome! Here’s how you can contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature or fix description"
   ```
4. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request with a detailed description of your changes.

### Development Notes
- Ensure all changes are compatible with the `qwen2.5-coder:7b` model used by Ollama.
- Add appropriate logging to debug issues during the development process.
- Test your changes by generating a sample app and running it.

## Troubleshooting
- **Error: "No module named 'flask_sqlalchemy'"**
  - Ensure you’ve installed the required dependencies:
    ```bash
    pip install flask-sqlalchemy
    ```
- **Error: "course_list route not found"**
  - Check the `development.log` in the generated app’s `logs/` folder to see if the `Developer` agent generated the route. If not, try enabling debug logging in `owera.py` to inspect the raw model responses.
- **Ollama Model Issues**
  - Verify that the `qwen2.5-coder:7b` model is pulled and running:
    ```bash
    ollama run qwen2.5-coder:7b
    ```
  - If the model fails to generate valid code, consider switching to a different model like `codellama:7b`.

## License
Owera CLI is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Built with [Flask](https://flask.palletsprojects.com/), [Tailwind CSS](https://tailwindcss.com/), and [Ollama](https://ollama.ai/).
- Inspired by collaborative AI-driven development workflows.
- Official site: [https://cli.owera.ai](https://cli.owera.ai)