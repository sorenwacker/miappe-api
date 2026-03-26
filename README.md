# MIAPPE-API

Schema-driven API for MIAPPE-compliant phenotyping metadata.

## Overview

MIAPPE-API provides tools for creating, editing, and validating experimental metadata following [MIAPPE](https://www.miappe.org/) (Minimum Information About Plant Phenotyping Experiments) standards.

### Features

- **Schema-driven**: YAML specifications define metadata standards
- **Ontology-backed**: References real ontologies (PPEO, ISA, PROV-O)
- **Factory pattern**: Dynamically generates Pydantic models from specs
- **Multiple interfaces**: REST API (FastAPI) and CLI (Typer)
- **Validation**: Built-in validation against MIAPPE 1.1/1.2 standards

## Installation

Requires Python 3.11+ and [UV](https://docs.astral.sh/uv/).

```bash
# Clone the repository
git clone <repository-url>
cd miappe-api

# Install dependencies
uv sync --extra dev --extra docs
```

## Development

```bash
# Run tests
uv run pytest

# Run linter
uv run ruff check src tests

# Format code
uv run ruff format src tests

# Serve documentation locally
uv run mkdocs serve
```

## Architecture

```
miappe-api/
├── src/miappe_api/
│   ├── specs/        # YAML schema specifications
│   ├── models/       # Generated Pydantic models
│   ├── validators/   # Validation logic
│   ├── storage/      # Persistence layer
│   ├── api/          # FastAPI REST endpoints
│   ├── cli/          # Typer CLI commands
│   └── core/         # Shared utilities
├── tests/            # Test suite
└── docs/             # MkDocs documentation
```

## License

MIT
