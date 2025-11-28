# CI/CD Pipeline - All Checks Documentation

## Overview

This document describes all checks performed in the CI/CD pipeline.

## Job 1: Code Quality & Testing (`lint-and-test`)

### ✅ CHECK 1: Syntax & Critical Errors (flake8)
**Status**: ❌ **FAILS CI** on errors  
**Tool**: flake8  
**What it checks**:
- `E9`: Syntax errors
- `F63`: Print statements
- `F7`: Syntax errors in statements
- `F82`: Undefined names

**Command**:
```bash
flake8 app/ --select=E9,F63,F7,F82 --show-source --statistics --config=.flake8
```

**Why it fails CI**: Critical errors prevent code from running.

---

### ⚠️ CHECK 2: Code Style (flake8)
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: flake8  
**What it checks**:
- Code complexity (max 10)
- Line length (max 127)
- Style issues
- Best practices

**Command**:
```bash
flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --config=.flake8
```

**Why it's non-blocking**: Style issues don't prevent code from running.

---

### ✅ CHECK 3: Code Formatting (black)
**Status**: ❌ **FAILS CI** on issues  
**Tool**: black  
**What it checks**:
- Code formatting consistency
- Line length (127 chars)
- Python 3.11+ style

**Command**:
```bash
black --check app/ --config pyproject.toml
```

**Why it fails CI**: Consistent formatting is important for maintainability.

**Fix**: Run `black app/ --config pyproject.toml`

---

### ⚠️ CHECK 4: Type Checking (mypy)
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: mypy  
**What it checks**:
- Type hints correctness
- Type consistency
- Missing type annotations

**Command**:
```bash
mypy app/ --config-file mypy.ini
```

**Why it's non-blocking**: Gradual typing allows code without full type coverage.

---

### ⚠️ CHECK 5: Import Sorting (isort)
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: isort  
**What it checks**:
- Import statement order
- Import grouping
- Consistency with black

**Command**:
```bash
isort --check-only app/ --profile black
```

**Why it's non-blocking**: Import order doesn't affect functionality.

**Fix**: Run `isort app/ --profile black`

---

### ⚠️ CHECK 6: Security Scan (bandit)
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: bandit  
**What it checks**:
- Security vulnerabilities
- Hardcoded secrets
- Insecure functions
- SQL injection risks
- XSS vulnerabilities

**Command**:
```bash
bandit -r app/ -ll
```

**Why it's non-blocking**: Some warnings may be false positives.

**Report**: Saved as `bandit-report.json`

---

### ⚠️ CHECK 7: Unit Tests (pytest)
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: pytest  
**What it checks**:
- All unit tests pass
- Test coverage
- Test execution time

**Command**:
```bash
pytest tests/ -v --tb=short
```

**Why it's non-blocking**: Tests may fail due to missing API keys or external dependencies.

---

### ⚠️ CHECK 8: Test Coverage (pytest-cov)
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: pytest-cov  
**What it checks**:
- Code coverage percentage
- Uncovered lines
- Coverage trends

**Command**:
```bash
pytest tests/ -v --cov=app --cov-report=xml --cov-report=term-missing --cov-report=html
```

**Why it's non-blocking**: Coverage threshold is set to 0% (can be increased).

**Reports**:
- XML: `coverage.xml` (for Codecov)
- HTML: `htmlcov/index.html` (for viewing)
- Terminal: Summary output

---

### 📤 CHECK 9: Upload Coverage to Codecov
**Status**: ✅ **INFO** (always runs)  
**Tool**: codecov-action  
**What it does**:
- Uploads coverage report to Codecov
- Tracks coverage over time
- Shows coverage trends

**Why it's non-blocking**: Upload failures don't affect CI status.

---

### 📤 CHECK 10: Upload Security Report
**Status**: ✅ **INFO** (always runs)  
**Tool**: actions/upload-artifact  
**What it does**:
- Saves bandit security report
- Available as downloadable artifact
- Can be reviewed later

---

## Job 2: Docker Build & Test (`docker-build`)

**Runs only on**: `main` branch pushes

### ✅ CHECK 11: Docker Build
**Status**: ❌ **FAILS CI** on errors  
**Tool**: docker/build-push-action  
**What it checks**:
- Dockerfile syntax
- Dependency installation
- Image build success
- Multi-platform support

**Why it fails CI**: Build failures prevent deployment.

**Features**:
- Uses Docker Buildx
- GitHub Actions cache for faster builds
- Multi-platform support (linux/amd64)

---

### ✅ CHECK 12: Docker Container Health
**Status**: ❌ **FAILS CI** on errors  
**Tool**: docker + curl  
**What it checks**:
- Container starts successfully
- Health endpoint responds
- Container is functional

**Command**:
```bash
docker run --rm -d -p 8000:8000 --name ai-tutor-test -e OPENROUTER_API_KEY=test-key ai-tutor:latest
sleep 15
curl -f http://localhost:8000/health
```

**Why it fails CI**: Container must be functional for deployment.

---

## Job 3: Dependency Check (`dependency-check`)

### ⚠️ CHECK 13: Dependency Vulnerability Scan
**Status**: ⚠️ **WARNING** (non-blocking)  
**Tool**: safety  
**What it checks**:
- Known vulnerabilities in dependencies
- Outdated packages with security issues
- CVE database matches

**Command**:
```bash
safety check --json
```

**Why it's non-blocking**: Some vulnerabilities may be acceptable or false positives.

---

## Summary Table

| Check # | Name | Tool | Status | Fails CI? |
|---------|------|------|--------|-----------|
| 1 | Syntax & Critical Errors | flake8 | ✅ | ❌ YES |
| 2 | Code Style | flake8 | ⚠️ | ✅ NO |
| 3 | Code Formatting | black | ✅ | ❌ YES |
| 4 | Type Checking | mypy | ⚠️ | ✅ NO |
| 5 | Import Sorting | isort | ⚠️ | ✅ NO |
| 6 | Security Scan | bandit | ⚠️ | ✅ NO |
| 7 | Unit Tests | pytest | ⚠️ | ✅ NO |
| 8 | Test Coverage | pytest-cov | ⚠️ | ✅ NO |
| 9 | Upload Coverage | codecov | ✅ | ✅ NO |
| 10 | Upload Security Report | actions | ✅ | ✅ NO |
| 11 | Docker Build | docker | ✅ | ❌ YES |
| 12 | Docker Health | docker+curl | ✅ | ❌ YES |
| 13 | Dependency Scan | safety | ⚠️ | ✅ NO |

## CI/CD Status Indicators

- ✅ **PASS**: Check passed successfully
- ⚠️ **WARNING**: Check found issues but doesn't fail CI
- ❌ **FAIL**: Check failed and blocks CI
- 📤 **INFO**: Informational step (always runs)

## Running Checks Locally

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all checks
flake8 app/ --config=.flake8                    # Check 1 & 2
black --check app/ --config pyproject.toml        # Check 3
mypy app/ --config-file mypy.ini                  # Check 4
isort --check-only app/ --profile black           # Check 5
bandit -r app/ -ll                                # Check 6
pytest tests/ -v                                  # Check 7
pytest tests/ -v --cov=app --cov-report=html     # Check 8
safety check                                      # Check 13
```

## Fixing Issues

### Critical Errors (Fail CI)
1. **Syntax Errors**: Fix the code
2. **Formatting Issues**: Run `black app/`
3. **Docker Build Failures**: Check Dockerfile and dependencies

### Warnings (Don't Fail CI)
1. **Style Issues**: Run `flake8 app/` and fix
2. **Type Issues**: Add type hints
3. **Import Order**: Run `isort app/`
4. **Security Issues**: Review and fix vulnerabilities
5. **Test Failures**: Fix tests or add missing mocks
6. **Coverage**: Write more tests

## Best Practices

1. **Run checks locally** before pushing
2. **Fix critical errors** immediately
3. **Address warnings** when possible
4. **Review security reports** regularly
5. **Maintain test coverage** above 70%
6. **Keep dependencies** up to date

