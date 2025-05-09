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
from functools import wraps

app = Flask(__name__)
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
    # Generate login template
    login_html = _get_login_template()
    with open(f"{output_dir}/templates/login.html", "w") as f:
        f.write(login_html)
    
    # Generate register template
    register_html = _get_register_template()
    with open(f"{output_dir}/templates/register.html", "w") as f:
        f.write(register_html)
    
    # Generate feature templates
    for feature_name, design in project.designs.items():
        template_path = f"{output_dir}/templates/{feature_name}.html"
        with open(template_path, "w") as f:
            f.write(design)
        logger.info(f"Generated template: {template_path}")

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
    
    # Move development log
    os.rename("development.log", f"{output_dir}/logs/development.log")

def _setup_git(output_dir: str) -> None:
    """Initialize git repository and make initial commit."""
    repo = git.Repo.init(output_dir)
    repo.index.add(["src/app.py", "templates/", "docs/README.md", "logs/development.log"])
    repo.index.commit("Initial commit") 