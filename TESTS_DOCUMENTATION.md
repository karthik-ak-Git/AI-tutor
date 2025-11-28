# Test Suite Documentation

## Overview

This document describes all tests in the CI/CD pipeline and how they're executed.

## Test Files

### 1. `tests/test_health.py`
**Purpose**: Tests basic API health and root endpoints

**Tests**:
- `test_root()` - Tests root endpoint returns 200 and includes version
- `test_health()` - Tests health endpoint returns 200 with status, version, and rag_available

**Coverage**: Basic API functionality

---

### 2. `tests/test_config.py`
**Purpose**: Tests configuration management

**Tests**:
- `test_settings_loads_from_env()` - Verifies settings load from environment variables
- `test_settings_defaults()` - Checks default configuration values
- `test_port_property()` - Tests port property reads from environment

**Coverage**: Configuration system

---

### 3. `tests/test_api_endpoints.py`
**Purpose**: Tests API endpoint behavior

**Tests**:
- `test_api_docs()` - Verifies Swagger UI is accessible
- `test_api_redoc()` - Verifies ReDoc is accessible
- `test_openapi_json()` - Tests OpenAPI schema endpoint
- `test_chat_endpoint_missing_message()` - Tests validation on chat endpoint
- `test_chat_endpoint_invalid_json()` - Tests invalid JSON handling
- `test_document_info_no_document()` - Tests document info when no document loaded
- `test_learn_endpoint_missing_fields()` - Tests validation on learn endpoint

**Coverage**: API endpoints and validation

---

### 4. `tests/test_services.py`
**Purpose**: Tests service classes

**Tests**:
- `test_memory_add_messages()` - Tests adding messages to memory
- `test_memory_clear_session()` - Tests clearing session from memory
- `test_memory_multiple_sessions()` - Tests multiple session isolation
- `test_memory_get_last_n()` - Tests getting last N messages

**Coverage**: Service layer functionality

---

## CI/CD Test Execution

### CHECK 7: Unit Tests (pytest)
**Command**:
```bash
pytest tests/ -v --tb=short
```

**What it runs**:
- All test files in `tests/` directory
- Verbose output (`-v`)
- Short traceback format (`--tb=short`)

**Status**: ⚠️ Non-blocking (warnings only)

**Environment**:
```yaml
OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY || 'test-key-for-ci' }}
```

---

### CHECK 8: Test Coverage (pytest-cov)
**Command**:
```bash
pytest tests/ \
  -v \
  --cov=app \
  --cov-report=xml \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-fail-under=0
```

**What it generates**:
- XML report: `coverage.xml` (for Codecov)
- HTML report: `htmlcov/index.html` (for viewing)
- Terminal report: Summary with missing lines

**Coverage Settings**:
- Source: `app/` directory
- Omit: `tests/`, `venv/`, `__pycache__/`
- Threshold: 0% (can be increased)

**Status**: ⚠️ Non-blocking (warnings only)

---

## Test Configuration

### pytest.ini (in pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

**What it does**:
- Looks for tests in `tests/` directory
- Finds files matching `test_*.py`
- Finds classes starting with `Test`
- Finds functions starting with `test_`
- Default options: verbose, short traceback

---

## Running Tests Locally

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_health.py -v
```

### Run Specific Test
```bash
pytest tests/test_health.py::test_health -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=app --cov-report=html
# View report: open htmlcov/index.html
```

### Run with Verbose Output
```bash
pytest tests/ -vv
```

### Run and Stop on First Failure
```bash
pytest tests/ -x
```

---

## Test Summary

| Test File | Tests | Coverage Area |
|-----------|-------|---------------|
| `test_health.py` | 2 | API health endpoints |
| `test_config.py` | 3 | Configuration management |
| `test_api_endpoints.py` | 7 | API endpoints & validation |
| `test_services.py` | 4 | Service layer |
| **Total** | **16** | **Multiple areas** |

---

## Test Categories

### ✅ Unit Tests
- Test individual functions/classes
- Fast execution
- No external dependencies
- Examples: `test_services.py`, `test_config.py`

### ✅ Integration Tests
- Test API endpoints
- Use TestClient
- May require mocked services
- Examples: `test_health.py`, `test_api_endpoints.py`

---

## Test Coverage Goals

**Current**: Basic coverage (health, config, endpoints)

**Recommended**:
- 70%+ overall coverage
- 100% for critical paths (health, config)
- 80%+ for API endpoints
- 60%+ for services

---

## Adding New Tests

### Template for API Endpoint Test
```python
def test_endpoint_name():
    """Test endpoint description."""
    response = client.get("/endpoint")
    assert response.status_code == 200
    assert "expected_field" in response.json()
```

### Template for Service Test
```python
def test_service_method():
    """Test service method description."""
    service = ServiceClass()
    result = service.method()
    assert result == expected_value
```

---

## Common Test Patterns

### Testing with Environment Variables
```python
def test_with_env(monkeypatch):
    monkeypatch.setenv("KEY", "value")
    # Test code
```

### Testing API Endpoints
```python
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/endpoint")
```

### Testing Exceptions
```python
def test_raises_exception():
    with pytest.raises(ValueError):
        function_that_raises()
```

---

## CI/CD Test Status

- ✅ **All tests run** in CI/CD
- ⚠️ **Non-blocking** - test failures don't fail CI
- 📊 **Coverage tracked** via Codecov
- 🔄 **Runs on every push** and pull request

---

## Troubleshooting

### Tests Fail Locally
1. Check environment variables are set
2. Install dev dependencies: `pip install -r requirements-dev.txt`
3. Run with verbose: `pytest tests/ -vv`

### Tests Pass Locally but Fail in CI
1. Check environment variables in CI
2. Verify all dependencies are installed
3. Check for platform-specific issues

### Coverage Too Low
1. Add tests for uncovered code
2. Focus on critical paths first
3. Use `--cov-report=html` to see what's missing

---

## Best Practices

1. ✅ Write tests for new features
2. ✅ Keep tests fast (< 1 second each)
3. ✅ Use descriptive test names
4. ✅ Test both success and failure cases
5. ✅ Mock external dependencies
6. ✅ Keep tests independent
7. ✅ Clean up after tests (fixtures)

