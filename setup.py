from setuptools import setup, find_packages

setup(
    name="owera",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=3.0.2",
        "flask-sqlalchemy>=3.1.1",
        "pyjwt>=2.8.0",
        "python-dotenv>=1.0.1",
        "requests>=2.31.0",
        "gitpython>=3.1.42",
        "click>=8.1.7",
        "tqdm>=4.66.2",
        "ollama>=0.1.6",
    ],
    entry_points={
        "console_scripts": [
            "owera=owera.main:owera",
        ],
    },
    author="Owera Team",
    author_email="info@owera.ai",
    description="AI-powered web application development tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rrecio/owera-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 