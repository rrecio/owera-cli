from setuptools import setup, find_packages

def read_requirements(filename):
    with open(f"requirements/{filename}") as f:
        return [
            line.strip()
            for line in f
            if not line.startswith("#") and line.strip()
        ]

setup(
    name="owera",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements("base.txt"),
    extras_require={
        "dev": read_requirements("dev.txt"),
        "test": read_requirements("test.txt")
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