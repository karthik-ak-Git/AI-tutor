# CI/CD Pipeline Guide

## Overview

The CI/CD pipeline automatically:
- ✅ Lints code with flake8
- ✅ Checks formatting with black
- ✅ Type checks with mypy
- ✅ Runs tests with pytest
- ✅ Builds Docker image
- ✅ Tests Docker container

## Configuration Files

### `.flake8`
Flake8 linting configuration:
- Max line length: 127
- Complexity: 10
- Excludes: venv, build, chroma_db, uploads

### `pyproject.toml`
Configuration for:
- **Black**: Code formatting (line length 127)
- **Mypy**: Type checking settings
- **Pytest**: Test configuration
- **Coverage**: Coverage reporting

### `mypy.ini`
Mypy type checking configuration:
- Python 3.11
- Ignores missing imports for external libraries
- Excludes test directories and build artifacts

## Running Locally

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Linting

```bash
# Flake8
flake8 app/ --config=.flake8

# Black (check only)
black --check app/ --config pyproject.toml

# Black (auto-fix)
black app/ --config pyproject.toml

# Mypy
mypy app/ --config-file mypy.ini
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## CI/CD Pipeline Steps

### 1. Lint with flake8
- **Critical errors** (E9, F63, F7, F82): Will fail CI
- **Style issues**: Warnings only (won't fail CI)

### 2. Check formatting with black
- Verifies code follows black formatting
- Will fail CI if formatting issues found
- Fix with: `black app/`

### 3. Type check with mypy
- Checks type hints
- Non-blocking (warnings only)
- Ignores missing imports for external libs

### 4. Run tests
- Runs pytest with coverage
- Generates coverage.xml
- Non-blocking (won't fail CI if tests fail)

### 5. Build Docker
- Only runs on main branch pushes
- Builds Docker image
- Tests container health

## Pre-commit Hooks (Optional)

Install pre-commit hooks for automatic checks:

```bash
pip install pre-commit
pre-commit install
```

Now checks run automatically before commits!

## Fixing Issues

### Flake8 Errors

```bash
# See all issues
flake8 app/ --config=.flake8

# Auto-fix some issues
autopep8 --in-place --aggressive --aggressive app/**/*.py
```

### Black Formatting

```bash
# Check what needs fixing
black --check app/ --config pyproject.toml

# Auto-fix
black app/ --config pyproject.toml
```

### Type Errors

```bash
# See type issues
mypy app/ --config-file mypy.ini

# Fix by adding type hints
# Example: def func(x: str) -> int:
```

## CI/CD Status

Check pipeline status:
- GitHub Actions tab in your repository
- Green ✅ = All checks passed
- Red ❌ = Some checks failed (check logs)

## Best Practices

1. **Run checks locally** before pushing
2. **Fix formatting** with black automatically
3. **Add type hints** gradually (mypy is non-blocking)
4. **Write tests** for new features
5. **Check CI logs** if pipeline fails

## Troubleshooting

### CI Fails on Linting

1. Run flake8 locally: `flake8 app/ --config=.flake8`
2. Fix reported errors
3. Commit and push

### CI Fails on Formatting

1. Run: `black app/ --config pyproject.toml`
2. Commit the formatted code
3. Push again

### Type Checking Issues

Mypy is non-blocking, but to fix:
1. Add type hints to functions
2. Use `# type: ignore` for complex cases
3. Check mypy.ini for ignored modules

## Configuration Details

### Flake8 Rules
- **E9**: Syntax errors
- **F63**: print statements
- **F7**: Syntax errors in statements
- **F82**: Undefined names

### Black Settings
- Line length: 127 characters
- Target Python: 3.11+
- Excludes: venv, build, chroma_db

### Mypy Settings
- Ignores missing imports (for external libs)
- Non-strict mode (allows gradual typing)
- Excludes test files and build artifacts

