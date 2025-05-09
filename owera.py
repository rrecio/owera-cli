import click
import os
import git
import logging
import ollama
import json
from datetime import datetime
from tqdm import tqdm
import sys
import requests
import re
from functools import wraps

# Configure logging for both file and console output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('development.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class Feature:
    def __init__(self, name, description, constraints=None):
        self.name = name
        self.description = description
        self.constraints = constraints or []
        self.has_design = False
        self.has_implementation = False
        self.has_passed_tests = False
        self.is_approved = False
        self.issues = []

class Issue:
    def __init__(self, description, feature):
        self.description = description
        self.feature = feature
        self.is_resolved = False

class Task:
    def __init__(self, type, feature, description):
        self.type = type
        self.feature = feature
        self.description = description
        self.status = "todo"
        self.assigned_to = None

class Project:
    def __init__(self, specs):
        logging.info("Initializing project with specs")
        self.specs = specs
        # Validate specs structure
        if not isinstance(self.specs, dict) or "project" not in self.specs or not isinstance(self.specs["project"], dict) or "features" not in self.specs["project"]:
            logging.warning("Invalid specs structure. Using default features.")
            self.specs = {
                "project": {
                    "name": "SimpleApp",
                    "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"},
                    "features": [{"name": "home_page", "description": "A basic home page to display a welcome message"}]
                }
            }
        self.features = [Feature(f["name"], f["description"], f.get("constraints", [])) for f in self.specs["project"]["features"]]
        self.tasks = []
        self.issues = []
        self.designs = {}
        self.code = {"backend": [], "frontend": []}
        self.test_results = {}
        logging.info(f"Project initialized with {len(self.features)} features")

    def is_complete(self):
        complete = (all(f.is_approved for f in self.features) and 
                    not any(i for i in self.issues if not i.is_resolved) and 
                    not any(t for t in self.tasks if t.status in ["todo", "in_progress"]))
        logging.debug(f"Project completion check: {complete}")
        return complete

class Agent:
    def __init__(self, role):
        self.role = role

    def perform_task(self, task, project):
        try:
            prompt = self.generate_prompt(task, project)
            logging.debug(f"{self.role} prompt: {prompt}")
            logging.info(f"{self.role} is working on: {task.description}")
            response = ollama.generate(model="qwen2.5-coder:7b", prompt=prompt, options={"timeout": 60})['response']
            logging.debug(f"{self.role} raw response: {response}")
            # Only extract code for UI Specialist and Developer
            if self.role in ["UI Specialist", "Developer"]:
                code = self.extract_code(response)
                logging.debug(f"{self.role} extracted code: {code}")
                if self.role == "Developer":
                    # Post-process to fix incorrect decorator usage and imports
                    code = self.fix_decorator_usage(code)
                    code = self.remove_unnecessary_imports(code)
                    logging.debug(f"{self.role} post-processed code: {code}")
                self.process_response(code, task, project)
            else:
                self.process_response(response, task, project)
            task.status = "done"
            logging.info(f"{self.role} finished: {task.description}")
        except requests.exceptions.Timeout:
            logging.error(f"{self.role} timed out while processing: {task.description}")
            task.status = "failed"
            project.issues.append(Issue(f"{self.role} timed out", task.feature))
        except Exception as e:
            logging.error(f"{self.role} encountered an issue: {str(e)}")
            task.status = "failed"
            project.issues.append(Issue(f"{self.role} failed: {str(e)}", task.feature))

    def extract_code(self, response):
        # Handle HTML for UI Specialist
        if self.role == "UI Specialist":
            html_blocks = re.findall(r'```html\n(.*?)\n```', response, re.DOTALL)
            if html_blocks:
                return html_blocks[0].strip()
            # Fallback: if no code block, assume the entire response is HTML
            if response.strip().startswith('<!DOCTYPE html>') or response.strip().startswith('<html'):
                return response.strip()
            # Broader fallback: look for any HTML-like content
            lines = response.split('\n')
            html_lines = [line for line in lines if line.strip().startswith(('<', '!DOCTYPE'))]
            if html_lines:
                return '\n'.join(html_lines).strip()
            logging.warning(f"No HTML found in response: {response}")
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placeholder</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-12">
        <h2 class="text-3xl font-bold mb-6 text-center">Placeholder: {self.feature.name}</h2>
        <p class="text-center">This is a placeholder template for {self.feature.name}.</p>
    </div>
</body>
</html>
"""
        # Handle Python code for Developer
        code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        # Broader extraction for Python code
        lines = response.split('\n')
        code_lines = []
        in_code = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(('@app.route', 'def ', 'from ', 'import ', 'if __name__')) or in_code:
                code_lines.append(line)
                in_code = True
            # Include common Flask patterns
            elif in_code and (line.startswith(('#', 'return', 'if ', 'for ', 'while ', 'try ', 'except ', 'with ', 'class ', '@login_required')) or any(line.startswith(prefix) for prefix in ('courses =', 'user =', 'enrollment ='))):
                code_lines.append(line)
            # Stop collecting if we hit a non-code line after starting
            elif in_code and not line.startswith(('#', 'return', 'if ', 'for ', 'while ', 'try ', 'except ', 'with ', 'class ', '@login_required')):
                break
        if code_lines:
            return '\n'.join(code_lines).strip()
        logging.warning(f"No valid Python code found in response: {response}")
        # Fallback: generate a minimal functional route
        auth_required = any("secure login" in constraint.lower() for constraint in self.feature.constraints)
        decorator = "@login_required" if auth_required else ""
        return f"""@app.route('/{self.feature.name}')
{decorator}
def {self.feature.name}():
    items = Course.query.all() if 'course' in '{self.feature.name}' else []
    return render_template('{self.feature.name}.html', items=items)"""

    def fix_decorator_usage(self, code):
        # Fix incorrect usage of @login_required() by removing parentheses
        lines = code.split('\n')
        fixed_lines = []
        for line in lines:
            if "@login_required()" in line:
                line = line.replace("@login_required()", "@login_required")
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)

    def remove_unnecessary_imports(self, code):
        # Remove incorrect imports like "from models import ..."
        lines = code.split('\n')
        fixed_lines = []
        for line in lines:
            if line.startswith("from models import"):
                logging.info(f"Removing unnecessary import: {line}")
                continue
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)

    def generate_prompt(self, task, project):
        raise NotImplementedError

    def process_response(self, response, task, project):
        raise NotImplementedError

class UISpecialist(Agent):
    def __init__(self):
        super().__init__("UI Specialist")

    def generate_prompt(self, task, project):
        constraints = ", ".join(task.feature.constraints) if task.feature.constraints else "responsive, modern design"
        self.feature = task.feature  # Store feature for use in extract_code
        return (f"Provide only the HTML code for a responsive template for '{task.feature.name}' using Tailwind CSS via CDN. "
                f"Do not include explanations or comments, just the raw HTML code. "
                f"Description: {task.feature.description}. Constraints: {constraints}.")

    def process_response(self, response, task, project):
        project.designs[task.feature.name] = response
        task.feature.has_design = True

class Developer(Agent):
    def __init__(self):
        super().__init__("Developer")

    def generate_prompt(self, task, project):
        tech_stack = project.specs["project"]["tech_stack"]
        constraints = ", ".join(task.feature.constraints) if task.feature.constraints else "clean, modular code"
        self.feature = task.feature  # Store feature for use in extract_code
        if task.type == "implement":
            design = project.designs.get(task.feature.name, "")
            return (f"Generate a Flask route for '{task.feature.name}' in {tech_stack['backend']}. "
                    f"Return only the Python code, without explanations, comments, or imports (assume Flask, render_template, request, redirect, url_for, session, jsonify, SQLAlchemy, and db are imported). "
                    f"The models (User, Course, Enrollment) are already defined in the file, so do NOT add any import statements for them (e.g., do NOT add 'from models import Course'). "
                    f"Define the route function as 'def {task.feature.name}():' to match the feature name. "
                    f"Use the route path '@app.route('/{task.feature.name}')'. "
                    f"Render the template '{task.feature.name}.html'. "
                    f"If the feature involves displaying items (e.g., courses), query the database using Course.query.all() and pass the results to the template as 'items'. "
                    f"If authentication is required, use the @login_required decorator without parentheses (e.g., @login_required, NOT @login_required()). "
                    f"Description: {task.feature.description}. Design: {design}. Constraints: {constraints}. "
                    f"Include necessary logic (e.g., database queries, authentication) as specified in the description.")
        elif task.type == "fix":
            code = "\n".join(project.code["backend"])
            return (f"Fix the issue in the Flask route for '{task.feature.name}': {task.description}. "
                    f"Current code: {code}. Provide only the corrected Python code without explanations or comments.")

    def process_response(self, response, task, project):
        if task.type == "implement":
            project.code["backend"].append(response)
        elif task.type == "fix":
            project.code["backend"] = [response]
        task.feature.has_implementation = True

class QASpecialist(Agent):
    def __init__(self):
        super().__init__("QA Specialist")

    def generate_prompt(self, task, project):
        code = "\n".join(project.code["backend"])
        design = project.designs.get(task.feature.name, "")
        return (f"Test the feature '{task.feature.name}'. Code: {code}. Design: {design}. "
                f"Description: {task.feature.description}. Provide only a brief result: 'No issues' or list specific issues.")

    def process_response(self, response, task, project):
        if "no issues" in response.lower() or "passes" in response.lower():
            task.feature.has_passed_tests = True
        else:
            issue = Issue(response, task.feature)
            project.issues.append(issue)
            fix_task = Task("fix", task.feature, f"Fix: {response}")
            fix_task.assigned_to = "Developer"
            project.tasks.append(fix_task)

class ProductOwner(Agent):
    def __init__(self):
        super().__init__("Product Owner")

    def generate_prompt(self, task, project):
        code = "\n".join(project.code["backend"])
        design = project.designs.get(task.feature.name, "")
        return (f"Verify if '{task.feature.name}' meets the spec: {task.feature.description}. "
                f"Code: {code}. Design: {design}. Provide only 'Approve' or list specific discrepancies.")

    def process_response(self, response, task, project):
        if "approve" in response.lower():
            task.feature.is_approved = True
        else:
            issue = Issue(response, task.feature)
            project.issues.append(issue)
            fix_task = Task("fix", task.feature, f"Fix: {response}")
            fix_task.assigned_to = "Developer"
            project.tasks.append(fix_task)

class ProjectManager(Agent):
    def __init__(self):
        super().__init__("Project Manager")

    def plan(self, project):
        logging.info("Planning tasks for features")
        for feature in project.features:
            if not feature.has_design and not any(t.feature == feature and t.type == "design" for t in project.tasks):
                task = Task("design", feature, f"Design {feature.name}")
                task.assigned_to = "UI Specialist"
                project.tasks.append(task)
            elif feature.has_design and not feature.has_implementation and not any(t.feature == feature and t.type == "implement" for t in project.tasks):
                task = Task("implement", feature, f"Implement {feature.name}")
                task.assigned_to = "Developer"
                project.tasks.append(task)
            elif feature.has_implementation and not feature.has_passed_tests and not any(t.feature == feature and t.type == "test" for t in project.tasks):
                task = Task("test", feature, f"Test {feature.name}")
                task.assigned_to = "QA Specialist"
                project.tasks.append(task)
            elif feature.has_passed_tests and not feature.is_approved and not any(t.feature == feature and t.type == "review" for t in project.tasks):
                task = Task("review", feature, f"Review {feature.name}")
                task.assigned_to = "Product Owner"
                project.tasks.append(task)
        logging.info(f"Planned {len(project.tasks)} tasks")

def parse_spec_string(spec_string):
    logging.info("Parsing specification string")
    json_structure = (
        "{'project': {'name': 'AppName', 'tech_stack': {'backend': 'Python/Flask', 'frontend': 'HTML/CSS'}}, "
        "'features': [{'name': 'feature name', 'description': 'feature description', 'constraints': ['constraint1']}]}}"
    )
    prompt = (
        f"Parse this app description into JSON with the following structure: {json_structure} "
        f"Default to Python/Flask, HTML/CSS, SQLite, JWT auth if unspecified. Ensure valid JSON output with 'features' key. "
        f"If the description is unclear, include at least one feature (e.g., a home page). Description: {spec_string}"
    )
    try:
        logging.info("Sending request to Ollama for JSON parsing...")
        response = ollama.generate(model="qwen2.5-coder:7b", prompt=prompt, options={"timeout": 60})['response']
        logging.debug(f"Raw JSON parsing response: {response}")
        parsed = json.loads(response)
        if "project" not in parsed:
            parsed["project"] = {}
        if "features" not in parsed or not parsed["features"]:
            parsed["features"] = [{"name": "home_page", "description": "A basic home page to display a welcome message"}]
        if "tech_stack" not in parsed["project"]:
            parsed["project"]["tech_stack"] = {"backend": "Python/Flask", "frontend": "HTML/CSS"}
        if "name" not in parsed["project"]:
            parsed["project"]["name"] = "SimpleApp"
        logging.info(f"Found {len(parsed['features'])} features to build.")
        return parsed
    except (json.JSONDecodeError, KeyError, requests.exceptions.Timeout) as e:
        logging.error(f"JSON parsing failed: {str(e)}. Falling back to manual parsing.")

    logging.info("Attempting manual parsing of the specification string")
    try:
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
            # Extract constraints (e.g., "clean, modern design")
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
            features.append({"name": name, "description": description, "constraints": constraints})

        if not features:
            features = [{"name": "home_page", "description": "A basic home page to display a welcome message"}]

        parsed = {
            "project": {
                "name": project_name,
                "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"},
                "features": features
            }
        }
        logging.info(f"Manually parsed {len(features)} features: {features}")
        return parsed
    except Exception as e:
        logging.error(f"Manual parsing failed: {str(e)}. Using default features.")
        return {
            "project": {
                "name": "SimpleApp",
                "tech_stack": {"backend": "Python/Flask", "frontend": "HTML/CSS"},
                "features": [{"name": "home_page", "description": "A basic home page to display a welcome message"}]
            }
        }

def generate_output(project, output_dir):
    try:
        logging.info("Generating output files")
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/src", exist_ok=True)
        os.makedirs(f"{output_dir}/templates", exist_ok=True)
        os.makedirs(f"{output_dir}/docs", exist_ok=True)
        os.makedirs(f"{output_dir}/logs", exist_ok=True)

        # Base Flask app code with predefined routes
        app_code_base = """from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor = db.relationship('User', backref=db.backref('courses', lazy=True))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    progress = db.Column(db.Float, default=0.0)
    user = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if role and user.role != role:
                return jsonify({'error': 'Unauthorized'}), 403
            return f(*args, **kwargs)
        return wrapped_function
    return decorator

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('course_list'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        user = User(email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
def home():
    try:
        return redirect(url_for('course_list'))
    except:
        return "Error: 'course_list' route not found. Please check if the route was generated correctly.", 500

# Fallback route for debugging
@app.route('/debug')
def debug():
    return "Debug: App is running. Check if the expected routes (e.g., course_list) are defined."

# Fallback for missing templates
@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error: A template might be missing. Please check the logs.", 500

with app.app_context():
    db.create_all()
"""

        # Log the generated routes
        logging.info("Generated routes:")
        for route_code in project.code["backend"]:
            logging.info(f"Route: {route_code}")

        # Combine predefined routes with generated routes
        app_code = app_code_base + "\n\n" + "\n\n".join(project.code["backend"]) + "\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n"

        # Log the final app code to verify the / route
        logging.debug(f"Final app.py code:\n{app_code}")

        # Write the app code to file
        with open(f"{output_dir}/src/app.py", "w") as f:
            f.write(app_code)

        login_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-12">
        <h2 class="text-3xl font-bold mb-6 text-center">Login</h2>
        {% if error %}
        <p class="text-red-500 text-center">{{ error }}</p>
        {% endif %}
        <form method="POST" class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-lg">
            <div class="mb-4">
                <label class="block text-gray-700">Email</label>
                <input type="email" name="email" class="w-full p-2 border rounded" required>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700">Password</label>
                <input type="password" name="password" class="w-full p-2 border rounded" required>
            </div>
            <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Login</button>
        </form>
        <p class="text-center mt-4">Don't have an account? <a href="{{ url_for('register') }}" class="text-blue-500">Register</a></p>
    </div>
</body>
</html>
"""
        with open(f"{output_dir}/templates/login.html", "w") as f:
            f.write(login_html)

        register_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-12">
        <h2 class="text-3xl font-bold mb-6 text-center">Register</h2>
        <form method="POST" class="max-w-md mx-auto bg-white p-6 rounded-lg shadow-lg">
            <div class="mb-4">
                <label class="block text-gray-700">Email</label>
                <input type="email" name="email" class="w-full p-2 border rounded" required>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700">Password</label>
                <input type="password" name="password" class="w-full p-2 border rounded" required>
            </div>
            <div class="mb-4">
                <label class="block text-gray-700">Role</label>
                <select name="role" class="w-full p-2 border rounded">
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                </select>
            </div>
            <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Register</button>
        </form>
        <p class="text-center mt-4">Already have an account? <a href="{{ url_for('login') }}" class="text-blue-500">Login</a></p>
    </div>
</body>
</html>
"""
        with open(f"{output_dir}/templates/register.html", "w") as f:
            f.write(register_html)

        # Log the templates being created
        logging.info("Generated templates:")
        for feature_name, design in project.designs.items():
            template_path = f"{output_dir}/templates/{feature_name}.html"
            with open(template_path, "w") as f:
                f.write(design)
            logging.info(f"Created template: {template_path}")

        with open(f"{output_dir}/docs/README.md", "w") as f:
            f.write(f"# {project.specs['project']['name']}\n\n"
                    f"A web app built by Owera.\n\n## Features\n" + 
                    "\n".join(f"- **{f.name}**: {f.description}" for f in project.features) + 
                    "\n\n## Setup\n1. Install Python and required packages (`pip install flask flask-sqlalchemy pyjwt`).\n2. Run `python src/app.py`.\n3. Visit `http://localhost:5000`.")

        os.rename("development.log", f"{output_dir}/logs/development.log")

        repo = git.Repo.init(output_dir)
        repo.index.add(["src/app.py", "templates/", "docs/README.md", "logs/development.log"])
        repo.index.commit("Initial commit")

        logging.info("\n=== Your App is Ready! ===")
        logging.info(f"App Folder: {output_dir}")
        logging.info("What's Inside:")
        logging.info(f"- src/app.py: The main app code to run your website.")
        logging.info(f"- templates/: Designed pages for your app's features.")
        logging.info(f"- docs/README.md: Instructions to start your app.")
        logging.info(f"- logs/development.log: A record of how your app was built.")
        logging.info("Next Steps: Check the README.md for how to run your app!")
    except Exception as e:
        logging.error(f"Failed to create app files: {str(e)}")
        raise

@click.command()
@click.option('--spec', default=None, help='Describe your app (e.g., "Build a blog with a home page")')
@click.option('--spec-file', type=click.Path(exists=True), default=None, help='Text file with app description')
@click.option('--output', required=True, help='Folder name for your app')
def owera(spec, spec_file, output):
    """Owera: Turns your app ideas into working software."""
    if spec and spec_file:
        raise click.UsageError("Use either --spec or --spec-file, not both.")
    if not spec and not spec_file:
        raise click.UsageError("Provide --spec or --spec-file.")

    logging.info("Starting Owera to build your app")

    spec_string = spec
    if spec_file:
        with open(spec_file, "r") as f:
            spec_string = f.read().strip()

    specs = parse_spec_string(spec_string)
    project = Project(specs)
    agents = {
        "UI Specialist": UISpecialist(),
        "Developer": Developer(),
        "QA Specialist": QASpecialist(),
        "Product Owner": ProductOwner(),
        "Project Manager": ProjectManager()
    }

    iteration = 0
    max_iterations = 100
    with tqdm(total=len(project.features) * 4, desc="Building Your App", unit="step") as pbar:
        while not project.is_complete() and iteration < max_iterations:
            iteration += 1
            logging.debug(f"Iteration {iteration}: {len(project.tasks)} tasks to process")
            agents["Project Manager"].plan(project)
            tasks_to_process = [task for task in project.tasks if task.status == "todo"]
            for task in tasks_to_process:
                task.status = "in_progress"
                agents[task.assigned_to].perform_task(task, project)
                pbar.update(1)
            if not tasks_to_process:
                logging.warning("No tasks to process, but project not complete. Possible deadlock.")
                break
        if iteration >= max_iterations:
            logging.error("Reached maximum iterations. Possible infinite loop detected.")

    generate_output(project, output)

if __name__ == "__main__":
    owera()