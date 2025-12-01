# Contributing to Kontrollzentrum

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/Kontrollzentrum.git
cd Kontrollzentrum
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

### Testing
```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Run specific test
python -m unittest tests.test_production -v

# Run production quick test
python test_production_quick.py
```

### Commit Messages
Use conventional commits:
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
test: Add tests
refactor: Refactor code
chore: Update dependencies
```

Example:
```bash
git commit -m "feat: Add Redis caching layer"
git commit -m "fix: Resolve circuit breaker timeout issue"
```

## Creating a New Module

### 1. Create Module File
```bash
# Create in modules/ directory
touch modules/my_new_modul.py
```

### 2. Module Template
```python
from core.key_check import require_keys

@require_keys
def run(*args):
    """Main module function"""
    return {"status": "success", "data": "result"}

def install():
    """Installation/setup"""
    print("Installing my_new_modul...")

def describe():
    """Module description"""
    return "My new module description"
```

### 3. Add Tests
```bash
# Create test file
touch tests/test_my_new_modul.py
```

### 4. Test Your Module
```bash
python -m unittest tests.test_my_new_modul -v
```

## Pull Request Process

### 1. Push Your Branch
```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request
- Go to GitHub repository
- Click "New Pull Request"
- Select your branch
- Add description
- Submit PR

### 3. PR Requirements
- [ ] Tests pass (CI/CD)
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commit messages are clear

### 4. Review & Merge
- Wait for code review
- Address feedback
- Merge when approved

## Project Structure

```
Kontrollzentrum/
├── core/                    # Core infrastructure
│   ├── api_gateway.py      # API Gateway
│   ├── database.py         # Database layer
│   ├── health_monitor.py   # Health checks
│   ├── rate_limiter.py     # Rate limiting
│   ├── auth.py             # Authentication
│   └── key_check.py        # Key validation
├── modules/                # Production modules (16 total)
├── tests/                  # Unit tests
├── .github/workflows/      # CI/CD pipelines
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Key Files to Know

- `core/key_check.py` - API key validation
- `core/api_gateway.py` - API Gateway & monitoring
- `core/database.py` - Data persistence
- `main.py` - Entry point with multiple modes
- `requirements.txt` - Python dependencies

## Common Tasks

### Add a New Dependency
```bash
pip install package-name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: Add package-name dependency"
```

### Update Documentation
```bash
# Edit README.md or create new .md file
git add *.md
git commit -m "docs: Update documentation"
```

### Fix a Bug
```bash
git checkout -b fix/bug-description
# Make changes
git commit -m "fix: Describe the fix"
git push origin fix/bug-description
# Create PR
```

### Add a Feature
```bash
git checkout -b feature/feature-name
# Make changes
git commit -m "feat: Describe the feature"
git push origin feature/feature-name
# Create PR
```

## Testing Guidelines

### Unit Tests
```python
import unittest
from modules.my_modul import run

class TestMyModul(unittest.TestCase):
    def test_run_success(self):
        result = run()
        self.assertEqual(result["status"], "success")
```

### Integration Tests
```python
# Test with other components
from core.database import db
from core.health_monitor import monitor
```

### Test Coverage
- Aim for >80% coverage
- Test happy path and error cases
- Test edge cases

## Documentation

### Code Comments
```python
# Good: Explains WHY
# We use circuit breaker to prevent cascading failures
if breaker.state == "OPEN":
    raise Exception("Service unavailable")

# Bad: Explains WHAT (code already does this)
# Check if breaker state is open
if breaker.state == "OPEN":
```

### Docstrings
```python
def execute_module(module_name: str, request: Request) -> Dict:
    """Execute module with circuit breaker protection.
    
    Args:
        module_name: Name of the module to execute
        request: HTTP request object
    
    Returns:
        Dictionary with execution result
    
    Raises:
        HTTPException: If module execution fails
    """
```

## Performance Considerations

- Use caching for expensive operations
- Implement rate limiting
- Monitor response times
- Use circuit breaker for resilience
- Log important events

## Security Checklist

- [ ] No hardcoded secrets
- [ ] Use .env for configuration
- [ ] Validate all inputs
- [ ] Use JWT for authentication
- [ ] Implement rate limiting
- [ ] Add error handling
- [ ] Log security events
- [ ] Review dependencies

## Reporting Issues

### Bug Report
- Describe the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version)

### Feature Request
- Describe the feature
- Use case
- Proposed implementation
- Benefits

## Questions?

- Check existing issues
- Read documentation
- Ask in discussions
- Create an issue

## Code of Conduct

- Be respectful
- Be inclusive
- Be constructive
- Report issues appropriately

---

**Thank you for contributing!** 🚀
