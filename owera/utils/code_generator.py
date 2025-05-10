import os
import git
import logging
import requests
import json
from importlib.metadata import version, PackageNotFoundError
from typing import Dict, Any, List, Set, Tuple
from ..models.base import Project
from ..config import config

logger = logging.getLogger(__name__)

# Core dependencies with version constraints
CORE_DEPENDENCIES = {
    'flask': '==2.3.3',
    'flask-sqlalchemy': '==3.1.1',
    'flask-login': '==0.6.3',
    'pyjwt': '==2.8.0',
    'python-dotenv': '==1.0.1',
    'requests': '==2.31.0',
    'gitpython': '==3.1.42',
    'click': '==8.1.7',
    'tqdm': '==4.66.2',
    'ollama': '==0.1.6'
}

# Development dependencies
DEV_DEPENDENCIES = {
    'pytest': '==7.4.3',
    'pytest-cov': '==4.1.0',
    'pytest-flask': '==1.2.0',
    'pytest-env': '==1.1.3'
}

# Sub-dependencies with specific versions
SUB_DEPENDENCIES = {
    'Werkzeug': '==2.3.7',
    'Jinja2': '==3.1.2',
    'SQLAlchemy': '==2.0.23',
    'MarkupSafe': '==2.1.3',
    'typing-extensions': '==4.8.0'
}

def get_latest_version(package_name: str) -> str:
    """Get the latest version of a package from PyPI."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['info']['version']
        return None
    except Exception as e:
        logger.warning(f"Failed to get latest version for {package_name}: {e}")
        return None

def check_dependency_updates(dependencies: Dict[str, str]) -> List[Tuple[str, str, str]]:
    """Check for available updates for dependencies.
    
    Returns:
        List of tuples containing (package_name, current_version, latest_version)
    """
    updates = []
    for package, version_constraint in dependencies.items():
        current_version = version_constraint.lstrip('=')
        latest_version = get_latest_version(package)
        if latest_version and latest_version != current_version:
            updates.append((package, current_version, latest_version))
    return updates

def check_dependency_compatibility(dependencies: Dict[str, str]) -> List[str]:
    """Check compatibility between dependencies and return any conflicts."""
    conflicts = []
    for package, version_constraint in dependencies.items():
        try:
            installed_version = version(package)
            required_version = version_constraint.lstrip('=')
            if installed_version != required_version:
                conflicts.append(f"Version conflict for {package}: installed {installed_version}, required {required_version}")
        except PackageNotFoundError:
            conflicts.append(f"Package not found: {package}")
        except Exception as e:
            logger.warning(f"Error checking compatibility for {package}: {e}")
            conflicts.append(f"Error checking {package}: {str(e)}")
    return conflicts

def update_dependency_versions(dependencies: Dict[str, str], force_update: bool = False) -> Dict[str, str]:
    """Update dependency versions to their latest versions.
    
    Args:
        dependencies: Dictionary of package names and their version constraints
        force_update: If True, update all dependencies regardless of compatibility
    
    Returns:
        Updated dictionary of dependencies
    """
    updated_deps = dependencies.copy()
    updates = check_dependency_updates(dependencies)
    
    for package, current_version, latest_version in updates:
        if force_update:
            updated_deps[package] = f"=={latest_version}"
            logger.info(f"Updated {package} from {current_version} to {latest_version}")
        else:
            # Check compatibility before updating
            try:
                # Create a temporary working set with the new version
                temp_deps = updated_deps.copy()
                temp_deps[package] = f"=={latest_version}"
                conflicts = check_dependency_compatibility(temp_deps)
                
                if not conflicts:
                    updated_deps[package] = f"=={latest_version}"
                    logger.info(f"Updated {package} from {current_version} to {latest_version}")
                else:
                    logger.warning(f"Skipping update for {package} due to compatibility issues: {conflicts}")
            except Exception as e:
                logger.warning(f"Failed to check compatibility for {package}: {e}")
    
    return updated_deps

def update_all_dependencies(force_update: bool = False) -> None:
    """Update all dependency groups to their latest compatible versions."""
    global CORE_DEPENDENCIES, DEV_DEPENDENCIES, SUB_DEPENDENCIES
    
    logger.info("Checking for dependency updates...")
    
    # Update core dependencies
    CORE_DEPENDENCIES = update_dependency_versions(CORE_DEPENDENCIES, force_update)
    
    # Update development dependencies
    DEV_DEPENDENCIES = update_dependency_versions(DEV_DEPENDENCIES, force_update)
    
    # Update sub-dependencies
    SUB_DEPENDENCIES = update_dependency_versions(SUB_DEPENDENCIES, force_update)
    
    logger.info("Dependency update check completed")

def generate_requirements_content(include_dev: bool = True) -> str:
    """Generate requirements.txt content with proper formatting and comments."""
    content = []
    
    # Add core dependencies
    content.append("# Core dependencies")
    for package, version in sorted(CORE_DEPENDENCIES.items()):
        content.append(f"{package}{version}")
    
    # Add development dependencies if requested
    if include_dev:
        content.append("\n# Development dependencies")
        for package, version in sorted(DEV_DEPENDENCIES.items()):
            content.append(f"{package}{version}")
    
    # Add sub-dependencies
    content.append("\n# Sub-dependencies with specific versions")
    for package, version in sorted(SUB_DEPENDENCIES.items()):
        content.append(f"{package}{version}")
    
    return "\n".join(content)

def generate_output(project: Project, output_dir: str) -> None:
    """Generate the application output."""
    # Create output directory structure
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'src'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'static'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'docs'), exist_ok=True)
    
    # Create __init__.py in src directory
    with open(os.path.join(output_dir, 'src', '__init__.py'), 'w') as f:
        f.write('""" ShopEasy application package. """\n')
    
    # Check for dependency updates
    try:
        update_all_dependencies(force_update=False)
    except Exception as e:
        logger.warning(f"Failed to check for dependency updates: {e}")
    
    # Check dependency compatibility
    all_deps = {**CORE_DEPENDENCIES, **DEV_DEPENDENCIES, **SUB_DEPENDENCIES}
    conflicts = check_dependency_compatibility(all_deps)
    if conflicts:
        logger.warning("Dependency conflicts detected:")
        for conflict in conflicts:
            logger.warning(f"  - {conflict}")
    
    # Create requirements.txt
    with open(os.path.join(output_dir, 'requirements.txt'), 'w') as f:
        f.write(generate_requirements_content(include_dev=True))
    
    # Create requirements-dev.txt for development dependencies
    with open(os.path.join(output_dir, 'requirements-dev.txt'), 'w') as f:
        f.write(generate_requirements_content(include_dev=True))
    
    # Initialize project code
    _initialize_code(project)
    
    # Generate application code
    _generate_app_code(project, output_dir)
    
    # Generate test files
    generate_tests(project, output_dir)
    
    # Generate documentation
    generate_documentation(project, output_dir)
    
    # Initialize git repository
    try:
        repo = git.Repo.init(output_dir)
        repo.index.add('*')
        repo.index.commit("Initial commit")
    except Exception as e:
        logger.warning(f"Failed to initialize git repository: {e}")

def generate_tests(project: Project, output_dir: str) -> None:
    """Generate test files for the application."""
    tests_dir = os.path.join(output_dir, 'tests')
    
    # Generate test files for each feature
    for feature in project.features:
        test_file = os.path.join(tests_dir, f'test_{feature.name}.py')
        test_content = generate_feature_tests(feature, project)
        with open(test_file, 'w') as f:
            f.write(test_content)
            
    # Generate test configuration
    conftest_content = generate_conftest(project)
    with open(os.path.join(tests_dir, 'conftest.py'), 'w') as f:
        f.write(conftest_content)
        
    # Generate test requirements
    requirements_content = generate_test_requirements(project)
    with open(os.path.join(tests_dir, 'requirements-test.txt'), 'w') as f:
        f.write(requirements_content)

def generate_feature_tests(feature: Dict[str, Any], project: Project) -> str:
    """Generate test content for a specific feature."""
    feature_name = feature.name if hasattr(feature, 'name') else feature['name']
    test_content = f'''import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app, db

class Test{feature_name.replace('_', ' ').title().replace(' ', '')}:
    """Test case for {feature_name} feature."""
    
    def setup_method(self):
        """Set up test environment."""
        self.app = app
        self.app.config.update({{
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False,
            'SECRET_KEY': 'test-key'
        }})
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Try to drop all tables, ignoring errors if they don't exist
        try:
            db.drop_all()
        except Exception:
            pass
            
        # Create all tables
        db.create_all()
        
    def teardown_method(self):
        """Clean up test environment."""
        try:
            # Clear any existing sessions and close connections
            db.session.remove()
            db.engine.dispose()
            # Drop all tables
            try:
                db.drop_all()
            except Exception:
                pass
            if hasattr(self, 'ctx'):
                self.ctx.pop()
        finally:
            pass
            
    def test_feature_initialization(self):
        """Test feature initialization."""
        assert True  # Add specific tests based on feature requirements
'''
    return test_content

def generate_conftest(project: Project) -> str:
    """Generate pytest configuration file."""
    return '''import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app, db

@pytest.fixture
def test_app():
    """Create a test Flask application."""
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-key'
    })
    return app

@pytest.fixture
def test_client(test_app):
    """Create a test client."""
    return test_app.test_client()

@pytest.fixture
def test_db(test_app):
    """Create a test database."""
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
'''

def generate_test_requirements(project: Project) -> str:
    """Generate test requirements file."""
    return generate_requirements_content(include_dev=True)

def generate_documentation(project: Project, output_dir: str) -> None:
    """Generate documentation for the application."""
    docs_dir = os.path.join(output_dir, 'docs')
    
    # Generate README
    feature_list = []
    for feature in project.features:
        feature_name = feature.name if hasattr(feature, 'name') else feature['name']
        feature_desc = feature.description if hasattr(feature, 'description') else feature['description']
        feature_list.append(f"- {feature_name}: {feature_desc}")
    
    readme_content = f'''# {project.name}

## Description
{project.description if hasattr(project, 'description') else 'A web application'}

## Features
{chr(10).join(feature_list)}

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python src/app.py`

## Testing
Run tests with: `pytest tests/`
'''
    
    with open(os.path.join(docs_dir, 'README.md'), 'w') as f:
        f.write(readme_content)

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
    """Generate the application code."""
    app_file = os.path.join(output_dir, 'src', 'app.py')
    
    # Get base app code
    app_code = _get_base_app_code()
    
    # Write the app code
    with open(app_file, 'w') as f:
        f.write(app_code)
    
    logger.info(f"Generated app code at {app_file}")

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

def auth_required(role=None):
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

@app.route('/product_list')
@auth_required()
def product_list():
    items = Course.query.all()
    return render_template('productlist.html', items=items)

@app.route('/product_page')
@auth_required()
def product_page():
    items = Course.query.all()
    return render_template('productpage.html', items=items)

@app.route('/cart_page')
@auth_required()
def cart_page():
    items = Course.query.all()
    return render_template('cartpage.html', items=items)

@app.route('/checkout_page')
@auth_required()
def checkout_page():
    items = Course.query.all()
    return render_template('checkoutpage.html', items=items)

@app.route('/debug')
def debug():
    return "Debug: App is running. Check if the expected routes (e.g., course_list) are defined."

@app.errorhandler(500)
def internal_error(error):
    return "Internal Server Error: A template might be missing. Please check the logs.", 500

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)"""

def _generate_templates(project: Project, output_dir: str) -> None:
    """Generate HTML templates for the application."""
    templates_dir = os.path.join(output_dir, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Generate templates based on project features
    for feature in project.features:
        feature_name = feature.name if hasattr(feature, 'name') else feature['name']
        template_name = f"{feature_name}.html"
        template_content = _get_template_for_feature(feature)
        
        template_path = os.path.join(templates_dir, template_name)
        with open(template_path, 'w') as f:
            f.write(template_content)
        logger.info(f"Generated template: {template_path}")

def _get_template_for_feature(feature: Dict[str, Any]) -> str:
    """Get the appropriate template content for a feature."""
    feature_name = feature.name if hasattr(feature, 'name') else feature['name']
    
    if feature_name == 'product_list':
        return _get_product_list_template()
    elif feature_name == 'product_page':
        return _get_product_page_template()
    elif feature_name == 'cart_page':
        return _get_cart_page_template()
    elif feature_name == 'checkout_page':
        return _get_checkout_page_template()
    else:
        return _get_fallback_home_template()

def _get_product_list_template() -> str:
    """Get the product list template."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopEasy - Products</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">ShopEasy</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" href="/products">Products</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/cart">Cart</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1>Our Products</h1>
        <div class="row">
            {% for product in products %}
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text">{{ product.description }}</p>
                        <p class="card-text"><strong>Price: ${{ "%.2f"|format(product.price) }}</strong></p>
                        <a href="{{ url_for('product_page', product_id=product.id) }}" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

def _get_product_page_template() -> str:
    """Get the product page template."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopEasy - {{ product.name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">ShopEasy</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/products">Products</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/cart">Cart</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-6">
                <img src="{{ product.image_url }}" class="img-fluid" alt="{{ product.name }}">
            </div>
            <div class="col-md-6">
                <h1>{{ product.name }}</h1>
                <p class="lead">{{ product.description }}</p>
                <p class="h3">${{ "%.2f"|format(product.price) }}</p>
                <form action="{{ url_for('add_to_cart', product_id=product.id) }}" method="POST">
                    <div class="mb-3">
                        <label for="quantity" class="form-label">Quantity</label>
                        <input type="number" class="form-control" id="quantity" name="quantity" value="1" min="1">
                    </div>
                    <button type="submit" class="btn btn-primary">Add to Cart</button>
                </form>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

def _get_cart_page_template() -> str:
    """Get the cart page template."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopEasy - Cart</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">ShopEasy</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/products">Products</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/cart">Cart</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1>Your Shopping Cart</h1>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Total</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in cart_items %}
                    <tr>
                        <td>{{ item.product.name }}</td>
                        <td>${{ "%.2f"|format(item.product.price) }}</td>
                        <td>{{ item.quantity }}</td>
                        <td>${{ "%.2f"|format(item.product.price * item.quantity) }}</td>
                        <td>
                            <form action="{{ url_for('remove_from_cart', item_id=item.id) }}" method="POST" style="display: inline;">
                                <button type="submit" class="btn btn-sm btn-danger">Remove</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
                <tfoot>
                    <tr>
                        <td colspan="3" class="text-end"><strong>Total:</strong></td>
                        <td><strong>${{ "%.2f"|format(total) }}</strong></td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
        <div class="d-flex justify-content-between mt-4">
            <a href="/products" class="btn btn-secondary">Continue Shopping</a>
            <a href="/checkout" class="btn btn-primary">Proceed to Checkout</a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

def _get_checkout_page_template() -> str:
    """Get the checkout page template."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopEasy - Checkout</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">ShopEasy</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/products">Products</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/cart">Cart</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <h1>Checkout</h1>
        <div class="row">
            <div class="col-md-8">
                <form action="{{ url_for('process_checkout') }}" method="POST">
                    <h3>Shipping Information</h3>
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="address" class="form-label">Address</label>
                        <input type="text" class="form-control" id="address" name="address" required>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="city" class="form-label">City</label>
                            <input type="text" class="form-control" id="city" name="city" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label for="state" class="form-label">State</label>
                            <input type="text" class="form-control" id="state" name="state" required>
                        </div>
                        <div class="col-md-3 mb-3">
                            <label for="zip" class="form-label">ZIP Code</label>
                            <input type="text" class="form-control" id="zip" name="zip" required>
                        </div>
                    </div>

                    <h3 class="mt-4">Payment Information</h3>
                    <div class="mb-3">
                        <label for="card" class="form-label">Card Number</label>
                        <input type="text" class="form-control" id="card" name="card" required>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="expiry" class="form-label">Expiry Date</label>
                            <input type="text" class="form-control" id="expiry" name="expiry" placeholder="MM/YY" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="cvv" class="form-label">CVV</label>
                            <input type="text" class="form-control" id="cvv" name="cvv" required>
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary">Place Order</button>
                </form>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h3>Order Summary</h3>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Subtotal:</span>
                            <span>${{ "%.2f"|format(subtotal) }}</span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span>Shipping:</span>
                            <span>${{ "%.2f"|format(shipping) }}</span>
                        </div>
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>Total:</strong>
                            <strong>${{ "%.2f"|format(total) }}</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

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