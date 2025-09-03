#!/usr/bin/env python3
"""
Setup script for AI Swarm IDE
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ai-swarm-ide",
    version="0.1.0",
    description="Autonomous AI Development Environment with Multi-Agent Collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI Swarm IDE Team",
    author_email="team@ai-swarm-ide.com",
    url="https://github.com/yourusername/ai-swarm-ide",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer[all]>=0.9.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "openai>=1.0.0",
        "anthropic>=0.7.0",
        "requests>=2.31.0",
        "websockets>=11.0.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "swarm=cli:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="ai, development, ide, agents, swarm, automation, testing, code-generation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-swarm-ide/issues",
        "Source": "https://github.com/yourusername/ai-swarm-ide",
        "Documentation": "https://github.com/yourusername/ai-swarm-ide/wiki",
    },
)
