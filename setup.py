from setuptools import setup, find_packages

setup(
    name="owera",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "flask>=2.0.0",
        "gitpython>=3.1.0",
        "ollama>=0.1.0",
        "tqdm>=4.65.0",
        "python-dotenv>=0.19.0",
        "werkzeug>=2.0.0",
        "jinja2>=3.0.0",
        "sqlalchemy>=1.4.0",
        "bcrypt>=4.0.0",
        "requests>=2.26.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pytest-env>=1.1.3",
            "pytest-timeout>=2.2.0",
            "pytest-xdist>=3.5.0",
            "coverage>=7.3.2",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
            "isort>=5.12.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "owera=owera.main:owera",
        ],
    },
    python_requires=">=3.8",
    author="Owera AI",
    author_email="contact@owera.ai",
    description="AI-powered web application development tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/owera-ai/owera-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 