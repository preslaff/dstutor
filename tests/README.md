# DS-Tutor Tests

## Status: Pending Implementation

This directory will contain unit and integration tests for the DS-Tutor platform.

## Planned Test Structure

```
tests/
├── unit/
│   ├── test_extension.py          # Test magic commands
│   ├── test_tutor_engine.py       # Test core engine
│   ├── test_validator.py          # Test validation logic
│   ├── test_lesson_loader.py      # Test YAML loading
│   └── test_feedback_engine.py    # Test AI feedback
├── integration/
│   ├── test_lesson_flow.py        # Test complete lesson flow
│   ├── test_validation_flow.py    # Test exercise validation
│   └── test_progress_tracking.py  # Test progress system
└── fixtures/
    ├── sample_lessons.yaml         # Test lesson data
    └── mock_responses.py           # Mock AI responses
```

## Testing Framework

- **pytest**: Main testing framework
- **pytest-cov**: Code coverage reporting
- **unittest.mock**: Mocking dependencies (Claude API, etc.)

## Running Tests (Once Implemented)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_validator.py

# Run with verbose output
pytest -v
```

## Test Coverage Goals

- **Unit Tests**: 80%+ coverage of core logic
- **Integration Tests**: Key user workflows
- **Edge Cases**: Error handling and validation

## Contributing Tests

When implementing tests:
1. Follow pytest conventions
2. Use descriptive test names: `test_<function>_<scenario>_<expected>`
3. Include docstrings explaining test purpose
4. Mock external dependencies (API calls, file I/O)
5. Test both success and failure cases

## Current Status

🚧 **In Development** - Platform code exists but tests not yet written.

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
