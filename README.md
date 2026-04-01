# Metaseed

Schema-driven API for MIAPPE-compliant phenotyping metadata.

## Overview

Metaseed provides tools for creating, editing, and validating experimental metadata following [MIAPPE](https://www.miappe.org/) (Minimum Information About Plant Phenotyping Experiments) standards.

### Features

- **Schema-driven**: YAML specifications define metadata standards
- **Ontology-backed**: References real ontologies (PPEO, ISA, PROV-O)
- **Factory pattern**: Dynamically generates Pydantic models from specs
- **Multiple interfaces**: REST API (FastAPI) and CLI (Typer)
- **Validation**: Built-in validation against MIAPPE 1.1/1.2 standards

## Capabilities

### What Metaseed Can Do

- Define entity schemas in YAML with nested tree structures
- Generate Pydantic models dynamically from specs
- Validate with composable rules (patterns, ranges, enums, conditionals, cross-field)
- Serialize to JSON/YAML
- Serve via REST API, CLI, or Python API
- Support multiple schema versions

### What Metaseed Cannot Do

- Arbitrary graph relationships (trees only)
- Database storage (file-based only)
- Binary/blob types, maps with arbitrary keys, union types
- Custom code execution in validation
- Query/search/filter operations
- Export to CSV, XML, Excel

## Installation

Requires Python 3.11+ and [UV](https://docs.astral.sh/uv/).

```bash
# Clone the repository
git clone <repository-url>
cd metaseed

# Install dependencies
uv sync --extra dev --extra docs
```

## Development

```bash
# Setup development environment
make dev

# Run tests
make test

# Run linter
make lint

# Format code
make format

# Serve documentation locally
make docs-serve
```

Run `make help` to see all available targets.

## Architecture

```
metaseed/
├── src/metaseed/
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
