import os
import git
import logging
from typing import Dict, Any
from ..models.base import Project
from ..config import config

logger = logging.getLogger(__name__)

class CodeGenerationError(Exception):
    """Raised when code generation fails."""
    pass

def generate_output(project: Project, output_dir: str) -> None:
    """Generate the final application files."""
    try:
        logger.info("Generating output files")
        _create_directories(output_dir)
        _initialize_code(project)
        _generate_app_code(project, output_dir)
        _generate_templates(project, output_dir)
        _generate_docs(project, output_dir)
        _setup_git(output_dir)
        
    except Exception as e:
        logger.error(f"Failed to generate output: {str(e)}")
        raise CodeGenerationError(f"Failed to generate output: {str(e)}")

def _create_directories(output_dir: str) -> None:
    """Create necessary directories for the project."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/src", exist_ok=True)
    os.makedirs(f"{output_dir}/templates", exist_ok=True)
    os.makedirs(f"{output_dir}/docs", exist_ok=True)
    os.makedirs(f"{output_dir}/logs", exist_ok=True)

def _initialize_code(project: Project) -> None:
    """Initialize code dictionaries."""
    if not hasattr(project, "code"):
        project.code = {}
    if "backend" not in project.code:
        project.code["backend"] = []
    if "frontend" not in project.code:
        project.code["frontend"] = []
    if not hasattr(project, "designs"):
        project.designs = {}
    if not hasattr(project, "tasks"):
        project.tasks = []
    if not hasattr(project, "issues"):
        project.issues = []

def _generate_app_code(project: Project, output_dir: str) -> None:
    """Generate the main application code."""
    app_code = _get_base_app_code()
    app_code += "\n\n" + "\n\n".join(project.code["backend"])
    app_code += "\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n"
    
    app_path = f"{output_dir}/src/app.py"
    with open(app_path, "w") as f:
        f.write(app_code)
    logger.info(f"Generated app code at {app_path}")

def _get_base_app_code() -> str:
    """Get the base Flask application code."""
    return f"""from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'))
app.config['SECRET_KEY'] = '{config.SECRET_KEY}'
app.config['SQLALCHEMY_DATABASE_URI'] = '{config.DATABASE_URI}'
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
                return jsonify({{'error': 'Unauthorized'}}), 403
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
            return redirect(url_for('home'))
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
    return render_template('home.html')

@app.route('/debug')
def debug():
    return "Debug: App is running. Check if the expected routes (e.g., course_list) are defined."

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error: A template might be missing. Please check the logs.", 500

with app.app_context():
    db.create_all()"""

def _generate_templates(project: Project, output_dir: str) -> None:
    """Generate HTML templates."""
    # Create templates directory if it doesn't exist
    templates_dir = f"{output_dir}/templates"
    os.makedirs(templates_dir, exist_ok=True)
    logger.info(f"Created templates directory: {templates_dir}")
    
    # Generate login template
    login_html = _get_login_template()
    login_path = f"{templates_dir}/login.html"
    with open(login_path, "w") as f:
        f.write(login_html)
    logger.info(f"Generated login template: {login_path}")
    
    # Generate register template
    register_html = _get_register_template()
    register_path = f"{templates_dir}/register.html"
    with open(register_path, "w") as f:
        f.write(register_html)
    logger.info(f"Generated register template: {register_path}")
    
    # Generate feature templates
    for feature_name, design in project.designs.items():
        template_name = feature_name.replace("_", "")  # Remove underscores for template name
        template_path = f"{templates_dir}/{template_name}.html"
        with open(template_path, "w") as f:
            f.write(design)
        logger.info(f"Generated template: {template_path}")
    
    # Generate home template if it doesn't exist
    home_path = f"{templates_dir}/home.html"
    if not os.path.exists(home_path):
        home_html = _get_fallback_home_template()
        with open(home_path, "w") as f:
            f.write(home_html)
        logger.info(f"Generated fallback home template: {home_path}")

def _get_login_template() -> str:
    """Get the login template."""
    return """<!DOCTYPE html>
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
</html>"""

def _get_register_template() -> str:
    """Get the register template."""
    return """<!DOCTYPE html>
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
</html>"""

def _get_fallback_home_template() -> str:
    """Get a fallback home template."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 font-sans">
    <div class="container mx-auto py-12">
        <h2 class="text-3xl font-bold mb-6 text-center">Welcome to Our Blog</h2>
        <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-lg">
            <p class="text-gray-600">This is the home page of our blog. Feel free to explore!</p>
            <div class="mt-6">
                <a href="{{ url_for('login') }}" class="text-blue-500 hover:text-blue-700">Login</a>
                <span class="mx-2">|</span>
                <a href="{{ url_for('register') }}" class="text-blue-500 hover:text-blue-700">Register</a>
            </div>
        </div>
    </div>
</body>
</html>"""

def _generate_docs(project: Project, output_dir: str) -> None:
    """Generate documentation."""
    readme_content = (
        f"# {project.specs['project']['name']}\n\n"
        f"A web app built by Owera.\n\n"
        f"## Features\n" +
        "\n".join(f"- **{f.name}**: {f.description}" for f in project.features) +
        f"\n\n## Setup\n"
        f"1. Install Python and required packages (`pip install flask flask-sqlalchemy pyjwt`).\n"
        f"2. Run `python src/app.py`.\n"
        f"3. Visit `http://localhost:5000`."
    )
    
    with open(f"{output_dir}/docs/README.md", "w") as f:
        f.write(readme_content)
    
    # Move development log if it exists
    if os.path.exists("development.log"):
        os.rename("development.log", f"{output_dir}/logs/development.log")
    else:
        # Create an empty log file if it doesn't exist
        with open(f"{output_dir}/logs/development.log", "w") as f:
            f.write("Development log initialized\n")

def _setup_git(output_dir: str) -> None:
    """Initialize git repository and make initial commit."""
    repo = git.Repo.init(output_dir)
    repo.index.add(["src/app.py", "templates/", "docs/README.md", "logs/development.log"])
    repo.index.commit("Initial commit") 