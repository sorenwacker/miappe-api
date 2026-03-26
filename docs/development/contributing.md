# Contributing

Guidelines for contributing to MIAPPE-API.

## Development Setup

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd miappe-api
    ```

2. Install dependencies:

    ```bash
    uv sync --extra dev --extra docs
    ```

3. Install pre-commit hooks:

    ```bash
    uv run pre-commit install
    ```

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_version.py
```

### Code Quality

Pre-commit hooks run automatically on commit. To run manually:

```bash
# Run all hooks
uv run pre-commit run --all-files

# Run ruff linter only
uv run ruff check src tests

# Run ruff formatter
uv run ruff format src tests
```

### Documentation

```bash
# Serve docs locally
uv run mkdocs serve

# Build docs
uv run mkdocs build
```

## Code Style

- Follow [PEP 8](https://pep8.org/) conventions
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Maximum line length: 100 characters
- Use type hints for all function signatures

## Commit Messages

- Use present tense ("add feature" not "added feature")
- Keep the first line under 72 characters
- Reference issues where applicable

## Pull Requests

1. Create a feature branch from `main`
2. Make your changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

## Project Structure

```
miappe-api/
├── src/miappe_api/     # Main package
│   ├── api/            # FastAPI routes
│   ├── cli/            # Typer commands
│   ├── core/           # Shared utilities
│   ├── models/         # Pydantic models
│   ├── specs/          # YAML schemas
│   ├── storage/        # Persistence
│   └── validators/     # Validation logic
├── tests/              # Test suite
└── docs/               # Documentation
```
