# Contributing to DevDollz: Atelier Edition 🤝

Thank you for your interest in contributing to DevDollz: Atelier Edition! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** thoroughly
6. **Submit** a pull request

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python development
- Familiarity with terminal applications

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/TermSwarmX.git
cd TermSwarmX

# Add the upstream remote
git remote add upstream https://github.com/devdollzai/TermSwarmX.git
```

### 2. Install Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements/dev.txt
```

### 3. Verify Installation

```bash
# Run tests to ensure everything works
python test_devdollz_core.py

# Try launching the application
python swarm_ide.py
```

## 🔧 Development Workflow

### 1. Create Feature Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create and switch to feature branch
git checkout -b feature/amazing-feature
```

### 2. Make Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add appropriate comments and docstrings
- Update tests for new functionality
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run the test suite
python test_devdollz_core.py

# Run with pytest for detailed output
pytest test_devdollz_core.py -v

# Check code quality
pylint swarm_ide.py termswarmx_integration.py

# Check syntax
python -m py_compile swarm_ide.py
```

### 4. Commit Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add amazing new feature

- Implements new functionality for X
- Adds tests for the new feature
- Updates documentation
- Fixes issue #123"
```

### 5. Push and Submit PR

```bash
# Push to your fork
git push origin feature/amazing-feature

# Create Pull Request on GitHub
```

## 📝 Code Style Guidelines

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Use descriptive variable and function names
- Add docstrings for all public functions and classes

### Example

```python
def generate_code(description: str, language: str = "python") -> str:
    """
    Generate code based on the given description.
    
    Args:
        description: The code description or requirement
        language: The programming language (default: python)
    
    Returns:
        Generated code as a string
        
    Raises:
        ValueError: If description is empty
    """
    if not description.strip():
        raise ValueError("Description cannot be empty")
    
    # Implementation here
    return generated_code
```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## 🧪 Testing Guidelines

### Test Coverage

- Aim for at least 80% test coverage
- Test both success and failure cases
- Test edge cases and boundary conditions
- Mock external dependencies when appropriate

### Test Structure

```python
def test_function_name():
    """Test description of what is being tested."""
    # Arrange
    input_data = "test input"
    expected_output = "expected result"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Running Tests

```bash
# Run all tests
python test_devdollz_core.py

# Run specific test file
pytest test_devdollz_core.py -v

# Run with coverage
pytest --cov=swarm_ide test_devdollz_core.py

# Run tests in parallel
pytest -n auto test_devdollz_core.py
```

## 🔍 Code Review Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No debugging code remains
- [ ] Commit messages are clear and descriptive

### Review Checklist

- [ ] Code is readable and well-documented
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities introduced
- [ ] Performance considerations addressed
- [ ] Cross-platform compatibility maintained

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues for duplicates
2. Try to reproduce the issue
3. Check if it's a configuration issue
4. Verify you're using the latest version

### Bug Report Template

```markdown
**Bug Description**
Brief description of the issue

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.8.10]
- DevDollz Version: [e.g., 1.0.0]

**Additional Information**
Any other context, logs, or screenshots
```

## 💡 Feature Requests

### Before Requesting

1. Check if the feature already exists
2. Consider if it fits the project scope
3. Think about implementation complexity
4. Consider maintenance burden

### Feature Request Template

```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why this feature would be useful

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you've considered

**Additional Information**
Any other relevant details
```

## 🚀 Advanced Development

### Adding New Agents

1. Create agent function in `swarm_ide.py`
2. Add to `Orchestrator.__init__()`
3. Update tests
4. Update documentation

### Plugin System

1. Create plugin file with `plugin_agent` function
2. Use `plugin load <path>` command
3. Follow plugin interface contract

### UI Customization

1. Modify CSS in `SwarmIDEApp.CSS`
2. Add new widgets if needed
3. Update bindings for new shortcuts

## 📚 Resources

- [Python Documentation](https://docs.python.org/)
- [Textual Framework](https://textual.textualize.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pylint Documentation](https://pylint.pycqa.org/)

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help other contributors
- Ask questions when needed
- Share knowledge and best practices
- Follow the project's code of conduct

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/devdollzai/TermSwarmX/issues)
- **Discussions**: [GitHub Discussions](https://github.com/devdollzai/TermSwarmX/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/devdollzai/TermSwarmX/wiki)

## 🙏 Recognition

Contributors will be recognized in:
- Repository contributors list
- Release notes
- Project documentation
- Community acknowledgments

---

**Thank you for contributing to DevDollz: Atelier Edition! 🚀**

Your contributions help make this project better for everyone in the development community.
