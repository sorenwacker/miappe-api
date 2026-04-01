# Installation

## Requirements

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) package manager

## Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd metaseed

# Install with UV
make install
```

## Development Installation

For development, install with extra dependencies and pre-commit hooks:

```bash
make dev
```

This includes:

- **dev**: Testing tools (pytest, pytest-cov), linting (ruff), and pre-commit hooks
- **docs**: MkDocs with Material theme for documentation

## Verify Installation

```bash
# Check the CLI is available
uv run metaseed --version

# Run the test suite
make test
```
