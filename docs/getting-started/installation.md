# Installation

## Requirements

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) package manager

## Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd miappe-api

# Install with UV
uv sync
```

## Development Installation

For development, install with extra dependencies:

```bash
uv sync --extra dev --extra docs
```

This includes:

- **dev**: Testing tools (pytest, pytest-cov), linting (ruff), and pre-commit hooks
- **docs**: MkDocs with Material theme for documentation

## Verify Installation

```bash
# Check the CLI is available
uv run miappe --version

# Run the test suite
uv run pytest
```
