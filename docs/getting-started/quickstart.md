# Quick Start

This guide walks through basic usage of MIAPPE-API.

## CLI Usage

The `miappe` command provides access to all functionality:

```bash
# Show available commands
uv run miappe --help
```

!!! note "Coming Soon"
    CLI commands are under development. Check back for updates.

## REST API

Start the development server:

```bash
uv run uvicorn miappe_api.api:app --reload
```

The API will be available at `http://localhost:8000`.

!!! note "Coming Soon"
    REST API endpoints are under development. Check back for updates.

## Next Steps

- Read the [Architecture Overview](../architecture/overview.md) to understand the system design
- See [Schema Specs](../architecture/schema-specs.md) to learn about metadata definitions
