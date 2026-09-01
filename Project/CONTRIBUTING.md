# 🤝 Contributing Guide

**Avalanche Intelligence Pro - How to Contribute**

Thank you for your interest in contributing! This guide will help you get started.

## Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/avalanche-intelligence.git`
3. **Create** a branch: `git checkout -b feature/your-feature-name`
4. **Make** your changes
5. **Test** locally: `pytest`
6. **Format** code: `black .`
7. **Push** to your fork
8. **Create** a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/avalanche-intelligence/pro.git
cd pro/Project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov black pylint mypy

# Run tests
pytest

# Format code
black app.py config.py

# Lint
pylint app.py --exit-zero
```

## Code Style Guide

### Python Code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use `black` for formatting
- Maximum line length: 88 characters
- Docstring format: Google style

```python
def calculate_risk_score(danger_level: float, seasonal_avg: float, 
                         volatility: float) -> float:
    """
    Calculate avalanche risk score from danger level and context.
    
    Args:
        danger_level: Base danger level (0-10)
        seasonal_avg: Seasonal average (0-10)
        volatility: Seasonal volatility (0-5)
    
    Returns:
        Risk score (0-10)
    
    Raises:
        ValueError: If inputs out of valid range
    """
    if not (0 <= danger_level <= 10):
        raise ValueError("danger_level must be 0-10")
    
    return danger_level * 1.0  # Implementation
```

### Type Hints
- Use type hints for all functions
- Use `Optional[Type]` for nullable values
- Use `List[Type]` for collections

```python
from typing import Optional, List, Dict

def process_data(data: List[float]) -> Dict[str, float]:
    result: Dict[str, float] = {}
    return result

def get_optional_value() -> Optional[str]:
    return None
```

### Docstrings
```python
def your_function(param1: str, param2: int) -> bool:
    """
    One-line summary.
    
    Extended description if needed, explaining the function's
    behavior in detail.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid input provided
        RuntimeError: When unexpected error occurs
    
    Example:
        >>> result = your_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Git Workflow

### Branch Naming
```
feature/description          # New features
bugfix/description           # Bug fixes
docs/description             # Documentation
refactor/description         # Code refactoring
perf/description             # Performance improvements
test/description             # Test additions
```

### Commit Messages
```
# Good commit messages
git commit -m "Add ensemble model training with cross-validation"
git commit -m "Fix: Model predictions returning NaN values"
git commit -m "Docs: Update architecture guide with new components"
git commit -m "Refactor: Extract risk calculation into separate module"

# Avoid vague messages
git commit -m "update stuff"        # ❌ Too vague
git commit -m "fixed bug"           # ❌ No context
git commit -m "asdfasdf"            # ❌ Not descriptive
```

### Pull Request Process

1. **Create PR** with descriptive title
   - "Add: Risk scoring algorithm"
   - "Fix: Model validation tab crashing"
   - "Docs: Add deployment guide"

2. **Write detailed description**
   ```markdown
   ## Description
   Brief explanation of changes
   
   ## Motivation
   Why this change is needed
   
   ## Testing
   How to verify the changes work
   
   ## Checklist
   - [ ] Tests pass locally
   - [ ] Code formatted with black
   - [ ] No linting errors
   - [ ] Documentation updated
   - [ ] No breaking changes
   ```

3. **Respond to review comments**
4. **Update based on feedback**
5. **Merge when approved**

## Areas for Contribution

### 🐛 Bug Fixes
- Performance issues
- Data loading errors
- Model training failures
- UI rendering bugs

### ✨ Features
- New visualization types
- Additional ML models
- Advanced filtering options
- Export format support

### 📚 Documentation
- API documentation
- Usage tutorials
- Deployment guides
- Architecture diagrams

### 🧪 Tests
- Unit tests for functions
- Integration tests for workflows
- End-to-end test coverage

### 🎨 UI/UX
- Styling improvements
- Better visualizations
- Mobile responsiveness
- Accessibility features

### 🚀 Performance
- Optimize data loading
- Cache improvements
- Model optimization
- Reduce memory usage

## Testing Guidelines

### Writing Tests
```python
import pytest
from app import calculate_risk_score

def test_risk_score_basic():
    """Test basic risk score calculation"""
    score = calculate_risk_score(5.0, 3.0, 1.0)
    assert isinstance(score, float)
    assert 0 <= score <= 10

def test_risk_score_edge_cases():
    """Test edge cases"""
    assert calculate_risk_score(0, 0, 0) == 0
    assert calculate_risk_score(10, 10, 10) <= 10

def test_risk_score_invalid_input():
    """Test invalid input handling"""
    with pytest.raises(ValueError):
        calculate_risk_score(-1, 0, 0)
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest test_app.py::test_risk_score_basic

# Run with verbose output
pytest -v
```

## Documentation

### When to Add Documentation

✅ **Add documentation for:**
- New public functions
- Complex algorithms
- Deployment procedures
- Configuration options
- Breaking changes

❌ **Don't over-document:**
- Simple getter/setter functions
- Obvious variable names
- Trivial logic

### Documentation Templates

**New Feature**
```markdown
## Feature Name

### Description
What the feature does and why it's useful

### Usage
```python
# Example code
```

### API
- Parameter 1: description
- Parameter 2: description

### Related
- [Link to relevant doc]
```

**Bug Fix**
```markdown
## Fix: Bug Title

### Problem
Description of the bug

### Solution
How it was fixed

### Testing
How to verify it's fixed
```

## Code Review Guidelines

### As a Reviewer
- ✅ Be constructive and kind
- ✅ Explain the reasoning behind comments
- ✅ Acknowledge effort and good work
- ✅ Ask questions instead of demanding
- ❌ Don't approve code you don't understand
- ❌ Don't request changes not essential to merge

### Common Review Comments
```
"Could you add a type hint here?"
"This function is complex - can we extract it?"
"Have you considered edge cases where...?"
"Great implementation! Minor: could we add tests?"
```

### As an Author
- ✅ Respond to all feedback
- ✅ Ask for clarification
- ✅ Mark conversations as resolved
- ✅ Thank reviewers for their time
- ❌ Don't take criticism personally
- ❌ Don't ignore review comments

## Reporting Issues

### Bug Reports
```markdown
## Title: [BUG] Short description

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Steps to Reproduce
1. First step
2. Second step
3. ...

### Environment
- OS: Windows/macOS/Linux
- Python: 3.11.0
- Streamlit: 1.36.0

### Error Message
```
Paste full error/traceback
```

### Screenshots
If applicable
```

### Feature Requests
```markdown
## Title: [FEATURE] Short description

### Problem Statement
Why this feature is needed

### Proposed Solution
How it should work

### Alternative Solutions
Other approaches considered

### Additional Context
Screenshots, use cases, etc.
```

## Code Quality Checklist

Before submitting a PR:

- [ ] Code is formatted with `black`
- [ ] No linting errors (`pylint`, `flake8`)
- [ ] Type hints added (`mypy` passes)
- [ ] Tests written and passing
- [ ] Docstrings added for new functions
- [ ] No breaking changes documented
- [ ] README/docs updated if needed
- [ ] Commit messages are clear
- [ ] No debug code or print statements left
- [ ] No sensitive data (passwords, keys) exposed

## Performance Considerations

When contributing:
- ✅ Profile code performance
- ✅ Consider memory usage
- ✅ Use caching appropriately
- ✅ Avoid nested loops
- ✅ Use vectorized operations (pandas/numpy)

```python
# ❌ Slow (nested loop)
for row in df.iterrows():
    for col in df.columns:
        process(row[col])

# ✅ Fast (vectorized)
df.apply(lambda x: process(x), axis=1)
```

## Getting Help

- 📖 **Documentation**: Check [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md)
- 🤔 **Questions**: Open a [GitHub Discussion](https://github.com/avalanche-intelligence/pro/discussions)
- 🐛 **Bugs**: [File an issue](https://github.com/avalanche-intelligence/pro/issues)
- 💬 **Chat**: Join our [Discord Community](https://discord.gg/your-server)

## Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes
- Project website
- Monthly community highlights

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you agree to:
- Be respectful and inclusive
- Avoid harassment or discrimination
- Welcome feedback gracefully
- Report violations confidentially

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

**Questions?** Open an issue or check the [FAQ](FAQ.md)

**Thank you for contributing! 🎉**
